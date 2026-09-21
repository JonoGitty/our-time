---
name: our-time-website
description: "OUR TIME clothing brand website (Jono's cousin) — brand facts, corrected assets, the design direction, and the reference-conditioned image pipeline"
metadata:
  type: project
---

**OUR TIME** — a streetwear/athleisure label (EST. 2026) belonging to **Jono's cousin, Oliver**.
Jono is building the website. Brand calls are Oliver's to make — do not presume them. Working dir `C:\AI\Overtime\` (folder name predates the
rename — the brand is OUR TIME, not Overtime).

## The name trap — read this first
Jono initially briefed it as "Overtime", then corrected it on 16 Sep 2026: **the brand is
OUR TIME**. The `OT` monogram = **O**ur **T**ime. But the supplied product renders are
*internally inconsistent* — shorts, sweatpants, jeans and four tees were printed
`OVERTIME`, while the hourglass/globe/watch tees read `OUR TIME`. **This is a production
issue, not just a web one** — flagged to Jono; artwork may need pulling from a
manufacturer. Corrected renders live in `brand/renamed/APPROVED/`.

## Brand facts
- Range: oversized tee, polo, crewneck, zip hoodie, sweat shorts, sweatpants, baggy jeans
  — 7 garment types, ~31 colourways. A real range, not a capsule.
- Motifs: hourglass · Roman-numeral clock face with OT at 12 · orbital globe with 24/7 ·
  engraved wristwatch · all-over tessellated OT pattern.
- Copy: `OUR TIME.` `EARN EVERY SECOND.` `TIME WON'T WAIT.` `DISCIPLINE. FOCUS.
  CONSISTENCY.` `EST. 2026`.
- Coordinates on the globe tee were Chicago (a generator artefact); Jono had them changed
  to **57.5878° N, 4.2383° W** (the Black Isle). That is a PRODUCT decision and it stands.
  **But the Black Isle BRAND POSITIONING is withdrawn** — Jono, 16 Sep 2026: "I don't want the
  Black Isle strategy brand thing, keep the time and stuff, that's for Oliver to decide."
  So: no Highland/Scottish origin story, no Highland-light narrative, no location photography
  direction, no coordinates as a brand signature. The 24-hour colour index SURVIVES — it is a
  time system and never needed the place. See `docs/brand/DECISIONS.md` §1.
- Measured palette in `brand/TOKENS.md`. **Two contrast traps, enforced in schema:**
  `#171717` washed black on `#0F0F0F` ground = 1.07:1 (invisible); `#A7A5A4` washed grey on
  `#DFDDDE` paper = 1.84:1. Every colourway carries a required `bg: dark | paper` field
  that decides both the generation backdrop and the display ground.

## Decisions taken
Full storefront (not a teaser page) · no Shopify store yet, so commerce sits behind a
swappable `StorefrontAdapter` · AI-gen budget ~$15 to prove the pipeline · casting
art-directed by us with faces approved before scaling.

Direction doc: `docs/DIRECTION.md` — **"THE LEDGER"**: time as the filing system, not
decoration. The judging panel split three ways (brand→SLOW HAND, engineering→GLASS
EMPTIES, commerce→COUNTER) so the direction is a deliberate hybrid. **Three things all
three concepts got wrong and were killed:** the hourglass scroll sequence (top-ranked
cliché, unrendered, single point of failure), fabricated photo datelines, and the
always-on countdown ("scarcity that's always on is a Shopify app").

## The image pipeline — the key capability
**`aiorch image` is text-to-image ONLY (GPT Image 2, no reference input)** — it can never
reproduce an exact logo or garment. Built `tools/genimg.py`: reference-conditioned
generation/editing via **Gemini 3 Pro Image** (`generateContent`, inline_data parts,
stdlib only, reads GEMINI_API_KEY from the aiorch .env). See [[gemini-image-editing]] for
the reusable technique and its failure modes.

Video is available on Jono's existing keys: **Sora 2 / Sora 2 Pro** (OpenAI) and **Veo 3.1
generate/fast/lite** (Gemini, `predictLongRunning`). Recommended: Veo 3.1 Fast, $0.10/s →
$0.80 per 8s clip. Gemini 3 Pro Image = $0.134 per 1K/2K image.

## Hard technical constraints (researched, cited in docs/research/)
- **`backdrop-filter: url(#svg)` is Chromium-only.** WebKit bug 245510 status NEW, PR 68614
  `merging-blocked`. **Firefox `@supports` returns TRUE while rendering nothing**, so
  feature detection is actively harmful — use an **engine gate**. Tier 2 (plain
  backdrop-blur) is the real product because that is what iPhone gets.
- Scroll media: **image sequence, not scrubbed video** (iOS Safari drops seeks under load).
- Gemini 3 Pro Image caps: **6 object + 5 character + 3 style references, 14 total.**

## Live
Glass Lab prototype (device-testable, shows which tier your browser resolves to):
https://claude.ai/artifact/MUqNpC348RvjcsbSGGES26
