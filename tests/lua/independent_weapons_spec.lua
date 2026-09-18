-- SPDX-License-Identifier: MIT
-- Exercise release consent against changing station inventory and safety inputs.
local values, shots = {}, {}
local stores = {
    [0] = {CLSID='{F23B-AIM9X-BLOCKII}', count=1},
    [8] = {CLSID='{F23B-AIM9X-BLOCKII}', count=1},
    [2] = {CLSID='{F23B-AIM424-MALICE}', count=1},
}
local args, bay, wow = {[47]=1, [49]=1, [135]=0.2}, 0, 0
local target, descriptor = 42, -2 -- Seeker can initialize one tick after selection.
local device = {}
function device:listen_command() end
function device:get_station_info(index) return stores[index] end
function device:select_station(index) self.selected = index end
function device:launch_station(index)
    assert(bay >= 0.999 and args[49] == 1 and wow == 0)
    assert(stores[index].count > 0)
    stores[index].count = stores[index].count - 1
    shots[#shots + 1] = index
end
function GetSelf() return device end
function GetDevice()
    return {update_arguments=function() end, get_argument_value=function(_, key) return args[key] end}
end
function get_base_data()
    local ground = function() return wow end
    return {getWOW_NoseLandingGear=ground, getWOW_LeftMainLandingGear=ground, getWOW_RightMainLandingGear=ground}
end
function get_param_handle(name)
    return {get=function() return values[name] or 0 end, set=function(_, value) values[name]=value end}
end
function get_aircraft_draw_argument_value() return bay end
function make_default_activity() end
log = {INFO=1, ERROR=2, write=function() end}
package.preload.lfs = function() return {writedir=function() return '' end} end
package.loadlib = function()
    return function() return function() return descriptor, target, 0.1, 0.02 end end
end
dofile('Mods/aircraft/F-23B-Player/Cockpit/Weapons/Controller.lua')
post_initialize()
SetCommand(3201, 1)
update()
descriptor = 100
update()
assert(values.F23B_WEAPON_READY == 1, 'Transient seeker initialization disabled weapons')
assert(values.F23B_WEAPON_COUNT == 2)
values.WS_IR_MISSILE_LOCK = 1
SetCommand(3200, 1)
update()
assert(#shots == 0, 'Closed bay permitted launch')
bay = 1
update()
assert(#shots == 1 and shots[1] == 0)
for _=1,10 do update() end
assert(#shots == 1 and values.F23B_WEAPON_COUNT == 1, 'Held trigger repeated')
SetCommand(3200, 0)
args[49] = 0
SetCommand(3200, 1)
update()
args[49] = 1
update()
assert(#shots == 1, 'Arming with held trigger fired a queued missile')
SetCommand(3200, 0)
wow = 1
SetCommand(3200, 1)
update()
wow = 0
update()
assert(#shots == 1, 'Weight-on-wheels consent was retained')
SetCommand(3200, 0)
args[135] = 0
SetCommand(3200, 1)
update()
assert(#shots == 1, 'Uncooled seeker permitted launch')
SetCommand(3200, 0)
args[135] = 0.2
SetCommand(3200, 1)
update()
assert(#shots == 2 and shots[2] == 8)
SetCommand(3202, 1)
target = 0
SetCommand(3200, 1)
update()
assert(#shots == 2, 'MALICE fired without a designated target')
SetCommand(3200, 0)
target = 42
SetCommand(3200, 1)
update()
assert(#shots == 3 and shots[3] == 2)
update()
assert(values.F23B_WEAPON_COUNT == 0)
print('PASS: actual station counts, door/arm/WOW/cooling/target interlocks, one shot per edge')
