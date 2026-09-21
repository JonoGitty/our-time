# OVERTIME — brand tokens

Source of truth: the four supplied product renders in `brand/source/`.
Colour values below are **measured** from those files (ffmpeg area-average over a
fabric patch), not eyeballed. Re-derive with `scratchpad/swatch.sh` if assets change.

## Ink & ground

| Token | Hex | Notes |
|---|---|---|
| `--ot-void` | `#000000` | The flat photographic backdrop. True black. |
| `--ot-ground` | `#0F0F0F` | The *textured* backdrop on the tee render. Use this as the page ground, not `#000` — it holds grain. |
| `--ot-bone` | `#FAF6F6` | Logo white. Very slightly warm — it is NOT `#FFF`. |

## Garment colourways (the actual product line)

| Colourway | Hex | Product |
|---|---|---|
| Navy | `#141B2C` | Oversized washed tee (hourglass back-print) |
| Navy (short) | `#141925` | Sweat short |
| Washed black | `#171717` | Sweat short — note it is distinctly *lighter* than the backdrop; it must never sit on `#000` |
| Washed grey | `#A7A5A4` | Sweat short — neutral, very slightly warm |
| Washed denim | `#54647E` | Sweat short — desaturated slate-blue |
| Off-white | `#DFDDDE` | Sweat short — cool-leaning |
| Cream / sand | `#CFC2B4` | Sweat short — the only warm tone in the range |

## Observations that constrain the design

- **Every colour in this brand is desaturated.** The most saturated thing in the
  entire range is `#54647E`, which is still a muted slate. Any accent colour
  introduced by the site will be the loudest thing the brand owns — so either
  don't, or make that a deliberate decision.
- **The logo lockup is a deliberate contrast pair**: a heavy, italic, sheared
  `OT` monogram against a thin, very widely letterspaced `OVERTIME` wordmark.
  That tension is the brand's typographic signature and the site type system
  should reproduce it rather than invent a third voice.
- **Motifs**: hourglass (distressed engraving), Roman-numeral clock face with
  `OT` at 12, all-over tessellated `OT` monogram pattern.
- **Copy voice seen so far**: `OUR TIME` · `EARN EVERY SECOND` · `TIME WON'T WAIT` · `EST. 2026`.
- **Photography language**: flat-lay, dead-on, soft top light, near-black ground,
  subtle vignette, fabric wash texture visible. Muted and tactile, never glossy.
