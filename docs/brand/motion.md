# 3. VISUAL IDENTITY SYSTEM

*Status: specification. Where this document and any existing artwork disagree, this document wins. Every value here is either measured from the approved renders or specified as a rule to be applied. Anything marked PROVISIONAL has not been measured yet and must be measured before it is used in production.*

---

## 3.0 The single source of truth (read this first)

The label has shipped garments printed **OVERTIME** and garments printed **OUR TIME**. That is not a print error, it is a governance error, and it will happen again unless the following is enforced.

**Rule 3.0.1 — Spelling.** The brand is **OUR TIME**. Two words. Always uppercase in the wordmark. Never "Overtime", never "OurTime", never "OURTIME", never "Our Time" in sentence case inside artwork. In running body copy it may be written *Our Time* in sentence case; in artwork it is never anything but OUR TIME.

**Rule 3.0.2 — The monogram means something.** OT = **O**ur **T**ime. Anyone who reads it as "overtime" has been given no reason not to. The wordmark's job is to close that gap (§3.1).

**Rule 3.0.3 — No live type in artwork.** The wordmark is supplied as outlined vector only. Nobody — printer, embroiderer, developer, the founder at 1am — types the words into a text box. The word space has already collapsed in production once (§3.1.6); typed spaces are how it collapses again.

**Rule 3.0.4 — The master library.** One cloud folder, one owner, read-only to everyone else:

| Folder | Contents | Format |
|---|---|---|
| `01_LOGO/` | Monogram, wordmark, 3 lockups | `.ai` master, `.svg`, `.eps`, `.pdf`, `.png` @1x/2x/3x |
| `02_COLOUR/` | `.ase` swatch library, lab-dip photos, this palette table | `.ase`, `.pdf` |
| `03_TYPE/` | Licensed font files + licence PDFs | vendor files |
| `04_MOTIFS/` | Hourglass, dial, globe, watch, pattern tile | `.ai`, `.svg` |
| `05_ARTWORK_APPROVED/` | Every production-ready print file, versioned | `.ai` + flattened `.pdf` |
| `99_ARCHIVE/` | Everything superseded, including the OVERTIME files | frozen |

**Rule 3.0.5 — Pre-press checklist.** No file goes to a supplier without a signed-off version of this, on one page, in the file name (`TEE_NAVY_BACK_HOURGLASS_v4_APPROVED.pdf`):
1. Spelling reads OUR TIME, two words, checked at 100% and at 25%.
2. Wordmark is outlined; word gap ≥ 3× letter gap (§3.1.6).
3. Colours match the palette hexes / approved lab dips — no stray RGB, no unnamed swatches.
4. Ground assignment respected (§3.2.5).
5. Minimum size respected for the process being used (§3.1.5).
6. Coordinates, if present, read **57.5878° N, 4.2383° W** (§3.4.3).

---

## 3.1 Logo system

### 3.1.1 The two voices

| | **OT monogram** | **OUR TIME wordmark** |
|---|---|---|
| Form | Heavy, right-leaning italic, chunky athletic, sharp angular shear cuts | Thin/light uppercase sans, very wide letterspacing |
| Register | Loud. Motorsport, varsity, team kit | Quiet. Premium, editorial, restrained |
| Job | **Identification at distance and at small size.** Chest marks, embroidery, buttons, pattern, favicon, anything under 30mm | **Naming and legitimising.** Says what the brand is called, in full, in its own voice. Back prints, hang tags, packaging, site header, footer, labels |
| Frequency | High. Appears on almost every garment | Low. Appears once per surface, never twice |
| Never | Set in a typeface — it is a drawn mark | Used as a chest mark; used below its minimum size |

**The typographic signature is the contrast between these two.** Heavy against thin, tight against wide, loud against quiet. Every other typographic decision in the brand (§3.3) reproduces that tension. **A third voice is not permitted** — no script, no serif, no condensed gothic, no display face that sits between the two.

### 3.1.2 Approved lockups

Only three. Nothing else is an approved configuration.

| Lockup | Construction | Use |
|---|---|---|
| **A — Horizontal** | Monogram left, wordmark right, both centred on a shared optical axis. Gap between monogram right edge and wordmark first letter = **0.75 M**. Wordmark cap height = **0.42 M** | Site header, hang tags, letterhead, lookbook masthead, email signature, anything wide and small |
| **B — Stacked** | Monogram above, wordmark below, both centred on a shared vertical axis. Gap from monogram baseline to wordmark cap line = **0.50 M**. Wordmark cap height = **0.34 M**; wordmark overall width should optically match monogram width ±10% | Back prints, packaging, woven labels, poster, social avatar at large sizes, shipping box |
| **C — Monogram alone** | The mark, unaccompanied | Chest marks, embroidery, buttons, zip pulls, favicon, pattern unit, anything below 30mm |

**Wordmark alone** is permitted but is not a lockup — it is a *typographic element*, used the way a masthead is: at the top or foot of a composition, never floated in the middle, never as the only identifier on a garment.

Lockups are **locked artwork**. Nobody rebuilds them from parts. Nobody changes the gaps.

### 3.1.3 The clear space unit

**M = the full vertical height of the OT monogram's bounding box**, measured on the upright rectangle that encloses the italic mark including its shear cuts (not the optical cap height — the cuts overshoot and must be inside the measurement).

| Element | Minimum clear space | Preferred |
|---|---|---|
| Monogram alone | **0.50 M** on all four sides | 1.00 M |
| Lockup A (horizontal) | **0.50 M** top/bottom, **0.75 M** left/right | 1.00 M all round |
| Lockup B (stacked) | **0.50 M** all round | 1.00 M |
| Wordmark alone | **1.50 W** above/below, **2.00 W** left/right, where W = wordmark cap height | 2.00 / 3.00 W |

The wordmark needs more air than the monogram because its own tracking is wide; crowd it and the letterspacing stops reading as intentional and starts reading as broken.

Nothing enters clear space: no other type, no image edge, no rule, no trim, no fold, no seam, no button, no stitch line.

### 3.1.4 Minimum sizes

| Asset | Screen (min width @1x) | Litho / digital print | Screen print / DTG on fabric | Embroidery | Emboss / deboss / foil |
|---|---|---|---|---|---|
| OT monogram | **24 px** | **8 mm** | **10 mm** | **25 mm** | **12 mm** |
| OUR TIME wordmark | **128 px** | **32 mm** | **40 mm** | **do not embroider below 60 mm — prefer a woven label** | **45 mm** |
| Lockup A | **160 px** | **40 mm** | **48 mm** | 70 mm | 55 mm |
| Lockup B | **112 px** | **28 mm** | **34 mm** | 55 mm | 40 mm |

Below the monogram's minimum the shear cuts fill in and the mark reads as a blob. Below the wordmark's minimum the hairline strokes drop out and the tracking closes (§3.1.6).

**Embroidery note:** the wordmark's thin strokes cannot be satin-stitched at any sane size. Where the full name is needed on a garment, use a woven or printed label, not thread.

### 3.1.5 Small-size behaviour

There is no separate "small logo". There is one monogram, and below 12 mm / 32 px the file to use is the **small-size master** in `01_LOGO/`, which has the shear cuts opened by 4% and the interior counters opened by 6% to survive ink gain. It is a production variant, not a redesign. Never scale the large master below 12 mm.

### 3.1.6 The word space rule (the one that has already failed)

The space between OUR and TIME is structural. It is the only thing preventing the brand being read as one word.

**Rule:** the gap between the R and the T (word gap) must be **≥ 3.0× the gap between two adjacent letters** (letter gap), measured optically between the nearest stems.

Implementation values:

| Context | Letter tracking | Word gap |
|---|---|---|
| Logo artwork (outlined) | **+320/1000 em (0.32 em)** | **+0.96 em minimum** (i.e. tracking + one full em space) |
| CSS | `letter-spacing: 0.32em` | `word-spacing: 0.64em` (additive → 0.96 em total) |
| Embroidery digitising | specified in **mm**, never as a character | ≥ 3× the digitised letter gap, stated on the spec sheet |

Below 32 mm / 128 px the gap is no longer reliably reproduced. That is *why* the minimum size exists — it is not a taste rule, it is the rule that stops OURTIME reaching a garment again.

### 3.1.7 Misuse — prohibited, with reasons

| # | Do not | Because |
|---|---|---|
| 1 | Outline or stroke the monogram | The mark's weight *is* its identity; a stroke thins the solid and thickens the counters, inverting the heavy/thin contrast the whole brand rests on |
| 2 | Add a drop shadow, glow, bevel or emboss effect | The brand is flat, matte and washed. A shadow makes it look like a 2012 gym-supplement logo, and it will not separate on the #0F0F0F ground |
| 3 | Recolour either mark | Only three colour states exist (§3.2.6). A recoloured mark is an unapproved brand |
| 4 | Stretch, condense, or scale non-proportionally | Distortion destroys the drawn shear angles, which are the mark's only distinguishing feature |
| 5 | Re-italicise, un-italicise, or change the lean angle | The lean is drawn, not applied. Re-slanting produces a double-obliqued mark |
| 6 | Set the wordmark tight, or default-tracked | At normal tracking it is a generic light sans and stops being a wordmark |
| 7 | Use the wordmark below 32 mm / 128 px | Tracking closes, hairlines drop out, OURTIME happens |
| 8 | Typeset the wordmark live in any font | The letterforms and space are outlined artwork. Live type will substitute, re-track, or reflow |
| 9 | Rebuild a lockup by eye | The three lockups have fixed gaps; a rebuilt one is a fourth, unapproved lockup |
| 10 | Place the monogram inside a circle, shield, box or badge | The shear cuts are the containment. A container fights them and adds a shape the brand does not own |
| 11 | Rotate either mark (except the pattern's one approved 90° tape variant, §3.4.6) | The italic already supplies the diagonal; rotation reads as a second, conflicting angle |
| 12 | Use the monogram as a letter inside a word (e.g. "OT-CORE") | It is a mark, not a glyph |
| 13 | Place either mark on a busy or mid-tone photographic area | See the contrast traps, §3.2.4 |
| 14 | Pair the monogram and wordmark other than at the specified sizes (0.42 M / 0.34 M) | The heavy/thin ratio is the signature; change the ratio and the tension goes |
| 15 | Show both marks twice on one surface | One identification per surface. Repetition reads as insecurity |

---

## 3.2 Colour

### 3.2.1 Roles

Every colour has exactly one job. Colours do not move between roles.

| Role | Hex | Name | Used for |
|---|---|---|---|
| **Ground** | `#0F0F0F` | Ground | The brand's base surface: photographic ground, site background, box interiors, tag backs. **This is the brand's black. `#000000` is not.** |
| **Ground (photographic only)** | `#000000` | Backdrop | Only the far backdrop in photography where true black falloff is wanted. Never a fill, never a type colour, never a CSS background |
| **Paper** | `#FAF6F6` | Logo White | The warm white of the marks and of positive-print surfaces. Slightly warm — **never `#FFFFFF`** |
| **Paper (secondary)** | `#DFDDDE` | Off-White | The paper *ground* for photography and layouts where `#FAF6F6` would clip; card stock reference |
| **Ink (on paper)** | `#0F0F0F` | Ground | All type on light surfaces |
| **Ink (on ground)** | `#FAF6F6` | Logo White | All type on dark surfaces |
| **Accent (the only one)** | `#54647E` | Washed Denim | The single permitted non-neutral. Links, active states, data marks, the coordinate line, the one thing on a page allowed to be a colour |
| **Neutral / support** | `#A7A5A4` | Washed Grey | Secondary type on the dark ground, rules, dividers, disabled states |
| **Warm neutral** | `#CFC2B4` | Cream/Sand | Alternate paper surface, packaging board, warm garment ground |

**Rule 3.2.1a — The accent ceiling.** `#54647E` is the most saturated colour the brand owns (C* ≈ 16). Any colour introduced above that chroma instantly becomes the loudest thing in the brand and breaks the washed/desaturated premise. **No new accent may exceed C\* 20 in CIELAB.** There is no "brand red", no highlight yellow, no neon. Emphasis is created by scale, weight and space, not hue.

### 3.2.2 Garment colours

| Hex | Name | Garment(s) |
|---|---|---|
| `#FAF6F6` | Logo White | Tee (wordmark, orbital-globe, wristwatch back prints), polo |
| `#DFDDDE` | Off-White | Sweat shorts |
| `#CFC2B4` | Cream / Sand | Tee, crewneck, zip hoodie, sweat shorts |
| `#141B2C` | Navy (jersey) | Tee (hourglass + wordmark back prints), polo, crewneck, zip hoodie |
| `#141925` | Navy (fleece/woven) | Sweat shorts, sweatpants — a *second, cooler-darker* navy; see 3.2.2a |
| `#171717` | Washed Black | Tee, crewneck, zip hoodie, sweat shorts, sweatpants, baggy jeans (washed black denim) |
| `#A7A5A4` | Washed Grey | Sweat shorts |
| `#54647E` | Washed Denim | Sweat shorts |
| PROVISIONAL | Forest Green | Polo |
| PROVISIONAL | Brown | Polo |
| PROVISIONAL | Tan | Zip hoodie |
| PROVISIONAL | Taupe | Crewneck |

**Rule 3.2.2a — Two navies is one navy too many.** `#141B2C` and `#141925` are visually indistinguishable apart and obviously different side by side. Pick one as the brand navy at the next production run and migrate. Until then: they may **never appear in the same photograph, flat-lay set, or product grid**. If the navy tee and the navy short are shown together, one of them is the wrong navy and a customer will notice on arrival.

**Rule 3.2.2b — Unmeasured colours.** Forest green, brown, tan and taupe have **no authoritative value**. They are to be sampled from an approved physical lab dip under D65 at 45°/0°, entered into this table as hex + CIELAB, and only then used in artwork or on the site. Until sampled they must not be rendered, swatched on the website, or described with a hex. Provisional targets for briefing the mill only, not for artwork: forest ≈ `#2E3B33`, brown ≈ `#6B5B4E`, tan ≈ `#A08F7B`, taupe ≈ `#8C8277`. All four must satisfy Rule 3.2.1a (C* ≤ 20).

### 3.2.3 Print equivalents

Hex is authoritative. CMYK builds below are **starting points for US Web Coated (SWOP) v2, total ink ≤ 300%** — they must be proofed. Pantone references are **nearest visual match, to be confirmed against a physical chip or lab dip before any run.** Where hex and a Pantone chip disagree, the hex wins and the Pantone number gets changed.

| Hex | CMYK (coated, start point) | Nearest Pantone (solid coated) | Textile (TCX, confirm by lab dip) |
|---|---|---|---|
| `#0F0F0F` | 63 / 52 / 51 / 100 *(rich black; use K100 alone for type under 14pt)* | Black 6 C *(runs slightly cool)* / Neutral Black C | 19-4007 TCX Anthracite |
| `#000000` | n/a — photographic only | n/a | n/a |
| `#FAF6F6` | **Do not build.** Use unprinted warm stock, or opaque white ink | No solid match — specify stock or opaque white | 11-0601 TCX Bright White |
| `#DFDDDE` | 0 / 1 / 0 / 13 | Cool Gray 1 C | 11-4201 TCX Cloud Dancer |
| `#CFC2B4` | 3 / 8 / 16 / 12 | Warm Gray 2 C *(less yellow than target)* | 13-0907 TCX Cement / 14-1116 TCX Oatmeal |
| `#141B2C` | 85 / 75 / 50 / 70 | 5395 C, alt 289 C *(289 is more saturated)* | 19-4052 TCX Navy Blazer *(reads one step light)* |
| `#141925` | 85 / 75 / 55 / 78 | Black 6 C | 19-4010 TCX Dress Blues (dark side of tolerance) |
| `#171717` | 60 / 50 / 50 / 95 | Neutral Black C | 19-0303 TCX Jet Black (washed finish) |
| `#A7A5A4` | 0 / 2 / 3 / 40 | Cool Gray 6 C *(marginally cooler)* | 16-3850 TCX? — use 15-4502 TCX Silver / confirm |
| `#54647E` | 70 / 55 / 30 / 15 | 5405 C | 18-3920 TCX Coronet Blue |

**Fabric printing notes (load-bearing):**
- Hand-feel must stay soft and washed. Default is **water-based / discharge**, not thick plastisol. A raised plastisol slab contradicts the entire aesthetic.
- **Discharge will not give you `#FAF6F6` on `#141B2C` navy** — reactive navy dyes discharge to tan/pink, not white. White-on-navy back prints need either a discharge-underbase strike-off approved in advance, or a soft-hand low-cure plastisol with a *tested* hand-feel. Require a physical strike-off. This is the single most likely production disappointment in the range.
- Washed-black `#171717` garments are garment-dyed: expect ΔE up to 3.0 between batches. State the tolerance in the PO (**ΔE ≤ 2.0 preferred, ≤ 3.0 acceptable, measured D65 45°/0°**) or the "washed black" crewneck and the "washed black" hoodie will not match on a customer's floor.

### 3.2.4 Contrast — hard rules

Computed per WCAG 2.1 from the measured hexes. These are not guidelines.

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| `#FAF6F6` | `#0F0F0F` | **17.9 : 1** | Primary pairing. Use this |
| `#DFDDDE` | `#0F0F0F` | **14.2 : 1** | Pass |
| `#0F0F0F` | `#FAF6F6` | **17.9 : 1** | Primary pairing (positive) |
| `#0F0F0F` | `#DFDDDE` | **14.2 : 1** | Pass |
| `#0F0F0F` | `#CFC2B4` | **10.8 : 1** | Pass |
| `#FAF6F6` | `#141B2C` | **16.0 : 1** | Pass |
| `#A7A5A4` | `#0F0F0F` | **7.8 : 1** | Pass — secondary type on ground |
| `#FAF6F6` | `#54647E` | **5.6 : 1** | Pass — white on the accent is fine |
| `#54647E` | `#DFDDDE` | **4.4 : 1** | ⚠ **Fails AA body text (needs 4.5).** Accent on paper is permitted for large text ≥ 24px/18.66px-bold and for UI marks only. For body-size links on paper, use `#141B2C` (12.7 : 1) |
| `#54647E` | `#0F0F0F` | **3.2 : 1** | ⚠ Large text and UI only. Never body copy |
| **`#171717`** | **`#0F0F0F`** | **1.07 : 1** | 🚫 **TRAP 1 — INVISIBLE. Forbidden in all media.** |
| **`#A7A5A4`** | **`#DFDDDE`** | **1.8 : 1** | 🚫 **TRAP 2 — FORBIDDEN.** |
| **`#141B2C`** | **`#0F0F0F`** | **1.12 : 1** | 🚫 **TRAP 3 — INVISIBLE.** Navy on ground is the same mistake as Trap 1 and is easier to make |
| `#141925` | `#0F0F0F` | 1.09 : 1 | 🚫 Same trap |
| `#A7A5A4` | `#CFC2B4` | 1.39 : 1 | 🚫 Grey on cream is unreadable |

**Rule 3.2.4a.** Minimum contrast for any type, any medium: **4.5 : 1** for body, **3.0 : 1** for text ≥ 24 px / 18 pt, and **3.0 : 1** for any non-text element a user must see (icons, form borders, the monogram over an image).

**Rule 3.2.4b.** The traps are not "hard to read". They are *invisible*. Every one of them is a plausible-looking design decision made by someone eyeballing swatches on a bright monitor. Check the number, not the screen.

### 3.2.5 The ground assignment rule

Every colourway is permanently assigned to **one** ground and may only ever be shown against that ground — in photography, on the website, in the lookbook, on packaging, in a paid ad.

**The test:** compute the garment colour's contrast against `#0F0F0F`.
- **≥ 3.0 : 1 → DARK GROUND colourway** (shot and displayed on `#0F0F0F`)
- **< 3.0 : 1 → PAPER GROUND colourway** (shot and displayed on `#DFDDDE`)

| Colourway | Ratio vs `#0F0F0F` | **Assigned ground** |
|---|---|---|
| `#FAF6F6` White | 17.9 | **DARK** `#0F0F0F` |
| `#DFDDDE` Off-White | 14.2 | **DARK** `#0F0F0F` |
| `#CFC2B4` Cream | 10.8 | **DARK** `#0F0F0F` |
| `#A7A5A4` Washed Grey | 7.8 | **DARK** `#0F0F0F` |
| `#54647E` Washed Denim | 3.2 | **DARK** `#0F0F0F` |
| `#171717` Washed Black | 1.07 | **PAPER** `#DFDDDE` (13.3 : 1) |
| `#141B2C` Navy | 1.12 | **PAPER** `#DFDDDE` (12.7 : 1) |
| `#141925` Navy | 1.09 | **PAPER** `#DFDDDE` (12.9 : 1) |
| Forest Green (prov.) | — | **PAPER**, pending measurement |
| Brown / Tan / Taupe (prov.) | — | Assign by the test once measured |

**Why this is a rule and not a preference:** the range is over half dark garments. Shot on the brand's own dark ground they disappear — a navy tee on `#0F0F0F` is a 1.12 : 1 silhouette. The instinct is to "fix" it with a rim light or a lifted background, which produces a different-looking background in every shot and destroys the grid. Assigning the ground once, per colourway, permanently, is what makes a 31-piece range look like one range.

**Corollary:** a product grid that mixes dark-ground and paper-ground tiles is *correct*, not broken. Do not "unify" it by putting everything on one background.

### 3.2.6 The logo's three colour states

Only these exist:

| State | Mark colour | Permitted grounds |
|---|---|---|
| **Positive** | `#0F0F0F` | `#FAF6F6`, `#DFDDDE`, `#CFC2B4`, and any garment ≥ 4.5 : 1 against it |
| **Reversed** | `#FAF6F6` | `#0F0F0F`, `#171717`, `#141B2C`, `#141925`, `#54647E` |
| **Tonal** | The garment's own colour at ΔL\* 8–12 (self-coloured embroidery, tonal print, debossed leather) | Any garment. This is the premium/quiet application — use it more than you think |

Tonal is exempt from the 3.0 : 1 rule because it is a *texture*, not a message. It must never be the only identification on a surface where identification is required.

---

## 3.3 Typography

### 3.3.1 The principle

The type system reproduces the logo's heavy/thin tension and nothing else. **Two weights do most of the work: something very heavy and wide, and something light and quiet.** Mid-weights are the enemy — they read as neither, and they are what "clueless-brand" looks like.

### 3.3.2 Recommended system (paid)

| Slot | Face | Foundry | Styles to buy | Licence | Indicative 2026 cost |
|---|---|---|---|---|---|
| **Display** | **Druk Wide** | Commercial Type | Bold Italic (+ Medium Italic optional) | Desktop 1–5 users + Web | ~£95–190 / style desktop; web from ~£95 |
| **Text** | **GT America** | Grilli Type | Regular, Medium, Light, + Extended Light for the wordmark voice | Desktop 1–3 users + Web (pageview tier) | ~£50–70 / style desktop; small web tier ~£50 |
| **Mono** | **GT America Mono** | Grilli Type | Regular, Medium | Desktop + Web | ~£50–70 / style |

Realistic launch kit: **4–6 styles total, ≈ £450–£800 all-in.** Buy fewer styles, not more — the system needs about five.

Alternatives at the same job, if the above are unavailable or over budget: display — **Monument Extended** (Pangram Pangram, ~£120 family, but heavily used), **Giorgio Sans** (Commercial Type); text — **Söhne** (Klim), **Neue Montreal** (Pangram Pangram, ~£100 family), **Founders Grotesk** (Klim); mono — **Basis Grotesque Mono** (Colophon), **Söhne Mono** (Klim).

> ⚠ **The licence clause that actually matters for a clothing label.** A standard desktop licence usually permits type **in artwork about the product** but **not type reproduced on merchandise for resale**. Printing a licensed typeface onto a garment you sell is frequently a separate, more expensive "merchandise", "product" or "logo" licence. Before any typeface goes on a garment: read the EULA section headed *Merchandise / Products for Resale*, and email the foundry for written confirmation. This is a real and commonly-breached restriction, and it is cheapest to solve before the first print run. **Prices above are indicative — confirm on the foundry's own site at purchase. Keep every licence PDF in `03_TYPE/`.**

### 3.3.3 Free / open alternatives (budget = £0)

All OFL-licensed: free for commercial use, **including on garments**, with no merchandise restriction. This is a legitimate system, not a compromise.

| Slot | Free face | Licence | Notes |
|---|---|---|---|
| **Display** | **Archivo Expanded Black Italic** (Omnibus-Type) | OFL | Variable width + weight + **true italics**. The closest free thing to the monogram's energy. Use the Expanded width axis at 110–125 |
| **Text** | **Switzer** (Indian Type Foundry / Fontshare) | Free for commercial | Clean neutral grotesk with a genuine Thin/Light — essential for the quiet voice. Second choice: **Inter** (OFL), though it reads "software" |
| **Mono** | **IBM Plex Mono** (OFL) | OFL | Neutral, wide-tracking-friendly. Second choice: **JetBrains Mono**. Avoid Space Mono — too characterful, fights the monogram |

**Never** use a faux-italic or faux-bold to fake a missing style. Set `font-synthesis: none;` globally in CSS and check that no print document is using a "fake italic" checkbox. Faking the heavy/thin contrast is the one failure mode that destroys the signature.

### 3.3.4 Type scale

Ratio 1.2 for text, deliberate jumps for display. Print sizes are the lookbook/tag equivalents.

| Token | Face / weight | Screen | Print | Tracking | Line-height | Use |
|---|---|---|---|---|---|---|
| `D1` | Display, Bold Italic | 96 px / 6 rem | 72 pt | **−0.02 em** | 0.92 | Full-bleed statements: "TIME WON'T WAIT." |
| `D2` | Display, Bold Italic | 64 px / 4 rem | 48 pt | −0.02 em | 0.94 | Section openers |
| `D3` | Display, Bold Italic | 48 px / 3 rem | 36 pt | −0.015 em | 0.98 | Product name, campaign title |
| `H1` | Text, Medium | 32 px / 2 rem | 24 pt | −0.01 em | 1.15 | Page heading |
| `H2` | Text, Medium | 24 px / 1.5 rem | 18 pt | −0.01 em | 1.25 | Sub-heading |
| `H3` | Text, Medium | 20 px | 15 pt | 0 | 1.30 | Small heading |
| `BODY-L` | Text, Regular | 18 px | 12 pt | **0** | 1.55 | Lead paragraph |
| `BODY` | Text, Regular | 16 px | 10.5 pt | **0** | 1.60 | All body copy |
| `SMALL` | Text, Regular | 14 px | 9 pt | 0 | 1.50 | Secondary, care copy |
| `LABEL` | **Mono**, Regular, UPPERCASE | 12 px | 8 pt | **+0.08 em** | 1.30 | Captions, spec labels, sizes, "EST. 2026", "24 / 7", coordinates |
| `MICRO` | **Mono**, Regular, UPPERCASE | 10 px | 7 pt | **+0.12 em** | 1.40 | Ledger index marks, file refs, page folios |
| *Wordmark* | *artwork — not type* | — | — | *+0.32 em* | — | §3.1 |

Minimum body size anywhere: **16 px on screen, 9 pt in print.** Care labels excepted (legal minimum applies).

### 3.3.5 Tracking — the rule that gets broken

**Wide tracking belongs to the mono and the wordmark ONLY.**

| Permitted wide tracking | Forbidden |
|---|---|
| The wordmark, at +0.32 em (fixed artwork) | Body copy at any positive tracking |
| Mono `LABEL` / `MICRO`, uppercase only, +0.08 / +0.12 em | Headings tracked out "for a premium feel" |
| — | Lowercase text tracked positively, ever |
| — | Sentence-case uppercase runs longer than 5 words |

Letterspacing lowercase is the single most common way a young label announces itself as a young label. Body text is tracked **0**. Heavy display type is tracked **negative** (large heavy faces always need it). The width in the brand comes from the *layout* (§3.6), not from stretched-out sentences.

### 3.3.6 Fallback stacks

```css
:root {
  --font-display: "Druk Wide", "Archivo Expanded", "Archivo",
                  "Arial Black", "Helvetica Neue", sans-serif;
  --font-text:    "GT America", "Switzer", "Inter",
                  -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  --font-mono:    "GT America Mono", "IBM Plex Mono", ui-monospace,
                  "SF Mono", Menlo, Consolas, monospace;
}
* { font-synthesis: none; }           /* no faux bold, no faux italic */
body { font-kerning: normal; font-feature-settings: "kern" 1, "liga" 1; }
.label, .micro { font-variant-numeric: tabular-nums; }  /* times/coords must not jitter */
```

`tabular-nums` on anything numeric is not optional: coordinates, prices, sizes and any displayed time must not shift width between states.

---

## 3.4 The motif system

### 3.4.1 Ranking

Five motifs is more than a launch brand can carry. They are ranked; rank determines frequency, prominence and budget.

| Rank | Motif | Tier | What it is FOR | Cliché risk |
|---|---|---|---|---|
| **1** | **All-over OT pattern** | **HERO** | Ownership. It is the logo, repeated — the only motif nobody else can use. Signature textile treatment | **Low** |
| **2** | **Roman-numeral dial (OT at 12)** | **HERO** | The brand's second mark. Badge, seal, pocket print, packaging seal, loading state | **High** — manageable (§3.4.4) |
| **3** | **Orbital globe + rings + compass star + 24/7** | **HERO (conditional)** | *Place.* The Black Isle coordinates. The brand's only concrete claim about where it is from | **Medium** — see §3.4.3 |
| **4** | **Engraved wristwatch** | SUPPORTING | Craft/quality register. Interior labels, hang-tag reverse, thank-you card | **High** |
| **5** | **Hourglass (distressed engraving)** | SUPPORTING — RESTRICTED | One heritage-engraving statement piece | **Very high** |

**Rule 3.4.1a — One motif per garment.** No garment carries two. A tee with an hourglass back print does not also get a dial on the sleeve.

**Rule 3.4.1b — One motif per surface.** Same for a page, a tag, a box, a post.

### 3.4.2 Rank 1 — The all-over OT pattern (hero)

The most valuable asset in this list, because it is the only one that is *definitionally* this brand. Push it: waistband tape, pocket bags, interior facings, box tissue, mailer bag, site texture, the denim wash.

Rules in §3.4.6.

### 3.4.3 Rank 3 — The orbital globe, and the Black Isle

The globe currently exists as a generic grind-culture object with coordinates attached — and the coordinates were, until recently, **Chicago, a generator artefact**. They are now **57.5878° N, 4.2383° W — the Black Isle, Scotland**. That change is worth more than every other motif combined, and it is not yet being cashed in.

A grind-culture label from nowhere is one of ten thousand. A garment-dyed heavyweight label from a Highland peninsula — sea, firth, farmland, red sandstone, nine hours of usable winter daylight — is one of roughly none. The globe is the motif that carries this. Therefore:

**Rule 3.4.3a — Orientation.** The globe is **always oriented to show the North Atlantic and the British Isles**, with the marker over the Black Isle. A globe showing the Americas is a bug, not a variant. This goes on the pre-press checklist (§3.0.5).

**Rule 3.4.3b — Coordinates are fixed artwork.** `57.5878° N, 4.2383° W` — set in the mono at `LABEL` tracking, never abbreviated, never rounded, never re-typed from memory. Locked file in `04_MOTIFS/`.

**Rule 3.4.3c — Never fabricate a second location.** No second set of coordinates for a "city drop", no fictional studio address, no dateline. The brand has one place. (This is the same failure class as the already-killed fabricated photography datelines.)

**Rule 3.4.3d — Don't caption it.** The globe and the coordinates do the work. No "MADE IN THE HIGHLANDS", no thistle, no saltire, no Gaelic unless the founder actually speaks it. The restraint is the premium signal, and an unexplained coordinate is more interesting than an explained one.

**Rule 3.4.3e — 24 / 7 stays with the globe.** The "24" and "7" flanking numerals are part of the globe lockup, not free-floating brand furniture. They do not appear on their own on a garment.

### 3.4.4 Rank 2 — The dial, kept out of cliché

A clock face is the most obvious possible move for a brand called OUR TIME. It survives only by being *specific*.

| Rule | Spec |
|---|---|
| **Fixed time** | The hands are **locked at 07:24** on every appearance — a nod to 24/7, asymmetric, and unmistakably a mark rather than an illustration. **Never 10:10** (the watch-industry "smile"), never 12:00, never a live or random time |
| **Own the numerals** | Only the brand's drawn Roman numeral set. Never a stock clock, never a photographed clock, never a system clock glyph |
| **OT at 12** | Mandatory. The monogram replaces XII. This is what makes it ours rather than a clip-art dial |
| **Never animate the hands** | A ticking or sweeping hand turns the brand into a countdown widget — the thing already killed. Rotation is permitted only for the *outer ring*, slowly, in the motion system, never the hands |
| **Scale** | ≥ 20 mm print / 64 px screen. Below that the numerals become mush — use the monogram instead |

### 3.4.5 Ranks 4 & 5 — Restrictions

**Wristwatch (4).** High risk of reading as a watch brand, and fine engraved rendering is the most recognisable "AI-generated artwork" tell there is. Permitted: **one garment per season, maximum**, plus interior/paper applications at small scale. Must be line-engraved in a single ink, never photographic, never rendered with gradients or metallic effects. If it looks like a product photo of a watch, it is wrong.

**Hourglass (5) — RESTRICTED.** It is the default symbol for "time" and therefore says nothing. It survives on the navy tee as an *engraving*, as a craft object. Hard limits:
- **Never animated. Never scroll-linked. Sand never moves.** (Already killed; it is the single most-built cliché for time-themed sites and it is not coming back.)
- Never as an icon, favicon, loading state, bullet, or UI element.
- Never paired with copy about time running out.
- One garment. Not a brand element.

### 3.4.6 All-over pattern specification

| Parameter | Denim wash (baggy jeans) | Textile print (tape, linings, tissue) | Screen texture |
|---|---|---|---|
| Motif height | **18 mm** | **14 mm** | **14 px** @1x |
| Tile | **48 × 48 mm**, half-drop **50%** | 40 × 40 mm, half-drop 50% | 48 × 48 px, half-drop 50% |
| Rotation | **0°** — the italic already supplies the lean | 0° | 0° |
| Density (motif ink area ÷ tile area) | **18–24%** | 18–24% | 12–18% |
| Contrast vs base | **ΔL\* ≤ 12** — it must read as *wash*, not as print | ΔL\* ≤ 25 | ≤ **6% opacity** over `#0F0F0F` |
| Alignment | Tile origin set from the centre front; **pattern must not be cut by a pocket edge mid-motif** | Centred on the tape width | Anchored to the 8 px baseline grid |

**Forbidden in the pattern:** random rotation; mixed sizes in one tile; drop shadows; mixing the wordmark into the tile; any colour outside the two-tone (base + one tone); placing the pattern behind body text on screen (it fails contrast before it fails taste); using the pattern on a garment that also carries a chest monogram at over 60 mm.

The 50% half-drop is what stops the tessellation reading as a grid of stamps; keep it.

---

## 3.5 Photography direction

### 3.5.1 Flat-lay — the existing language, codified

This is the volume format: every one of the ~31 colourways gets one. Consistency across all 31 is worth more than any individual shot.

| Parameter | Specification |
|---|---|
| **Camera angle** | Dead-on nadir, **90° ± 0.5°**. Levelled with a bubble/digital level on the rig, not by eye. Any keystone across a 31-shot grid is instantly visible |
| **Lens** | **50–85 mm full-frame equivalent**, shot from height. Never a wide lens — barrel distortion bows the shoulder line |
| **Aperture / ISO** | f/8–f/11, base ISO, tethered |
| **Lighting** | **One large soft source directly overhead**, feathered — 120 cm octabox or a 1 × 2 m scrim. Key:fill ≈ **3 : 1**. No second source, no rim, no kicker |
| **Colour temp** | **5200 K**, fixed for the whole range. White-balanced to a grey card at the start of every session; the card shot is kept |
| **Shadow** | Soft, falling **toward 6 o'clock**, length **≤ 8%** of garment height, density **25–35%**. No hard edge. The shadow exists to lift the garment off the ground, not to be seen |
| **Ground** | **`#0F0F0F` textured** (dark colourways: `#DFDDDE`, see §3.2.5). Physical surface: matte painted plaster, book cloth or untreated card. **LRV ≈ 3%, sheen ≤ 5 GU @ 60°.** A shiny ground reflects the softbox and ruins the vignette |
| **Vignette** | **−0.4 stop at the corners**, smooth, oversized radius. Applied in-camera by light falloff where possible, matched in post |
| **Highlight handling** | **The white tee must render as `#FAF6F6`, not `#FFFFFF`.** Max luma on white garments **246/255**. Clipping the white kills the warmth that defines the brand's paper colour |
| **Garment fill** | Single garment: **72–80%** of the shorter frame dimension. Detail crop: 100% (bleeds all edges). Pair/stack: 68% combined |
| **Styling** | Folded flat, sleeves symmetrical, no mannequin, no pins visible, no creases from packaging — steamed. **Fabric texture must be visible** at 100%: this is a heavyweight, garment-dyed product and the texture is the proof |
| **Ground assignment** | Enforced per §3.2.5. A `#171717` garment on `#0F0F0F` is a 1.07 : 1 non-photograph |

**Crop ratios:**

| Ratio | Use | Garment fill |
|---|---|---|
| **4 : 5** | Primary product (PDP, feed) | 76% of height |
| **1 : 1** | Grid / thumbnails | 72% |
| **3 : 2** | Editorial, lookbook page | 64% — more air |
| **16 : 9** | Site hero | 50% — the garment is off-centre, the rest is ground (§3.6.5) |
| **9 : 16** | Story / vertical | 68%, garment placed in the upper two-thirds |

One master capture per garment, cropped to all five. Never reshoot for a ratio.

### 3.5.2 On-body — does not exist yet

The rule is **anti-fashion, pro-fit**. The point of on-body is to show how a heavyweight oversized tee actually sits, not to sell a lifestyle.

| Parameter | Specification |
|---|---|
| **Casting** | Real people, not agency models. Range of builds, because "oversized" means nothing without a body it's oversized *on*. No flexing, no gym physiques — that's the grind-culture cliché the brand needs to avoid |
| **Styling** | The garment plus plain items in the brand's own neutrals. No competing logos, no borrowed hype pieces, no accessories that out-loud the product |
| **Lens / distance** | **35 mm** full-length, **50 mm** three-quarter. Camera at the subject's **chest-to-eye height** — never low-angle hero framing |
| **Aperture** | f/2.8–f/4 outdoors, f/4–5.6 in studio. Background separation, not bokeh soup |
| **Shutter** | ≥ 1/250 s — wind is a feature (§3.5.3) and must be frozen, not smeared |
| **Pose** | Standing, walking, hands in pockets, turning away, mid-nothing. **No jumping, no crossed arms, no chin-down stare, no arms-out "fit pic".** If it looks posed, it is |
| **Crop** | Full-length, or three-quarter cropped at **mid-thigh**. The head may be cropped out — it keeps focus on the garment and keeps casting honest |
| **Detail** | One tight crop per look: neck seam, cuff, the tonal chest monogram, the pattern in the denim |
| **Grade** | Matches the flat-lays. Skin stays natural; **do not apply the desaturation to skin tones** — desaturate the environment, not the person |

### 3.5.3 Location — the Black Isle

The brand's biggest untapped asset. The instruction is: **photograph a working landscape in real weather, not a destination.**

**Approved locations**

| Place | What it gives |
|---|---|
| **Chanonry Point** | Shingle spit, lighthouse, the tide race where two firths meet. Stone, water, wind |
| **Rosemarkie / Fairy Glen** | Red sandstone cliffs, dark wet woodland, waterfall, beach |
| **Cromarty** | Working harbour, the Sutors, painted stone, salt-marked walls — and the **oil rigs laid up in the Cromarty Firth**, which is the single most striking and least expected image available to this brand |
| **Above Avoch / Munlochy** | Ploughed fields, stubble, gate posts, dry-stone dykes, big weather over flat farmland |
| **Kessock Bridge / the firth edge** | Industrial line against water |

**Weather and light**

- **Overcast (8/8 cloud) is the default condition**, not the fallback. It matches the palette exactly: flat grey sky ≈ the `#A7A5A4`/`#54647E` family.
- **Shoot in weather.** Haar (sea fret) rolling in, rain beading on cotton, wind visibly loading a heavyweight tee. Wet stone is darker, more saturated and better than dry stone.
- **Latitude 57.6° N is a production fact, not a flourish.** In June there is usable light until roughly **23:00**, low and raking — shoot 21:00–23:00. In December the sun is up around **09:00 and down around 15:30**, so the entire working day is golden/blue hour — shoot 10:00–15:00 and stop. Plan shoot days around this; it is free production value nobody else has.

**Grade**
Bring the location into the brand palette: **global saturation −20 to −30%**, blacks lifted slightly to `#0F0F0F` rather than crushed to `#000000`, highlights rolled off. The sea and sky may sit in the `#54647E` family — that is the brand's own accent occurring naturally, which is the whole point. **Red sandstone must be desaturated 25–35%**; left alone it becomes the most saturated thing the brand has ever shown and breaks Rule 3.2.1a.

**Banned — tourist-board register**

Blue-sky postcard days · sunset over the water · rainbows · drone establishing shots over the firth · **dolphins (Chanonry Point is famous for them; that is exactly why they cannot be used)** · highland cattle · tartan · castles · whisky · heather-and-glen framing · Gaelic signage as decoration · anything a Visit Scotland campaign would also shoot · the word "Scotland" anywhere in the artwork.

**Wanted — working-landscape register**

Feed bags and pallets · tractor ruts in mud · a gate with orange baler twine on it · harbour bollards and mooring rope · road salt on a wall · peeling paint on a shed · a parked rig · a bus shelter · frost on stubble · a hand, wet, in a cuff.

**The test:** if the shot would work as a postcard, reshoot it. If it would only make sense to someone who has stood there in the rain, it is right.

---

## 3.6 Layout & grid

### 3.6.1 Screen grid

| | Mobile (< 768) | Tablet (768–1279) | Desktop (≥ 1280) |
|---|---|---|---|
| Columns | **4** | **8** | **12** |
| Gutter | 16 px | 20 px | **24 px** |
| Outer margin | **24 px** | 40 px | **64 px** (min; 80 px preferred ≥ 1600) |
| Max content width | — | — | **1440 px**, centred; full-bleed media may exceed |

### 3.6.2 Print grid (lookbook / tags)

- **Lookbook format: 240 × 320 mm**, portrait.
- Margins, deliberately asymmetric: **top 22 mm · outer 20 mm · inner 26 mm · foot 32 mm.** The heavier foot is what stops a page looking like a Word document.
- **12 columns**, 4 mm gutter. **Baseline grid 4 mm**, all text snapped to it.
- Hang tag: **50 × 90 mm**, 400 gsm uncoated, margins 6 mm.

### 3.6.3 Spacing scale

One scale, **base 8**, used for every gap in every medium. No arbitrary values.

`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 192 · 256`

(Print equivalent, mm: `2 · 4 · 6 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96`)

| Gap | Value |
|---|---|
| Within a component (label → value) | 8 |
| Between related blocks | 24 |
| Between subsections | 64 |
| Between major sections | **128** (desktop) / 64 (mobile) |
| Section top/bottom padding | 96–192 |

Section separation is created by **space**, not by lines or boxes. The brand owns one rule weight: **1 px / 0.25 pt, `#A7A5A4` at 40%**, used sparingly.

### 3.6.4 The composition rules that make it editorial

1. **Asymmetry is the default.** Centring is reserved for exactly one case: a single mark alone on an otherwise empty surface. Everything else sits off-axis.
2. **The 7-column rule.** On the 12-column desktop grid, a primary text block occupies **columns 1–7 or 6–12** — never 1–12, never 3–10 (dead-centre). A full-width text block is what a template looks like.
3. **One focal element per view.** One image, or one statement, or one product. Not two competing.
4. **60% of spreads carry a bleed or a gutter-crossing element.** An image that runs off one edge; a `D1` statement that loses its last letter to the trim. Deliberate, and only ever on **one** edge per spread.
5. **Off-grid crops are allowed on exactly one element per page.** One element may break the margin. If two do, neither reads as intentional.
6. **The almost-empty page is mandatory, not a luxury.** At least **one page in five** (and one screen section in four) carries **≤ 10% ink coverage** — a line of mono, the monogram, and nothing else. This is the single cheapest, most reliable premium signal available, it costs nothing, and it is the first thing an inexperienced founder will want to fill in. **Do not fill it in.** Empty space is what says the brand isn't worried.
7. **Measure discipline.** Body text **60–72 characters** per line. Never full-bleed-width paragraphs.
8. **Type contrast per view:** one `D`-level display element maximum. If everything is loud, the monogram stops being loud.
9. **Alignment:** flush left, ragged right. **No justified text** (it opens rivers at this measure) and **no centred paragraphs**.
10. **"The Ledger" index mark.** Every section, page and spread carries a **`MICRO` mono index in the top-left of the margin** — section, item, date, e.g. `03 · VISUAL IDENTITY · 002 · MMXXVI`. It is what makes the layout read as a filing system rather than decoration, it costs one line, and it is the through-line between this system and the website direction.
11. **Corner radius: 0.** Everything is square — cards, images, buttons, tiles. The monogram's shear cuts are the brand's only non-orthogonal geometry and they must stay the only one.
12. **Motion inherits all of the above.** Whatever the clockwork/orbital motion system ends up doing, it moves *within* this grid, in these colours, at this saturation — concentric rings and meshing geometry on `#0F0F0F`, tonal, slow. Never neon, never gold-and-blue, never sci-fi, and the hourglass never drains.

### 3.6.5 Worked example — the site hero

> **16 : 9.** Ground `#0F0F0F`, full bleed. The flat-lay of the white tee (dark-ground colourway ✓) occupies **columns 7–12**, bleeding off the right edge, filling ~50% of frame height. Columns 1–5 carry, stacked from the vertical centre: `MICRO` mono index top-left in the margin (`OUR TIME · EST. MMXXVI · 57.5878° N`); then `D1` "EARN EVERY SECOND." in Display Bold Italic, `#FAF6F6`, tracked −0.02 em, leading 0.92, across three lines; then 48 px of space; then one `LABEL` mono line, `#A7A5A4`. Nothing else. Columns 6 and the entire lower third are empty. The OT monogram appears once, in the fixed header, at 32 px. Contrast: 17.9 : 1.

---

### Open items for the founder to close

| # | Item | Blocking |
|---|---|---|
| 1 | Measure and record hex + CIELAB for **forest green, brown, tan, taupe** from approved lab dips | Any use of those four colourways in artwork or on the site |
| 2 | Choose **one** navy (`#141B2C` or `#141925`) and migrate | Product photography that shows navy tops with navy bottoms |
| 3 | Confirm **merchandise/product licence terms** in writing with the chosen foundry, or adopt the OFL system in §3.3.3 | Any typeface printed on a garment for resale |
| 4 | Obtain a physical **white-on-navy discharge strike-off** | The navy hourglass and navy wordmark back prints |
| 5 | Confirm Pantone references against **physical chips**, and amend §3.2.3 | Any spot-colour print job |
| 6 | Recall/relabel or sell through the existing **OVERTIME** garments as a deliberate, named first-run anomaly — decide which, in writing, once | The brand's own story about itself |