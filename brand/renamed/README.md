# Renamed renders — OVERTIME → OUR TIME

Produced with `tools/genimg.py` (Gemini 3 Pro Image, reference-conditioned edit).
Source images untouched in `brand/source/`.

**`APPROVED/` holds the four files to use.** Everything else in this folder is
a superseded attempt, kept so the iterations are auditable.

| Garment | Approved file | Attempts | What the earlier passes got wrong |
|---|---|---|---|
| Tees ×4 (white/black/navy/cream) | `07-tees-white-black-navy-cream.png` | v1, **v2** | v1 printed dark ink on the washed-black tee, leaving it almost illegible. v2 forced pale ink on the dark garments. |
| Shorts (washed grey + denim) | `02-shorts-washed-grey-denim.png` | **v1** | Correct first time — both the vertical leg mark and the above-pocket mark, clock-face print preserved. |
| Sweatpants (washed black) | `05-sweatpants-black.png` | **v1** | Correct first time. OT back-pocket monogram preserved. |
| Jeans (washed black baggy) | `06-jeans-black-baggy.png` | v1, v2, **v3** | v1 set both marks as `OURTIME` with no word space. v2 fixed the leg but reverted the waistband to `OVERTIME`. v3 fed v2 back in and corrected only the waistband. |

## What this proved

1. **Reference-conditioned editing works on this key** and holds garment shape,
   fabric wash, seams, lighting and the near-black backdrop essentially intact.
2. **Existing graphics survive.** The Roman-numeral clock-face pocket print and
   the all-over OT pattern came through untouched every time.
3. **Two failure modes to prompt against, every time:**
   - *Word space collapse* — `OUR TIME` renders as `OURTIME` unless the prompt
     explicitly demands a gap several times the letter-spacing.
   - *Ink-contrast drift* — on dark garments it defaults to dark ink. State the
     ink colour per colourway.
4. **Iterating on a generated file is the reliable repair.** Fixing one mark at
   a time on the previous output beat re-prompting the original.
5. Aspect drifts very slightly (source 1402×1122 = 1.2496; output 2304×1856 =
   1.2414). Irrelevant for mockups; crop if pixel-parity is ever needed.

## Cost

7 generations at 2K, ~1,120 output image tokens each. Roughly **$1** all in.

## Still printed OVERTIME — not regenerated

Nothing. All four affected sheets are done. Sheets 04, 08, 09 and 12 carry only
the `OT` monogram, and 03, 10 and 11 already read `OUR TIME`.
