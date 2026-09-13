-- SPDX-License-Identifier: MIT
-- Tracked selector for the real private F-23B development exterior. Private
-- compiled assets remain ignored; build and packaging fail closed if absent.
return {
    content_class = "PRIVATE_LICENSED_DEVELOPMENT_REQUIRED",
    package_version = "0.9.0-alpha.dev",
    display_name = "F-23B Black Widow II",
    exterior_shape = "F-23B",
    cockpit_shape = "F-23B-cockpit",
    center_of_mass = { 0.0, 0.15, 0.0 },

    -- Hash-pinned integration locations measured in the licensed exterior.
    cockpit_local_point = { 6.25, 0.40, 0.0 },
    hud_anchor = { 0.760729, -0.356144, 0.001605 },
    nose_gear_position = { 5.651484, -2.320483, -0.027345 },
    main_gear_position = { -1.401347, -2.430470, 2.188081 },
    engines = {
        { -6.048938751, 0.039560661, -1.312060237 },
        { -6.048938751, 0.039560661,  1.310768247 }
    },

    -- Presentation only. The installed Hornet owns engine state and sounds.
    -- Native plume joins the authored burner tail inside the measured channel.
    -- Positions use DCS {X,Z,Y}; dimensions are fitted to the F-23B aperture.
    engine_effects_enabled = true,
    engine_effects = {
        profile = "F23B_LICENSED_ENGINE_NATIVE_EFFECTS",
        origins = {
            { -6.90, -0.351090653, -1.307693511 },
            { -6.90, -0.351090758,  1.314346552 }
        },
        elevation = -1.5,
        -- Diameter is fitted to the measured channel gap (~0.508 m), not Hornet 0.765 m.
        -- Length is unchanged so the nominal plume stays inside the tiled trough.
        diameter = 0.50,
        exhaust_length_ab = 2.405228758,
        exhaust_length_ab_K = 0.707,
        smokiness_level = 0.05,
        -- Texture and native plume/haze rendering resolve from installed DCS.
        afterburner_effect_texture = "afterburner_f-18c",
        -- Circle settings are omitted, retaining the installed Hornet defaults.
        -- White native light on both outlets floods this pale enclosed trough.
        -- Explicit zeros suppress DCS's default point light; BANO owns the core.
        afterburner_light_color = { 0.0, 0.0, 0.0 }
    },

    crew_position = { 6.4446, -0.333522, 0.001605 },
    canopy_position = { 6.402974, 0.214973, -0.001044 }
}
