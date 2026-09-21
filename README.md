# OUR TIME

Website, brand system and asset pipeline for **OUR TIME** — a streetwear label,
EST. 2026.

Built by Jono for Oliver. Everything here is a working draft for Oliver to
approve, reject or change. **Brand decisions are his.**

---

## Look at the site first

The site is a working storefront — home, shop, product pages, a bag that
remembers what you put in it. 22 products on a local catalogue.

### Option 1 — the hosted link (easiest)

Ask Jono for the current link. Nothing to install.

### Option 2 — run it yourself

> ⚠️ **Do not just double-click `web/index.html`.** You will get a blank page.
> The site uses JavaScript modules, which browsers refuse to load straight off
> the filesystem for security reasons. It needs to be *served*. This trips
> everyone up once.

Easiest way, if you have Python (macOS has it already):

```bash
cd web
python3 -m http.server 8000
```

Then open **http://localhost:8000** in your browser. Press `Ctrl+C` in the
terminal to stop it.

There is also a zipped copy of just the site at
**`dist/our-time-site.zip`** — same files, if you want to hand it to someone
without the rest of the repo. It still needs serving, not double-clicking.

---

## What's in here

| Folder | What it is |
|---|---|
| **`web/`** | The website. Open this to see the thing. |
| **`brand/source/`** | The 12 original product renders, untouched. |
| **`brand/renamed/APPROVED/`** | **The corrected renders — use these.** |
| **`brand/TOKENS.md`** | The palette, measured off the actual garments. |
| **`brand/MANIFEST.md`** | Every supplied asset, and which ones had the wrong name on them. |
| **`docs/DIRECTION.md`** | The website design direction and why. |
| **`docs/brand/`** | The brand book — strategy, voice, visual system, motion, applications, commercial. |
| **`docs/research/`** | Seven technical briefs the build is grounded in (glass, scroll media, the video/image APIs, Shopify, competitors). |
| **`docs/concepts/`** | Three competing site concepts and the three critiques of them. |
| **`tools/`** | The scripts that made the assets. |
| **`memory/`** | Claude's notes on this project, so the repo is self-contained. |

### Read this one first

**`docs/brand/DECISIONS.md`** is the standing record. Where it contradicts any
other document, it wins. It carries four things that matter:

1. **The Black Isle positioning is withdrawn** — that is Oliver's call and it has
   not been made. The time theme stays; it never depended on the place.
2. **The care label** — the draft ended up with four different versions, two of
   them contradicting each other. On garment-dyed heavyweight that is a real
   consumer-law problem. One canonical line is now fixed. **Sort this before
   anything is printed.**
3. **The launch range** — 31 colourways is roughly £39,000 of stock. The costed
   recommendation is 3 garment types, 6 colourways, 320 units.
4. **A known error** — the price architecture treats RRP as revenue and ignores
   VAT, so every margin in it is overstated. Don't act on those figures yet.

---

## The naming system

Products are named on a **24-hour index**, and the hour belongs to the
**colour**, not the garment. `0300` is washed black forever. `1600` is washed
denim. `2200` is navy.

So a piece is its hour plus its shape: **`0600 CREW`**. A print gets a suffix:
**`2200 TEE / HOURGLASS`**.

Because the hour belongs to the colour, everything at one hour is automatically a
set — *the 0300 set* sells itself and nobody had to invent a name for it. The
full ledger is in `docs/brand/verbal.md` §4.3.

---

## Two things about the garments

**Several pieces are printed `OVERTIME`, not `OUR TIME`.** The shorts, the
sweatpants, the jeans and four tees. The `OT` monogram works for both, which is
why it went unnoticed. Corrected renders are in `brand/renamed/APPROVED/`. **If
any of these are already with a manufacturer, the artwork needs pulling.**

**The globe tee's coordinates were Chicago.** They came out of a generator.
They now read `57.5878° N, 4.2383° W`.

---

## The tools

All stdlib-only Python. They read API keys from `~/.aiorch/.env` at runtime —
**no keys are stored in this repo.**

| Script | What it does |
|---|---|
| `tools/genimg.py` | Reference-conditioned image generation via Gemini 3 Pro Image. This is what produced the corrected renders — it can reproduce an *exact* logo or garment, which plain text-to-image cannot. |
| `tools/trace_logo.py` | Bitmap → SVG. Marching squares + Douglas–Peucker, written because `potrace` wasn't available. Turned the logo into a 901-byte vector at 99.2% accuracy. |
| `tools/check_trace.py` | Scores a traced SVG against its source bitmap. How that 99.2% was measured rather than eyeballed. |
| `imagery/ot_shoot.py` | The model-shoot generator — garments on AI models, with the reference budget enforced (6 object + 5 character + 3 style, 14 total). |

---

## Technical notes worth keeping

**The liquid-glass nav degrades in three tiers, gated on browser *engine*, not
feature detection.** True refraction (`backdrop-filter: url(#svg)`) is
Chromium-only — WebKit bug 245510 is still open, and **Firefox reports support
while rendering nothing**, so `@supports` is actively misleading here. Tier 2,
plain backdrop-blur, is what iPhone gets and therefore what the design is judged
on. `web/glass-lab.html` is a diagnostic page that reports which tier your device
resolves to.

**The mechanism is procedural Canvas 2D**, not a video or an image sequence:
sharp at any pixel ratio, weighs nothing, and scroll drives it. Five concentric
rings on fixed *integer* gear ratios (`−1 : +2 : −3 : +6 : −12`) — whole numbers
make the rings drift and periodically realign, the way a real gear train does.
The escapement ring is quantised to 60 discrete steps and recoils into each one.

**Commerce sits behind an adapter** (`web/assets/storefront.js`). No storefront
is connected. Swapping in Shopify means writing one more file implementing the
same five methods — no page or template changes. Inventory is deliberately
tri-state: `null` means *untracked*, which reads as available, never as zero.

---

## Still open

- Regenerate the dark colourways on a light backdrop, so the ground-assignment
  rule is actually visible (navy on near-black is a 1.12:1 silhouette). ~$1.10.
- A drop date. The `/drop` page and any countdown depend on a real window —
  there is deliberately no always-on timer, because scarcity that never ends
  isn't scarcity.
- Real fit and shrinkage numbers for the size guide.
- Casting for the AI model photography — faces to be approved before a full set
  is generated.
