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
    -- Native plume meets the short recessed collar inside the measured channel.
    -- Positions use DCS {X,Z,Y}; dimensions are fitted to the F-23B aperture.
    engine_effects_enabled = true,
    engine_effects = {
        profile = "F23B_LICENSED_ENGINE_NATIVE_EFFECTS",
        origins = {
            { -6.03, -0.328308940, -1.307693511 },
            { -6.03, -0.328309045,  1.314346552 }
        },
        elevation = -1.5,
        -- Diameter is fitted to the measured channel gap (~0.508 m), not Hornet 0.765 m.
        -- The recessed source sits well forward of the channel exit. Give the
        -- Hornet plume enough length to remain visible beyond the exhaust trough.
        diameter = 0.50,
        exhaust_length_ab = 6.5,
        exhaust_length_ab_K = 1.0,
        smokiness_level = 0.05,
        -- Installed Hornet flame and shock artwork; the model references
        -- F18C_afterburn for its staged source. No stock texture is bundled.
        afterburner_effect_texture = "afterburner_f-18c",
        afterburner_circles_count = 8,
        -- White native light on both outlets floods this pale enclosed trough.
        -- Explicit zeros suppress DCS's default point light; BANO owns the core.
        afterburner_light_color = { 0.0, 0.0, 0.0 }
    },

    crew_position = { 6.4446, -0.333522, 0.001605 },
    canopy_position = { 6.402974, 0.214973, -0.001044 }
}
