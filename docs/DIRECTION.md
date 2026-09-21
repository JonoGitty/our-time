# OUR TIME — website design direction

**Decision document · 16 Sep 2026**
Synthesised from 7 research briefs, 3 independent design concepts and 3 adversarial
judgements (14 agents). Research in `docs/research/`, raw concepts and scorecards in
`docs/concepts/`.

---

## 1. THE DIRECTION — "THE LEDGER"

**The site is a record. Time is the filing system, and the filing system is also the shop.**

OUR TIME's competitors decorate with clocks. This site refuses to, and is more
time-obsessed for it. Time appears as *metadata attached to real things*: the date a
piece was made, the drop it belongs to, the minute a size sold out, the hour a drop
closes. The collection sorts chronologically by default and category is a filter
applied on top. Strip every hourglass and clock illustration off this site and the
time concept survives intact — because it lives in the information architecture, not
the wallpaper.

Commercially it is a shop first: product within one screen, size and add-to-bag
inside the thumb arc on mobile, sizing and shrinkage stated openly rather than buried.
Visually it is an editorial quarterly: big confident type, generous emptiness, images
bleeding off the edge, and exactly one piece of chrome — a floating glass pill.

---

## 2. WHY THIS ONE — and the honest disagreement

The panel **split three ways**. Every judge picked a different winner, which means no
single concept was right and a straight pick would have been dishonest.

| Concept | Brand | Engineering | Commerce | Total | Fatal flaws |
|---|---|---|---|---|---|
| THE SLOW HAND | **8** | 7 | 6.5 | 21.5 | 5 |
| THE GLASS EMPTIES | 6.5 | **8** | 5 | 19.5 | 3 |
| THE COUNTER | 7.5 | 6 | **8.5** | 22.0 | 6 |

THE COUNTER scored highest in total and has zero commercial fatal flaws — but four
engineering ones. THE SLOW HAND has the only time idea that survives deleting the
props. THE GLASS EMPTIES is the only one that opens on a phone in under half a
megabyte.

**So: SLOW HAND's spine, COUNTER's commerce layer, GLASS EMPTIES's performance
architecture.** Specifically —

- **From THE SLOW HAND** — time as the filing system; the `/shop` ledger built for 7
  garment types × ~31 colourways from day one; colour selection as a real sibling URL
  (`/shorts-cream`) not a query param; the `bg: dark | paper` field per colourway; the
  nerve to leave a screen almost empty.
- **From THE COUNTER** — stock written as a timestamp (`SOLD OUT — 23:14, SUN 12 OCT`);
  the always-open sizing and garment-dye shrinkage band; notify-me capturing the size;
  the cart drawer with real discount-code failure; and the PDP nav pill morphing into
  `[S][M][L][XL] · ADD` bottom-anchored in the thumb arc — the best mobile conversion
  decision in the set.
- **From THE GLASS EMPTIES** — open on one preloaded AVIF, not an autoplay video;
  defer heavy media past `load` and suppress under Save-Data; the match cut; two
  optical sizes of one grotesque rather than two families.

### Three things all three concepts got wrong, now killed

1. **The hourglass scroll sequence is dead.** All three made it the structural climax,
   none had rendered it, and the teardown ranks the hourglass and clock face as the
   *most* built cliché for time-themed sites. The brand judge called it a costume, the
   commerce judge a single point of failure, and the client was already told Blender
   was overkill. **We are not building it.** The one scroll-scrubbed sequence becomes a
   garment in motion — fabric, not sand.
2. **Fabricated datelines are out.** `PHOTOGRAPHED 09.26 / NORTH TRACK, 19:40 BST` on
   an AI image of an invented place is a lie with good manners. Datelines stay, but
   only on facts we actually hold: made date, drop number, sell-out timestamp, dispatch
   cut-off. A real record or nothing.
3. **The always-on countdown is out.** *"Scarcity that's always on isn't scarcity; it's
   a Shopify app."* The counter appears **only** inside a genuine live drop window and
   is absent the rest of the time.

---

## 3. ART DIRECTION

### Palette — measured, not invented

No new hue enters the brand from the website. Every value is sampled from the supplied
renders (`brand/TOKENS.md`).

| Token | Hex | Role |
|---|---|---|
| `--ot-ground` | `#0F0F0F` | The page. **Never `#000`.** |
| `--ot-void` | `#000000` | Photographic backdrop *inside images only*. Never a CSS surface. |
| `--ot-ink` | `#FAF6F6` | Bone ink on dark. 17.9:1 on ground. Not `#FFF`. |
| `--ot-paper` | `#DFDDDE` | The light ground (off-white colourway). |
| `--ot-navy` | `#141B2C` | Deep section ground. |
| `--ot-slate` | `#54647E` | The single accent. The most saturated colour the brand owns. |
| `--ot-grey` | `#A7A5A4` | Washed grey garment. |
| `--ot-sand` | `#CFC2B4` | Cream garment. The only warm tone. |
| `--ot-coal` | `#171717` | Washed black garment. |

**The contrast trap — enforced, not noted.** `#171717` on `#0F0F0F` is **1.07:1** — a
washed-black garment on the dark ground is invisible, and so is any UI chip using it.
`#A7A5A4` on `#DFDDDE` is **1.84:1** — washed grey disappears on paper. Therefore every
colourway in the catalogue carries a required `bg: "dark" | "paper"` field, enforced in
the schema, which decides both which ground it is *displayed* on and which backdrop it
is *generated* against. Washed black is shot on warm sand. Washed grey is shot on the
dark ground. This is fixed at generation time, not patched in CSS.

### Typography

Two optical sizes of one grotesque, one mono, and no serif. The brand's own signature
is already a contrast pair — heavy sheared italic monogram against a thin wide-tracked
wordmark — so the site reproduces that tension rather than inventing a third voice.

- **Display** — Neue Haas Grotesk Display Pro 55/65. Headlines, 40px+.
- **Text** — Neue Haas Grotesk Text 55/75. Body, nav, buttons.
- **Mono** — one grotesque mono. Datelines, prices, the counter, timestamps. **This is
  the only place wide tracking is permitted.**
- The `OUR TIME` wordmark is **artwork, never a webfont** — an inline SVG, so the word
  space can never collapse.

Licensing: Monotype webfont tier, lowest band for a launch label. Budget £150–£400
one-off. Self-hosted subset woff2, `font-display: swap`, preloaded.

> **The word-space guard.** The rename work in this session proved `OUR TIME` collapses
> to `OURTIME` under the slightest pressure. A Playwright CI assertion measures the
> rendered pixel gap between the `R` and the `T` and **fails the build** below `0.5em`.

### Motion — a budget, not a preference

Four permitted motions. Anything not on this list does not move.

1. A slow specular sweep across the glass pill's rim, driven by scroll progress — one
   revolution top to bottom of the document.
2. One scroll-scrubbed image sequence (fabric in motion), once per site.
3. `animation-timeline: view()` reveals, with an `IntersectionObserver` fallback.
4. The drop counter ticking — tabular digits, no odometer roll — *only during a live drop*.

Any autoplaying loop carries a **visible pause control**. WCAG 2.2.2 (Level A) requires
it, and `prefers-reduced-motion` does not satisfy it — that is a different user.

---

## 4. THE LIQUID GLASS NAV — SPEC

**It is a pill, not a bar, and that is a technical decision as much as an aesthetic one.**
The dominant performance term is *blurred area × dpr²*, and `position: fixed` +
`backdrop-filter` makes WebKit recompute the blur on **every scroll frame**. A 560px
pill instead of a 100vw bar cuts that cost 60–75%. It is also the better object: the
teardown found **zero** streetwear brands blurring their nav, so we are the one that
does — which means it has to be small, and it has to be perfect.

**Geometry.** Desktop: centred, `max-width: 560px`, `height: 52px`, `top: 20px`,
`border-radius: 999px`. Contents: `[OT monogram] · SHOP · DROP · STORY · BAG (2)`.
Mobile: `inset-inline: 12px`, `height: 48px`, three targets — `[OT] · BAG · MENU`.
Wrapper is `pointer-events: none`, pill is `pointer-events: auto`. **The thin wordmark
never appears at nav scale — only the heavy monogram.**

### The browser truth table

| Tier | Technique | Chrome/Edge | Safari (all) | Firefox |
|---|---|---|---|---|
| **1 — true refraction** | `backdrop-filter: url(#svg)` + `feDisplacementMap` | ✅ | ❌ | ❌ |
| **2 — the product** | `backdrop-filter: blur() saturate()` + rim gradient | ✅ | ✅ | ✅ |
| **3 — fallback** | `rgb(15 15 15 / .94)`, no blur | ✅ | ✅ | ✅ |

**Tier 1 is Chromium-only and will not ship on iPhone.** WebKit bug 245510 is status
**NEW**; PR #68614 is open and labelled `merging-blocked`; nothing in the Safari 26.5
notes (11 May 2026).

**This is the single most important implementation detail:** Firefox's
`@supports (backdrop-filter: url(#x))` returns **`true` while silently rendering
nothing**. Feature detection is therefore *actively harmful* here. The backdrop cannot
be read back from JS (deliberately, for cross-origin security), so there is no pixel
probe. **The only honest gate is an engine gate** — ship Tier 1 to Chromium only, and
re-test when PR 68614 lands.

**Tier 2 is the real product.** It must look deliberate and finished on an iPhone,
because that is where the traffic is. Tier 1 is a bonus on desktop Chrome, never the
design. `prefers-reduced-transparency` is honoured where supported (note: not in
Safari). The focus ring is 2px ink, 2px offset, 4px ground halo, always painted *above*
the glass, colours swapped on paper.

---

## 5. THE SITE

| # | Section | Purpose | Desktop | Mobile |
|---|---|---|---|---|
| 00 | The pill | Persistent chrome | Top-centred, 560px | Top, 3 targets; morphs to size+ADD on PDP |
| 01 | Plate | One image, one line, no buttons | 78svh, caption in corner | 72svh, full bleed |
| 02 | The rail | **Product within one screen** | 4-up horizontal scroll, quick-add | 1.4-card peek |
| 03 | The run | The shorts, six colourways | Colour bar, off-grid | Stacked, swipe |
| 04 | The sequence | The one scroll-scrub — fabric in motion | Pinned, 140vh | Pinned, 120vh, reduced frames |
| 05 | Fit & care | Shrinkage, measurements — **always open** | Two columns | Stacked |
| 06 | OUR TIME | The payoff line | Full bleed, type only | Full bleed |
| 07 | The list | Email capture | Inline | Inline |
| — | `/shop` | The ledger | Chronological default + filters | Sticky filter bar |
| — | `/shop/:handle` | PDP | Gallery + buy column | Gallery, bottom-anchored buy |
| — | Bag | Drawer, not a page | Right drawer | Full-height sheet |

The **match cut**: section 04 ends by cutting — not transitioning — into a full-bleed
still at identical crop height, key-light angle and subject scale.

---

## 6. THE ASSET PIPELINE

**Proven this session, not speculative.** The rename work (`brand/renamed/`) established
the chain end to end.

```
brand/source/*.jpg                    supplied flat-lays, untouched
        ↓  tools/genimg.py            Gemini 3 Pro Image, reference-conditioned
brand/renamed/APPROVED/*.png          corrected wordmark + Black Isle coordinates
        ↓  same tool, character refs
lookbook stills — garments on models
        ↓  Veo 3.1 Fast (image→video)
8s silent clips
        ↓  ffmpeg
AVIF poster + WebP frame sequence + mp4/webm
```

### Hard limits — budget every call

**Gemini 3 Pro Image caps at 6 object + 5 character + 3 style references, 14 total.**
One concept's group shot exceeded the character cap by 2×. Every multi-reference call
gets a budget check before it is sent.

### Verified pricing

| Model | Unit | Cost |
|---|---|---|
| Gemini 3 Pro Image | 1K/2K image | **$0.134** (4K $0.24; batch = half) |
| Veo 3.1 **Lite** 720p | per second | $0.05 → **$0.40** / 8s |
| Veo 3.1 **Fast** 720p | per second | $0.10 → **$0.80** / 8s |
| Veo 3.1 Standard 720/1080p | per second | $0.40 → $3.20 / 8s |
| Sora 2 720p | per second | $0.10 → $0.80 / 8s |
| Sora 2 Pro 1080p | per second | $0.70 → $5.60 / 8s |

**Recommendation: Veo 3.1 Fast.** Silent, cheap, image-conditioned, 8s is plenty for a
loop. Sora 2 is equivalently priced at 720p and worth one A/B in the pilot.
⚠️ Tier-1 spend rate limit is $10 per rolling 10 minutes — batch on Fast/Lite overnight
or sit in `429`s.

### Scroll media — settled

**Image sequence, not scrubbed video.** Video scrubbing is keyframe-dependent (GOP 1
approaches image-sequence bytes anyway) and iOS Safari coalesces and drops seeks under
load. A frame sequence behaves identically in every browser. WebCodecs is Safari 26+
only and would mean shipping two pipelines — not worth it.

### The pilot — ~$9 against the $15 ceiling

| Step | Calls | Cost |
|---|---|---|
| Casting candidates | 2 × 2K | $0.27 |
| Character sheet (chosen face, 5 views) | 5 × 2K | $0.67 |
| Style plates | 3 × 2K | $0.40 |
| Hero garment-on-model | 1 × 4K | $0.24 |
| Two colourways | 2 × 2K | $0.27 |
| Re-roll allowance (3×) | ~9 × 2K | $1.21 |
| **Veo 3.1 Fast test clip** | 1 × 8s | $0.80 |
| Sora 2 A/B | 1 × 8s | $0.80 |
| **Subtotal** | | **~$4.66** |
| Contingency | | ~$4 |

Spent so far: **8 generations ≈ $1.15** (the renames + Black Isle coordinates).

---

## 7. TECH STACK AND THE COMMERCE SEAM

**Astro 5 · TypeScript strict · hand-written CSS · no Tailwind · no React on the critical path.**

All three concepts converged on this independently. Astro ships zero JS by default and
hydrates only islands — the pill (`client:idle`), the sequence (`client:visible`), the
PDP buy column (`client:load`), the cart drawer. PDPs and collection pages are
statically generated, which is what storefront SEO actually needs; a client-only SPA
would be an own-goal.

**No Shopify store exists yet**, so commerce sits behind an adapter:

```ts
export interface StorefrontAdapter {
  getProduct(handle: string): Promise<Product | null>
  listProducts(filter?: CollectionFilter): Promise<Product[]>
  createCart(): Promise<Cart>
  addLines(cartId: string, lines: CartLineInput[]): Promise<Cart>
  checkoutUrl(cartId: string): Promise<string>   // always a redirect out
}
```

Modelled correctly from day one against fake data, because these leak into the UI and
are expensive to retrofit: **variants as size × colour option sets**; tri-state
inventory (`quantityAvailable: null` = untracked = available, *never* zero);
compare-at price; media galleries; cart lines with attributes; discount codes that can
genuinely fail. `local.ts` today → `shopify.ts` later, one file.

**Checkout is always a redirect to hosted checkout.** That is not a limitation to design
around; it is the constraint, on every platform at this tier.

---

## 8. ANTI-VIBE-CODE CHECKLIST

Check the build against this before showing anyone.

- [ ] No purple→blue gradient. No gradient the brand doesn't own.
- [ ] No glassmorphism cards. **One** glass object on the site — the pill.
- [ ] No emoji anywhere. No lucide icons in circles. No floating orbs.
- [ ] Not Inter. Not system-ui at default weights.
- [ ] No centred hero with two buttons.
- [ ] No Features / Testimonials / FAQ / CTA section rhythm.
- [ ] No uniform 8px radii. No default Tailwind shadows.
- [ ] Tokens named for materials (`--ot-sand`), never `--primary` / `--accent`.
- [ ] Real dates, real places, real numbers — or none at all.
- [ ] At least one screen with almost nothing on it, on purpose.
- [ ] Images bleed off the viewport edge somewhere.
- [ ] `#171717` never sits on `#0F0F0F`. `#A7A5A4` never sits on `#DFDDDE`.
- [ ] The `OUR TIME` word space survives at every breakpoint (CI-enforced).

---

## 9. BUILD PLAN

| Phase | What | Spend |
|---|---|---|
| 1 | Design tokens, type scale, the glass pill with all three tiers, tested on a real iPhone | £0 |
| 2 | Catalogue schema + `local.ts` adapter, all 7 types × ~31 colourways, `bg` field enforced | £0 |
| 3 | `/shop` ledger, PDP, cart drawer — on fake data, fully working | £0 |
| 4 | **Asset pilot** — casting, character sheet, 2 colourways, 1 video A/B | **~$9** |
| 5 | Home page assembled against real assets | £0 |
| 6 | Full asset run once the pilot look is approved | costed separately |
| 7 | Perf pass: payload budget, Lighthouse on throttled mobile, CI word-space guard | £0 |

Phases 1–3 spend nothing and produce a fully working shop on fake data. **The pilot is
the only gate that needs money, and it is deliberately placed after the site works.**

---

## 10. OPEN QUESTIONS

1. **The `OVERTIME` / `OUR TIME` print conflict is a production issue, not a web one.**
   If any garment is already with a manufacturer, the artwork needs pulling now.
2. **Is there a drop date?** The counter, the archive and the whole `/drop` structure
   depend on a real window. Without one, section 02 becomes an always-on shop.
3. **Fit and shrinkage figures** — needed as real numbers for the Fit & Care band. On
   garment-dyed washed pieces this is the entire returns bill.
4. **Casting** — I'll bring 2 candidate faces from the pilot for approval before
   generating the full set.
5. **UK ASA disclosure.** AI-generated models in fashion advertising: Google outputs
   carry SynthID. Worth a one-line decision on whether the site discloses it.
