# OVERTIME — Design-Intelligence Teardown: What Real Fashion Sites Do in 2026

## 0. Method & confidence

I fetched the live HTML and the primary theme stylesheets of 18 sites on **16 Sep 2026** with `curl` and analysed them directly (fonts, letter-spacing tokens, aspect ratios, header markup, video elements, countdown configs, motion libraries). Everything below marked with a code snippet is **verified from source**, not inferred.

**Corpus saved at** `/tmp/claude-1000/-mnt-c-Users-jonog/ab01cf7a-8049-4ea4-83af-8ecfa89c04cc/scratchpad/` (`*.html`, `*.css`) if you want to re-check any claim.

Limits, stated honestly:
- I did **not** render these in a browser. I can prove what's in the markup/CSS; I can't prove how a transition *feels*. Anything about perceived motion quality is flagged.
- **Jacquemus** (`jacquemus.com`) and **Bottega Veneta** (`bottegaveneta.com`) both returned **HTTP 403** to both curl and WebFetch. Their specifics are **UNVERIFIED** and I've excluded them from the numbered teardown rather than invent detail.
- Motion-library detection covers delivered HTML + the main theme CSS. Hashed app bundles were not exhaustively audited.

---

## THE HEADLINE ANSWER TO THE "LIQUID GLASS BAR" QUESTION

I scanned every `backdrop-filter` rule in seven major streetwear/fashion stylesheets (Stüssy, Corteiz, Cole Buxton, Palace, Sporty & Rich, Aimé Leon Dore, Broken Planet), specifically looking for one attached to a header/nav selector.

**Result: zero. Not one brand in this category blurs its navigation bar.**

The two places glass *is* actually used, verified:

1. **Sporty & Rich — the sticky FILTER bar on collection pages** (the only nav-adjacent blur found anywhere):
```css
.filter-bar.filter-bar--sticky{background-color:var(--color-background-semi-transparent-80);
-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
```
2. **Represent — a full-screen scrim *behind* the open mega-menu**, not the bar itself:
```html
<div shadow class="fixed inset-0 bg-black bg-opacity-[0.03] z-20"
     style="backdrop-filter: blur(24px); display:none; opacity:0;"></div>
```

And the floating bar *does* exist in this category — but **solid, not glass**. Palace:
```html
<header class="fixed pointer-events-none left-0 top-0 z-220 pt-(--header-padding) w-full flex justify-center">
  <div data-testid="header-pill-desktop" class="justify-center relative w-full hidden md:flex">
    <div class="w-auto bg-black text-white h-[var(--header-height)] rounded-full clip-rounded flex pointer-events-auto">
```
`border-radius: 2147483647px` (max-int pill) in their CSS. Contents of the pill: **Web Shop · Shops · Advice · Cart · Menu** — five words. Everything else (All, New, Jackets, Shirting, Tops, Bottoms, Shorts, Tracksuits, Hoods, Sweatshirts, T-Shirts, Hats, Underwear, Footwear, Bags, Accessories, Hardware) lives behind "Menu".

**So: the floating bar is legitimate; the glass is not.** The reason is legibility — this whole category flies white type over dark photography, and a blur over a busy photographic background produces variable contrast. Apple's own Liquid Glass has been repeatedly criticised on exactly this ([CSS-Tricks](https://css-tricks.com/getting-clarity-on-apples-liquid-glass/), [ekino](https://medium.com/ekino-france/liquid-glass-in-css-and-svg-839985fcb88d)), the true refraction effect needs `backdrop-filter: url(#svg-filter)` which **does not work in WebKit**, and `backdrop-filter` only looks like anything when there is content underneath it.

**Recommendation for OVERTIME: build a floating pill, but earn the glass.** Ship it as a near-opaque smoked pill (`rgba(10,10,10,0.72)` + `backdrop-filter: blur(20px) saturate(1.4)`) with a `@supports` fallback to solid, a 1px hairline top-edge highlight, and a hard rule that contrast never drops below 4.5:1 against the video behind it. Use the *real* blur where the category actually uses it — the mega-menu scrim and the sticky filter bar.

---

## 1–6. THE SITES

### ① Palace — `shop.palaceskateboards.com` — **the floating-bar precedent**

- **Nav:** `position:fixed`, centred, full-pill, `bg-black text-white`, opaque. Separate desktop and mobile pills. Wrapper is `pointer-events-none` with the pill `pointer-events-auto` — the page behind stays clickable. Five labels max; the rest behind "Menu". **No blur.** Custom stack (Shopify Oxygen + Tailwind v4), not a Liquid theme.
- **Hero:** stills. Product is immediately reachable.
- **Type:** **Neue Helvetica W01** (`neue-helvetica-w01-CykExj90.woff2`). Exactly **one** `letter-spacing` declaration in the whole 65KB stylesheet, and it's `inherit`. Zero decorative tracking.
- **Grid/PDP:** `aspect-ratio:1/1` on cards, `9/10` on PDP media. `quick-add` present (52 refs). No colour swatches on the PDP, no Klarna/Clearpay clutter, no accordions. Product slugs are opaque hashes (`/products/dnscafruwia0`).
- **Drop:** weekly, **Friday 11:00 GMT**, globally simultaneous ([PalaceCommunity](https://www.palacecmty.com/help/drop-times/), [Hypebeast](https://hypebeast.com/2026/3/palace-skateboards-spring-2026-drop-6-release-info)). The *calendar* is the mechanic — the site itself carries no countdown.
- **Lesson:** discipline. A floating bar works because it holds five words.

### ② Corteiz — `corteiz.com` — **the countdown masterclass, and the anti-design stance**

- **Countdown, verified in full** (Essential Countdown Timer app):
```json
{"name":"STORE CLOSING SOON.","endDate":"2026-09-09T23:00:00.000Z","timerType":"toDate",
 "type":"top-bar","legendCopyDays":"DAYS","legendCopyHours":"HOURS","legendCopyMins":"MINS",
 "legendCopySecs":"SECS","onceItEnds":"hide","closeButton":false,
 "style":{"timerSize":"20","legendSize":"12","timerColor":"#ffffff","singleColor":"#A20000",
          "position":"bottom-page","stickyBar":false}}
```
  **This is the single most important finding for OVERTIME.** Corteiz's timer does not count down to a launch — it counts down to the **store closing**. Inverted scarcity: not "wait", but "you have this long". `closeButton:false` (you can't dismiss it), `onceItEnds:"hide"` (it vanishes cleanly, no dead zeros), 20px digits / 12px legends, white on Corteiz red.
- **Type:** the most extreme position in the category:
```css
body,input,textarea,button,select{font-size:12px;font-family:Courier New,courier,serif;color:#ffd500;line-height:1.6}
h1,.h1,h2,.h2,h3,.h3{font-family:Courier New,courier,serif;font-weight:400;color:#ffd500}
```
  **12px Courier New, yellow-on-black, headings in the same face at the same weight.** By every conventional metric this is a bad website. It is also one of the most valuable streetwear brands in Britain. Proof that "un-vibe-coded" is a *stance*, not polish.
- **Nav/hero:** sticky bar, full category list, **no hero at all** — straight into product. Time-to-product: zero scroll.
- **Grid/PDP:** `aspect-ratio:1.0` and `4/5`. Size buttons are plain text (`XS S M L XL XXL`), `Sold Out` / `PRE-ORDER` states, featherlight lightbox, size guide as a raw HTML table pasted into the description.
- **Motion:** none detected. No carousel library, no IntersectionObserver, nothing.
- **Access model:** historically password-gated on drop days, entry via a newsletter access code, private Instagram, no pre-announced timing ([Euronews](https://www.euronews.com/culture/2023/03/17/the-rise-of-corteiz-inside-the-genius-marketing-strategies-of-londons-hottest-streetwear-b), [LOVE Creative](https://www.lovecreative.com/blog/3x-ways-corteiz-is-breaking-all-the-rules)).

### ③ Cole Buxton — `colebuxton.com` — **closest positional match to OVERTIME**

Vintage-athletic, muted, deliberately unbranded, British, Shopify, built by [Reap Agency](https://www.reapagency.co.uk/portfolio/colebuxton/). Study this one hardest.

- **Nav — the exact behaviour to copy:**
```html
<header-component class="header color-scheme-1" transparent="not-sticky" sticky="scroll-up">
```
  Transparent while it's over the hero; becomes a solid sticky bar **only on scroll-up**. Scroll down and it gets out of the way. This is the sophisticated move: context-aware, not a permanent chrome band.
- **Homepage section order (verified):** `header_announcements → header → hero → product_list → hero → product_list → collection_list → hero → product_list → collection_list → footer`. **Product appears in section 3.** Editorial and commerce alternate in a strict rhythm, ~1.5 screens per beat.
- **Hero countdown, verified:**
```html
<countdown-timer-… class="ai-countdown-timer text-center flex flex-column"
  data-end-date="2026-09-11" data-end-time="10:00:00" data-timezone="store">
  <h2 class="ai-countdown-timer__title">PRE-AUTUMN GRAPHICS</h2>
  <div class="countdown-timer__expired hidden"><a href="/collections/pre-autumn-graphics">view collection</a></div>
  <div class="countdown-timer__display …
```
  Plus this, which is the detail everyone misses:
```css
.hero__content-wrapper:has(.ai-countdown-timer){visibility:hidden;opacity:0;transition:all 0.3s ease}
```
  The hero copy is **hidden until the timer has resolved**, so you never see a flash of `00:00:00` or duplicated messaging. And on expiry the countdown **swaps in-place into a "view collection" link** — no dead state, no refresh required. Named drop ("PRE-AUTUMN GRAPHICS"), `data-timezone="store"` so everyone worldwide sees the same moment.
- **Type:** **Akkurat** (`Akkurat-Light.woff2`, `Akkurat-Bold.woff2`) — Lineto's Swiss grotesque. Light + Bold only, no middle weights. Fully tokenised (`--font-h1--family`, `--font-h1--letter-spacing`).
- **Grid:** `--product-grid-columns-desktop: repeat(4, 1fr)` desktop, 2-up mobile, `aspect-ratio: 4 / 5`, `hover_image` (hover-to-second-shot, 24 instances), `quick-add`. PDP: `aspect-ratio: 1/1.25`, colour swatches, zoom, `<details>` accordions, `Add to cart` / `Out of Stock`, Klarna/Clearpay/Afterpay/Shop Pay badges.

### ④ Aimé Leon Dore — `aimeleondore.com` — **the micro-typography system to steal**

The most considered type system of the eighteen.

- **Fonts:** **Söhne** (Klim, body), **Financier Display** (Commercial Type, editorial serif), **DIN W01** (nav/UI), **Pitch** (mono). Four faces, each with a job.
- **The rule that matters most to you** — ALD tracks wide, but **only at 8–12px, uppercase, never on headlines**:
```css
.link,.small-caption{letter-spacing:.15em;text-transform:uppercase;font-size:.625rem}   /* 10px */
.navbar{text-transform:uppercase;letter-spacing:.1em;font-family:DIN W01 Regular,Arial,sans-serif}
.plp-product__tag{letter-spacing:.15em;text-transform:uppercase;font-size:.625rem;position:absolute;top:20px;left:20px}
.gated-product{letter-spacing:.15em;text-transform:uppercase;font-size:.5rem;color:#c4c4c4}  /* 8px */
.filter-menu h3,.category-menu h3,.sorting-menu h3{text-transform:uppercase;letter-spacing:.15em;font-size:.625rem}
.panel__content table{letter-spacing:.15em;font-size:.625rem;font-variant-numeric:diagonal-fractions}
```
  Meanwhile the headline scale is `.headline{font-size:2.75rem}` → `.headline--fbig{font-size:5.75rem}` (44–92px) with **no tracking at all**. That inversion — *tight and large, or tiny and wide-tracked, never both* — is the whole game, and it is precisely where OVERTIME's thin wide "O V E R T I M E" wordmark could go wrong if it's used as a headline face.
- Note `.gated-product` — ALD literally ships a **gated product** state class. And `font-variant-numeric: diagonal-fractions` on size tables: a one-line detail no template would ever include.
- **Nav:** `header--crest-transition header--light` over a light hero — the crest/logo morphs on scroll (transition named in the class; visual behaviour **UNVERIFIED**).
- **Hero:** two `<video>` elements, autoplay/loop/muted/playsinline, **separately class-gated** `.video-desktop.d-none.d-lg-block` and `.video-mobile.d-lg-none`, Vimeo 1080p progressive renditions.
- **Grid:** `4/5`, `16/9`, `69/50`. Homepage is almost entirely editorial — Lookbook and News sit *inside* the commerce nav.

### ⑤ Stüssy — `stussy.com` — **maximum restraint**

- **Type:** Helvetica Neue LT Pro, three weights (`Roman`, `Md`, `Bd`). That is the entire type system.
- **Letter-spacing, the whole stylesheet (191KB), four values:** `-.015em`, `.01em`, `0`, `inherit`. **Effectively zero decorative tracking anywhere on the site.**
- **Radius:** `0`, one `.25rem`, one `624.9375rem` (a badge pill). Square by default.
- **Nav:** `<header class="shopify-section fixed w-full top-0">`, hamburger ("MENU / CLOSE") with a nested mega-menu. Header is `h-[81px]` mobile, `h-[54px]` **desktop** — the desktop bar is *shorter* than mobile, the opposite of the default instinct.
- **Grid:** Tailwind `grid-cols-1/2/3/4`, `aspect-ratio: 4/5` and `7/5`, driven by `--ar-desktop` / `--ar-mobile` CSS vars so the ratio can differ per breakpoint. `Sold Out` and `Notify Me`.
- **Motion:** Swiper + IntersectionObserver + `animation-timeline` (scroll-driven CSS). No JS animation library.
- **Homepage:** `header → section_homepage_feature_blocks`. One section. That's it.

### ⑥ Represent — `representclo.com` — **the best video technique**

- **Nav:**
```html
<header-navigation data-style="dark" data-active="0" data-theme="light" open="false"
  class="block fixed top-[var(--top-bar-height)] z-40 w-full text-xs whitespace-nowrap
  [body:not(.search_open)_&[data-style='light-solid'][open='false']]:bg-white
  [body:not(.search_open)_&[data-style*='light']]:text-black …">
```
  Fixed, offset by a **CSS-variable announcement-bar height**, and its colour scheme flips via a `data-style` attribute (`dark` / `light` / `light-solid`) — so the bar recolours per section as you scroll past dark imagery into light. That's the grown-up alternative to glass: **the bar adapts to what's behind it instead of blurring it.**
- **The video trick — one element, two orientations:**
```html
<video class="block object-cover h-full w-full absolute inset-0" loop muted playsinline autoplay
       data-autoplay-on-intersect="0" poster="data:image/gif;base64,R0lGOD…">
  <source src="…63692686.mp4" media="(orientation: portrait)" type="video/mp4">
  <source src="…63692682.mp4" type="video/mp4">
```
  `media="(orientation: portrait)"` inside `<source>` — the browser picks the phone cut vs the desktop cut natively, no JS, no double download. Served through SpeedSize (`scdn.speedsize.com`) at HD-1080p/7.2Mbps. **Use this exact pattern for OVERTIME's AI-generated hero.**
- **Glass:** `blur(24px)` on the mega-menu scrim, `blur(8px)` on the auth drawer, `blur(4px)` on the cart drawer and cookie banner. Blur on **overlays**, never chrome.
- **Type:** **STK Bureau Sans** (`STKBureauSans-Book.woff2`) for nav, otherwise a system stack.
- **Commerce:** full image-tiled mega-menus, `QuickAdd` (25 refs), `position:sticky` (3), `window.countdownCutoff` (an order-by-time-for-next-day-dispatch cutoff — a *different*, non-hype use of a timer worth stealing).

### ⑦ Sporty & Rich — `sportyandrich.com` — **the type-mixing model + the only glass**

- **Type — five faces, and it works:** **Jost** (grotesque UI), **Big Caslon Medium** (display serif), **Bookmania** (serif), **Industrial 736 BT Italic** (the retro-athletic italic — closest living relative to your OT monogram's energy), plus system. Tracking: `.025em`, `.05em`, `.075em` — a real graduated scale, not one arbitrary value.
- **Nav:** `data-enable-sticky-header="true" data-transparent-header="true"`, `header--layout-logo-center-nav-left` — **centred logo, nav pushed left**. Asymmetric, and it reads as deliberate.
- **Hero:** `video_hero` is the **first section after the header**. Section order: `announcement → header → quickCart → video_hero → [editorial] → image_hero → [editorial] → collection_list_slider → footer`. Commerce arrives late.
- **A mistake to avoid:** both the desktop and mobile `<video>` load the **same `.mov` file** (`cdn.shopify.com/videos/c/o/v/4d0bb443…mov`). `.mov` is Safari-friendly and broadly wasteful. Ship H.264 MP4 + a WebM/AV1 alternate.
- **Glass:** the sticky filter bar (quoted above) — `blur(10px)` over `--color-background-semi-transparent-80`.
- **Commerce:** 64 `sold out` refs, `Notify Me`, a dedicated **back-in-stock/restock app** with pre-order forms. `aspect-ratio: .8` (=4/5) and `2/3`. `QuickAdd` (62 refs).

### ⑧ Fear of God / ESSENTIALS — `fearofgod.com` — **hero-only homepage**

- **Section order:** `header → hero → hero → hero → footer`. **Three heroes and no product grid at all.** Time-to-product: you must click. That's a confidence play only a brand with demand can make — and worth noting as the ceiling of restraint, not a target for a 2026 launch.
- **Type:** **Helvetica Neue LT Pro Condensed** + **Light Condensed** + **Optima** (all four formats: woff2/woff/otf/ttf). Condensed grotesque for structure, Optima's humanist flare for the luxury register. Two moods, two faces.
- **Hero video:** `autoplay loop muted playsinline preload="me[tadata]"`, `aspect-ratio: 1.7777…` (16:9), Shopify CDN HD-1080p/7.2Mbps.
- **Nav:** enormous mega-menu (Featured / Collections / Essentials / Athletics / Mens / Womens with deep sub-trees) — proof that a huge menu and a spare homepage coexist fine.

### Supporting reads (shorter)

**Arc'teryx** — `<video autoplay loop muted playsinline>` serving `ARC_CampaignCD_DotCom_FW_2026_FW26-SperroSV_Clean_Homepage_Loop_N_16x9.mp4` through **imgix with `?fm=mp4&video-bitrate=3m`** — video transcoded on the fly by an image CDN, bitrate as a URL parameter. Ships an accessible fallback `<a>` download link and an `aria-label`. Card components carry an explicit `hasHoverImage` flag.

**Gymshark** — the best mobile/desktop video discipline: **separate assets** (`SEPT_SEASONAL_MENS_8x3_WEB_BANNER.mp4` vs `SEPT_SEASONAL_MENS_MOBILE_9x16.mp4`), `preload="none"`, a JPEG `poster` on every one, `data-desktop-breakpoint="tablet"`. Grid is uniformly `aspect-ratio:4/5`. Drop banner copy lives in Contentful (`"Ecomm - Fall MSS - DUAL - Build-up - Countdown"` → `"LAST CHANCE SALE COMING SOON"`) — the countdown is **content-managed**, not hardcoded. Copy that.

**Trapstar** — **the cautionary tale.** A genuinely major London brand running:
```
--font-heading--family: Inter, sans-serif;  --font-heading--weight: 300;
--font-body--family:    Inter, sans-serif;  --font-body--weight:    300;
```
Inter Light for headings *and* body, unmodified Shopify Dawn-family tokens, no custom faces, no hero video, 3 quick-add refs. **It is the most "vibe-coded"-looking site of the eighteen despite predating vibe coding** — which proves the tells are really about *defaults*, not about AI. Kith (`kith.com`) is also on `Inter,sans-serif`.

**Broken Planet** — custom **Remix** app (not Liquid). **Anton** (condensed display) + **Circular Std Book** + **Panton Rust Heavy** (distressed). Meta description: *"The official home of sustainable streetwear. Limited drops monthly. Oversized fits."* — "Limited drops monthly" is in the `<meta>`, i.e. the drop cadence *is* the positioning.

**Adanola** (`adanola.com`) — British muted athleisure, nearest commercial analogue to OVERTIME's palette. **Bogart** + **Bogart Alt** (display, incl. italic) + **Favorit** (grotesque). `aspect-ratio: 2.4` for wide editorial bands alongside `1.0` product cards. Uses `backdrop-filter: brightness(0.9)` — *brightness, not blur* — as a hover state. Clever, cheap, and it doesn't hurt contrast.

**SSENSE** — **FavoritSSENSE** + **Times Now SemiLight**. Header class is literally `opaque-header`. The reference for grid discipline at scale.

**Nike SNKRS** — the drop-mechanic vocabulary, for reference ([drop-list](https://www.drop-list.com/guides/nike-snkrs-explained/), [Peachy Pings](https://peachypings.com/blog/nike-snkrs-advice-tips-and-guidance)): **LEO** (2-minute randomised entry window, then falls through to FLOW), **DAN** (10–30 min draw window, no queue), **FLOW** (first-come-first-served), **Exclusive Access** (invite-only push offer, time-limited). The `<html>` carries `Neue Frutiger Arabic`. The useful takeaway: *"if there is a timer, it's a DAN release"* — **the presence of a visible timer is itself a signal of the drop type.** That's a semantic you can own outright.

---

## 7. THE "VIBE-CODED" TELLS — lint checklist

Use this as a literal build gate. Anything in **A** or **B** present = fail.

### A. Colour — instant tells
1. Purple→blue / indigo→violet gradients anywhere. The specific Tailwind defaults to ban by hex: `#615fff`, `#8e51ff`, `#4f39f6`, `#7f22fe`, `#0f172b` ([sikora.software](https://sikora.software/blog/ai-website-design)).
2. Any gradient at all on a CTA button.
3. Gradient text (`bg-clip-text`) on headings.
4. Slate/zinc/neutral-900 backgrounds straight out of the box (`#0f172b`, `#18181b`, `#0a0a0a`).
5. A hue on an interactive element that appears nowhere in the garment palette.
6. Coloured glow / `box-shadow` in the accent hue under buttons or cards.
7. `--primary` / `--secondary` / `--accent` as the only colour tokens — no material-derived names.

### B. Typography
8. **Inter** as both heading and body face (see Trapstar, Kith — real brands, still a tell).
9. Any Google-Fonts-top-20 default: Inter, Poppins, Montserrat, Roboto, Open Sans, Lato, Raleway, Nunito, DM Sans, Manrope, Space Grotesk, Plus Jakarta Sans.
10. Default weights only (400/500/600/700) with no 300 or 800+, and no italic.
11. Font sizes all from the Tailwind scale (`text-sm/base/lg/xl/2xl/…`) with no custom `clamp()`.
12. A wide-tracked uppercase eyebrow label above *every* section heading. Real sites use tracked micro-type for **labels on objects** (ALD's `.plp-product__tag`), not as a decorative rhythm.
13. Tracked-out **large** type. ALD tracks `.15em` at 10px and `0` at 92px — never the reverse.
14. Heading + subhead + two buttons, centred, every section.
15. Emoji anywhere in a heading, nav item or button.
16. Curly quotes `""` and em-dashes at machine density in body copy.
17. Straight `-` where a real brand would use a hairline `·` or nothing.

### C. Layout & components
18. Centred hero + one-line headline + "Get Started" / "Learn More" pair.
19. The **Features / Testimonials / FAQ / CTA** section rhythm.
20. A three-up card grid where n is always exactly 3 (or a 2×2), with visually equalised text lengths.
21. Every card at the same radius, same padding, same height — `rounded-2xl p-6` repeated ([925studios](https://www.925studios.co/blog/ai-slop-web-design-guide)).
22. Uniform 8px/16px radii on *everything*. Real sites are `0` (Stüssy) or an extreme pill (Palace's max-int) — rarely a polite in-between, and never both on the same page.
23. Glassmorphism cards in a grid: `bg-white/10 backdrop-blur-md border border-white/20`.
24. Floating blurred gradient orbs / meshes / blobs in a hero background.
25. Lucide/Heroicons line icons inside circular tinted containers, one per feature card.
26. Tailwind default shadows (`shadow-lg`, `shadow-xl`) on a dark background, where they do nothing but grey the edges.
27. `border border-white/10` on every container.
28. Numbered step timelines ("01 / 02 / 03") with a connecting line.
29. A stats band: three big numbers with tiny labels ("10K+ Customers").
30. Symmetric max-width container, every section, no bleed, no crop.
31. `py-24` everywhere — mechanical vertical rhythm with no editorial judgement.
32. A "trusted by" logo strip.
33. Marquee/ticker of words with no information in it.
34. A badge pill above the H1 ("✨ Now in beta").
35. A footer with four equal link columns and a newsletter box in the last one.
36. A sticky bottom CTA bar on mobile that isn't Add-to-Bag.

### D. Motion
37. The same `fade-in-up` on every element as it enters, at the same duration and delay.
38. Stagger delays in tidy 100ms increments.
39. Scroll-progress bar at the top of the page.
40. A custom cursor (dot + trailing ring) with no relationship to the content.
41. 3D tilt-on-hover cards.
42. Count-up number animations.
43. Typewriter text.
44. Parallax on every layer at once.
45. Hover states that change nothing perceptible, and buttons that snap rather than ease ([925studios](https://www.925studios.co/blog/ai-slop-web-design-guide)).
46. No `prefers-reduced-motion` block anywhere.

### E. Imagery & copy
47. Any AI person with plastic skin, symmetrical face, or glassy eyes.
48. Stock people smiling at laptops in bright offices.
49. Abstract 3D blobs/isometric shapes/mesh gradients standing in for photography.
50. Product shown only as flat-lays, never worn, never in a place.
51. Headlines that could belong to any brand ("Elevate your everyday", "Redefining streetwear", "Where style meets comfort").
52. Feature copy in `Title Case Three Words` + one generic sentence.
53. Invented testimonials with statistically common names and job titles.
54. Lorem-flavoured filler in a live section.
55. No real numbers, no real dates, no real place names anywhere on the page.

### F. Code-level
56. `class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900"`.
57. Component names like `FeatureCard`, `TestimonialSection`, `HeroSection`, `CTASection`.
58. Default `<title>` patterns: "Brand — Premium Streetwear | Shop Now".
59. Identical `alt` text on every image, or `alt=""` on content images.
60. No favicon, or an emoji favicon.
61. A `README.md` tone leaking into UI microcopy.

---

## 8. THE COUNTER-MOVES — what these sites do instead

Each one is evidenced above.

1. **Let the photograph be the page.** Fear of God's homepage is three heroes and a footer. Stüssy's is one section. The UI chrome is the thinnest possible layer over the image.
2. **Make the nav adapt rather than blur.** Represent's `data-style="dark|light|light-solid"` recolours the bar per section. Cole Buxton's `transparent="not-sticky" sticky="scroll-up"` makes it disappear going down and return going up.
3. **Cap the nav at five words.** Palace: Web Shop · Shops · Advice · Cart · Menu. Depth goes behind a single opener.
4. **Break the container.** ALD runs `aspect-ratio: 69/50` — a ratio with no round number in it, derived from a crop, not a token. Adanola runs `2.4` editorial bands against `1.0` cards. Crop into the garment; let images bleed off the edge.
5. **Two type registers, three weights.** FOG: Helvetica Neue Condensed + Optima. Sporty & Rich: Jost + Big Caslon + Industrial 736 Italic. Cole Buxton: Akkurat Light + Akkurat Bold, nothing between.
6. **Invert the tracking.** Tight/none at display size, `.1em–.15em` uppercase at 8–12px on labels attached to objects.
7. **Square or pill, commit.** Stüssy is `border-radius: 0`. Palace is max-int. Pick a pole.
8. **Colour comes from the goods.** Corteiz's site is literally `#ffd500` on black because that's the brand. Not one of these sites has an accent colour that isn't in the product or the logo.
9. **Motion is video, carousels and reveals — not a library.** Across eleven sites I found **no GSAP, no Lenis, no Locomotive, no Framer Motion, no three.js** referenced in the delivered HTML/CSS. What's actually there: Swiper, IntersectionObserver, `animation-timeline` (native CSS scroll-driven), Barba page transitions, and autoplaying muted loops. *(Caveat: hashed app bundles not fully audited — absence of reference, not proof of absence.)*
10. **Mobile and desktop get different footage.** Represent does it in one `<video>` with `media="(orientation: portrait)"`. ALD and Gymshark ship two elements and two files. Nobody letterboxes a 16:9 into a phone.
11. **Always a poster frame, and `preload="none"`.** Gymshark posters everything; Represent uses a 1×1 transparent GIF data-URI to avoid a flash.
12. **Commerce arrives on the third beat.** Cole Buxton: hero → products → hero → products. Sporty & Rich: video hero → editorial → image hero → editorial → collection slider.
13. **Grid ratios are `4/5` or `1/1`, hover reveals the second shot, quick-add on the card.** This is near-universal: Cole Buxton `4/5`, Stüssy `4/5` + `7/5`, Gymshark `4/5`, Palace `1/1`, Corteiz `1/1` + `4/5`.
14. **Ship real states.** `Sold Out`, `Out of Stock`, `Notify Me`, `Back in Stock`, `Pre-Order`, and ALD's `.gated-product`. Sold-out is *designed*, not an error.
15. **One fully specific detail per page** that no template would contain — ALD's `font-variant-numeric: diagonal-fractions` on the size chart, Arc'teryx's downloadable-video fallback link, Cole Buxton's `:has()` guard against the countdown flash.

---

## 9. THE DIRECTION FOR OVERTIME

### The thesis
**Cole Buxton's structural restraint + Aimé Leon Dore's micro-typography + Corteiz's inverted countdown.** Those three, with Palace's floating pill as the nav. That combination is coherent, is differentiated from all of them, and maps exactly onto the assets you already have.

### What lands

**Nav.** Floating centred pill, Palace-style, near-opaque smoked black with a restrained blur and a `@supports` fallback. **Only the OT monogram in the pill** — never the thin wordmark at nav scale. Four labels: `Shop · Drops · World · Cart`. Everything else behind `Menu`. Steal Cole Buxton's `sticky="scroll-up"` so it retreats on scroll-down. Steal Represent's `data-style` so it inverts to black-on-bone over the cream/sand sections.

**The countdown is the site's signature, and it must be honest.** Corteiz's model beats a launch timer: count down to **the drop closing**, not opening. Copy from the brand's own slogans — `TIME WON'T WAIT` above `03 : 14 : 22 : 09`, legends `DAYS HOURS MINS SECS` in 10px at `.15em` (ALD's label spec), digits large and untracked. Implement Cole Buxton's three refinements verbatim: `:has()` visibility guard against the zero-flash, `onceItEnds` swapping in-place to a live link, `data-timezone="store"` so it's one global moment. Make it **content-managed** like Gymshark's, never hardcoded. And borrow Represent's *second*, unhyped use of a timer: an order-by cutoff in the footer or cart. Two timers, two registers — that's what stops it reading as a gimmick.

**Typography.** The heavy italic OT monogram is your display voice; do **not** set headlines in the thin wide wordmark. Concretely:
- **Display/headline:** a condensed or wide grotesque at 44–92px, **zero tracking**, uppercase. ALD's ceiling is 5.75rem — resist 20vw.
- **The wordmark treatment (`O V E R T I M E` at `.3em`+)** appears **exactly twice**: the footer lockup and the loading/intro state. Nowhere else. Its scarcity is what makes it read as a mark rather than a style.
- **Micro-labels** — "EST. 2026", drop names, sold-out tags, sizes, filters — 10px uppercase at `.15em`. This is where the wide-tracked look actually belongs, and it will make the whole site read as art-directed.
- **Body:** a real grotesque, not Inter. Favorit (SSENSE, Adanola), Akkurat (Cole Buxton) and Söhne (ALD) are the three proven in this exact register. Two faces, three weights, one italic. Stop.

**Colour.** Your palette is already the discipline. Near-black `#0A0A0A`, bone `#EDE8DF`, navy, washed denim, sand, washed grey. **One accent only**, and it must come off a garment — the washed denim-blue is the right one. Nothing saturated, no gradients, and a countdown that is white-on-near-black, not red-alert.

**Motion.** Follow the category: no animation library. Autoplaying muted loops, IntersectionObserver reveals at ~600ms with real easing (not 100ms staggers), CSS `animation-timeline` for scroll-linked crops, and a `prefers-reduced-motion` block that actually works. The single luxury: a slow, near-still hero loop — fabric moving in wind, dust in light — that reads as a photograph that happens to breathe.

**AI video hero — the exact technique.** Shoot two crops per asset, 16:9 and 9:16, and serve them with Represent's `<source media="(orientation: portrait)">` in one `<video>`. Always a poster JPEG (Gymshark), `preload="none"`, `muted playsinline loop autoplay`, H.264 MP4 ~4–7 Mbps with a WebM alternate. **Don't ship `.mov`** (Sporty & Rich's mistake).

**Models.** Non-negotiable — the category shows garments worn, on a person, in a place. Flat-lays are for the grid, not the hero. Art-direct against the tells: no symmetrical faces, no glassy eyes, no plastic skin, no smiling-at-camera. Motion-blurred, cropped at the jaw, backs turned, mid-stride, overcast light — which conveniently is both the brand's register *and* the failure mode AI image models handle best.

**Hourglass and clock.** Use them **as print on garments and as full-bleed editorial texture** — the distressed engraving at 1600px bleeding off a section edge, tonally flattened into the near-black. That's an art-directed asset. The moment they become UI — a clock icon in a button, an hourglass as a loading spinner — they become the cliché.

**3D.** Blender is overkill and he's right. The one thing genuinely worth 3D is a **single slow hero object**: the hourglass, matte, in the brand's light, sand falling in real time. Even that is better done as a rendered loop than a live WebGL canvas (which drags mobile and adds a library you'd otherwise avoid). If you want depth, get it from **video parallax and cropped photography**, not geometry.

### AVOID — cliché list, ranked

1. **A ticking-clock cursor. Yes, too much.** It fails four tells at once (custom cursor, literal metaphor, meaningless motion, desktop-only), it breaks on touch, and it turns the concept into a joke. A real clock motif belongs on a garment, not on the pointer.
2. **A live current-time readout in the header.** Slightly cleverer, still a novelty. It says nothing, and it dates the page every second.
3. **Hourglass loading spinner.** Everyone thinks of it. That's the problem.
4. **Sand-particle canvas background.** Floating-orbs energy wearing a costume.
5. **Second-hand sweep as a scroll-progress indicator.** Scroll bars are on the ban list already; making it a clock doesn't redeem it.
6. **Roman numerals in UI.** They're on the pocket print, which is where they work. `XII` as a section number is fancy-dress.
7. **"OUR TIME" as an H1 over a centred hero with two buttons.** The slogan is strong; the arrangement is the tell. Put it small, tracked, in a corner, over a full-bleed image — the way ALD sets a caption.
8. **Countdown on every product.** One countdown, one drop. Scarcity that's always on isn't scarcity; it's a Shopify app.
9. **An analogue clock face rendered in CSS/SVG as a hero graphic.** It is the single most-generated shape in the "time-themed website" prompt space.
10. **Tessellated OT monogram as the page background.** It's a great *garment* pattern. Behind text it becomes visual noise and destroys contrast. If you must, use it once — inside a single section, at low contrast, cropped hard.
11. **Stretching the thin wordmark to 100vw across the hero.** It's the most obvious move available and it will read as a 2019 template.
12. **Glass everywhere.** One pill and one filter bar. The moment a card gets `backdrop-blur`, you're in tell #23.

### The one-line test to hold every decision against
*Would this exist on the site if the brand had a full-time art director and no AI tools?* Corteiz's yellow 12px Courier passes. A ticking-clock cursor does not.

---

**Sources:** [Corteiz](https://corteiz.com/) · [Represent](https://representclo.com/) · [Aimé Leon Dore](https://www.aimeleondore.com/) · [Stüssy](https://www.stussy.com/) · [Palace](https://shop.palaceskateboards.com/) · [Cole Buxton](https://www.colebuxton.com/) · [Fear of God](https://fearofgod.com/) · [Sporty & Rich](https://sportyandrich.com/) · [Arc'teryx](https://arcteryx.com/gb/en/) · [Gymshark](https://uk.gymshark.com/) · [Trapstar](https://trapstarlondon.com/) · [Broken Planet](https://brokenplanet.com/) · [Adanola](https://adanola.com/) · [SSENSE](https://www.ssense.com/en-gb) · [Kith](https://kith.com/) · [Reap Agency — Cole Buxton](https://www.reapagency.co.uk/portfolio/colebuxton/) · [Palace drop times](https://www.palacecmty.com/help/drop-times/) · [Hypebeast — Palace drops](https://hypebeast.com/2026/3/palace-skateboards-spring-2026-drop-6-release-info) · [Euronews — Corteiz strategy](https://www.euronews.com/culture/2023/03/17/the-rise-of-corteiz-inside-the-genius-marketing-strategies-of-londons-hottest-streetwear-b) · [LOVE Creative — Corteiz](https://www.lovecreative.com/blog/3x-ways-corteiz-is-breaking-all-the-rules) · [SNKRS explained](https://www.drop-list.com/guides/nike-snkrs-explained/) · [Peachy Pings — SNKRS](https://peachypings.com/blog/nike-snkrs-advice-tips-and-guidance) · [CSS-Tricks — Liquid Glass](https://css-tricks.com/getting-clarity-on-apples-liquid-glass/) · [ekino — Liquid Glass in CSS/SVG](https://medium.com/ekino-france/liquid-glass-in-css-and-svg-839985fcb88d) · [w3c/svgwg #1142](https://github.com/w3c/svgwg/issues/1142) · [925studios — AI slop web design](https://www.925studios.co/blog/ai-slop-web-design-guide) · [sikora.software — 10 signs](https://sikora.software/blog/ai-website-design) · [By Association Only — menswear on Shopify](https://www.byassociationonly.com/articles/nine-memorable-mens-fashion-brands-on-shopify) · [Envato — 2026 trends](https://elements.envato.com/learn/web-design-trends)