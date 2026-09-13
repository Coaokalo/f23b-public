# Experimental preview release status

The public-facing repository is staged privately. The preview download is a
draft, not a published public release.

## Prepared

- Fresh Git history containing the preview's corresponding software source.
- Buildable flight bridge, flight-model tests, and installer regression tests.
- Installation/removal instructions and software/content license separation.
- Exact input hashes and source-origin records.
- Purchased source files, extracted game geometry, development archives, and
  old agent instructions excluded from the source tree.

## Remaining download checks

1. Check the restored YF-23 external cockpit for pilot-view interference and
   confirm the medium/far model transitions in DCS.
2. Complete a fresh-user DCS install, spawn/fly, missile verification, and removal
   check of the final aircraft ZIP. Confirm the menu graphics and mission text.

The draft uses runtime source `4c254be08a8d23ba5ad29e4a8cbf7962dc5d340b` and
retains the flight bridge from `46cc8cbf387d`. The F-35 exterior insert and eight
texture maps are replaced by the licensed YF-23 cockpit; all remaining maps are
referenced. Two simplified distance models are added. The encyclopedia and all
three mission briefings are corrected, and eleven original graphics replace the
old artwork. Software behavior and the native missile installer are unchanged.

The licensed YF-23 remains subject to its external terms; source models and
purchase evidence remain private. These changes do not invent a broader license
grant. Offline checks do not replace the remaining in-game checks. The repository
and its draft release remain private.
