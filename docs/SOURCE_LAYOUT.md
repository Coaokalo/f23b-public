# Source layout

| Location | Purpose |
| --- | --- |
| `Mods/aircraft/` | Exact Lua and configuration files from the prepared preview |
| `experiments/independent-weapons/` | Version-guarded primary-cockpit weapon connection |
| `experiments/native-force-bridge/` | Windows native bridge, callback generators, propulsion and control tests |
| `experiments/flight-feel/` | Flight-model library, adapter, tests, and performance report |
| `native_patch.py` | Verified legacy missile restoration and atomic game-file writes |
| `setup_f23b.py` | Single-window aircraft setup, repair and removal |
| `tools/build_setup.py` | Bundle the Windows setup executable |
| `tests/tools/` | Installer regression tests using temporary fixtures |
| `tools/` | Source verification and draft packaging |
| `config/licensing/` | Attribution for included third-party-derived software |
| `config/releases/` | Exact private runtime-input inventory and hashes |
| `docs/images/` | Project screenshots |

The `experiments` paths are retained so the corresponding source can be built
using the existing build scripts.

The Git tree contains software, documentation, and the two documentation screenshots
listed in `config/releases/documentation-images.json`. Runtime images, textures,
models, missions, and the DLL belong to the separately prepared aircraft ZIP.
Development history, private working assets, old releases, and agent instruction
files are absent from this repository.
