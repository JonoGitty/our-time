# LIQUID GLASS ON THE WEB — IMPLEMENTATION BRIEF (Sept 2026)

## 0. THE HEADLINE (read this before designing anything)

**Real backdrop refraction — `backdrop-filter: url(#svg-filter)` — is Chromium-only as of September 2026. It does not work in Safari (any platform) or Firefox. Neither has shipped it. Both have open, unresolved bugs.**

This is not a "mostly works, minor gaps" situation. On iPhone — which is where a streetwear brand's traffic actually lives — the refraction tier renders **nothing at all**, and `@supports` will lie to you about it.

Therefore the architecture must be: **Tier 2 (blur + gradients) is the product. Tier 1 (refraction) is a progressive garnish for Chromium desktop only.** Any plan that treats refraction as the baseline will ship a broken site to the majority of the audience.

There is a second, separate technique — **`filter: url(#...)` applied to a cloned copy of the background** — which *does* work cross-browser and is how the honest libraries get refraction into Safari. It has serious costs. Covered in §2.6.

---

## 1. WHAT APPLE'S LIQUID GLASS ACTUALLY IS

Announced 9 June 2025 at WWDC; shipped across iOS 26, iPadOS 26, macOS Tahoe 26, tvOS 26, watchOS 26, visionOS 26. Apple's own framing: a material that "combines the optical properties of glass with a sense of fluidity," rendered **in real time** using lighting and shaders on Apple silicon, which "reflects and refracts its surroundings" and "reacts to movement with specular highlights."

Decomposed into buildable ingredients:

| # | Ingredient | What it does | Browser feasibility |
|---|---|---|---|
| 1 | **Backdrop blur + saturation boost** | Frosted read of what's behind | ✅ Universal |
| 2 | **Edge/rim lensing (refraction)** | Content behind the panel *bends* near the border — a lens, not a blur. The single biggest tell. | ⚠️ Chromium only via backdrop-filter |
| 3 | **Specular highlight** | A moving bright streak on the top-left/bottom-right rim, as if a light source is raking across it | ✅ Universal (gradients + masks) |
| 4 | **Chromatic dispersion** | Faint R/G/B fringing at the refracted edge | ⚠️ Chromium only (backdrop); ✅ on cloned content |
| 5 | **Adaptive light/dark tinting** | Material senses backdrop luminance and flips its own tint + text colour to stay legible | ✅ Universal (needs JS/scroll observers) |
| 6 | **"Gel" squash-and-stretch** | Springy deformation on press/drag; elements morph and merge | ✅ Universal (transforms + spring easing) |
| 7 | **Regular vs Clear variants** | *Regular* = adaptive, legible, for chrome/nav. *Clear* = more transparent, for media-rich contexts only | ✅ Design decision |

**Important context:** Apple itself has walked this back on accessibility grounds. Reception was mixed, with legibility criticism (notably in direct sunlight). Apple shipped increased opacity in navigation bars and refined overlays through the iOS 26.x cycle, and at WWDC 2026 announced iOS 27 would **reduce default transparency further**. The design language's own author is dialling it down. Build restrained.

**Note:** Apple has a private CSS property `-apple-visual-effect` accepting values like `-apple-system-glass-material`. It works only in WKWebView with a private `WKPreferences` setting (`useSystemAppearance`) that disqualifies an app from App Store approval. **It does not work on the web.** Do not plan around it.

---

## 2. HOW TO BUILD EACH INGREDIENT IN A BROWSER

### 2.1 The tinted glass panel (layering trick) — Tier 2 core

The mistake is putting a translucent background colour and a backdrop-filter on the same element and calling it done. That produces flat glassmorphism (2020), not glass. You need **three stacked layers**:

```css
.ot-glass {
  position: relative;
  isolation: isolate;               /* contain blend modes */
  border-radius: 999px;             /* pill nav */
  /* Layer 1: the refraction/blur of the backdrop */
  -webkit-backdrop-filter: blur(18px) saturate(180%) brightness(1.06);
          backdrop-filter: blur(18px) saturate(180%) brightness(1.06);
  /* Layer 2: the glass body tint (NOT the blur) */
  background:
    linear-gradient(180deg, rgb(255 255 255 / .10), rgb(255 255 255 / .03) 42%, rgb(255 255 255 / .07));
  /* Layer 3: interior depth — top rim light, bottom bounce, outer drop */
  box-shadow:
    inset 0  1px 0 0 rgb(255 255 255 / .38),   /* top edge catch */
    inset 0 -1px 0 0 rgb(255 255 255 / .10),   /* bottom bounce   */
    inset 0  0  20px 0 rgb(255 255 255 / .05), /* interior sheen  */
    0 8px 32px -8px rgb(0 0 0 / .45),          /* cast shadow     */
    0 1px  2px  0  rgb(0 0 0 / .20);
}
```

`saturate(180%)` is doing more work than the blur. Glass concentrates colour; without the saturation bump you get fog, not glass. `brightness()` above 1 in dark contexts and below 1 in light contexts is the cheap version of adaptivity.

### 2.2 Real refraction — SVG displacement (Tier 1, Chromium only)

`backdrop-filter` accepts ten filter functions; **none of them displace a pixel**. Blur cannot produce refraction — that requires moving pixels, which means `feDisplacementMap`.

`feDisplacementMap` reads a second image where each pixel's channel values encode a 2D offset. Per spec, for channel value `C` normalised to `[0,1]`:

```
displacement = scale × (C − 0.5)
```

So `128` = zero displacement, `255` = `+scale/2` px, `0` = `−scale/2` px. Encode R = X-offset, G = Y-offset.

**Generating the map.** Two approaches:

- **Cheap/procedural:** `feTurbulence` noise driving the displacement. This gives a *wobbly, watery* look — good for an organic blob, **wrong** for a crisp nav bar. It does not know where your rounded-rect edge is.
- **Correct:** a **rounded-rectangle signed-distance field → bevel profile → normal map**, rendered to a canvas and injected as a data-URI PNG. This concentrates displacement in a band at the border and leaves the centre neutral — which is exactly what real glass does and why it reads as a lens.

The rigorous version (kube.io) ray-traces Snell's law (n₁=1 air, n₂=1.5 glass) across a convex-squircle surface profile, then encodes:

```js
const r = 128 + x * 127;   // X displacement → red
const g = 128 + y * 127;   // Y displacement → green
const b = 128;             // unused
const a = 255;
```

**Generator (SDF → normal map → data URI).** Drop-in, no dependencies:

```js
/**
 * Build a displacement map for a rounded rect.
 * Neutral (128,128) in the middle; displacement ramps up inside `bevel` px of the edge.
 */
function makeGlassMap({ w, h, radius = 999, bevel = 22, strength = 1, dpr = 1 }) {
  const W = Math.ceil(w * dpr), H = Math.ceil(h * dpr);
  const R = Math.min(radius * dpr, Math.min(W, H) / 2);
  const B = bevel * dpr;
  const cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  const img = ctx.createImageData(W, H);
  const d = img.data;

  // Signed distance to a rounded box, centred coords. Negative = inside.
  const sdf = (px, py) => {
    const qx = Math.abs(px) - (W / 2 - R);
    const qy = Math.abs(py) - (H / 2 - R);
    const mx = Math.max(qx, 0), my = Math.max(qy, 0);
    return Math.hypot(mx, my) + Math.min(Math.max(qx, qy), 0) - R;
  };

  // Smootherstep — C2 continuous, avoids a visible banding ring at the bevel edge.
  const smoother = t => { t = Math.min(Math.max(t, 0), 1); return t*t*t*(t*(t*6-15)+10); };

  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const px = x - W / 2 + 0.5, py = y - H / 2 + 0.5;
      const dist = sdf(px, py);                 // ~0 at the border
      const i = (y * W + x) * 4;

      // Gradient of the SDF = outward surface normal (central differences).
      const gx = sdf(px + 1, py) - sdf(px - 1, py);
      const gy = sdf(px, py + 1) - sdf(px, py - 1);
      const len = Math.hypot(gx, gy) || 1;

      // Bevel profile: 0 in the flat centre, 1 at the rim.
      // t = how far into the bevel band we are (dist runs -B..0 across it).
      const t = smoother(1 - Math.min(Math.abs(dist) / B, 1));
      // Convex squircle surface → steep near the rim. Matches a real lens edge.
      const bend = Math.pow(t, 1.6) * strength;

      const nx = (gx / len) * bend;
      const ny = (gy / len) * bend;

      const inside = dist < 0;
      d[i]     = inside ? 128 + nx * 127 : 128;
      d[i + 1] = inside ? 128 + ny * 127 : 128;
      d[i + 2] = 128;
      d[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  return cv.toDataURL('image/png');
}
```

**The filter markup.** Inline in the document, `width="0" height="0"`, absolutely positioned out of flow:

```html
<svg width="0" height="0" aria-hidden="true"
     style="position:absolute;pointer-events:none">
  <defs>
    <!-- userSpaceOnUse is MANDATORY. objectBoundingBox is unreliable on iOS WebKit
         and the backdrop-filter filter region does NOT auto-size to the element. -->
    <filter id="ot-refract"
            filterUnits="userSpaceOnUse"
            x="0" y="0" width="420" height="56"
            color-interpolation-filters="sRGB">

      <!-- Set BOTH href and xlink:href: older WebKit only reads the xlink form. -->
      <feImage result="MAP"
               href="data:image/png;base64,…"
               xlink:href="data:image/png;base64,…"
               x="0" y="0" width="420" height="56"
               preserveAspectRatio="none" />

      <!-- In a backdrop-filter, SourceGraphic == the backdrop behind the element. -->
      <feDisplacementMap in="SourceGraphic" in2="MAP"
                         scale="48"
                         xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
</svg>
```

```css
@supports (backdrop-filter: url(#ot-refract)) {
  html[data-glass="refract"] .ot-nav {
    backdrop-filter: url(#ot-refract) blur(6px) saturate(180%);
  }
}
```

**Three correctness traps here:**

1. **`color-interpolation-filters="sRGB"` is not optional.** The SVG default is `linearRGB`. Leave it off and your displacement and blends are computed in the wrong colour space — results look washed and dimmer than intended, differently per browser.
2. **The filter region does not track the element.** You must recompute `x/y/width/height` and regenerate the map on resize. This is the main source of "it works on my laptop, it's broken on a phone."
3. **`scale` is in user-space px and clamped:** displacement is limited to the −128…+127 range the 8-bit map can express. Big lensing needs a bigger bevel, not just a bigger scale.

### 2.3 Chromatic dispersion (3× displacement, per-channel)

Run the displacement three times at slightly different scales, isolate one channel from each pass with `feColorMatrix`, recombine with `feBlend mode="screen"`. Scales differ by roughly 3–8% — real glass disperses blue most.

```xml
<filter id="ot-refract-ca" filterUnits="userSpaceOnUse"
        x="0" y="0" width="420" height="56"
        color-interpolation-filters="sRGB">

  <feImage result="MAP" href="data:image/png;base64,…"
           xlink:href="data:image/png;base64,…"
           x="0" y="0" width="420" height="56" preserveAspectRatio="none"/>

  <feDisplacementMap in="SourceGraphic" in2="MAP" scale="46"
                     xChannelSelector="R" yChannelSelector="G" result="dR"/>
  <feDisplacementMap in="SourceGraphic" in2="MAP" scale="48"
                     xChannelSelector="R" yChannelSelector="G" result="dG"/>
  <feDisplacementMap in="SourceGraphic" in2="MAP" scale="50"
                     xChannelSelector="R" yChannelSelector="G" result="dB"/>

  <!-- Keep only R / only G / only B, alpha preserved (last row = 0 0 0 1 0). -->
  <feColorMatrix in="dR" type="matrix" result="oR"
    values="1 0 0 0 0
            0 0 0 0 0
            0 0 0 0 0
            0 0 0 1 0"/>
  <feColorMatrix in="dG" type="matrix" result="oG"
    values="0 0 0 0 0
            0 1 0 0 0
            0 0 0 0 0
            0 0 0 1 0"/>
  <feColorMatrix in="dB" type="matrix" result="oB"
    values="0 0 0 0 0
            0 0 0 0 0
            0 0 1 0 0
            0 0 0 1 0"/>

  <feBlend in="oR" in2="oG" mode="screen" result="oRG"/>
  <feBlend in="oRG" in2="oB" mode="screen" result="rgb"/>

  <!-- Slight softening of the refracted band only -->
  <feGaussianBlur in="rgb" stdDeviation="0.4"/>
</filter>
```

Screen-blending works here precisely *because* each intermediate has exactly one non-zero channel; screen(a,b) = a+b−ab reduces to addition when the channels don't overlap.

**Cost warning:** this triples the displacement work. For OVERTIME's muted, washed aesthetic, aberration is close to off-brand anyway — it reads as RGB-split glitch, which is the opposite of vintage-athletic. **Recommend: dispersion at 1–2px maximum, or omit.**

### 2.4 Rim light / specular highlight (works everywhere)

Two parts. The **static rim** is inset box-shadows (already in §2.1). The **raking specular streak** is a masked conic gradient border:

```css
.ot-glass::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.25px;                    /* = rim thickness */
  background: conic-gradient(
    from var(--ot-light, 210deg),
    transparent            0deg,
    rgb(255 255 255 / .95) 48deg,     /* primary specular */
    transparent           118deg,
    transparent           222deg,
    rgb(255 255 255 / .55) 288deg,    /* secondary bounce */
    transparent           360deg);
  /* Border-only mask: fill the box, punch out the content box, keep the ring. */
  -webkit-mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
          mask-composite: exclude;
  pointer-events: none;
}
```

Animate `--ot-light` (register it so it interpolates) to make the highlight rake as the user scrolls or moves the pointer — this is the single highest-value-per-byte trick in the whole document, and it works in every browser:

```css
@property --ot-light {
  syntax: '<angle>'; inherits: false; initial-value: 210deg;
}
```

### 2.5 The "gel" squash-and-stretch

```css
.ot-glass-btn {
  transition:
    transform 520ms linear(0, .42 12%, .86 24%, 1.06 36%, 1.02 52%, .995 72%, 1),
    box-shadow 220ms ease;
}
.ot-glass-btn:active { transform: scale(.955) scaleY(.93); }

@media (prefers-reduced-motion: reduce) {
  .ot-glass-btn { transition: none; }
  .ot-glass-btn:active { transform: none; }
}
```

`linear()` easing gives a true spring curve without JS. **UNVERIFIED:** exact minimum versions for `linear()` — verify before relying on it; the `transition` declaration degrades to no transition if unparsed, which is a safe failure.

### 2.6 The cross-browser escape hatch: filter on a *cloned* backdrop

Since Safari and Firefox won't refract the real backdrop, the working libraries refract a **duplicate of the content** instead. `filter: url(#…)` with `feDisplacementMap` on ordinary DOM content **is** supported in all three engines (full SVG 1.1 filter support, including `feDisplacementMap`).

The pattern: render the page background a second time inside a clipped, positioned wrapper sitting behind the nav, apply `filter: url(#ot-refract)` to *that*, and keep the nav's own text unfiltered above it.

Honest assessment of this route:

- ✅ Genuinely works in Safari + Firefox.
- ❌ You must duplicate and keep in sync whatever is behind the bar. For a fixed nav over a scrolling page, that means the whole hero. Doubles paint cost.
- ❌ Safari will not run SVG filters over **live video** (WebKit limitation) — fatal if the plan is AI-generated *video* scroll backdrops, which it is.
- ❌ Safari **caps filter source sizes**; large refracted regions degrade or drop out.
- ❌ Accessibility/interaction hazard: the clone must be `aria-hidden` and `pointer-events: none`, and must not duplicate focusable nodes.

**Verdict for OVERTIME: do not do this for the nav bar.** The video-in-Safari limitation alone kills it given the brief. It is viable for a small, static, decorative element — e.g. a glass lens over the hourglass motif on a still image.

---

## 3. THE BROWSER-SUPPORT TRUTH TABLE (September 2026)

### 3.1 Baseline `backdrop-filter` with standard functions

| Browser | Support | Notes |
|---|---|---|
| Chrome | **76+** | |
| Edge | **79+** (`-webkit-` 17–79) | |
| Firefox | **103+** | Before FF 123, unsupported on systems with unknown GPU vendor ([bug 1868737](https://bugzil.la/1868737)) |
| Safari macOS | **18+** unprefixed; **9+** with `-webkit-` | **Ship both properties.** |
| Safari iOS | mirrors macOS | |
| Samsung Internet | 12+ | |

Baseline "newly available" since Sept 2024. `filter`, `saturate`, `brightness`, `contrast`, `blur` all fine.

### 3.2 `backdrop-filter: url(#svg-filter)` — THE LANDMINE

| Browser | Works? | Evidence |
|---|---|---|
| **Chrome / Edge / Chromium** | ✅ **Yes** | The only engine where refraction-in-backdrop works. Every liquid-glass write-up converges on this. |
| **Safari — macOS, iPadOS, iOS** | ❌ **No** | [WebKit bug 245510](https://bugs.webkit.org/show_bug.cgi?id=245510) status **NEW** (not fixed). [PR #68614](https://github.com/WebKit/WebKit/pull/68614) — software rendering for SVG reference filters in backdrop-filter — is **open, not merged, labelled `merging-blocked`**, reviewer requested changes. Sibling PRs #68613, #69566 address an associated GPU-process crash. Nothing in the [Safari 26.5 release notes](https://webkit.org/blog/17938/webkit-features-for-safari-26-5/) (11 May 2026). |
| **Firefox (all platforms)** | ❌ **No** | [Bug 1961378](https://bugzilla.mozilla.org/show_bug.cgi?id=1961378) — "backdrop-filter gets ignored if it would fall back to a blob image (such like with some SVG url filters)" — status **NEW**, severity **S3**, part of the `wr-backdrop-filter-correctness` meta. Dupes: [1787623](https://bugzilla.mozilla.org/show_bug.cgi?id=1787623), 1972363, [1995195](https://bugzilla.mozilla.org/show_bug.cgi?id=1995195). WebRender limitation. |

**Note on iOS specifically:** every browser on iOS is WebKit. Chrome on iPhone is Safari. There is no Chromium escape hatch on iOS.

**Standards status:** [w3c/svgwg#1142](https://github.com/w3c/svgwg/issues/1142) (filed 25 June 2026) requests an interoperable backdrop displacement/refraction primitive — proposing a defined "BackdropGraphic" input, security boundaries preventing JS pixel readback, and possibly a higher-level refraction primitive. **No browser-vendor responses visible.** This is years away, not months.

### 3.3 `filter: url(#svg-filter)` on normal content

| Browser | Support |
|---|---|
| Chrome / Edge | ✅ |
| Firefox | ✅ |
| Safari | ✅ (with caveats: no live video, source-size caps, prefers `xlink:href` on `feImage`, historically flaky `feImage` handling — see [WebKit PR #73280](https://github.com/WebKit/WebKit/pull/73280) fixing fragmented external hrefs; `data:` URLs in `feImage` are legitimately supported) |

### 3.4 Accessibility media queries — verified from MDN browser-compat-data

| Feature | Chrome | Firefox | Safari |
|---|---|---|---|
| `prefers-reduced-motion` | 74 | 63 | 10.1 | 
| `prefers-contrast` | 96 | 101 | 14.1 |
| `forced-colors` | 89 | 89 | 16 |
| **`prefers-reduced-transparency`** | **118** | **113, BEHIND A PREF** (`layout.css.prefers-reduced-transparency.enabled`) | ❌ **NOT SUPPORTED** ([webkit.org/b/175497](https://webkit.org/b/175497)) |

**This is the second landmine.** The one media query that exists specifically to turn glass off is **unavailable on Apple platforms** — the exact platform whose users are most likely to have "Reduce Transparency" switched on, because Apple shipped it as the system-level remedy for Liquid Glass legibility complaints. You cannot honour that preference in Safari. Design so that the glass is legible *without* needing the opt-out. See §5.

### 3.5 `@supports` GIVES FALSE POSITIVES — do not trust it

Firefox's `@supports (backdrop-filter: url(#x))` returns **true** while silently not applying the filter. It parses the syntax; it just doesn't render it. Reported repeatedly across the Bugzilla dupes. **UNVERIFIED** whether Safari does the same — assume it does and probe anyway.

There is no pixel-readback probe available (the backdrop is deliberately unreadable from JS for cross-origin security reasons — an explicit constraint noted in svgwg#1142). So the only honest detection is an **engine gate**:

```js
/**
 * Refraction in backdrop-filter is Chromium-desktop/Android only (Sept 2026).
 * @supports lies in Firefox, so it cannot be the gate. Engine-sniff, reluctantly,
 * and re-test this function whenever WebKit PR 68614 lands.
 */
function glassTier() {
  const supportsBackdrop =
    CSS.supports('backdrop-filter', 'blur(1px)') ||
    CSS.supports('-webkit-backdrop-filter', 'blur(1px)');

  if (!supportsBackdrop) return 'solid';                       // Tier 3

  // userAgentData is Chromium-only and absent in all iOS browsers (all WebKit).
  const brands = navigator.userAgentData?.brands ?? [];
  const isChromium = brands.some(b => b.brand === 'Chromium');
  const isApple = /iPhone|iPad|iPod/.test(navigator.platform) ||
                  (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

  const canRefract = isChromium && !isApple &&
                     CSS.supports('backdrop-filter', 'url(#ot-refract)');

  // Refraction is desktop-only regardless: see §4 on iOS scroll repaint.
  const roomy = matchMedia('(min-width: 900px) and (pointer: fine)').matches;

  return (canRefract && roomy) ? 'refract' : 'blur';            // Tier 1 : Tier 2
}
document.documentElement.dataset.glass = glassTier();
```

### 3.6 The progressive-enhancement ladder

```css
/* ---------- TIER 3: universal floor. No backdrop-filter at all. ---------- */
.ot-nav {
  background: color-mix(in oklab, var(--ot-near-black) 88%, transparent);
  border: 1px solid rgb(255 255 255 / .12);
  box-shadow: 0 8px 32px -8px rgb(0 0 0 / .5);
}

/* ---------- TIER 2: THE PRODUCT. Safari, Firefox, all mobile. ---------- */
@supports ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .ot-nav {
    background: linear-gradient(180deg,
                  rgb(255 255 255 / .10), rgb(255 255 255 / .03) 42%,
                  rgb(255 255 255 / .07));
    -webkit-backdrop-filter: blur(18px) saturate(180%);
            backdrop-filter: blur(18px) saturate(180%);
    box-shadow:
      inset 0  1px 0 0 rgb(255 255 255 / .38),
      inset 0 -1px 0 0 rgb(255 255 255 / .10),
      0 8px 32px -8px rgb(0 0 0 / .45);
  }
}

/* ---------- TIER 1: Chromium desktop garnish only. ---------- */
html[data-glass="refract"] .ot-nav {
  backdrop-filter: url(#ot-refract) blur(6px) saturate(180%);
}

/* ---------- Forced overrides, all tiers ---------- */
@media (prefers-reduced-transparency: reduce), (prefers-contrast: more) {
  .ot-nav {
    -webkit-backdrop-filter: none !important;
            backdrop-filter: none !important;
    background: var(--ot-near-black) !important;
    border-color: rgb(255 255 255 / .4) !important;
  }
}
@media (forced-colors: active) {
  .ot-nav {
    -webkit-backdrop-filter: none; backdrop-filter: none;
    background: Canvas; border: 1px solid CanvasText;
  }
}
```

Note the ladder is **additive**, and Tier 2 carries the full visual identity. If Tier 1 never ships in WebKit, nothing is missing.

---

## 4. PERFORMANCE — WHY THIS GOES WRONG ON PHONES

### The mechanism

To blur what's behind a panel, the compositor must **snapshot the backdrop, blur it, and composite the result**. Cost scales with **blurred area × devicePixelRatio²**, and if anything in that chain changes, the whole chain re-runs.

### The iOS killer

**`position: fixed` / `position: sticky` + `backdrop-filter` causes WebKit to recompute the blur on every scroll frame instead of caching it.** This is the single most-reported glass performance bug, it hits Safari *and* Chrome on iOS (same engine), and it does not reproduce on desktop — so it will pass your local testing and tank on the client's phone.

**A floating glass scroll-bar is by definition `position: fixed`. This is the exact worst case and it is the centre of the brief.**

### Mitigations, ranked by actual impact

1. **Shrink the blurred area.** This is the dominant term and it's free. A **floating pill** (max ~560px, centred, inset from the top) instead of a full-bleed `100vw` bar cuts the cost by 60–75%. It's also the more premium look, so this is not a compromise.
2. **Never animate `blur()` radius.** A static blur can be cached; a transitioning blur cannot. If you want the bar to "solidify" on scroll, **cross-fade two pre-blurred layers with `opacity`** — opacity is the cheapest thing a compositor does.
   ```css
   .ot-nav__glass  { opacity: 1; transition: opacity 240ms linear; }
   .ot-nav__opaque { opacity: 0; transition: opacity 240ms linear; }
   [data-scrolled] .ot-nav__glass  { opacity: 0; }
   [data-scrolled] .ot-nav__opaque { opacity: 1; }
   ```
3. **Never blur over animating content.** If a hero video or a scroll-driven animation sits behind the bar, the backdrop is dirty every frame and the blur re-rasterises every frame. Given the brief explicitly wants AI-generated **video** backdrops, this is a direct collision. Either (a) let the bar leave the video region, or (b) accept an opaque bar while over video.
4. **Isolate the layer, sparingly.**
   ```css
   .ot-nav { contain: paint; transform: translateZ(0); }
   ```
   Use `will-change: backdrop-filter` **only** on the one persistent nav — not on every glass card. Over-using `will-change` inflates memory and GPU overhead and makes things slower.
5. **Cap the blur.** Above ~20px, low-end devices degrade sharply with negligible visual gain. 14–18px is the sweet spot.
6. **Budget one glass surface per viewport.** Stacked glass (modal over glass nav over glass card) multiplies snapshot cost non-linearly — this is the documented cause of the nested-modal exponential-lag class of bug.
7. **Drop to opaque on touch devices** as an explicit, deliberate choice:
   ```css
   @media (hover: none) and (pointer: coarse) {
     .ot-nav { backdrop-filter: blur(12px) saturate(160%); } /* reduced, not removed */
   }
   ```
8. **Verify, don't assume.** Chrome DevTools → Rendering → **Paint flashing** + **Layer borders**. If the nav region flashes green on every scroll tick, the blur is not being cached.

### Battery

Each re-blur is a GPU raster pass at full device resolution. A continuously-recomputing fullscreen blur during a long scroll session is measurably expensive on mobile. Mitigation 1 (small area) and mitigation 3 (no blur over moving video) are the two that matter for power.

---

## 5. ACCESSIBILITY — MAKING NAV TEXT SURVIVE AN UNPREDICTABLE BACKDROP

The problem, stated precisely: OVERTIME's nav will pass over a near-black hero *and* a bone/off-white product shot. A single text colour cannot hit 4.5:1 against both. Translucency means **you cannot compute the contrast ratio at author time** — it depends on pixels you don't control.

### Solution 1 — A contrast floor (do this unconditionally)

Do not rely on the backdrop. Guarantee a minimum opaque tint under the text so the worst case is still legible:

```css
:root {
  --ot-scrim: 0.72;          /* never below 0.60 for body-size nav text */
}
.ot-nav {
  background:
    linear-gradient(180deg, rgb(255 255 255 / .10), rgb(255 255 255 / .04)),
    rgb(10 10 12 / var(--ot-scrim));     /* ← the floor, under the glass tint */
}
```

At `--ot-scrim: 0.72` over near-black `#0A0A0C`, off-white text (`#F4F1EA`) clears 4.5:1 regardless of what's behind. Tune once, verify with a contrast checker against your two extremes (bone and near-black), then treat it as a locked token.

### Solution 2 — Adaptive tinting (this is the Apple move, and it's the un-vibe-coded detail)

Flip the nav's entire token set based on what section is currently under it. Mark up sections with their luminance class, observe with `IntersectionObserver` using a root margin pinned to the nav's band:

```js
const nav = document.querySelector('.ot-nav');
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (e.isIntersecting) {
      // data-nav-theme="light" on cream/bone sections, "dark" on near-black
      nav.dataset.over = e.target.dataset.navTheme || 'dark';
    }
  }
}, {
  // Sliver of viewport exactly where the pill sits: top 24px..80px
  rootMargin: '-24px 0px -92% 0px',
  threshold: 0
});
document.querySelectorAll('[data-nav-theme]').forEach(s => io.observe(s));
```

```css
.ot-nav[data-over="dark"] {
  --ot-ink: #F4F1EA;                     /* bone */
  --ot-scrim-color: rgb(10 10 12 / .72);
  --ot-rim: rgb(255 255 255 / .38);
}
.ot-nav[data-over="light"] {
  --ot-ink: #14141A;                     /* near-black */
  --ot-scrim-color: rgb(244 241 234 / .70);
  --ot-rim: rgb(255 255 255 / .85);
}
.ot-nav { color: var(--ot-ink); transition: color 200ms ease, background 200ms ease; }
```

This is the thing that separates a considered build from a template: the glass *knows what it's over*. It also directly serves the brief's "adaptive light/dark tinting" ingredient without needing any unsupported CSS.

### Solution 3 — Honour every preference that actually works

```css
@media (prefers-reduced-transparency: reduce) { /* Chrome 118+, FF behind pref, NOT Safari */
  .ot-nav { backdrop-filter: none; background: var(--ot-solid); }
}
@media (prefers-contrast: more) {               /* Chrome 96+, FF 101+, Safari 14.1+ — works everywhere */
  .ot-nav {
    backdrop-filter: none; background: var(--ot-solid);
    border: 1px solid currentColor;
  }
}
@media (prefers-reduced-motion: reduce) {       /* universal */
  .ot-nav, .ot-glass-btn { transition: none; animation: none; }
  :root { --ot-light: 210deg; }                 /* freeze the raking specular */
}
@media (forced-colors: active) {
  .ot-nav { backdrop-filter: none; background: Canvas; color: CanvasText; }
}
```

**Because `prefers-reduced-transparency` is unsupported in Safari, `prefers-contrast: more` is your only working lever on Apple platforms.** Wire both, and make sure Solution 1's scrim floor is high enough that a user who gets *neither* query honoured is still fine. Apple's own remedy for this problem was to raise navigation-bar opacity; follow them.

### Other

- Never rely on the glass edge alone to convey a boundary — keep a `1px` `--ot-rim` border with real contrast.
- Any cloned-backdrop layer (§2.6) must be `aria-hidden="true"` and `pointer-events: none`, and must not contain focusable elements.
- Focus rings must sit **above** the glass and use a solid colour, not a translucent one.

---

## 6. EXISTING IMPLEMENTATIONS — HONEST VERDICTS

| Project | What it does | Verdict |
|---|---|---|
| **[rdev/liquid-glass-react](https://github.com/rdev/liquid-glass-react)** (~6.2k★, MIT) | Most-starred React take. Props: `displacementScale`, `blurAmount`, `saturation`, `aberrationIntensity`, `cornerRadius`, `elasticity`, `mode` (standard/polar/prominent/shader), `overLight`. | **Study, don't ship.** Its own README states: *"Safari and Firefox only partially support the effect (displacement will not be visible)."* Honest, which is to its credit — but it means the headline feature is absent for most of your traffic. `shader` mode self-described as "not the most stable". ~16 commits on master; thin maintenance. |
| **[PallavAg/liquid-glass-web-react](https://github.com/PallavAg/liquid-glass-web-react)** | The genuinely cross-browser one. Generates a displacement map on the fly and applies `feDisplacementMap` **to the content itself**, not the backdrop — so it works in Chrome, Safari and Firefox. Zero deps, ~5 kB min+gzip, SSR-safe, imperative `setPosition()` ref for per-frame updates. Props incl. `chromaticAberration`, `curvature`, `glow`, `edgeHighlight`. | **The best engineering here, and the best thing to read.** But its stated limits are fatal for this brief: *SVG filters don't process live video on Safari*; *Safari caps filter source sizes*; iOS needs `objectBoundingBox`→`userSpaceOnUse` conversion. Steal the map-generation approach and the `userSpaceOnUse` handling. Don't adopt it for the nav. |
| **[dpawlikowski/liquid-glass](https://github.com/dpawlikowski/liquid-glass)** (MIT) | `feTurbulence` + `feDisplacementMap` on a duplicated scene layer; chromatic fringing via `mix-blend-mode: screen` on pseudo-elements. README claims Chrome/Edge 105+, Safari 16+ (*"keep `scale ≤ 18` to avoid artifacts"*), Firefox 103+ all "Full". | **Claims check out only because it doesn't use `backdrop-filter: url()`** — it filters cloned content, which genuinely is cross-browser. But turbulence-driven displacement produces a *watery/organic* wobble, not a crisp rounded-rect lens. **Wrong aesthetic for OVERTIME** — it looks liquid, not like glass over a nav bar. |
| **[nikdelvin/liquid-glass](https://github.com/nikdelvin/liquid-glass)** | "Pixel-perfect" iOS 26 recreation, CSS+SVG only; LiquidGlass containers, LiquidText, LiquidButton. | Worth a look for the component decomposition. **UNVERIFIED:** I did not confirm its browser-support claims against the bugs above — treat any "works everywhere" claim with the §3 table in hand. |
| **[kube.io write-up](https://kube.io/blog/liquid-glass-css-svg/)** | Not a library — the best *technical* article. Ray-traces Snell's law (n₁=1, n₂=1.5) over convex-circle / convex-squircle / concave / lip surface profiles, 127 radial samples, numerical-derivative normals. | **Read this first.** It is the most rigorous public treatment of map generation. It also states the constraint plainly: *"Only Chrome currently supports using SVG filters as `backdrop-filter`."* Also flags that the map rebuild is expensive on resize. |
| **[mycatwrotethis.blog](https://mycatwrotethis.blog/blog/liquid-glass-effect)** | Full filter chain incl. Fresnel rim via `feMorphology(erode)` → `feGaussianBlur` → `feComposite(operator="out")`, and specular sharpening via `feComponentTransfer` / `feFuncA type="gamma" exponent="5.0"`. Per-channel CA at scales −130/−140/−135. | **Steal the Fresnel and specular primitives verbatim** — they're good and they work on normal content everywhere. Ignore its browser-support silence. |
| **[shadcn-ui/ui#327](https://github.com/shadcn-ui/ui/issues/327)** | Not an implementation — the canonical "backdrop-filter is killing our performance" thread. | **Read as a cautionary tale** before committing to glass on many components. |
| `@callstack/liquid-glass` | React **Native** — real iOS 26 system material. | Irrelevant here. Listed only so nobody wastes time on it. |

**Overall recommendation: hand-roll.** The reasons are specific, not stylistic purism:

1. Every library's headline feature (backdrop refraction) is unavailable on the brief's primary platform. You'd be importing a dependency for something that doesn't run.
2. The libraries that *do* work cross-browser do so via content-cloning, which collides with the brief's AI-generated **video** backdrops (Safari won't filter live video).
3. The brief explicitly demands the "un-vibe-coded" look. Shipping the most-starred glass component means shipping the most-recognisable glass component. The differentiation is in the §5 adaptive tinting and the raking `--ot-light` specular, neither of which any library gives you.
4. The whole Tier 2 implementation is ~60 lines of CSS. The cost of hand-rolling is low; the cost of a dependency whose core feature is dark on iPhone is high.

Steal: kube.io's map maths, PallavAg's `userSpaceOnUse` handling, mycatwrotethis's Fresnel/specular primitives.

---

## 7. WHAT THIS MEANS FOR OVERTIME SPECIFICALLY

- **Build the floating pill, not the full-bleed bar.** It's better-looking, it's more premium, and it cuts the dominant performance term by ~70%. The two goals coincide — take the free win.
- **Tier 2 is the design.** Art-direct the blur/saturate/rim/scrim combination until *that* looks like the finished product on an iPhone. Add Tier 1 refraction afterwards, and only if it still looks right when it silently vanishes.
- **Dispersion: dial to near-zero or omit.** RGB fringing reads as glitch. OVERTIME is washed, muted, desaturated, vintage-athletic. Chromatic aberration fights the brand.
- **The time theme has an obvious hook here that nothing else gives you:** drive `--ot-light` (the raking specular angle) from scroll progress, so the highlight sweeps the rim like a second hand crossing a watch face. One custom property, works in every browser, costs nothing, and is exactly the kind of considered detail that reads as bespoke rather than generated.
- **Direct collision to resolve early:** the brief wants AI-generated video backdrops *and* a glass scroll bar. Blur over playing video = re-rasterise every frame, on the platform with the worst caching. Decide now: either the bar goes opaque while over video sections (use the §4 mitigation-2 opacity cross-fade, driven by the same `IntersectionObserver` as §5's adaptive tinting — one mechanism, two payoffs), or video does not sit under the bar.
- **Shopify implication:** everything above is vanilla CSS + one inline `<svg>` + ~40 lines of JS. It ports into a Shopify theme section or a Hydrogen component without modification. Keep the displacement-map generator in a single module with no DOM assumptions beyond `document.createElement('canvas')` so the design survives the storefront decision either way.

---

## 8. THINGS I COULD NOT VERIFY (flagged, not asserted)

- **`linear()` easing minimum versions** — used in §2.5. Believed widely supported but not confirmed in this research. Failure mode is safe (transition drops).
- **Whether Safari's `@supports` also returns a false positive** for `backdrop-filter: url()`. Confirmed for Firefox only. The §3.5 probe assumes it does.
- **Whether iOS Chrome exposes `navigator.userAgentData`.** The §3.5 probe includes a belt-and-braces Apple-platform check for this reason.
- **nikdelvin/liquid-glass's browser-support claims** — not independently tested.
- **Exact Chromium version** that first shipped SVG reference filters *in backdrop-filter* specifically (as distinct from `backdrop-filter` itself in Chrome 76). Sources agree Chromium supports it; none pinned the version. Treat as "modern Chromium".
- **Whether WebKit PR #68614 will land, and in which Safari version.** It was open and `merging-blocked` at the time of research. **Re-check [bug 245510](https://bugs.webkit.org/show_bug.cgi?id=245510) before shipping** — if it lands, Tier 1 becomes worth real investment and the §3.5 probe needs rewriting.

---

## Sources

- [WebKit Bug 245510 — backdrop-filter: url(#some-svg-filter) doesn't work with SVG filters like feDisplacementMap](https://bugs.webkit.org/show_bug.cgi?id=245510)
- [WebKit PR #68614 — backdrop-filter: url() SVG reference filters are not rendered](https://github.com/WebKit/WebKit/pull/68614)
- [WebKit PR #73280 — [SVG] feImage with a fragmented external href never loads the image](https://github.com/WebKit/WebKit/pull/73280)
- [Mozilla Bug 1961378 — backdrop-filter gets ignored if it would fall back to a blob image](https://bugzilla.mozilla.org/show_bug.cgi?id=1961378)
- [Mozilla Bug 1787623 — backdrop-filter: url(#svg-filter) causes the element to not render](https://bugzilla.mozilla.org/show_bug.cgi?id=1787623)
- [Mozilla Bug 1995195 — backdrop-filter doesn't work with svg filters](https://bugzilla.mozilla.org/show_bug.cgi?id=1995195)
- [w3c/svgwg Issue #1142 — Filter Effects: define interoperable backdrop displacement/refraction for "liquid glass" UI](https://github.com/w3c/svgwg/issues/1142)
- [mdn/browser-compat-data Issue #24110 — SVG filters not supported in Firefox or Safari](https://github.com/mdn/browser-compat-data/issues/24110)
- [MDN browser-compat-data raw source — css/properties/backdrop-filter.json](https://raw.githubusercontent.com/mdn/browser-compat-data/main/css/properties/backdrop-filter.json)
- [MDN browser-compat-data raw source — css/at-rules/media.json](https://raw.githubusercontent.com/mdn/browser-compat-data/main/css/at-rules/media.json)
- [MDN — backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter)
- [MDN — prefers-reduced-transparency](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-transparency)
- [Can I Use — css-backdrop-filter](https://caniuse.com/css-backdrop-filter)
- [WebKit Features for Safari 26.5 (11 May 2026)](https://webkit.org/blog/17938/webkit-features-for-safari-26-5/)
- [WebKit Features in Safari 26.0](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/)
- [Wikipedia — Liquid Glass](https://en.wikipedia.org/wiki/Liquid_Glass)
- [Apple has a private CSS property to add Liquid Glass effects to web content — alastair.is](https://alastair.is/apple-has-a-private-css-property-to-add-liquid-glass-effects-to-web-content/)
- [Liquid Glass in the Browser: Refraction with CSS and SVG — kube.io](https://kube.io/blog/liquid-glass-css-svg/)
- [Building Apple's Liquid Glass Effect for Web — mycatwrotethis.blog](https://mycatwrotethis.blog/blog/liquid-glass-effect)
- [Liquid Glass in CSS (and SVG) — ekino-france](https://medium.com/ekino-france/liquid-glass-in-css-and-svg-839985fcb88d)
- [rdev/liquid-glass-react](https://github.com/rdev/liquid-glass-react)
- [PallavAg/liquid-glass-web-react](https://github.com/PallavAg/liquid-glass-web-react)
- [dpawlikowski/liquid-glass](https://github.com/dpawlikowski/liquid-glass)
- [nikdelvin/liquid-glass](https://github.com/nikdelvin/liquid-glass)
- [shadcn-ui/ui Issue #327 — CSS Backdrop filter causing performance issues](https://github.com/shadcn-ui/ui/issues/327)
- [ant-design Issue #56707 — Modal lag worsening exponentially with nested modals due to backdrop-filter blur](https://github.com/ant-design/ant-design/issues/56707)
- [Chromatic Aberration with SVG Filters — John D. Jameson](https://johndjameson.com/posts/chromatic-aberration-with-svg-filters)
- [Filter Effects – SVG 1.1 (Second Edition), W3C](https://www.w3.org/TR/SVG11/filters.html)
- [web.dev — Create OS-style backgrounds with backdrop-filter](https://web.dev/articles/backdrop-filter)
- [Mozilla Connect — Support SVG filters in backdrop-filter for advanced glass effects](https://connect.mozilla.org/t5/ideas/support-svg-filters-in-backdrop-filter-for-advanced-glass/idi-p/98453)
- [CSS prefers-reduced-transparency — Chrome for Developers](https://developer.chrome.com/blog/css-prefers-reduced-transparency)