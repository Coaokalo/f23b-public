# Source layout

| Location | Purpose |
| --- | --- |
| `Mods/aircraft/` | Exact Lua and configuration files from the prepared preview |
| `experiments/native-force-bridge/` | Windows native bridge, callback generators, propulsion and control tests |
| `experiments/flight-feel/` | Flight-model library, adapter, tests, and performance report |
| `native_patch.py` | Local missile installer, verification, and rollback |
| `tests/tools/` | Installer regression tests using temporary fixtures |
| `tools/` | Source verification and draft packaging |
| `config/licensing/` | Attribution for included third-party-derived software |
| `config/releases/` | Exact private runtime-input inventory and hashes |

The `experiments` paths are retained so the corresponding source can be built
without changing the accepted runtime code. They describe the source's origin,
not a second installation method.

The Git tree contains software and documentation. Runtime images, textures,
models, missions, and the DLL belong to the separately prepared aircraft ZIP.
Development history, private working assets, old releases, and agent instruction
files are absent from this repository.
