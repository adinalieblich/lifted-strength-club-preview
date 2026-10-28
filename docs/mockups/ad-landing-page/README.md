# Ad landing page mockups (Oct 27, 2026)

Source for the two mockups sent to Sharon:
- A, exactly as she asked: https://claude.ai/artifact/THpuENYgk8cm67HrxbWE2g
- B, with recommendations: https://claude.ai/artifact/AEMpbsN8XvPHzcDgkxLbxM

To rebuild, run from the repo root:

```
python3 docs/mockups/ad-landing-page/prep_images.py
python3 docs/mockups/ad-landing-page/build.py <artifact-A-url> <artifact-B-url>
```

This writes `lifted-ad-page-a.html` and `lifted-ad-page-b.html` next to `build.py`. Publish each with its
`img/` folder as supporting files, republishing to the same artifact URL so the links Sharon has keep working.
The generated HTML and `img/` are git-ignored. `build.py` is the source of truth.

The calendar in the mockups is a stand-in, because a real Cal.com embed can't run inside an Artifact. On the
real page, use the Cal.com embed code already in `flagship.html`.
