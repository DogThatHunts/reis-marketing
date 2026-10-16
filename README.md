# REIS Marketing: New Homes Review social teasers

Short vertical videos (1080×1920, 9:16) for YouTube Shorts, Instagram Reels and X. Each one teases the highlights of a market's New Homes Review.

## Myrtle Beach & Brunswick County (Jan–Aug 2026)

### Sample videos

**Watch online (no GitHub account needed):** https://dogthathunts.github.io/reis-marketing/

The Q&A version is the current draft. The single-voice versions are parked.

`myrtle_beach/video/`:

| File | Format | Voice(s) | Length |
|---|---|---|---|
| `myrtle_beach_teaser_qa.mp4` | Q&A (**current draft**) | Anna = Bella (questions), George = Onyx (answers) | 38.5s |
| `myrtle_beach_teaser_mono_af_heart.mp4` | Single voice | Heart (US female), **preferred single voice** | 29.3s |
| `myrtle_beach_teaser_mono_af_bella.mp4` | Single voice | Bella (US female) | 28.7s |
| `myrtle_beach_teaser_mono_af_sarah.mp4` | Single voice | Sarah (US female) | 28.9s |
| `myrtle_beach_teaser_mono_am_onyx.mp4` | Single voice | Onyx (US male, deep) | 29.5s |
| `myrtle_beach_teaser_mono_am_onyx_deep.mp4` | Single voice | Onyx, pitch lowered | 29.6s |
| `myrtle_beach_teaser_mono_am_fenrir.mp4` | Single voice | Fenrir (US male) | 29.9s |
| `myrtle_beach_teaser_mono_am_adam.mp4` | Single voice | Adam (US male) | 28.0s |
| `myrtle_beach_teaser_mono_am_michael.mp4` | Single voice | Michael (US male) | 29.6s |
| `myrtle_beach_teaser_mono_bm_george.mp4` | Single voice | George (British male) | 29.8s |
| `myrtle_beach_teaser_mono_bm_lewis.mp4` | Single voice | Lewis (British male) | 29.1s |

### Other files

- `myrtle_beach/myrtle_beach_video_brief.md`: highlights with report page references, script, post copy, and decisions made so far.
- `myrtle_beach/Nhr_Myb_0826_2.md`: the full report converted to Markdown. Charts are in `Nhr_Myb_0826_2_images/`.

**The call-to-action URL `reis-myrtlebeach.com` is made up. Replace it before posting anything publicly.**

## How to regenerate

```bash
brew install espeak-ng ffmpeg
python3 -m venv venv && ./venv/bin/pip install kokoro-onnx soundfile pillow numpy
# Kokoro model files (~350 MB), from github.com/thewh1teagle/kokoro-onnx releases (model-files-v1.0):
#   kokoro-v1.0.onnx, voices-v1.0.bin  → put them in myrtle_beach/video/kokoro/ (or set KOKORO_DIR)
cd myrtle_beach/video
../../venv/bin/python vo.py scripts/qa.json --speed 1.2      # voiceover segments → vo/qa/
../../venv/bin/python render.py scripts/qa.json               # → myrtle_beach_teaser_qa.mp4
../../venv/bin/python vo.py scripts/mono.json --voice af_heart
../../venv/bin/python render.py scripts/mono.json af_heart
```

Each script file in `scripts/` defines the voiceover text, the captions (question or answer style) and which scene shows during which lines. Scene graphics are defined in `render.py`.

## Credits

- Voices: [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache 2.0).
- Music: "Inspired" by Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0. **Credit it in every post caption.**
- Heat map base map: Esri, HERE, Garmin, USGS, NGA (the credit is shown on screen).
