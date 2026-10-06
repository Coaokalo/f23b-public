-- SPDX-License-Identifier: MIT
local root = os.getenv("F23B_RUNTIME_ROOT") or "Mods/aircraft"
LockOn_Options = {script_path = root .. "/F-23B-Player/Cockpit/ExteriorVisuals/"}
local path = LockOn_Options.script_path .. "RadarUpgrade.lua"
local calls, notices, logs = 0, 0, {}
local messages = {}
log = {INFO=1, ERROR=2, write=function(_, _, message) logs[#logs+1]=message end}
print_message_to_user = function(message) notices=notices+1; messages[#messages+1]=message end
local original = package.loadlib
local result = 0
local scope
local cue
package.loadlib = function(dll, symbol)
    assert(dll == LockOn_Options.script_path .. "../../bin/F23B_Radar.dll")
    assert(symbol == "luaopen_f23b_radar")
    return function() return function(enabled, cue_ir)
        scope=enabled; cue=cue_ir; calls=calls+1
        return result, 720, 1, 0, 0.2, -0.1, 1
    end end
end
local tick = dofile(path)
tick(); result=1; tick(); local target, side = tick()
assert(scope == false, "missing mode enabled native ranking exclusion")
assert(target == 720 and side == 1, "native target classification was discarded")
local _, _, az, el, valid = tick(false, true)
assert(cue == true and az == 0.2 and el == -0.1 and valid,
    "native Sidewinder target cue was discarded")
assert(calls==4 and #logs==2 and notices==0)
result=0; tick(true); assert(#logs==3 and scope == true)
result=-1; tick(); tick(); assert(calls==6 and notices==1)
package.loadlib = function() return nil, "missing DLL" end
tick=dofile(path); tick(); tick(); assert(notices==2)
package.loadlib = function() error("load failure") end
tick=dofile(path); tick(); tick(); assert(notices==3)
package.loadlib = original
-- Support extension values: install state once, then change-only target reports.
local support = {1, 0, 0}
package.loadlib = function()
    return function() return function()
        return 0, 0, 0, 0, 0, 0, 0, support[1], support[2], support[3]
    end end
end
logs = {}
local function support_logs()
    local found = {}
    for _, line in ipairs(logs) do if line:find("Missile support", 1, true) then found[#found+1] = line end end
    return found
end
tick = dofile(path)
tick(); local s = support_logs()
assert(#s == 1 and s[1]:find("extension active", 1, true), "support install not reported")
support = {1, 40, 16777728}; tick(); tick(); s = support_logs()
assert(#s == 2 and s[2]:find("target=16777728", 1, true), "support grant not reported once")
support = {1, 90, 16777472}; tick(); s = support_logs()
assert(#s == 3 and s[3]:find("target=16777472", 1, true), "second target not reported")
support = {0, 90, 16777472}; tick(); s = support_logs()
assert(#s == 4 and s[4]:find("unavailable", 1, true), "support loss not reported")
-- MALICE profile values: reported once when active, and once when refused.
local profile = 0
package.loadlib = function()
    return function() return function() return 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, profile end end
end
logs = {}
tick = dofile(path)
local function profile_logs()
    local found = {}
    for _, line in ipairs(logs) do if line:find("MALICE profile", 1, true) then found[#found+1] = line end end
    return found
end
tick(); assert(#profile_logs() == 0, "pending profile reported early")
profile = 1; tick(); tick()
assert(#profile_logs() == 1 and profile_logs()[1]:find("seeker FOV 15 deg", 1, true), "active profile not reported once")
profile = -4; tick()
assert(#profile_logs() == 2 and profile_logs()[2]:find("code -4", 1, true), "refused profile not reported")
-- Support diagnostics: each native line is logged once, unchanged, and nil logs nothing.
local diag
package.loadlib = function()
    return function() return function() return 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, diag end end
end
logs = {}
tick = dofile(path)
local function diag_logs()
    local found = {}
    for _, line in ipairs(logs) do if line:find("Missile support diag", 1, true) then found[#found+1] = line end end
    return found
end
tick(); assert(#diag_logs() == 0, "diagnostic logged without a line")
diag = "target=16798720 decision=extension trackfile=1 fresh=0 memory=1 mask=0x10 age_e8=-1.0 age_f0=10.0 age_f8=-1.0"
tick(); assert(#diag_logs() == 1 and diag_logs()[1]:find(diag, 1, true), "diagnostic line not logged verbatim")
diag = nil; tick(); assert(#diag_logs() == 1, "nil diagnostic logged")
-- Native energy refusal must be an error. One queued ignition produces one log line.
local energy_status, energy_message = 1, nil
local levels = {}
log.write = function(_, level, message) logs[#logs+1]=message; levels[#levels+1]=level end
package.loadlib = function()
    return function() return function()
        return 0,0,0,0,0,0,0,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,energy_status,energy_message,nil
    end end
end
logs = {}; tick = dofile(path); tick()
assert(logs[#logs]:find("energy profile active", 1, true))
energy_message = "MALICE pulse: missile_id=123 time=48.5 seeker_time=48.495 range=29500"
tick(); assert(logs[#logs] == energy_message and levels[#levels] == log.INFO)
energy_message = nil; local count = #logs; tick(); assert(#logs == count)
energy_status = -36; tick()
assert(logs[#logs]:find("code -36", 1, true) and levels[#levels] == log.ERROR)
-- The SA scale extension is reported once as INFO, and a refusal once as an error.
local sa_status = 1
package.loadlib = function()
    return function() return function()
        return 0,0,0,0,0,0,0,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,0,nil,nil,sa_status
    end end
end
logs = {}; levels = {}; tick = dofile(path); tick()
assert(logs[#logs]:find("SA scale extended to 640 NM", 1, true) and levels[#levels] == log.INFO)
count = #logs; tick(); assert(#logs == count, "SA status repeated")
sa_status = -50; tick()
assert(logs[#logs]:find("code -50", 1, true) and levels[#levels] == log.ERROR)
sa_status = 0; count = #logs; tick(); assert(#logs == count, "inactive SA status logged")
-- A manual installation on an unknown DCS build must give an actionable message.
package.loadlib = function() return function() return function() return -1 end end end
tick = dofile(path); tick(); tick()
assert(messages[#messages]:find("connection OFF", 1, true))
assert(messages[#messages]:find("MALICE, Block II", 1, true))
assert(messages[#messages]:find("native Hornet cockpit", 1, true))
assert(messages[#messages]:find("releases/latest", 1, true))
-- Detect the old cockpit edit once, without writing to the DCS installation.
local original_io = io
local closed = false
io = {open=function(name, mode)
    assert(name == "Mods/aircraft/FA-18C/Cockpit/Scripts/device_init.lua" and mode == "r")
    return {read=function() return "-- BEGIN F23B INDEPENDENT WEAPONS" end,
            close=function() closed=true end}
end}
package.loadlib = function() return function() return function() return 0 end end end
local before = #messages
tick = dofile(path); tick(); tick()
assert(closed and #messages == before + 1)
assert(messages[#messages]:find("Check all files (slow)", 1, true))
io = original_io
package.loadlib = original
print("PASS: radar loader, bounded failures, native reports, manual-install warning and read-only legacy detection")
