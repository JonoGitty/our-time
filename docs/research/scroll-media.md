# OVERTIME — Scroll-Driven Media on the Web, 2026
## Definitive technical brief

---

## 0. THE VERDICT (read this, then the evidence)

**Ship a canvas-drawn image sequence for the one hero moment. Ship native CSS scroll-driven animations behind `@supports` for everything else. Do not ship a scroll-scrubbed `<video>`. Do not ship Three.js.**

Concretely for OVERTIME:
- **1 hero sequence**: 100–140 WebP frames, canvas-drawn, ~1.6 MB mobile / ~4.5 MB desktop, deferred until after LCP. This is the hourglass-sand or clock-sweep moment.
- **Everything else**: `animation-timeline: view()` for reveals/parallax (progressive enhancement), IntersectionObserver as the universal fallback. Zero JS animation library needed for 80% of the site.
- **GSAP ScrollTrigger (27.4 KB gz)** only if you need *pinning* — sticky sections with a scrubbed timeline. That is one dependency and it is now genuinely free.
- **3D flair**: depth-map parallax in ~60 lines of raw WebGL. Not Three.js (185 KB gz), not R3F (52 KB gz + three + React).
- **Budget**: ≤ 2.5 MB total on mobile at first interaction; hero sequence loads *after* `load`.

The single most important structural decision: **a `<canvas>` is not an LCP candidate element** ([web.dev/articles/lcp](https://web.dev/articles/lcp)). Your hero must be a real `<img>` (frame 1, `fetchpriority="high"`) sitting behind the canvas, or your LCP resolves to random nav text and you lose control of the metric entirely.

---

## 1. THE CORE DECISION — scrubbed video vs image sequence

### What top-tier sites actually ship

Apple's product pages use **canvas + pre-extracted image frames**, not video. The technique is a flipbook: scroll position → frame index → `drawImage()`. There is no decoder in the loop, no seek queue, no device-to-device variance. ([CSS-Tricks walkthrough of the AirPods Pro page](https://css-tricks.com/lets-make-one-of-those-fancy-scrolling-animations-used-on-apple-product-pages/), [GSAP Vault](https://gsapvault.com/blog/scroll-image-sequence-tutorial))

> **UNVERIFIED (2026 currency):** I verified the *technique* is canvas-image-sequence from multiple teardowns and tutorials, but I did not fetch and inspect a live 2026 apple.com product page in this session. Treat "Apple still does this in 2026" as high-confidence-by-consensus, not primary-source-verified. The exact frame count (~147 for AirPods Pro) is widely quoted but unverified here.

### Honest engineering comparison

| Axis | Scrubbed `<video>` (`currentTime`) | Image sequence → canvas | WebCodecs `VideoDecoder` |
|---|---|---|---|
| **Seek latency** | 10–120 ms per seek, wildly device-dependent. Seeks *queue*; a flick scroll piles up seeks and the element visibly lags the finger. | ~0 ms. `drawImage` of a decoded bitmap is a GPU blit. Locked to the finger because there is literally nothing in between. | ~1–8 ms if the frame is in your decoded ring buffer; 30–100 ms on a cold seek (must decode from prior keyframe). |
| **Keyframe dependence** | Total. GOP 100 = unusable. GOP 5 = acceptable on Chrome/Safari, still janky on Firefox (needs ~GOP 2). GOP 1 (all-intra) works everywhere but the bytes approach the image-sequence bytes anyway. ([muffinman.io](https://muffinman.io/blog/scrubbing-videos-using-javascript/)) | None. Every frame is independent by construction. | You control it — decode forward from a keyframe yourself and cache. |
| **iOS Safari** | The worst target. Safari's seek machinery recreates delta frames but coalesces/drops seeks under load. Low Power Mode additionally injects a play-button overlay on autoplay video. Historically iOS refuses `webm`; Firefox is choppy with `mp4` — so you ship both. | Identical behaviour to every other browser. No platform-specific code. | Safari 26+ only (Sept 2025). Anything older = no WebCodecs. |
| **Decode cost (mid-range Android)** | High and *sustained* — the hardware decoder is being asked to random-access 60×/sec. Thermal throttling is real on a Snapdragon 6-series. | One decode per *unique* frame shown, and you can skip frames freely. Cheapest steady-state option. | Similar to video but you own the scheduling, so you can throttle. |
| **Peak memory** | Low — the decoder holds a few frames. This is video's one real win. | **The main hazard.** A decoded RGBA frame is `W × H × 4` bytes. 1440×810 = **4.45 MiB *per frame***. 120 frames fully decoded = **534 MiB**. You must use a sliding window. | Also a hazard: `VideoFrame` objects hold GPU memory and leak unless you call `.close()` on every one. |
| **Total bytes** | All-intra H.264 CRF 20 @1440×810 ≈ 60–100 KB/frame → **7–12 MB** for 120 frames (worse than WebP). GOP-5 CRF 22 ≈ **2–3 MB** (better, but janky). | WebP q72 @1440-wide, desaturated/washed content ≈ **30–45 KB/frame** → **3.6–5.4 MB**. Mobile @828-wide ≈ 16–20 KB/frame → **~1.8 MB**. | Same file as video (~2–3 MB at GOP 5, since you decode forward yourself and don't need short GOP). **Smallest payload of the three.** |
| **Cacheability** | One URL, one immutable cache entry, one range-request dance. Trivially CDN-cached. | 120 URLs. Needs HTTP/2 or HTTP/3 (any modern CDN — Cloudflare, Netlify, Vercel, Shopify's CDN — gives you this free). On HTTP/1.1 it is a disaster: 6-connection limit, 20 round trips. | One URL. Best of both. |
| **Ship it?** | **No.** | **Yes — default choice.** | **Only as a progressive upgrade.** Baseline "limited": Chrome 94, Firefox 130, **Safari 26 (2025-09-15)** ([webstatus.dev](https://api.webstatus.dev/v1/features/webcodecs)). You'd still need the image-sequence fallback, so you'd be shipping two pipelines. Not worth it for a clothing brand. |

### The decisive argument

Video's only advantage is peak memory. Image sequence's advantage is *determinism* — it behaves identically on a Pixel 9 and a £150 Moto G. For a premium fashion brand, the failure mode of video ("it stutters on some phones") is exactly the failure mode you are paying a designer to avoid. The whole point of "un-vibe-coded" is that it doesn't feel cheap on the device the customer actually holds.

**If you take one thing from section 1:** the byte gap between all-intra video and a WebP sequence is roughly zero, and the sequence wins on every other axis.

---

## 2. IF YOU GO VIDEO ANYWAY — the encoding rules

Use this for *ambient, forward-playing* video (lookbook b-roll, a model walking, fabric moving). It is the right tool for that. It is the wrong tool for scrubbing. Both configs below are given.

### 2a. Codec choice, 2026

- **H.264 High profile, `yuv420p`** — the only universally safe choice. "Baseline profile" is a 2010 concern; every device that runs a 2026 browser decodes High@L4.0 in hardware. Use High.
- **HEVC** — Safari yes, Chrome hardware-only and patchy. Not worth the second encode.
- **AV1** — **do not rely on it.** Safari 17+ supports it, *but only on devices with a hardware AV1 decoder*: M3+ Macs, M4 iPad Pro, iPhone 15 Pro family, iPhone 16 family. Apple ships **no system software decoder**, so an iPhone 14 running Safari 17 simply cannot play your AV1 file. ([Bitmovin](https://bitmovin.com/blog/apple-av1-support/), [Bitmovin AV1 state](https://bitmovin.com/blog/av1-playback-support/)) AV1 is a bandwidth optimisation for a `<source>` list, never a sole encode.
- **VP9/WebM** — only as the Firefox-friendly second source if you insist on scrubbing.

### 2b. Autoplay policy — the exact WebKit rules

From [WebKit's own post](https://webkit.org/blog/6784/new-video-policies-for-ios/), quoted:

- `"<video> elements will be allowed to autoplay without a user gesture if their source media contains no audio tracks."`
- `"<video muted> elements will also be allowed to autoplay without a user gesture."`
- `"If a <video> element gains an audio track or becomes un-muted without a user gesture, playback will pause."`
- `"<video autoplay> elements will only begin playing when visible on-screen such as when they are scrolled into the viewport"`
- `"<video> elements will be allowed to play() when not visible on-screen or when out of the viewport."` (i.e. `play()` is *less* restricted than the `autoplay` attribute)

**Practical rule:** strip the audio track entirely (`-an`). That is stronger than `muted` — a file with no audio track can never "gain an audio track", so it can never be paused by that rule.

`playsinline` is **not** an autoplay condition — it stops iPhone from going fullscreen. You still need it, always.

**Low Power Mode** is the one that will bite you and is *not* in the WebKit post: iOS in Low Power Mode shows a play-button overlay on autoplaying video, and Safari 16.4+ on macOS blocks muted autoplay when Low Power Mode is on battery. ([SiteLint](https://www.sitelint.com/blog/fixing-html-video-autoplay-blank-poster-first-frame-and-improving-performance-in-safari-and-ios-devices), [Apple dev forums](https://developer.apple.com/forums/thread/727855)) Always set a `poster` that is a real designed frame, because a meaningful share of users will only ever see the poster.

```html
<video
  playsinline
  muted
  autoplay
  loop
  preload="metadata"
  poster="/media/lookbook-poster.avif"
  disablepictureinpicture
  disableremoteplayback>
  <source src="/media/lookbook.mp4" type="video/mp4; codecs=avc1.640028">
</video>
```

`preload` rules: `"none"` for anything below the fold; `"metadata"` for the hero (gets you dimensions + seekability without the bytes); `"auto"` **only** if you are scrubbing and the file is small, because `auto` on mobile competes with your LCP image for bandwidth.

### 2c. ffmpeg — scrub-viable encodes

**All-intra (GOP 1) — every frame is a keyframe, seeking is instant:**
```bash
ffmpeg -i in.mov -an \
  -vf "fps=30,scale=1440:-2:flags=lanczos,format=yuv420p" \
  -c:v libx264 -profile:v high -level:v 4.0 \
  -x264-params "keyint=1:min-keyint=1:scenecut=0:bframes=0:ref=1" \
  -crf 20 -preset slow \
  -movflags +faststart \
  out_allintra.mp4
```

**GOP 5 — the practical compromise (Chrome/Safari smooth, Firefox marginal):**
```bash
ffmpeg -i in.mov -an \
  -vf "fps=30,scale=1440:-2:flags=lanczos,format=yuv420p" \
  -c:v libx264 -profile:v high -level:v 4.0 \
  -x264-params "keyint=5:min-keyint=5:scenecut=0:bframes=0:ref=1" \
  -crf 22 -preset slow \
  -movflags +faststart \
  out_gop5.mp4
```

**GOP 2 WebM for Firefox** (Firefox needs roughly double the keyframe density of Chrome/Safari — [muffinman.io](https://muffinman.io/blog/scrubbing-videos-using-javascript/)):
```bash
ffmpeg -i in.mov -an \
  -vf "fps=30,scale=1440:-2:flags=lanczos" \
  -c:v libvpx-vp9 -g 2 -crf 30 -b:v 0 -row-mt 1 -deadline good -cpu-used 2 \
  out_gop2.webm
```

**Ambient forward-play encode (NOT for scrubbing) — this is what you actually want for lookbook b-roll:**
```bash
ffmpeg -i in.mov -an \
  -vf "fps=25,scale=1280:-2:flags=lanczos,format=yuv420p" \
  -c:v libx264 -profile:v high -level:v 4.0 -g 50 -keyint_min 50 -sc_threshold 0 \
  -crf 26 -preset slower -tune film \
  -movflags +faststart \
  out_ambient.mp4
# + an AV1 alternate for the devices that can take it:
ffmpeg -i in.mov -an -vf "fps=25,scale=1280:-2,format=yuv420p" \
  -c:v libsvtav1 -crf 34 -preset 5 -svtav1-params "keyint=50" out_ambient.av1.mp4
```

`-bframes 0` and `-ref 1` matter more than people think for scrubbing: B-frames force out-of-order decode, which turns a seek into a multi-frame reconstruction.

### 2d. Fragmented MP4 — correcting a common myth

**For a plain `<video>` element being scrubbed, you do NOT want fragmented MP4.** You want a *normal* MP4 with `-movflags +faststart`, which moves the `moov` atom (containing the `stts`/`stss` sample tables, i.e. the frame index) to the front. That index is what makes `currentTime = x` land on the right byte range on the first try.

Fragmented MP4 (`-movflags +frag_keyframe+empty_moov+default_base_is_moof`) is for **MSE and WebCodecs pipelines**, where *you* demux. In that context it is correct and necessary:
```bash
ffmpeg -i in.mov -an -c:v libx264 -profile:v high -x264-params "keyint=30:scenecut=0" \
  -crf 22 -movflags +frag_keyframe+empty_moov+default_base_is_moof \
  out_fragmented.mp4
```

Additional real-world trick for scrubbing: **fetch the whole file as a Blob and set `video.src = URL.createObjectURL(blob)`**. A blob URL is fully seekable with zero network round-trips per seek. Range requests over the network during a flick scroll are what actually kills mobile scrubbing.

### 2e. Why `requestVideoFrameCallback` matters

`rVFC` fires **when a new frame has actually been composited**, giving you `mediaTime` (the true presented timestamp) and `presentedFrames`. Without it you are guessing: `timeupdate` fires at ~4 Hz, and `seeked` lies about compositing.

The concrete use is **seek coalescing** — never issue a second seek until the first has visibly landed:

```js
const v = document.querySelector('video');
let target = 0, seeking = false, rafQueued = false;

function onScroll() {
  target = progress() * v.duration;
  if (!rafQueued) { rafQueued = true; requestAnimationFrame(pump); }
}

function pump() {
  rafQueued = false;
  if (seeking) return;                       // drop, don't queue
  if (Math.abs(v.currentTime - target) < 1 / 30) return;
  seeking = true;
  v.currentTime = target;
  v.requestVideoFrameCallback(() => { seeking = false; if (Math.abs(v.currentTime - target) > 1/30) onScroll(); });
}
addEventListener('scroll', onScroll, { passive: true });
```

**Support (verified, [web-platform-dx explorer](https://web-platform-dx.github.io/web-features-explorer/features/request-video-frame-callback/)):** Baseline *newly available* since **2024-10-29**. Chrome 83, Chrome Android 83, Edge 83, Firefox 132, Safari 15.4, **Safari iOS 15.4**. Reaches *widely available* 2027-04-29. Safe to use with a `timeupdate`/`rAF` fallback. Note it is intentionally non-functional under DRM playback (irrelevant here).

---

## 3. IMAGE SEQUENCE — the recommended route, in full

### 3a. Frame count vs scroll distance

The relation you tune is **pixels of scroll per frame**:

- **Desktop:** 8–14 px/frame feels premium. Below 6 and the sequence rushes; above 20 and it feels like it's fighting you.
- **Mobile:** 6–10 px/frame (thumb flicks cover more distance faster).

Work backwards from the pin length you want:

```
runway_px   = (pin_multiplier − 1) × viewport_height
frame_count = runway_px / px_per_frame
```

Worked example, 250vh pinned section on a 900px-tall desktop viewport:
```
runway   = 1.5 × 900 = 1350 px
frames   = 1350 / 11 ≈ 123 frames
```
**100–140 frames is the working range.** Do not exceed 160 — bytes and memory both go superlinear against a benefit nobody perceives.

Critically: at a hard flick (~2500 px/s) with 11 px/frame you are traversing ~227 frames/sec. You cannot decode that. **Your loop must skip frames, never queue them** (see 3d).

### 3b. Format and sizing

**Use WebP.** Not AVIF, despite AVIF being Baseline *widely available* since Safari 16.4 ([webstatus.dev](https://api.webstatus.dev/v1/features/avif)). Reason: AVIF decode is roughly **5–10× slower than JPEG** and measurably slower than WebP ([crystallize](https://crystallize.com/blog/avif-vs-webp), [pixotter](https://pixotter.com/blog/webp-vs-avif/)). Decode speed is irrelevant for a single hero image and *is the entire bottleneck* for 120 sequential decodes on a mid-range Android. AVIF also encodes 14–47× slower than WebP, which makes your build pipeline miserable.

**AVIF is still correct for your static product photography and lookbook stills.** Just not for the sequence.

**Three responsive tiers** (`srcset`-equivalent, selected in JS from `devicePixelRatio` and viewport):

| Tier | Frame size (4:5 portrait) | WebP q72, washed/desaturated | 120 frames |
|---|---|---|---|
| Mobile | 828 × 1035 | ~16–20 KB | **~2.2 MB** |
| Mobile-lite (Save-Data / 3G) | 540 × 675 | ~8–11 KB | ~1.2 MB |
| Desktop | 1440 × 1800 | ~38–50 KB | **~5.3 MB** |

> These KB figures are estimates for *your* content class (muted, low-saturation, near-black backgrounds — which compresses unusually well). **UNVERIFIED — measure your actual frames before committing to a budget.**

**Hard budgets:**
- Mobile hero sequence: **≤ 2.5 MB**, fetched *after* `load`, never before LCP.
- Desktop hero sequence: **≤ 6 MB**.
- Total page weight at first interaction on mobile: **≤ 1.5 MB** (sequence excluded, because it's deferred).
- **One sequence per page. Two is self-indulgent and you will feel it on a Moto G.**

### 3c. ffmpeg — producing the sequence

**From a render or video source → PNG → WebP (best quality control):**
```bash
mkdir -p png webp

# 1. Extract frames, scale with lanczos, no frame duplication/drop
ffmpeg -i source.mov \
  -vf "fps=30,scale=1440:-2:flags=lanczos" \
  -vsync 0 \
  png/%04d.png

# 2. Encode to WebP with sharp chroma (matters for the OT monogram edges)
for f in png/*.png; do
  cwebp -q 72 -m 6 -sharp_yuv -mt "$f" -o "webp/$(basename "${f%.png}").webp"
done
```

**Single-pass ffmpeg WebP (faster, slightly worse):**
```bash
ffmpeg -i source.mov \
  -vf "fps=30,scale=1440:-2:flags=lanczos" \
  -vsync 0 -c:v libwebp -lossless 0 -q:v 72 -compression_level 6 -preset picture \
  webp/%04d.webp
```

**Generate all three responsive tiers in one pass:**
```bash
ffmpeg -i source.mov -vsync 0 \
  -filter_complex "[0:v]fps=30,split=3[a][b][c]; \
                   [a]scale=1440:-2:flags=lanczos[d]; \
                   [b]scale=828:-2:flags=lanczos[m]; \
                   [c]scale=540:-2:flags=lanczos[s]" \
  -map "[d]" png_1440/%04d.png \
  -map "[m]" png_828/%04d.png \
  -map "[s]" png_540/%04d.png
```

**Sprite-atlas variant** (cuts 120 requests to 12; one decode serves 10 frames):
```bash
# 10 frames per atlas, 2 cols × 5 rows, mobile tier
ffmpeg -i source.mov -vf "fps=30,scale=414:-2:flags=lanczos,tile=2x5" -vsync 0 atlas_%03d.png
for f in atlas_*.png; do cwebp -q 74 -m 6 -sharp_yuv "$f" -o "${f%.png}.webp"; done
```
Then `drawImage(atlas, sx, sy, sw, sh, 0, 0, w, h)`. **Caveat:** keep any atlas under **4096 × 4096** — iOS Safari subsamples images above roughly 16.7 Mpx and canvas area limits bite there too. Atlases also pin their decoded memory for the whole batch, so they trade request count against peak RAM. Use them for the mobile tier where the per-frame pixels are small; use individual files for desktop.

### 3d. The canvas draw loop (production-grade)

This is the part everyone gets wrong. Three non-negotiable rules:

1. **Never queue draws.** Coalesce to one `rAF`, always draw the *latest* target.
2. **Never hold all frames decoded.** Sliding window of `ImageBitmap`s with explicit `.close()`.
3. **Decode off the main thread.** `createImageBitmap(blob)` decodes off-thread and returns a GPU-ready handle; `new Image()` + `onload` does not reliably.

```js
// ───────────────────────────────────────────────────────────
// OVERTIME — scroll-driven frame sequence
// ───────────────────────────────────────────────────────────
const TOTAL   = 123;
const WINDOW  = 16;          // ±16 frames held decoded (see memory math below)
const CONCURRENCY = 6;

const dpr   = Math.min(devicePixelRatio || 1, 2);   // cap at 2; 3x is wasted bytes
const tier  = innerWidth * dpr > 1100 ? 1440 : (navigator.connection?.saveData ? 540 : 828);
const url   = i => `/seq/${tier}/${String(i + 1).padStart(4, '0')}.webp`;

const canvas = document.getElementById('seq');
const ctx    = canvas.getContext('2d', { alpha: false, desynchronized: true });

const cache   = new Map();   // index -> ImageBitmap
const inflight = new Set();
let drawn = -1, target = 0, queued = false;

// ── sizing (CLS-safe: the element already has aspect-ratio in CSS) ──
function resize() {
  const r = canvas.getBoundingClientRect();
  canvas.width  = Math.round(r.width  * dpr);
  canvas.height = Math.round(r.height * dpr);
  drawn = -1;                 // force a repaint at the new size
  schedule();
}

// ── decode ──
async function load(i) {
  if (cache.has(i) || inflight.has(i) || i < 0 || i >= TOTAL) return;
  if (inflight.size >= CONCURRENCY) return;
  inflight.add(i);
  try {
    const res  = await fetch(url(i), { priority: i === target ? 'high' : 'low' });
    const bmp  = await createImageBitmap(await res.blob());
    cache.set(i, bmp);
    if (i === target) schedule();
  } catch { /* a dropped frame is not a crash */ }
  finally { inflight.delete(i); evict(); pump(); }
}

function evict() {
  for (const [i, bmp] of cache) {
    if (Math.abs(i - target) > WINDOW) { bmp.close(); cache.delete(i); }
  }
}

// Fetch outward from the current frame, forward-biased (scroll usually goes down)
function pump() {
  for (let d = 0; d <= WINDOW; d++) {
    for (const i of (d === 0 ? [target] : [target + d, target - d])) {
      if (i >= 0 && i < TOTAL && !cache.has(i) && !inflight.has(i)) {
        if (inflight.size < CONCURRENCY) load(i); else return;
      }
    }
  }
}

// ── draw: cover-fit, nearest available frame, never blank ──
function nearest(i) {
  if (cache.has(i)) return i;
  for (let d = 1; d <= WINDOW; d++) {
    if (cache.has(i - d)) return i - d;
    if (cache.has(i + d)) return i + d;
  }
  return -1;
}

function draw() {
  queued = false;
  const i = nearest(target);
  if (i < 0 || i === drawn) return;
  const b = cache.get(i);
  const s = Math.max(canvas.width / b.width, canvas.height / b.height);
  const w = b.width * s, h = b.height * s;
  ctx.drawImage(b, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h);
  drawn = i;
}

function schedule() { if (!queued) { queued = true; requestAnimationFrame(draw); } }

// ── scroll driver ──
const section = document.getElementById('seq-section');
function onScroll() {
  const r = section.getBoundingClientRect();
  const p = Math.min(1, Math.max(0, -r.top / (r.height - innerHeight)));
  const next = Math.min(TOTAL - 1, Math.round(p * (TOTAL - 1)));
  if (next !== target) { target = next; pump(); evict(); schedule(); }
}

// ── boot ──
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
function start() {
  resize();
  addEventListener('resize', debounce(resize, 150), { passive: true });
  if (reduced.matches) { target = Math.floor(TOTAL * 0.62); load(target); return; }  // one hero frame, no motion
  addEventListener('scroll', onScroll, { passive: true });
  pump(); onScroll();
}
// Defer past LCP — the <img> behind the canvas is the LCP element
addEventListener('load', () => requestIdleCallback ? requestIdleCallback(start, { timeout: 1200 }) : setTimeout(start, 300));

function debounce(fn, ms) { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; }
```

```html
<section id="seq-section" style="height:250vh">
  <div style="position:sticky;top:0;height:100vh;overflow:hidden">
    <!-- LCP element. Canvas is NOT an LCP candidate — this img is. -->
    <img src="/seq/828/0001.webp" alt="" fetchpriority="high" decoding="sync"
         style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
    <canvas id="seq" style="position:absolute;inset:0;width:100%;height:100%"></canvas>
  </div>
</section>
<link rel="preload" as="image" href="/seq/828/0001.webp" fetchpriority="high">
```

### 3e. Memory math — the number that decides `WINDOW`

Decoded RGBA = `W × H × 4`.

| Tier | Per-frame decoded | WINDOW=16 (33 frames held) | WINDOW=24 (49 frames) |
|---|---|---|---|
| 540 × 675 | 1.39 MiB | 45 MiB | 68 MiB |
| 828 × 1035 | **3.27 MiB** | **108 MiB** | 160 MiB |
| 1440 × 1800 | 9.89 MiB | 326 MiB ⚠️ | 485 MiB ☠️ |

A Chrome renderer process on a 4 GB Android gets into memory pressure well before 300 MiB. **Therefore: `WINDOW` must scale inversely with tier.** Use `WINDOW = 16` at 828, `WINDOW = 8` at 1440, `WINDOW = 24` at 540. Or better — downscale at decode time:

```js
const bmp = await createImageBitmap(blob, {
  resizeWidth: canvas.width, resizeQuality: 'high'
});
```
This caps decoded memory at *display* size regardless of source tier, and is the single highest-leverage line in the whole implementation.

### 3f. Progressive / low-res-first

Ship a **12-frame "proxy" sequence at 320px wide (~3 KB/frame, 36 KB total)** that loads immediately and gives you a coarse but *instantly responsive* scrub. Swap to full tier per-frame as each arrives. `nearest()` above already gives you graceful degradation; the proxy just guarantees `nearest()` never returns −1.

---

## 4. NATIVE CSS SCROLL-DRIVEN ANIMATIONS — verified support

**This is the section you asked me not to guess on. Here is primary-source data.**

### Verified status (September 2026)

From **[webstatus.dev API, `scroll-driven-animations`](https://api.webstatus.dev/v1/features/scroll-driven-animations)** (raw response):
```json
{
  "baseline": { "status": "limited" },
  "browser_implementations": {
    "chrome":  { "version": "115", "date": "2023-07-18", "status": "available" },
    "edge":    { "version": "115", "date": "2023-07-21", "status": "available" },
    "firefox": { "version": null,  "date": null,         "status": null },
    "safari":  { "version": "26",  "date": "2025-09-15", "status": "available" }
  }
}
```

From **[MDN's Experimental Features page](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Experimental_features)** (Firefox detail):

| Property | Value |
|---|---|
| Preference | `layout.css.scroll-driven-animations.enabled` |
| Enabled by default | **Yes (Nightly 136+); No in Developer Edition, Beta, and Release** |
| Not yet implemented | `animation-range-start`, `animation-range-end`, `animation-range` shorthand ([Firefox bug 1676779](https://bugzil.la/1676779)) |

**Interop 2026** names scroll-driven animations (`animation-timeline`, `scroll-timeline`, `view-timeline`) as an official focus area, agreed by Apple, Google, Microsoft and Mozilla on 12 Feb 2026. ([WebKit](https://webkit.org/blog/17818/announcing-interop-2026/), [Mozilla Hacks](https://hacks.mozilla.org/2026/02/launching-interop-2026/), [Igalia](https://www.igalia.com/news/interop-2026.html))

### The verdict, stated precisely

- **NOT Chrome-only.** It shipped in **Safari 26 (Sept 2025)**, which is a genuinely large change from the 2024 situation. Chrome + Edge + Safari + Opera is the large majority of a UK fashion audience.
- **NOT Baseline**, and will not be until Firefox flips the pref in Release. It is `baseline: "limited"`.
- Even where supported, **`animation-range` is missing in Firefox** even behind the flag, so `view()` with custom ranges (`entry 0% cover 50%` etc.) is not portable there.

> **Blog claims I could NOT verify and which you should treat as UNVERIFIED:** that it is specifically Firefox 152 that still has it flagged; the "82.58% global support" figure; that Safari 26.4 added threaded scroll-driven animations and 26.5 fixed progress-accuracy bugs. These came from secondary blogs ([buildmvpfast](https://www.buildmvpfast.com/blog/css-scroll-driven-animations-replace-js-2026), [cssawwwards](https://cssawwwards.com/blog/css-scroll-driven-animations-guide-2026)), not from WebKit release notes or Bugzilla. The *shape* of the claim (Firefox flagged in Release, Safari shipped) is confirmed by the two primary sources above.

### Therefore: shippable, as progressive enhancement, today

```css
/* Baseline: visible. Never hide content behind an animation that may not run. */
.reveal { opacity: 1; transform: none; }

@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .reveal {
      opacity: 0;
      transform: translateY(2rem);
      animation: reveal linear both;
      animation-timeline: view();
      animation-range: entry 10% cover 35%;
    }
  }
}
@keyframes reveal { to { opacity: 1; transform: none; } }

/* Named scroll timeline — e.g. the OT monogram rotating with page progress */
@supports (animation-timeline: scroll()) {
  :root { timeline-scope: --page; }
  body  { scroll-timeline: --page block; }
  .ot-mark {
    animation: spin linear both;
    animation-timeline: --page;
  }
}
@keyframes spin { to { rotate: 360deg; } }
```

**Why this matters commercially:** these animations run **on the compositor thread**, off the main thread. An `animation-timeline: view()` reveal costs you approximately zero INP. A JS `IntersectionObserver` + class-toggle costs a style recalc per element. A GSAP scrub costs a main-thread tick per frame. For the ~40 small reveals a fashion site wants, native CSS is not just smaller — it is *categorically* cheaper.

**Fallback for Firefox** (and anything else): one `IntersectionObserver`, ~15 lines, `{ once: true }`. Do not reach for a library for this.

**Do NOT use native CSS scroll-driven animations for the frame sequence.** There is no way to drive `drawImage` from a CSS timeline. The `ScrollTimeline` JS API (`new ScrollTimeline({source, axis})` + `new ViewTimeline(...)`, driving WAAPI `element.animate()`) has the *same* support matrix as the CSS form — Chrome/Edge/Safari 26, Firefox flagged — and does not help you either, since you need a per-frame JS callback regardless.

---

## 5. THE JS ECOSYSTEM — verified sizes and when each is justified

All figures from the **[Bundlephobia size API](https://bundlephobia.com/)**, fetched this session:

| Package | Version | Min | **Min + gzip** | Verdict for OVERTIME |
|---|---|---|---|---|
| `lenis` | 1.3.26 | 18.8 KB | **5.5 KB** | ✅ Justified *only if* you want momentum smoothing. 0 deps. |
| `gsap` (core) | 3.15.0 | 70.6 KB | **27.4 KB** | ✅ Justified for **pinning** and scrubbed timelines. ScrollTrigger is an additional ~11 KB gz (UNVERIFIED — the 27.4 KB figure is core; the npm package total is larger and tree-shakes). |
| `motion` | 13.3.0 | 142.7 KB | **47.7 KB** (full) | ⚠️ Full import is heavy. The `motion/mini` entry (`animate` only) is ~2.5–5 KB gz — **UNVERIFIED, measure it**. Use mini or skip. |
| `three` | 0.186.0 | 736.2 KB | **184.9 KB** | ❌ Not justified. This is ~74× your Lenis budget for an effect you can fake. |
| `@react-three/fiber` | 9.7.0 | 163.4 KB | **51.8 KB** + 10 deps | ❌ And that's *on top of* three (185 KB) *and* React. You'd be shipping ~280 KB gz of JS for parallax. |

### GSAP licensing — VERIFIED

Webflow acquired GreenSock in **October 2024** and made the entire library free in **April 2025**. From [gsap.com/pricing](https://gsap.com/pricing/), quoted verbatim:

> **"GSAP is now 100% free for all users, thanks to Webflow's support."**

All formerly Club-only plugins are included: **ScrollTrigger, ScrollSmoother, SplitText, MorphSVG, DrawSVG, Inertia, GSDevTools, CustomEase**. No membership, no licence key, no auth token, commercial use permitted, and usable **outside Webflow**. ([Webflow announcement](https://webflow.com/updates/gsap-becomes-free))

> **UNVERIFIED:** the specific SPDX licence identifier on the npm package. The npm page returned HTTP 403 to my fetch. Before shipping a commercial storefront, check `node_modules/gsap/LICENSE.md` yourself — it is historically a "GreenSock Standard License", not MIT, and "free" ≠ "open source". This is a 30-second check and worth doing for a client project.

### When each is justified

| Need | Use | Not |
|---|---|---|
| Fade/slide reveals on scroll | `animation-timeline: view()` + IO fallback. **0 KB.** | Any library |
| Parallax on a background layer | `animation-timeline: scroll()` + `translate3d`. **0 KB.** | GSAP |
| **Pinned section with scrubbed timeline** (the hero sequence container) | **GSAP ScrollTrigger.** Pinning is genuinely hard — scrollbar compensation, resize, nested pins, `refresh()` on layout change. This is the one place a library earns 27 KB. | Hand-rolled `position: sticky` maths that breaks on iOS rubber-band |
| Momentum/easing on the page scroll itself | **Lenis, 5.5 KB.** But see the warning below. | GSAP ScrollSmoother (free now, but heavier and more opinionated) |
| React component transitions | `motion/mini`, or plain CSS | `framer-motion` full |
| Real 3D: a garment you can orbit, real lighting, a GLB from Blender | Three.js — and **only** on a dedicated `/3d` route, code-split, desktop-gated | Three.js on the homepage |

### The Lenis warning

Lenis works by hijacking native scroll and lerping a transform. That means:
- It **breaks** `animation-timeline: scroll()` / `view()` unless you're careful, because the browser's real scroll position no longer matches the visual position.
- It adds input latency by design (that's the effect).
- It is a known accessibility irritant: it overrides the user's OS scroll settings, breaks find-in-page scroll position on some platforms, and interacts badly with screen readers.

**Recommendation:** ship the site *without* Lenis first. If the art direction genuinely demands it, add it gated behind `prefers-reduced-motion: no-preference` **and** a desktop media query, and accept that you then commit to GSAP ScrollTrigger (which has `scrollerProxy` integration) rather than native CSS timelines. Mixing Lenis with native scroll timelines is a bug factory.

---

## 6. "3D FLAIR" WITHOUT A 3D ENGINE

Three.js is 185 KB gzipped and ~300–500 ms of parse+init on a mid-range Android before a single pixel. For a clothing brand, you almost certainly want the *look* of depth, not a scene graph.

### Tier 1 — Layered parallax (0 KB, works everywhere)

Export your AI imagery as 3 PNG layers (foreground garment / model / background). Then:

```css
.parallax { perspective: 1px; transform-style: preserve-3d; overflow-y: auto; height: 100vh; }
.layer-bg { transform: translateZ(-2px) scale(3);   }
.layer-md { transform: translateZ(-1px) scale(2);   }
.layer-fg { transform: translateZ(0);               }
```
Pure compositor, zero JS, zero main-thread cost. This is the "CSS perspective parallax" trick and it is *free*. Good enough for 70% of what people mean by "a bit of 3D flair".

### Tier 2 — Depth-map 2.5D parallax (~4 KB of raw WebGL) ⭐ **Recommended**

This is the one that looks genuinely expensive. Take a single AI-generated model shot, produce a monocular depth map, and displace UVs per-pixel. The result is a photo that has real parallax as you scroll or move the pointer.

**Generating the depth map** — [Depth Anything V2](https://arxiv.org/pdf/2406.09414) is the current default for monocular depth estimation:
```bash
# Offline, at build time — bake it once per image, ship the PNG
pip install transformers torch pillow
python - <<'PY'
from transformers import pipeline
from PIL import Image
pipe = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Large-hf")
img = Image.open("model_shot.png").convert("RGB")
d = pipe(img)["depth"]
d.resize(img.size).convert("L").save("model_shot_depth.png")
PY
```
Ship `model_shot_depth.png` as a **greyscale WebP at half resolution** — depth maps are smooth, they compress to ~8–15 KB and half-res is visually indistinguishable after the displacement.

Browser-side pipelines exist too ([depthbake](https://github.com/roukara/depthbake), Depth Studio), but **bake at build time** — you do not want a depth model in a customer's browser.

**The renderer** — no Three.js, just raw WebGL. Fragment shader:

```glsl
precision highp float;
uniform sampler2D uImage;
uniform sampler2D uDepth;
uniform vec2  uOffset;   // from scroll progress and/or pointer, range ≈ ±0.03
uniform float uStrength; // 0.6–1.4; tune per image
varying vec2 vUv;

void main() {
  vec2 uv = vUv;
  // Iterative refinement: each pass re-samples depth at the corrected UV.
  // 6 steps is plenty; 2 looks like a melting hologram.
  for (int i = 0; i < 6; i++) {
    float d = texture2D(uDepth, uv).r;
    uv = vUv + uOffset * uStrength * (d - 0.5);
  }
  gl_FragColor = texture2D(uImage, uv);
}
```

Vertex shader is a two-triangle fullscreen quad. Total: **~60 lines of JS, ~4 KB, no dependency.** Drive `uOffset` from scroll progress and from `pointermove` (desktop only), lerped.

The quality of the effect is entirely determined by the depth map, not the renderer — *"a mediocre photo with an excellent depth map looks good; an excellent photo with a sloppy depth map looks like a melting hologram"* ([Sygnal KB](https://www.sygnal.com/kb/image-25d-parallax-effects)). Budget your effort accordingly: hand-touch the depth maps in Photoshop where the model's silhouette meets the background.

**On mid-range Android:** one fullscreen quad with 2 textures and a 6-iteration loop is trivially 60 fps. This is nothing like shipping a scene graph.

### Tier 3 — Three.js. When it IS justified

Only if you have a *real* GLB with real geometry and real material response — an actual garment turntable, or the OT monogram as a physical metal object with an HDRI environment. Even then:
- Dynamic `import()`, desktop-only, behind an intersection trigger.
- `powerPreference: 'low-power'`, cap DPR at 1.5, cap `setAnimationLoop` to 30 fps when off-viewport, `renderer.dispose()` on unmount.
- **Blender is not overkill for producing the asset** — it is exactly the right tool for rendering the 120-frame hourglass sequence (Cycles/EEVEE, orthographic camera, transparent or matched-black background, render to PNG, run through the ffmpeg pipeline in §3c). Use Blender as an *offline renderer*, not as a reason to ship WebGL. That's the key distinction your cousin is missing: Blender produces the frames; the browser just flips them.

---

## 7. PERFORMANCE AND MOBILE REALITY

### Core Web Vitals — verified thresholds ([web.dev/articles/vitals](https://web.dev/articles/vitals))

| Metric | Good | Measured at |
|---|---|---|
| **LCP** | ≤ **2.5 s** | 75th percentile of page loads, split mobile/desktop |
| **INP** | ≤ **200 ms** | same |
| **CLS** | ≤ **0.1** | same |

INP replaced FID as a stable Core Web Vital in **2024**.

### What each effect does to each metric

**LCP**
- The killer: `<canvas>` is **not an LCP candidate**. Video *is* (poster load time or first-frame presentation, whichever is earlier). `<img>` is. Background `url()` is. Block-level text is.
- ⇒ Put a real `<img>` of frame 1 behind the canvas, `fetchpriority="high"`, `<link rel="preload" as="image">`. That is now your LCP element and you control it.
- ⇒ **Never** start fetching the sequence before `load`. 120 parallel frame requests during page load will destroy LCP by starving the hero image of bandwidth. The code in §3d gates on `load` + `requestIdleCallback`.

**INP**
- Nuance most people get wrong: **scroll is not itself an INP interaction** — INP measures click, tap and keypress. But a heavy scroll handler *blocks the main thread*, which delays the next paint for a tap that lands during the scroll. That's how scroll work inflates INP indirectly.
- ⇒ All scroll listeners `{ passive: true }`. All work coalesced into one `rAF`. Never `getBoundingClientRect()` more than once per frame.
- ⇒ Native CSS scroll-driven animations run on the compositor and cost essentially **0 ms** of INP. This is their killer feature.
- ⇒ `createImageBitmap()` decodes off the main thread. `new Image()` + synchronous `decode` does not, reliably.

**CLS**
- Pinned/sticky sections and JS-sized canvases are CLS generators. Reserve space with CSS `aspect-ratio` on the canvas wrapper **before** JS runs. Never set canvas dimensions in a way that changes layout.
- Mobile URL-bar show/hide changes `100vh`. Use `100svh` / `100dvh` for pinned sections, and debounce `resize`.

### Mid-range Android reality check

Target device: Snapdragon 6-series / Dimensity 7000-class, 4–6 GB RAM, Chrome, 60 Hz.

| Load | Effect |
|---|---|
| 120 × 1440×1800 frames, all decoded | **1.2 GB.** Tab killed. |
| 120 × 828×1035, sliding window of 16 | ~108 MiB. Survivable, near the edge. |
| `createImageBitmap` with `resizeWidth` to display size | ~35–50 MiB. **Do this.** |
| Three.js homepage | 185 KB gz parse + WebGL context + scene init ≈ 400–700 ms of main thread before first paint. Visible jank. |
| `backdrop-filter: blur(24px)` on a full-width nav during scroll | Real cost. GPU compositing scales with blur radius × pixel area, and it recomposites every scroll frame. |

### The "liquid glass" nav specifically

`backdrop-filter` is Baseline **newly available since 2024-09-16** — Chrome 76, Firefox 103, **Safari 18 / Safari iOS 18** ([webstatus.dev](https://api.webstatus.dev/v1/features/backdrop-filter)). It is safe to use. It is *not* free.

Rules for keeping it smooth:
```css
.nav-glass {
  position: fixed; inset-block-start: 0;
  height: 56px;                                  /* keep the blurred AREA small */
  backdrop-filter: blur(14px) saturate(140%);    /* radius ≤ 20px */
  background: rgb(10 10 12 / 0.55);              /* fallback + reduces perceived blur cost */
  -webkit-backdrop-filter: blur(14px) saturate(140%);
  will-change: backdrop-filter;
  contain: paint;
}
@supports not (backdrop-filter: blur(1px)) {
  .nav-glass { background: rgb(10 10 12 / 0.92); }
}
/* Mid-range Android escape hatch */
@media (max-width: 860px) and (prefers-reduced-transparency: reduce) {
  .nav-glass { backdrop-filter: none; background: rgb(10 10 12 / 0.94); }
}
```
- **Never animate the blur radius.** It re-triggers compositing every frame and drops you to ~30 fps on mobile. Animate opacity/translate instead.
- **Never stack more than 3–4 blurred surfaces** in one viewport.
- Do not run the glass nav *over* the canvas sequence at full width — that's a fullscreen blur composited on top of a per-frame canvas repaint, the single most expensive combination on the page. Either narrow the glass bar, or drop to solid over the hero.
([Empire UI](https://empire-ui.com/blog/backdrop-filter-css), [Mozilla bug 1718471](https://bugzilla.mozilla.org/show_bug.cgi?id=1718471))

### Cellular data

Real-world UK mobile (train, high street, indoors) is 3–8 Mbps, not the headline 4G/5G number.
- 2.5 MB sequence @ 5 Mbps = **~4 s**. Acceptable *because it is deferred* and the static hero is already painted.
- 6 MB @ 5 Mbps = 9.6 s. Never ship the desktop tier to a phone.

Respect the signals:
```js
const c = navigator.connection;
const cheap = c?.saveData || ['slow-2g','2g','3g'].includes(c?.effectiveType);
if (cheap) { /* static hero image only, no sequence, no WebGL */ }
```
`Save-Data: on` is a **user request**, not a hint. Honour it by shipping the static frame and nothing else.

### `prefers-reduced-motion` — the obligation

WCAG **2.3.3 Animation from Interactions** is Level **AAA**, and it explicitly names *"parallax effects when scrolling, where the page foreground and background move at different speeds"*. It requires that such motion can be disabled unless essential. ([W3C Understanding 2.3.3](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html), [W3C technique C39](https://www.w3.org/WAI/WCAG21/Techniques/css/C39))

Separately, **SC 2.2.2 Pause, Stop, Hide is Level A** (not AAA) and governs content that moves automatically without user interaction — i.e. your **autoplaying lookbook video**. That one is a baseline legal-exposure item for a commercial storefront in the UK/EU, not a nice-to-have.

The preference must affect **CSS transitions, CSS animations, JS animations, scroll-driven effects, and video autoplay** ([Pope Tech](https://blog.pope.tech/2025/12/08/design-accessible-animation-and-movement/)).

Global belt-and-braces:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
    animation-timeline: auto !important;   /* neutralise scroll timelines */
  }
}
```
Plus, in JS: the sequence renders **one chosen hero frame** (not frame 1 — pick the best-composed frame, ~60% through), Lenis never initialises, the WebGL depth parallax never initialises, and autoplaying video gets `autoplay` removed with visible controls. The §3d code already does the sequence half.

---

## 8. RECOMMENDED STACK — OVERTIME, concretely

```
Build:      Astro (or Next.js if the Shopify Hydrogen route wins)
Scroll:     native CSS animation-timeline (view/scroll) behind @supports
            + IntersectionObserver fallback           →   0 KB
Pinning:    GSAP ScrollTrigger, dynamic import, one section only  →  ~27 KB gz
Smoothing:  none. (Lenis only if art direction insists, desktop-only)
Hero:       123-frame WebP sequence → canvas, 3 responsive tiers
            828px mobile (~2.2 MB), 1440px desktop (~5.3 MB), deferred past load
Depth:      Depth Anything V2 baked at build → 60-line raw WebGL shader  →  ~4 KB
3D:         Blender renders the frames offline. No WebGL scene graph ships.
Glass nav:  backdrop-filter, 56px tall, blur ≤ 14px, solid fallback ≤860px
Formats:    WebP for the sequence (decode speed), AVIF for static product shots (bytes)
Video:      ambient lookbook only, -an, playsinline, GOP 50, poster always designed
```

**The time theme maps cleanly onto the one sequence you can afford:** an hourglass whose sand falls as you scroll, or a clock whose hands sweep from 11:59 to 12:00 as the page progresses, Blender-rendered at 30 fps for ~4 seconds = 123 frames. Rendered in Blender, flipped by canvas. That is the entire "3D flair" budget, spent in the one place it reads as intentional rather than decorative — which is precisely what "un-vibe-coded" means.

---

## Sources

- [web.dev — Core Web Vitals](https://web.dev/articles/vitals) · [web.dev — LCP](https://web.dev/articles/lcp)
- [webstatus.dev API — scroll-driven-animations](https://api.webstatus.dev/v1/features/scroll-driven-animations) · [webcodecs](https://api.webstatus.dev/v1/features/webcodecs) · [avif](https://api.webstatus.dev/v1/features/avif) · [backdrop-filter](https://api.webstatus.dev/v1/features/backdrop-filter)
- [MDN — Firefox Experimental Features](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Experimental_features) · [MDN — animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline) · [MDN — requestVideoFrameCallback](https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement/requestVideoFrameCallback)
- [Web Platform Features Explorer — requestVideoFrameCallback](https://web-platform-dx.github.io/web-features-explorer/features/request-video-frame-callback/)
- [WebKit — Announcing Interop 2026](https://webkit.org/blog/17818/announcing-interop-2026/) · [Mozilla Hacks — Launching Interop 2026](https://hacks.mozilla.org/2026/02/launching-interop-2026/) · [Igalia — Interop 2026](https://www.igalia.com/news/interop-2026.html)
- [WebKit — New &lt;video&gt; Policies for iOS](https://webkit.org/blog/6784/new-video-policies-for-ios/)
- [Muffin Man — Scrubbing videos using JavaScript](https://muffinman.io/blog/scrubbing-videos-using-javascript/)
- [CSS-Tricks — Apple product page scrolling animations](https://css-tricks.com/lets-make-one-of-those-fancy-scrolling-animations-used-on-apple-product-pages/) · [GSAP Vault — scroll image sequence](https://gsapvault.com/blog/scroll-image-sequence-tutorial)
- [GSAP Pricing](https://gsap.com/pricing/) · [Webflow — GSAP becomes free](https://webflow.com/updates/gsap-becomes-free)
- [Bundlephobia](https://bundlephobia.com/) (three 0.186.0, gsap 3.15.0, lenis 1.3.26, motion 13.3.0, @react-three/fiber 9.7.0)
- [Bitmovin — Apple AV1 Support](https://bitmovin.com/blog/apple-av1-support/) · [Bitmovin — AV1 playback support](https://bitmovin.com/blog/av1-playback-support/)
- [Crystallize — AVIF vs WebP](https://crystallize.com/blog/avif-vs-webp) · [Pixotter — WebP vs AVIF 2026 benchmark](https://pixotter.com/blog/webp-vs-avif/)
- [Depth Anything V2 (arXiv 2406.09414)](https://arxiv.org/pdf/2406.09414) · [Sygnal — Image 2.5D Parallax Effects](https://www.sygnal.com/kb/image-25d-parallax-effects) · [depthbake](https://github.com/roukara/depthbake)
- [W3C — Understanding SC 2.3.3](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html) · [W3C — Technique C39](https://www.w3.org/WAI/WCAG21/Techniques/css/C39) · [Pope Tech — accessible animation](https://blog.pope.tech/2025/12/08/design-accessible-animation-and-movement/)
- [Empire UI — backdrop-filter](https://empire-ui.com/blog/backdrop-filter-css) · [Mozilla bug 1718471](https://bugzilla.mozilla.org/show_bug.cgi?id=1718471)
- [Chrome for Developers — WebCodecs](https://developer.chrome.com/docs/web-platform/best-practices/webcodecs) · [diffusionstudio/webcodecs-scroll-sync](https://github.com/diffusionstudio/webcodecs-scroll-sync)

**Flagged UNVERIFIED:** Apple's 2026 live implementation (technique confirmed by teardowns, not by primary inspection this session); the "147 frames" AirPods Pro figure; Firefox 152-specific status and the 82.58% global-support figure; Safari 26.4/26.5 scroll-timeline fixes; GSAP's SPDX licence identifier (npm returned 403 — check `node_modules/gsap/LICENSE.md` before commercial ship); `motion/mini` and ScrollTrigger standalone gzip sizes; all per-frame KB estimates (measure your own frames).