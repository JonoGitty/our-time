# MOTION LANGUAGE — "THE MECHANISM"

*OUR TIME Brand Book · Section — Motion*

---

## 0. What this section is

OUR TIME has one animated object. Not a motion "style", not a library of effects — **one object, built once, used everywhere**. It is called **THE MECHANISM**. Everything that moves on the website, in a Reel, or on the end of a lookbook film is either the Mechanism, or a plain 180ms fade.

That constraint is the whole point. A new label with seven garment types, thirty-one colourways and two spellings of its own name on real product does not need a motion system with options in it. It needs one thing that is unmistakably its own.

---

## 1. The reference, researched

The client's brief is the Peter Capaldi-era *Doctor Who* title sequence. Before translating it, here is what it actually is — not from memory.

**Origin.** The sequence was not designed by the BBC. It began as a fan concept by **Billy Hanshaw**, a freelance motion-graphics designer from Leeds, made over about a month after Capaldi's casting was announced in 2013. Posted to YouTube, it passed 700,000 views. Showrunner Steven Moffat saw it and called it *"the only truly new idea I've seen since the very original in 1963"* — then had BBC Wales Graphics build the broadcast version from Hanshaw's storyboards, style-frames, typographic treatments and animatic. ([Campaign](https://www.campaignlive.co.uk/article/youtube-sensation-bbc-one-story-behind-doctor-whos-new-title-sequence/1309229), [AV Club](https://www.avclub.com/the-new-doctor-who-title-sequence-was-originally-design-1798271349), [Art of the Title](https://www.artofthetitle.com/title/doctor-who-series-8/))

**What it actually does, in order.** It opens in *"a flurry of gold, Gallifreyan-themed cogs in a smoky, straight vortex"* — a clockwork tunnel, gears rendered in 3D with neon glow against dusty smoke. The camera travels the tunnel; cogs mesh and turn. It then reaches the sequence's centrepiece: an **M.C. Escher-style recursive, never-ending clock face**, silver, which the TARDIS glides past before the clock **unwinds "gracefully, like a ribbon."** The recursive clockface spirals open into a field of planets, stars and nebulae; planets wind along an invisible path that echoes the unwinding clock. Capaldi's eyes appear; the logo forms and pushes to camera. Palette: *"blue, silver, black and gold."* ([Doctor Who TV — Examining Series 8's Title Sequence](https://www.doctorwhotv.co.uk/examining-series-8s-new-title-sequence-66050.htm), [Art of the Title](https://www.artofthetitle.com/title/doctor-who-series-8/), [Tardis Wiki](https://tardis.fandom.com/wiki/Title_sequence))

**The idea underneath it.** Hanshaw's own rationale: clockwork, because *"humans make up the entirety of the viewing audience, and so will immediately understand the analogy."* His concept was a journey that begins **inside the Doctor's pocket watch**, travels out through cogwheels, and opens into an *"escher-esque timey-wimey never-ending clock face."* The original also carried a fob watch and the Seal of Rassilon — **the BBC's only two mandatory changes were to remove both.** Built in Cinema 4D, After Effects, Photoshop and Illustrator. ([Doctor Who TV — Hanshaw interview](https://www.doctorwhotv.co.uk/interview-billy-hanshaw-on-series-8s-title-sequence-66152.htm), [Behance — Hanshaw's concept](https://www.behance.net/gallery/11198575/Doctor-Who-Title-Sequence-Concept), [IBTimes](https://www.ibtimes.com/doctor-who-season-8-meet-billy-hanshaw-whose-title-sequence-steven-moffat-loved-so-much-he-1668548))

**The part worth stealing that nobody talks about.** Hanshaw on the outcome: *"The clockwork also gave this era of the show brand assets to work with. A lot of publicity and merchandise that came out during Capaldi's run featured cogs as part of their design, giving cohesion to the brand."* ([Motionworks](https://motionworks.co.uk/doctor-who-retrospective/))

That is the actual lesson for OUR TIME. The titles worked as a brand system because the animated object and the print object were **the same object**. That is exactly the position OUR TIME is already in and does not yet know it: the label's own garments already carry concentric orbit rings, a Roman-numeral clock face with OT at twelve, a compass star, "24 / 7", and an all-over tessellated monogram. The Mechanism is not a *Doctor Who* homage bolted onto the brand. It is the back-print of the globe tee and the pocket print of the jeans, turning.

### 1.1 Take / Leave

| We take | We leave |
|---|---|
| **Concentricity.** Rings inside rings, sharing a centre. | **The palette.** No gold, no amber, no blue-and-gold, no silver. |
| **Meshed gearing** — that adjacent things counter-rotate at related rates. | **The glow.** No neon, no bloom, no lens flare, no chromatic aberration. |
| **Lock-into-place timing.** Things arrive and stop dead on a beat. | **The density.** Their frame holds dozens of objects. Ours holds five rings. |
| **Implied recession** — a tunnel read through nested scale. | **The 3D.** No WebGL, no rendered cogs with bevels and specular. |
| **The clock face as the hero object**, not as decoration. | **The swirl.** No camera flight, no vortex travel, no "journey". |
| **One mechanism used across site, film and print.** | **The IP.** No TARDIS, no Gallifreyan, no easter eggs. See §5.4. |

Their sequence is a *journey through* a mechanism. Ours is a *mechanism, observed*. The camera never moves. That single decision resolves most of the tension between a gold sci-fi title sequence and a washed, near-black, premium clothing label.

---

## 2. The core mechanism, specified

One object. Five concentric elements around a fixed centre. All geometry is expressed as a fraction of **R**, the assembly's outer radius, so it scales from a 64px loading state to a 1080px social sting without a second set of numbers.

### 2.1 The stack, inside out

| Ring | Content | Radius | Weight | Opacity | Motion |
|---|---|---|---|---|---|
| **R0 — The Core** | OT monogram | `0 → 0.30R` | Heavy (logo as-is) | `1.00` | **Never moves.** |
| **R1 — Numerals** | Roman numerals I–XII, centred on the ring | centred `0.44R`, cap height `0.085R` | I–XI thin (wordmark face); **XII heavy** | I–XI `0.42`, XII `0.92` | Stepped, **CW**, 12 teeth |
| **R2 — Escapement** | 60 ticks + hairline circle | circle `0.62R`; minor ticks `0.58→0.62R`, every 5th `0.545→0.62R` | Hairline, 1 device px | circle `0.22`, minor `0.28`, major `0.55` | Stepped, **CCW**, 60 teeth |
| **R3 — Orbits** | 2 ellipses + 2 nodes + fixed compass star | `rx 0.86R`; A `ry 0.30R` at `+23.5°`, B `ry 0.22R` at `−23.5°` | Hairline, 1 device px | ellipses `0.30`, nodes `0.85` | **Continuous**, linear, opposed |
| **R4 — Bezel** | 30 shear-cut teeth, outlined not filled | inner `0.92R`, outer `1.00R` | 2 device px stroke | `0.38` | Stepped, **CW**, 30 teeth |

**R0 never rotates.** The monogram is the fixed point and time moves around it. This protects the mark from being rendered as a spinning logo (the single fastest way to make a new label look cheap) and it happens to be the brand's literal argument: *our* time.

**The heavy XII is the hand.** R1 sets I–XI in the thin wordmark weight and **XII in the heavy monogram weight**. That reproduces the brand's heavy/thin typographic signature *inside a single ring*, carries forward the artwork's "OT at twelve", and gives the eye exactly one object to track — the heavy numeral sweeping a full circuit every 12 seconds. It is the only heavy thing in the assembly that moves. There is never a second one.

**The compass star does not rotate.** From the globe tee. A four-point hairline star at `0.08R`, pinned at the top of R3's bounding box, fixed to true north. At sizes ≥ 240px it may carry the coordinate string **57.5878° N · 4.2383° W** set at `0.055R` in the wordmark face beneath it. This is the only place the Black Isle enters the motion system, and it enters as a fixed reference point that everything else turns around — which is the correct relationship between a place and a label.

### 2.2 The gear train — the part that matters

Rings that spin at arbitrary speeds read as "spinning circles." Rings whose rates are the **inverse of their tooth counts** read as clockwork, because that is what gearing is. Angular velocity ω ∝ 1 / (tooth count).

| Ring | Teeth | Step angle | Direction | Period |
|---|---|---|---|---|
| R1 Numerals | 12 | **30.000°** | CW | 12 s |
| R4 Bezel | 30 | **12.000°** | CW | 30 s |
| R2 Escapement | 60 | **6.000°** | CCW | 60 s |

**ω(R1) : ω(R4) : ω(R2) = 5 : 2 : 1** — the exact inverse of 12 : 30 : 60. Integer ratios, a real train.

Direction alternates across the toothed members going outward — **CW, CCW, CW** for R1, R2, R4 — because meshed gears counter-rotate, and that alternation is the strongest single cue the eye has. (R3 sits physically between R2 and R4 but is not in the train; it is celestial, not mechanical, and is exempt.)

**Everything advances exactly one tooth per beat.** One beat = **1000 ms**, in sync with the viewer's own clock. The geared train realigns to its start position every **60 s**.

### 2.3 The orbits — "24 / 7"

The two orbit nodes are the only continuous motion in the system.

- **Orbit A** — period **24.000 s**, clockwise.
- **Orbit B** — period **7.000 s**, counter-clockwise.

That is the "24 / 7" from the globe tee, made literal. The two orbits return to phase together every **168 s** — one week, counted in hours. At sizes ≥ 240px the two nodes may be labelled `24` and `7` in the wordmark face at `0.05R`; below that they are bare dots.

**Orbit B's node is the only saturated colour in the entire motion system.** It is `#54647E` — washed denim, the most saturated colour the brand owns — rendered as a **3 device-pixel dot, no glow, no trail.** The brand's loudest possible colour, used at the smallest possible size, once. That is the whole accent policy. There is no second accent, ever.

### 2.4 Depth and vortex without 3D

The Capaldi titles fly a camera down a tunnel. We cannot do that and stay premium, and we should not want to. Recession is implied instead, in flat 2D, with five draw calls:

Draw the R2 + R4 geometry five times at **scales 1.00, 0.72, 0.52, 0.37, 0.27** — a constant ratio of **0.72** — with opacity on the same geometric fall: **0.26, 0.18, 0.12, 0.08, 0.05**, and line weight held at 1 device pixel throughout (do *not* scale stroke width; constant hairline at diminishing scale is what reads as "far away and sharp" rather than "small and blurry").

To make it a vortex rather than a static nest, multiply every ghost's scale by `0.72^(Δt / 2000ms)` and respawn a ghost at scale 1.00 every 2000 ms. The human eye reads constant-ratio scaling as constant-velocity recession, so five rings and one multiply produce a tunnel. No perspective matrix, no depth buffer, no WebGL.

**The vortex is OFF by default.** It exists in exactly two places: the site intro and the 404. Everywhere else the Mechanism is flat.

### 2.5 Colour, surface and the two traps

The Mechanism is **monochrome**: `#FAF6F6` bone on `#0F0F0F` textured ground, varied only by opacity. Depth is scale and alpha. It is never hue.

- Ground is always **`#0F0F0F`**, never `#000000`. `#000` is the photographic backdrop only.
- **Never render any ring in `#171717` on `#0F0F0F`.** That is **1.07:1** and completely invisible. A developer reaching for "a darker ring for depth" will do this. It is banned; use alpha on bone instead.
- On light grounds (off-white `#DFDDDE`, cream `#CFC2B4`) the Mechanism **inverts to `#171717`** (≈13.4:1 on `#DFDDDE`). It is never bone-on-cream, and never `#A7A5A4` on `#DFDDDE` (1.84:1).
- **Grain, not glow.** A static monochrome grain, generated once into an offscreen canvas and composited at **3% opacity**, matches the washed/garment-dyed surface of the product. It is **never animated** — animated grain reads as VHS analog-horror, costs a full repaint every frame, and is the opposite of premium.
- **No gradients anywhere.** Flat ground plus grain. This is an aesthetic choice that is also the fix for near-black banding in video export (§6).

---

## 3. Motion principles

Six named rules. These are the rules, not suggestions, and they are the thing to check work against.

### ONE BEAT
Everything mechanical advances on the same 1000 ms escapement. There is one clock source in the codebase and one `requestAnimationFrame` loop on the page. No component gets its own private timing. If two things on screen are ticking out of phase, something is wrong.

### MECHANISMS TICK, BODIES GLIDE
Geared elements (R1, R2, R4) are **quantised** — they hold, then snap. Celestial elements (R3's orbits) are **continuous and linear**. Nothing in the system eases smoothly between two rotational states. This is the single rule that separates clockwork from a loading spinner, and it is the first thing to fix if the animation "looks generic."

### THE CENTRE HOLDS
The OT monogram does not rotate, pulse, breathe, scale on loop, or bounce. Ever. Time moves around it.

### ONE HEAVY, ONE THIN
The logo system's heavy/thin contrast is reproduced in motion. At any moment exactly **one** moving element may be heavy — the XII. Everything else is hairline. Two loud things at once and the brand stops reading as premium and starts reading as a template.

### IT KEEPS TIME, IT DOESN'T SELL IT
The Mechanism displays elapsed real seconds. **It never counts down.** No deadline, no drop timer, no scarcity clock, no acceleration as the cursor nears a CTA. Scarcity that is always on is not scarcity, it is a Shopify app. The Mechanism's honesty — that it is simply keeping time, not selling it — is what makes it possible to put a clock on a clothing site in 2026 without embarrassment.

### THE RESTRAINT BUDGET
Hard numbers, enforceable in review:

| Constraint | Limit |
|---|---|
| Animated regions per viewport | **≤ 2** |
| Total animated area | **≤ 12% of viewport** |
| Mechanism diameter outside intro/404 | **≤ 240 device px** |
| Maximum translation of any element | **24 px** |
| Maximum opacity delta in a transition | **0.35** |
| Idle after no scroll/pointer | **20 s** → drop to 1 fps sampling |
| Off-screen or tab hidden | **stop entirely** |
| Motion during scroll | **paused** (continuous elements only) |
| Motion from add-to-cart onward | **zero** |

---

## 4. Timing and easing

### 4.1 Tokens

```css
:root {
  /* The beat */
  --ot-beat: 1000ms;

  /* Durations — this is the complete ladder. Nothing else exists. */
  --ot-d-exit:    120ms;
  --ot-d-ui:      180ms;
  --ot-d-reveal:  320ms;
  --ot-d-settle:  520ms;
  --ot-d-intro:   900ms;

  /* Easing */
  --ot-ease-lock:     cubic-bezier(0.2, 1.6, 0.35, 1);   /* the tick — overshoot + settle */
  --ot-ease-settle:   cubic-bezier(0.16, 1, 0.3, 1);     /* expo-out — arrives and stops dead */
  --ot-ease-standard: cubic-bezier(0.4, 0, 0.2, 1);      /* UI, invisible */
  --ot-ease-exit:     cubic-bezier(0.4, 0, 1, 1);
  --ot-ease-orbit:    linear;                            /* orbits are ALWAYS linear */
}
```

### 4.2 Where motion is quantised vs continuous

**This is the section that decides whether the whole thing works.**

| Element | Treatment |
|---|---|
| R1, R2, R4 | **Quantised.** Angle = `floor(t / 1000) × stepAngle`. |
| R3 orbits | **Continuous.** Angle = `(t / period) × 360`, linear, no easing, no variation. |
| Vortex ghost scale | **Continuous**, exponential. |
| Opacity reveals | Continuous, but only on the intro. Never on loop. |

A pure `floor()` gives you `steps()`, and `steps()` reads as *digital*, not *mechanical*. A real lever escapement overshoots slightly and settles. That difference is the entire character:

**Per beat (1000 ms):**
- `0 – 90 ms` — **advance**, one full tooth, using `--ot-ease-lock`, with **18% overshoot** of the step angle, single excursion, no oscillation.
- `90 – 1000 ms` — **dead hold.** Nothing rotates. 91% of every second, the mechanical rings are perfectly still.

In canvas, implement the advance directly rather than via CSS, so the still frame and the animation come from one code path:

```js
const BEAT = 1000, ADVANCE = 90, OVERSHOOT = 0.18;

// cubic-bezier(0.2, 1.6, 0.35, 1) sampled — returns >1 mid-flight, settles to 1
function lock(p) {
  const c1 = 3 * 0.2, c2 = 3 * (0.35 - 0.2) - c1, c3 = 1 - c1 - c2;
  // ... standard bezier solve for t given x=p, then evaluate y ...
}

function ringAngle(t, stepDeg) {
  const beat  = Math.floor(t / BEAT);
  const phase = Math.min((t % BEAT) / ADVANCE, 1);
  const eased = phase >= 1 ? 1 : lock(phase) * (1 + OVERSHOOT) - OVERSHOOT * phase;
  return (beat + eased) * stepDeg;
}
```

For any DOM element that needs the beat without canvas (a loading state, a divider rule), the CSS equivalent is:

```css
@keyframes ot-tick { to { transform: rotate(360deg); } }
.ot-tick-60 { animation: ot-tick 60s steps(60, end) infinite; }
.ot-tick-12 { animation: ot-tick 12s steps(12, end) infinite; }
.ot-orbit-7 { animation: ot-tick  7s linear infinite; }
```
`steps()` loses the overshoot. Accept that in DOM fallbacks; never accept it in the hero.

### 4.3 The intro beat sheet

Total **1800 ms**, hard cap. Once per session (`sessionStorage: ot_intro_v1`). Any input skips it; a skip jumps to the settled frame over 120 ms.

| Time | Event |
|---|---|
| `0` | Ground `#0F0F0F` + grain. Nothing else. |
| `0 – 240` | R2 hairline circle strokes on, 0→360°, linear (dash-offset sweep). |
| `200 – 520` | Numerals I–XII fade in, clockwise stagger **18 ms** apart, `--ot-ease-settle`. |
| `420 – 760` | Orbit ellipses sweep on, linear; nodes appear at phase 0. |
| `620 – 980` | Bezel teeth appear **snapped, not faded**, 30 teeth at **12 ms** stagger. |
| `900` | **BEAT ONE.** Every geared ring advances one tooth together. This is the moment it becomes a machine rather than a diagram. |
| `900 – 1420` | OT monogram: opacity 0→1, scale 1.04→1.00, `--ot-ease-settle`. |
| `1420 – 1800` | Wordmark **OUR TIME** reveals beneath: letterspacing `0.38em → 0.32em`, opacity 0→0.85, `--ot-ease-settle`. |
| `1800` | Done. The Mechanism continues on the beat only. |

**The wordmark is never live text with a space character in it.** It is a pre-kerned vector asset with the word gap baked in at a fixed `0.62em`. This is the animation-side fix for the brand's recurring "OURTIME" collapse: a `letter-spacing` animation on live text will close a real space, and a video encoder will erase what is left of it. Minimum render width for the wordmark: **132 px on web, 180 px in video.** Below that it does not go on screen at all.

---

## 5. Where it appears — and where it must not

### 5.1 Appears

| Placement | Spec |
|---|---|
| **Site intro** | Full Mechanism, vortex **on**, 1800 ms, once per session, skippable. |
| **Section transition (THE LEDGER)** | **Not the Mechanism.** R2 unrolled into a straight line — a horizontal tick rule at the section boundary whose ticks advance on the same 1 Hz beat, travelling 6px per beat. The ring, unrolled, *is* the ledger rule. Same object, flattened. |
| **Loading state** | 64px. **R2 + R4 only** — no numerals, no orbits, no vortex, no monogram. Appears only after **400 ms** of genuine wait; never flashed. If the wait passes 8 s it does **not** escalate: no acceleration, no progress bar, no reassuring lie. |
| **404** | 320px, vortex **on**, compass star with the Black Isle coordinates. Copy: **TIME WON'T WAIT.** One link home. This is the only page allowed to be indulgent, because it is already a dead end. |
| **Product hover** | 180 ms crossfade to the back-print shot, `--ot-ease-standard`. **No Mechanism.** The garment is the hero; a turning cog beside a flat-lay is competing with the product. |
| **Video / social** | §6. |

### 5.2 The anti-list

Never:

- A scroll-scrubbed hourglass draining sand. Killed, and it stays killed — it is the single most-built cliché for every time-themed site since 2014.
- Any countdown, drop timer, or "scarcity" clock.
- Parallax on product photography.
- A marquee or ticker scrolling the taglines.
- Cursor-followers, magnetic buttons, custom cursors.
- Page-transition wipes, curtains, or masked reveals.
- Autoplaying video with sound.
- WebGL, 3D, or rendered metal cogs with bevels and speculars.
- Gold, amber, blue-and-gold, neon, glow, bloom, lens flare, chromatic aberration, motion blur.
- A rotating OT monogram.
- Animated grain.
- More than one Mechanism visible at once.

### 5.3 Homepage motion inventory

Above the fold, after the intro: **one** Mechanism at ≤240px and **nothing else moving**. Below the fold: the ledger tick rule at section boundaries, and image crossfades on hover. That is the entire homepage motion inventory, and it is deliberately shorter than the list of things we are not doing.

### 5.4 No *Doctor Who* reference, ever, in public

The Capaldi titles are the **private** creative brief for this section. They are not a public reference, a caption, an easter egg, a TARDIS silhouette, a Gallifreyan glyph, or a hidden frame. Two reasons, both serious: it is licensed BBC intellectual property and a clothing label has no business borrowing it visibly; and an in-joke about a television programme instantly converts a premium washed label into a fan-merch brand. The reference earned us a mechanism. It does not appear in the output.

---

## 6. Accessibility and performance

### 6.1 Reduced motion — and the canonical still frame

`@media (prefers-reduced-motion: reduce)` → **the Mechanism renders one still frame and never animates.** The intro does not play. The 404 vortex is off. The loading state becomes a static hairline ring plus the word `LOADING`.

The still frame is not a random pause. It is a **designed composition**, defined once:

> **THE SETTLED FRAME.** Beat index 0. XII at top. R2 tick 0 at top. R4 tooth 0 at top. Both orbit major axes horizontal, node A at 0°, node B at 180°. Vortex ghosts present at 1.00 / 0.72 / 0.52 / 0.37 / 0.27. OT at full opacity. Compass star north.

It is rendered from the same canvas code with `t = 0`, so it can never drift from the animation. And it does double duty: it is the reduced-motion frame, the Open Graph image, the email header, the favicon source, the print lockup, and the last frame of every video (§6.4). One composition, six jobs.

### 6.2 Contrast

Bone `#FAF6F6` on ground `#0F0F0F` is ≈ **18:1** at full opacity. The opacity ladder lands at:

| Element | Alpha | Effective | Ratio |
|---|---|---|---|
| Numerals I–XI | 0.42 | ≈ `#717171` | **≈ 3.9:1** |
| R2 major ticks | 0.55 | ≈ `#909090` | **≈ 5.9:1** |
| R2 minor ticks | 0.28 | ≈ `#515151` | **≈ 2.5:1** |

Rule: **any element carrying meaning must clear 3:1.** Purely decorative hairlines (minor ticks, vortex ghosts) may sit below it. Under `prefers-contrast: more`, raise the ladder floor from `0.28` to `0.55`.

The Mechanism is decorative throughout and is marked `aria-hidden="true"`. It never carries information a screen reader needs, and it never replaces a text label. The 404's message is real text; the Mechanism beside it is not.

### 6.3 Why Canvas 2D at devicePixelRatio, not SVG and not a video file

**Not SVG.** The full assembly is 60 ticks + 12 numerals + 30 teeth + 2 ellipses + 5 vortex ghosts — **110+ DOM nodes, each with its own transform, restyled every frame.** On a mid-range Android the style recalculation alone eats the frame budget before anything paints. Worse for this specific brand: SVG hairlines do not snap reliably to the device-pixel grid, and a crisp 1-device-pixel hairline *is* the look. A blurry 1.3px stroke is a different, cheaper brand.

**Not a video file.** Transparency is not portable (WebM alpha is not Safari-safe; HEVC-with-alpha is not Chrome-safe), so the ground colour would have to be baked — and then it will never exactly match `#0F0F0F` under the grain layer. A 2-second loop is 1–3 MB against a 6 KB script. It cannot be paused on the beat, cannot be quantised, cannot respond to `prefers-reduced-motion` beyond swapping a poster, and — decisively — **near-black video bands.** A `#0F0F0F` field is exactly where 8-bit 4:2:0 compression falls apart.

**Canvas 2D.** One DOM node. One rAF. We own the device-pixel grid, so hairlines are exactly one device pixel. We own quantisation, so the beat is ours. The still frame comes out of the same function as frame 900. And because the mechanical rings are quantised, **the canvas does not need 60 fps.**

```js
const dpr = Math.min(window.devicePixelRatio || 1, 2);  // cap at 2
canvas.width  = cssW * dpr;
canvas.height = cssH * dpr;
const ctx = canvas.getContext('2d', { alpha: false, desynchronized: true });
ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
ctx.lineWidth = 1 / dpr;          // exactly one device pixel
ctx.translate(0.5 / dpr, 0.5 / dpr);  // odd-width crispness
```

DPR is capped at **2**: at hairline weights a third device pixel is invisible and costs 2.25× the fill rate.

### 6.4 Frame budget

- Numerals and bezel teeth are rasterised **once** into an `OffscreenCanvas` sprite and blitted with `drawImage`. Re-rasterised only on resize or DPR change.
- Grain is generated **once** into an offscreen canvas and composited.
- The rAF loop **early-returns** unless (a) an orbit or vortex is enabled and visible, or (b) the beat index changed since the last paint.
- Target: **≤ 4 ms per painted frame** at 1440×900 DPR 2 with a 320px assembly (~110 path operations). Instrument with `performance.now()` deltas and log the 95th percentile in dev.
- In idle mode — beat only, orbits paused — the page paints **1 frame per second**. That is roughly **0.4% CPU**, against **6–9%** for the same complexity at 60 fps. On a phone that is the difference between a battery drain a user can feel and none at all.

### 6.5 Battery, thermal and data

```js
document.addEventListener('visibilitychange', () => hidden ? stop() : start());
new IntersectionObserver(([e]) => e.isIntersecting ? start() : stop()).observe(canvas);

// Pause continuous motion during scroll; keep the beat.
// Honour saveData and low battery by rendering the settled frame only.
if (navigator.connection?.saveData) renderStill();
navigator.getBattery?.().then(b => {
  if (b.level < 0.2 && !b.charging) renderStill();
});
```

Mechanical rings never exceed 1 paint/second. Continuous motion is the only thing that ever asks for 60 fps, and it is paused during scroll, off-screen, on hidden tabs, on Save-Data, and below 20% battery.

---

## 7. The social and video extension

The same code, a fixed-step clock, and a different canvas size. Nothing is re-animated in After Effects, ever — if the site and the Reel drift apart, the brand is back where it started with two spellings of its own name.

### 7.1 The 3-second Instagram sting

**1080 × 1350** (feed) and **1080 × 1920** (story). **30 fps → 90 frames → exactly 3 beats.** 30 fps is chosen so the 1000 ms beat lands on frame 30 and 60 with no rounding.

| Frame | Time | Event |
|---|---|---|
| 0 – 26 | 0 – 900 ms | Assembly draws on. The site intro at 0.5× duration. |
| **27** | **900 ms** | **BEAT ONE.** All geared rings advance one tooth. Single mechanical tick on the audio. |
| 27 – 56 | 0.9 – 1.9 s | OT locks into the centre. |
| **57** | **1900 ms** | **BEAT TWO.** Wordmark **OUR TIME** appears — **snapped on the tick, not faded.** |
| 57 – 86 | 1.9 – 2.9 s | Hold. Orbit B's `#54647E` node completes a full pass. |
| **87** | **2900 ms** | **BEAT THREE.** The wordmark is replaced, on the beat, by one line: `EARN EVERY SECOND.` / `TIME WON'T WAIT.` / `DISCIPLINE. FOCUS. CONSISTENCY.` — rotated per post. |
| 89 | 2966 ms | **Last frame = THE SETTLED FRAME** (§6.1). |

**That last row is the important one.** A paused Reel, a muted autoplay that never loaded, the OG image, the email header, the reduced-motion site and the 404 all show the **identical composition**. Whatever surface a person meets the brand on, and whatever fails to load, they see one image. That is a brand system rather than a set of assets, and it is the thing this label does not currently have.

**Audio.** One recorded mechanical escapement tick per beat, at −18 LUFS. **No music bed on a 3-second sting.** The silence between the ticks is the entire point. Instagram autoplays muted anyway, so the sting must read with sound off — and it does, because the information is carried by the snap, not the sound.

### 7.2 Export

Render from the same canvas with a fixed clock (`t = frame / 30`) to PNG, then:

```bash
ffmpeg -framerate 30 -i frame_%04d.png \
  -c:v libx264 -preset slow -crf 15 -profile:v high \
  -pix_fmt yuv420p -x264-params "aq-mode=3" \
  -movflags +faststart ot-sting.mp4
```

CRF 15, not 23: a near-black field needs the headroom. The real defence against banding is upstream and already in the design — **flat `#0F0F0F` with static grain and no gradients anywhere.** There is nothing for the encoder to band. Instagram will re-encode regardless, so ship at maximum quality and let the grain absorb it.

### 7.3 Video end-card

**4.0 s.** Mechanism at **22% of frame height**, optically centred. Beat at `t = 1.0 s` locks the OT. Wordmark at `t = 2.0 s`, snapped. Hold to `4.0 s`. Cut on the beat, never mid-hold — the handles are the dead 910 ms of each second, which is generous and is another reason the timing works.

The URL sits **below** the wordmark, in the wordmark face, at the same letterspacing rule — never inside the rings. Nothing goes inside the rings except the monogram.

---

## 8. Build checklist

A developer should be able to ship this from the section above. Minimum viable order:

1. Canvas at capped DPR, `#0F0F0F` ground, static grain sprite at 3%.
2. R2 escapement — 60 ticks, 6°/beat CCW, with the 90 ms lock easing. **Verify the tick reads as mechanical before building anything else.** If it does not, nothing added later will fix it.
3. R1 numerals — 30°/beat CW, XII in the heavy weight.
4. R4 bezel — 12°/beat CW, 2px outlined shear teeth. Measure the shear angle from the actual monogram file and record it once as `--ot-shear` in the brand tokens.
5. R0 monogram, static.
6. R3 orbits — 24 s and 7 s, linear, opposed, one `#54647E` node.
7. Vortex ghosts, behind a flag, off by default.
8. The settled frame, exported as SVG and PNG.
9. Reduced-motion, visibility, intersection, scroll-pause, Save-Data and battery gates.
10. The fixed-step export path for video.

---

**Sources**

- [Interview: Billy Hanshaw on Series 8's Title Sequence — Doctor Who TV](https://www.doctorwhotv.co.uk/interview-billy-hanshaw-on-series-8s-title-sequence-66152.htm)
- [Examining Series 8's New Title Sequence — Doctor Who TV](https://www.doctorwhotv.co.uk/examining-series-8s-new-title-sequence-66050.htm)
- [The Series 8 Title Sequence — Doctor Who TV](https://www.doctorwhotv.co.uk/the-series-8-title-sequence-65250.htm)
- [Doctor Who: Series 8 (2014) — Art of the Title](https://www.artofthetitle.com/title/doctor-who-series-8/)
- [Doctor Who Title Sequence Concept — Billy Hanshaw, Behance](https://www.behance.net/gallery/11198575/Doctor-Who-Title-Sequence-Concept)
- [From YouTube sensation to BBC One — Campaign](https://www.campaignlive.co.uk/article/youtube-sensation-bbc-one-story-behind-doctor-whos-new-title-sequence/1309229)
- [The new Doctor Who title sequence was originally designed by a fan — The A.V. Club](https://www.avclub.com/the-new-doctor-who-title-sequence-was-originally-design-1798271349)
- [Doctor Who retrospective — Motionworks](https://motionworks.co.uk/doctor-who-retrospective/)
- [Meet Billy Hanshaw — IBTimes](https://www.ibtimes.com/doctor-who-season-8-meet-billy-hanshaw-whose-title-sequence-steven-moffat-loved-so-much-he-1668548)
- [Title sequence — Tardis Wiki](https://tardis.fandom.com/wiki/Title_sequence)