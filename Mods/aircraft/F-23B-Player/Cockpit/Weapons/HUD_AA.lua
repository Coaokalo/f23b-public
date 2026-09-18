-- SPDX-License-Identifier: MIT
-- Execute the installed page; replace only its weapon identification/count.
local original_add = Add
Add = function(element)
    if element.name == 'AA_Weapon_type' or element.name == 'AA_Weapon_count' then
        element.element_params = {'F23B_WEAPON_MODE'}
        local native = element.name == 'AA_Weapon_type' and 'HUD_AA_WeaponType' or 'HUD_AA_WeaponCount'
        element.controllers = {{native}, {'parameter_in_range', 0, -0.1, 0.1}}
    elseif element.name == 'F23B_Weapon_Count' then
        element.element_params = {'F23B_WEAPON_MODE', 'F23B_WEAPON_COUNT'}
    elseif element.name == 'F23B_IR_Lock' then
        element.element_params = {'F23B_IR_LOCK'}
    elseif element.name == 'F23B_Weapon_1' or element.name == 'F23B_Weapon_2' then
        element.element_params = {'F23B_WEAPON_MODE'}
    end
    original_add(element)
end
dofile(LockOn_Options.script_path .. 'Multipurpose_Display_Group/HUD_AVQ32/indicator/Pages/HUD_AA.lua')
for mode, label in ipairs({'9XII', 'MALICE'}) do
    local element = addStrokeText('F23B_Weapon_' .. mode, label, STROKE_FNT_DFLT_150,
        'RightCenter', {0, -345}, 'AA_Weapon_Count',
        {{'parameter_in_range', 0, mode - 0.1, mode + 0.1}})
    element.element_params = {'F23B_WEAPON_MODE'}
end
local count = addStrokeText('F23B_Weapon_Count', nil, STROKE_FNT_DFLT_150,
    'CenterCenter', {33, -345}, 'AA_Weapon_Count',
    {{'parameter_in_range', 0, 0.5, 2.5}, {'text_using_parameter', 1, 0}}, {'%.0f'})
count.element_params = {'F23B_WEAPON_MODE', 'F23B_WEAPON_COUNT'}
local lock = addStrokeText('F23B_IR_Lock', 'LOCK', STROKE_FNT_DFLT_100,
    'CenterCenter', {0, -375}, 'AA_Weapon_Count',
    {{'parameter_in_range', 0, 0.5, 1.5}})
lock.element_params = {'F23B_IR_LOCK'}
Add = original_add
