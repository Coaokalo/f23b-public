-- SPDX-License-Identifier: MIT
-- Keep the native radar page, with project weapon counts from actual stations.
local original_add = Add
Add = function(element)
    if element.name == 'Current_AA_Weapon' then
        element.element_params = {'F23B_WEAPON_MODE'}
        element.controllers = {{'MPD_RDR_AA_SelectedWeaponInfo'}, {'parameter_in_range', 0, -0.1, 0.1}}
    elseif element.name == 'F23B_Radar_Weapon_1' or element.name == 'F23B_Radar_Weapon_2' then
        element.element_params = {'F23B_WEAPON_MODE', 'F23B_WEAPON_COUNT'}
    end
    original_add(element)
end
dofile(LockOn_Options.script_path .. 'Multipurpose_Display_Group/Common/indicator/Pages/MPD/RDR/RDR_AA.lua')
for mode, label in ipairs({'9XII', 'MALICE'}) do
    addStrokeText('F23B_Radar_Weapon_' .. mode, nil, STROKE_FNT_DFLT_120,
        'CenterCenter', {370, 435}, nil,
        {{'parameter_in_range', 0, mode - 0.1, mode + 0.1}, {'text_using_parameter', 1, 0}},
        {label .. ' %.0f'})
end
Add = original_add
