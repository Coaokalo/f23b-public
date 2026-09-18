-- SPDX-License-Identifier: MIT
-- Invoked by the installer hook only for F-23B; donor scripts stay on disk.
local root = require('lfs').writedir() .. 'Mods/aircraft/F-23B-Player/Cockpit/Weapons/'
assert(creators[201] == nil, 'F-23B weapon device slot is already occupied')
creators[201] = {'avSimpleWeaponSystem', root .. 'Controller.lua'}
for _, indicator in pairs(indicators) do
    for _, name in ipairs({'AVQ32', 'MDI_left', 'MDI_right', 'AMPCD'}) do
        if indicator[2]:match('/' .. name .. '_init%.lua$') then
            indicator[2] = root .. name .. '_init.lua'
        end
    end
end
