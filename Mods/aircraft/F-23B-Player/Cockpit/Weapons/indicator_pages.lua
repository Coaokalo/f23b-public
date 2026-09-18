-- SPDX-License-Identifier: MIT
for index, path in pairs(page_subsets) do
    for _, name in ipairs({'HUD_AA', 'RDR_AA'}) do
        if path:match('/' .. name .. '%.lua$') then
            page_subsets[index] = require('lfs').writedir() .. 'Mods/aircraft/F-23B-Player/Cockpit/Weapons/' .. name .. '.lua'
        end
    end
end
