-- SPDX-License-Identifier: MIT
-- Rewrite only the Hornet A/A select and trigger rows. The caller externally
-- composes the installed Hornet profile first, so every unrelated Hornet
-- binding and axis remains represented by the installed module. The caller
-- also resolves BridgeCommands from its DCS-provided Saved Games folder.
return function(profile, devices, hotas_commands, commands)
    if type(profile) ~= "table" or type(devices) ~= "table"
        or type(hotas_commands) ~= "table" or type(commands) ~= "table" then
        error("F-23B input bridge received an incomplete Hornet profile contract")
    end
    local replacements = {
        [hotas_commands.STICK_TRIGGER_2ND_DETENT] =
            commands.TRIGGER_SECOND_DETENT,
        [hotas_commands.STICK_WEAPON_SELECT_DOWN] = commands.SELECT_SIDEWINDER,
        [hotas_commands.STICK_WEAPON_SELECT_IN] = commands.SELECT_AMRAAM,
        [hotas_commands.STICK_WEAPON_SELECT_AFT] = commands.SELECT_GUN,
        [hotas_commands.STICK_WEAPON_SELECT_FWD] = commands.SELECT_SPARROW,
    }
    local replaced = {}
    for _, row in ipairs(profile.keyCommands or {}) do
        local native = row.down
        local replacement = replacements[native]
        if replacement ~= nil and row.cockpit_device_id == devices.HOTAS then
            row.down = replacement
            if row.up == native then row.up = replacement end
            row.cockpit_device_id = nil
            replaced[native] = true
        end
    end
    for native in pairs(replacements) do
        if not replaced[native] then
            error("installed Hornet input profile is missing required HOTAS row "
                .. tostring(native))
        end
    end
    return profile
end
