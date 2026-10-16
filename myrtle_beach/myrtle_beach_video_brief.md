# Myrtle Beach New Homes Review: Social Video Brief

**Source:** New Homes Review, Myrtle Beach Region, Vol 20 · Issue 4 (01/01/2026 – 08/31/2026). Full conversion: `Nhr_Myb_0826_2.md`
**Deliverable:** one vertical video, 1080×1920 (9:16), up to 30 seconds, for YouTube Shorts, Instagram Reels and X
**Status:** script draft v1

---

## 1. Key numbers (all checked against the report)

| # | Highlight | Number | Source page |
|---|---|---|---|
| H1 | Closings, Jan–Aug 2026 | **5,812** | p.3 |
| H2 | August closings, compared with Aug '25 | **766, up 3.0%** (744 last year) | p.3 |
| H3 | National new-home sales, Aug '26 vs Aug '25 | **down 2.0%** (South region up 3.4%) | p.4 |
| H4 | Average new-home price, trailing 12 months | **$374,680, up 1.2%** | p.3 |
| H5 | Top builder | **DR Horton: 1,614 closings, 28% share** | p.3, p.38 |
| H6 | Fastest-growing top-10 builder | **Logan Homes: closings up 55% (155 to 241)** | p.3, p.39 |
| H7 | Busiest community | **Auberon Woods: 157 closings** | p.5, p.43 |
| H8 | Leading county | **Horry: 3,581 closings, 61.6% of the region** | p.3 |
| H9 | Top-10 builders' total sales volume | **$1.62B, up 8%** | p.41 |
| H10 | New communities this period | Bayview, Winfield Farms, Blue Heron Retreat | p.3 |
| H11 | Report length | 112 pages | n/a |

## 2. Graphics shortlist (charts from the report shown on screen)

| Slot | Graphic | File | Note |
|---|---|---|---|
| G1 | Closings heat map | `Nhr_Myb_0826_2_images/Nhr_Myb_0826_2.pdf-0006-04.png` | Square, so it suits a vertical frame. The Esri credit must stay visible. |
| G2 | Closings by month, 2022–2026 | `…-0015-04.png` | Landscape. Slow zoom onto the 2026 red bars. |
| G3 | Builder market share pie | `…-0038-04.png` | Square. Push in on the DR Horton slice. |
| G4 | Top-20 subdivisions bar chart | `…-0043-04.png` | Square. Auberon Woods is already highlighted red. |
| G5 | Report cover / page flip | PDF pp.1–3 rendered | For the call to action at the end. |

Brand colours taken from the report: navy `#1B3A7A` and red `#C8282D`, on white.

## 3. Script v2 (rendered, about 29 seconds)

| Scene | Voiceover | On screen | Graphic |
|---|---|---|---|
| 1. Hook | "U.S. new home sales slipped two percent in August. Myrtle Beach and Brunswick County? Up three." | ▼2.0% U.S. → ▲3.0% Myrtle Beach & Brunswick Co. | Stat cards |
| 2. Volume | "Over fifty-eight hundred new homes closed this year, with average prices at three seventy-five." | 5,812 (counts up) → $374,680 ▲1.2% | G1 heat map → G2 closings by month |
| 3. Builders | "D.R. Horton leads with twenty-eight percent. The breakout? Logan Homes, up fifty-five percent." | #1 DR HORTON, 28% → LOGAN HOMES ▲55%, 155 → 241 | G3 pie → top-10 builder YoY chart (p.39) |
| 4. Community | "Busiest community: Auberon Woods, with a hundred fifty-seven closings." | AUBERON WOODS, 157 closings | G4 top-20 subdivisions |
| 5. Call to action | "Builder rankings, pricing, and a hundred more pages at REIS Myrtle Beach dot com." | 112 PAGES, report pages flipping | Pages 1, 51, 43 |
| End card | (music only) | Logo · reis-myrtlebeach.com · "Get the full report" | White card |

## Production (`video/`)

- `vo.py`: renders each voiceover line with Kokoro (needs `brew install espeak-ng`). Output goes to `vo/<voice>_lineN.wav`.
- `render.py <voice>`: draws the frames with Pillow, encodes with ffmpeg, and mixes the voiceover with music that dips under the voice. Output: `myrtle_beach_teaser_<voice>.mp4` (1080×1920, 30 fps, H.264/AAC).
- Voices rendered: `af_heart` (US female), `am_michael` (US male), `bm_george` (British male).
- Music (placeholder): "Inspired" by Kevin MacLeod (incompetech.com), CC BY 4.0. **The post caption must credit it:** Music: "Inspired" Kevin MacLeod (incompetech.com), Licensed under Creative Commons: By Attribution 4.0

## 4. Post copy (draft)

- **YouTube Short title:** Myrtle Beach new homes are beating the national trend 📈
- **Instagram / X caption:** U.S. new home sales ▼2%. Myrtle Beach ▲3%. 5,812 closings so far in 2026, DR Horton on top and Logan Homes up 55%. The full 112-page New Homes Review is at reis-myrtlebeach.com
- **Hashtags:** #MyrtleBeach #NewConstruction #RealEstateData #Homebuilders #GrandStrand #HousingMarket

## 5. Decisions (2026-10-16)

- **Logo:** use the one from the PDF for now.
- **Naming:** all data comes from public sources, so builders and communities can be named.
- **Graphics:** use the report's charts as they are; improve them if the concept works.
- **Call to action:** a made-up URL, given as "REIS_myrtle_beach.com". Domain names can't contain underscores, so the proposed spelling is **reis-myrtlebeach.com**. Swap in the real URL before posting anywhere public.
- **Voiceover, test version:** Kokoro-82M. It is free, runs on the Mac and its Apache 2.0 licence allows commercial use. For the final version, either the ElevenLabs Starter plan ($5/month, includes commercial rights) or keep Kokoro.
- **Music:** a royalty-free track whose licence has been checked (candidate sources are listed in the chat).

- **Pronunciation:** say REIS as letters, R-E-I-S (the voiceover text is written "R. E. I. S."). Say "DR Horton" with no pause between D and R (written "DR Horton" in the voiceover text; captions use the correct spelling "D.R. Horton").
- **Single-voice version:** the preferred voice is `af_heart`.
- **Q&A version (being tested):** Bella reads the intro ("This is the REIS New Homes Review for Myrtle Beach and Brunswick County") and asks the questions; Onyx answers with the data. Script: `video/scripts/qa.json`. Runs about 35.6s.
- **Sharing:** private repo at github.com/DogThatHunts/reis-marketing.

## 6. Open questions

1. Price in the voiceover: "$375K" (easier to hear) or the exact "$374,680"?
2. Is "Myrtle Beach region" the right name? It includes Brunswick County, NC.
3. Voice: pick from the Kokoro samples once they're generated.
