-- SPDX-License-Identifier: MIT
-- Overlay device loaded by add_plugin_systems; the Hornet cockpit remains the
-- aircraft's primary cockpit and is neither copied nor replaced.
if get_aircraft_type() ~= "F-23B" then
    return
end

MainPanel = {
    "ccMainPanel",
    LockOn_Options.script_path .. "mainpanel_init.lua",
    {}
}

creators = {
    [1] = {
        "avLuaDevice",
        LockOn_Options.script_path .. "ExteriorVisualAdapter.lua"
    }
}
