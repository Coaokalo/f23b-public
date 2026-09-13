-- SPDX-License-Identifier: MIT
-- Project-original Block II approximation using the native Hornet AIM-9X slot.
-- Requires first-registration native patch. No late declare_weapon permitted.
-- F-22 v2.1 benchmark: same 84.46 kg mass, drag and 8 s / 6 kg/s burn;
-- project thrust is 15542.1 N (+5%). Simulation values, not real motor data.
-- IR tracking remains native. Weapon-datalink/LOAL capability is not established.
local weapon = {
    category = CAT_AIR_TO_AIR, name = "AIM_9X",
    user_name = _("AIM-9X Block II (F-23B project-defined)"),
    display_name_short = "AIM-9XII",
    wsTypeOfWeapon = {4, 4, 7, AIM_9X},
    Escort = 0, Head_Type = 1, sigma = {1, 1, 1},
    M = 84.46, mass = 84.46, H_max = 18000, H_min = -1, Diam = 127,
    Cx_pil = 1.03, D_max = 20000, D_min = 50, Head_Form = 0,
    Life_Time = 80, Nr_max = 70, v_min = 100, v_mid = 750, Mach_max = 3.2,
    t_b = 0, t_acc = 8, t_marsh = 0, Range_max = 29000, H_min_t = 1,
    -- Preserve Hornet-native seeker acquisition/tracking geometry. The FC-host
    -- reference's 2-radian free-search cone is not a Hornet integration contract.
    -- gimbal travel and instantaneous search cone are separate parameters.
    Fi_start = 1.57, Fi_rak = math.pi, Fi_excort = 1.57,
    Fi_search = 0.09, OmViz_max = 1.1,
    warhead = predefined_warhead("AIM_9"),
    exhaust = {0.7, 0.7, 0.7, 0.08}, smoke_opacity_type = 1,
    X_back = -1.6, Y_back = 0, Z_back = 0, Reflection = 0.03, KillDistance = 9,
    SeekerGen = 4, SeekerSensivityDistance = 29000, ccm_k0 = 0.001,
    SeekerCooled = true, x_wing_anim = -1, PN_gain = 6,
    shape_table_data = {{name = "aim-9x", file = "aim-9x", life = 1,
        fire = {0, 1}, username = "AIM-9XII", index = AIM_9X}},
    supersonic_A_coef_skew = 0.3, nozzle_exit_area = 0.0068,
    -- Native legacy solver: area/drag/lift, stage times, flow, force, guidance,
    -- then launch-zone estimates. Entries 16/23/30 are the boost contract.
    ModelData = {
        58, 0.35, 0.04, 0.08, 0.02, 0.05, 1.2, 1.0,
        1.2, 0.8, 1.0, 0.5, 2.0,
        -1, -1, 8, 0, 0, 0, 1e9,
        0, 0, 6, 0, 0, 0, 0,
        0, 0, 15542.1, 0, 0, 0, 0,
        1e9, 80, 0, 0.45, 1e9, 1e9, 0, 30, 0, 2.2, 1, 1,
        9, -13, -2.1, 16500, 6500, 29000, 12000, 11500, 3500,
        2500, 0.55, -0.01, 0.5,
    },
}
-- F23B_NATIVE_DEFINITION_END
declare_loadout({
    category = CAT_AIR_TO_AIR, CLSID = "{F23B-AIM9X-BLOCKII}",
    Picture = "AIM-9XX.png", displayName = weapon.user_name,
    attribute = weapon.wsTypeOfWeapon, wsTypeOfWeapon = weapon.wsTypeOfWeapon,
    Count = 1, Weight = weapon.M, Cx_pil = 0.0005,
    Elements = {{ShapeName = "aim-9x", DrawArgs = {{1, 1}, {2, 1}}}},
})
return weapon
