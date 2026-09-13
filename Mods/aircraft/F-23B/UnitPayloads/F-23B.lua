-- SPDX-License-Identifier: MIT
-- Hornet-recognized logical stations placed at the five F-23 bay connectors.
local AIM9X = "{F23B-AIM9X-BLOCKII}"
local AIM120C = "{40EF17B7-F508-45de-8566-6FFECC0C1AB8}"
local MALICE = "{F23B-AIM424-MALICE}"
local tasks = { [1] = 11, [2] = 10, [3] = 18, [4] = 19 }

local unitPayloads = {
    ["name"] = "F-23B",
    ["payloads"] = {
        [1] = {
            ["name"] = "Air Superiority (2x AIM-9X Block II + 3x AIM-424 MALICE)",
            ["pylons"] = {
                [1] = { ["CLSID"] = AIM9X, ["num"] = 1 },
                [2] = { ["CLSID"] = MALICE, ["num"] = 3 },
                [3] = { ["CLSID"] = MALICE, ["num"] = 4 },
                [4] = { ["CLSID"] = MALICE, ["num"] = 6 },
                [5] = { ["CLSID"] = AIM9X, ["num"] = 9 }
            },
            ["tasks"] = tasks
        },
        [2] = {
            ["name"] = "Air Superiority (2x AIM-9X Block II + 3x AIM-120C)",
            ["pylons"] = {
                [1] = { ["CLSID"] = AIM9X, ["num"] = 1 },
                [2] = { ["CLSID"] = AIM120C, ["num"] = 3 },
                [3] = { ["CLSID"] = AIM120C, ["num"] = 4 },
                [4] = { ["CLSID"] = AIM120C, ["num"] = 6 },
                [5] = { ["CLSID"] = AIM9X, ["num"] = 9 }
            },
            ["tasks"] = tasks
        },
        [3] = {
            ["name"] = "Within Visual Range (2x AIM-9X Block II)",
            ["pylons"] = {
                [1] = { ["CLSID"] = AIM9X, ["num"] = 1 },
                [2] = { ["CLSID"] = AIM9X, ["num"] = 9 }
            },
            ["tasks"] = tasks
        }
    },
    ["unitType"] = "F-23B"
}
return unitPayloads
