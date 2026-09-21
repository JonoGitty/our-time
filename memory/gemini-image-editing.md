---
name: gemini-image-editing
description: "Reference-conditioned image editing via Gemini 3 Pro Image — the technique, the two failure modes, and the repair that works"
metadata:
  type: reference
---

For any job needing an **exact** logo, garment or product reproduced — which plain
text-to-image cannot do — use **Gemini 3 Pro Image** (`gemini-3-pro-image`,
`generateContent`) with the source image(s) as `inline_data` parts alongside the prompt.

Reference tool built for [[our-time-website]]: `C:\AI\Overtime\tools\genimg.py` (stdlib
only, no deps; falls back down a ladder of `generationConfig` shapes on a 400 so an
unknown field never kills the call).

**Capacity: 6 object + 5 character + 3 style references, 14 total.** Budget every
multi-reference call — exceeding the character cap is a silent quality cliff.
**Cost: $0.134 per 1K/2K image, $0.24 per 4K.** Batch tier is half price.

## It holds up well
Garment shape, fabric wash and texture, seams, stitching, lighting, shadows, the backdrop
and *existing printed graphics* all survive an edit essentially intact.

## Two failure modes — prompt against both, every time
1. **Letterspaced word spaces collapse.** `OUR TIME` came back as `OURTIME` repeatedly.
   Fix: demand the gap explicitly — "at least three times the gap between individual
   letters", and spell the target as `O U R` + gap + `T I M E`.
2. **Dark garments default to dark ink.** A print specified as light came back near-black
   on a black tee, illegible. Fix: state the ink colour **per colourway**, explicitly.

## The repair that works
**Iterate on the previous OUTPUT, not the original.** Re-prompting the source re-rolls
everything and often fixes one mark while breaking another (on the jeans, v2 fixed the leg
and reverted the waistband). Feeding v2 back in and correcting only the remaining error
worked first time. Fix one mark per pass.

Aspect drifts slightly (1.2496 in → 1.2414 out). Irrelevant for mockups; crop if parity matters.
