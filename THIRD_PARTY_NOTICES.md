# Third-party notices

## Grinnelli Designs F-22A performance source

The flight-model adaptation uses GPL-covered source from
[Grinnelli Designs F-22A](https://github.com/grinnellidesigns/f-22a), tag `v2.1.0`,
commit `24dc1f51a8d0d9427c7bd3c368ccabd3e0ade53c`.

Copyright (C) 2025 Branden Hooper (upstream portions/behavior).
Copyright (C) 2026 F-23B project contributors (adaptation).

The relevant RAPTOR.h and RAPTOR.cpp notices specify GPL-3.0-or-later. Their
file-specific notices are retained; the upstream EFM directory's separate MIT
notice does not replace them. The combined software is GPL-3.0-or-later, with
existing project-original MIT grants retained at file level. License texts are
in [COPYING](COPYING) and [LICENSES/MIT.txt](LICENSES/MIT.txt).

Exact upstream hashes, included derived files, and modification records are in
[the reuse manifest](config/licensing/third-party-code-reuse.json). The
[performance provenance record](experiments/flight-feel/docs/provenance/GRINNELLI_V2_1_PERFORMANCE_REFERENCE.md)
describes the adaptation and its limitations. No upstream aircraft models,
textures, audio, or compiled binaries are bundled in this source tree.

## Purchased visual content in the preview

- SytaPastel: Northrop YF-23 Black Widow II, CGTrader product 2046482.

These assets retain their external licenses. They are separate from the GPL
software and absent from the Git source tree. See
[LICENSE-ASSETS.md](LICENSE-ASSETS.md) for the draft download's status.

The external cockpit, control panels and displays are from the same licensed
YF-23 source. The F-35-derived exterior insert and its textures are no longer
shipped. The Hornet supplies the pilot cockpit from the user's installation.

## Eagle Dynamics / DCS World

The runtime requires DCS World and an installed, activated DCS: F/A-18C Hornet.
The native bridge uses the user's installed Hornet, and builds require the user's
installed SDK headers. The small test stub is project-authored and is not the
real SDK. The missile installer reads and modifies native weapon definitions
locally, keeping rollback copies. Those native files are not distributed.

THIS MATERIAL IS NOT MADE OR SUPPORTED BY EAGLE DYNAMICS SA.
