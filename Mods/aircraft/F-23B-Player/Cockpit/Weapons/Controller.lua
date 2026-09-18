-- SPDX-License-Identifier: MIT
-- Runs in the primary cockpit so DCS supplies the Hornet's selected radar target.
local self = GetSelf()
local STEP = 0.02
local root = require('lfs').writedir() .. 'Mods/aircraft/F-23B-Player/'
local init, failure = package.loadlib(root .. 'bin/F23B_Weapons.dll', 'luaopen_f23b_weapons')
local prepare = init and init()
local mode, station, pending, trigger = 0, nil, false, false
local sensor = get_base_data()
local handles = {}
local function param(name)
    if not handles[name] then handles[name] = get_param_handle(name) end
    return handles[name]
end
local function set(name, value) param(name):set(value) end
local clsids = {[1] = '{F23B-AIM9X-BLOCKII}', [2] = '{F23B-AIM424-MALICE}'}
for _, command in ipairs({3200, 3201, 3202, 3203}) do self:listen_command(command) end
make_default_activity(STEP)

function SetCommand(command, value)
    log.write('F23B_WEAPONS', log.INFO, 'Control command=' .. command .. ' value=' .. value)
    if command == 3200 then
        if value > 0.5 and not trigger then pending = true end
        trigger = value > 0.5
        if not trigger then pending = false end
    elseif value > 0.5 then
        mode = command == 3201 and 1 or (command == 3202 and 2 or 0)
        station, pending, trigger = nil, false, false
    end
end

function update()
    local panel = GetDevice(0)
    panel:update_arguments()
    local aa = panel:get_argument_value(47) > 0.5
    local armed = panel:get_argument_value(49) > 0.5
        and sensor.getWOW_NoseLandingGear() < 0.5
        and sensor.getWOW_LeftMainLandingGear() < 0.5
        and sensor.getWOW_RightMainLandingGear() < 0.5
    local count, next_station = 0, nil
    if mode ~= 0 then
        for index = 0, 8 do
            local info = self:get_station_info(index)
            if info and info.CLSID == clsids[mode] and info.count > 0 then
                count = count + info.count
                next_station = next_station or index
            end
        end
    end
    if next_station ~= station then
        station = next_station
        if station then self:select_station(station) end
    end
    set('F23B_WEAPON_MODE', aa and mode or 0)
    set('F23B_WEAPON_COUNT', count)
    set('F23B_WEAPON_READY', prepare and 1 or 0)
    local locked, target = false, 0
    if prepare and aa and station then
        local kind, id, az, el = prepare(self.link, station)
        if kind and kind > 0 then
            target = id or 0
            if mode == 1 then
                set('WS_IR_MISSILE_SEEKER_DESIRED_AZIMUTH', az or 0)
                set('WS_IR_MISSILE_SEEKER_DESIRED_ELEVATION', el or 0)
                locked = param('WS_IR_MISSILE_LOCK'):get() == 1
                    and panel:get_argument_value(135) > 0.1
            end
        elseif kind == -1 or kind == -4 or kind == -6 then
            log.write('F23B_WEAPONS', log.ERROR, 'Unsupported weapon connection: ' .. kind)
            prepare = nil -- Unsupported native layout: inhibit launch.
        end
    end
    set('F23B_IR_LOCK', mode == 1 and locked and 1 or 0)
    if not aa or not armed then pending = false end
    if pending and prepare and station and get_aircraft_draw_argument_value(1009) >= 0.999
        and ((mode == 1 and locked) or (mode == 2 and target ~= 0)) then
        self:launch_station(station)
        log.write('F23B_WEAPONS', log.INFO, 'Launch mode=' .. mode .. ' station=' .. station)
        pending = false -- One missile per trigger edge, including a held trigger.
    end
end

function post_initialize()
    if type(prepare) ~= 'function' then
        prepare = nil
        log.write('F23B_WEAPONS', log.ERROR, 'Independent weapons unavailable: ' .. tostring(failure or 'unsupported DCS binaries'))
    else
        log.write('F23B_WEAPONS', log.INFO, 'Independent weapons connected to primary cockpit')
    end
end
need_to_be_closed = false
