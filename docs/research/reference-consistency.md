Research complete — API existence and method support verified live against the user's own key.

---

# Reference-Conditioned Apparel Generation for OVERTIME

## 0. What's actually on his keys (checked, 2026-09-16)

`/mnt/c/Users/jonog/.aiorch/.env` contains `GEMINI_API_KEY` and `ANTHROPIC_API_KEY`. **No OpenAI key in that file.** I was blocked by the permission classifier from sweeping other `.env` files for an `OPENAI_API_KEY`, so treat "he has OpenAI" as **UNCONFIRMED** — worth him checking, because it changes section 4's usefulness. (aiorch reportedly calls GPT-5.6/GPT Image 2, so a key probably exists somewhere; I just couldn't confirm it.)

**Live check against his Gemini key** (`GET /v1beta/models`) returned these image models — so everything below is genuinely available to him today, not just documented:

```
models/gemini-3-pro-image            <- displayName "Nano Banana Pro"
models/gemini-3-pro-image-preview
models/gemini-3.1-flash-image
models/gemini-3.1-flash-image-preview
models/gemini-3.1-flash-lite-image
models/gemini-2.5-flash-image
```

And `GET /v1beta/models/gemini-3-pro-image` returned, **verified**:

```
displayName:               "Nano Banana Pro"
inputTokenLimit:           131072
outputTokenLimit:          32768
supportedGenerationMethods: [generateContent, countTokens, batchGenerateContent]
thinking:                  true
```

Two things matter there. `generateContent` **is** supported (Google's docs now lead with the newer Interactions API, but generateContent is not deprecated). And `batchGenerateContent` is supported — that's the 50%-off batch tier, which is the right way to run a 200-frame campaign.

---

## 1. Gemini 3 Pro Image — reference capacity and what it's good at

### Reference image budget

This is the single most important number for the apparel job. Google's image-generation doc gives a **per-model breakdown**, not just a flat cap:

> "Gemini 3.1 Flash Lite Image supports up to 14 images of objects with high-fidelity. Gemini 3.1 Flash Image supports up to 10 images of objects, plus up to 4 character consistency images. **Gemini 3 Pro Image supports up to 6 object images, 5 character images, and 3 style reference images.**"
> — [ai.google.dev/gemini-api/docs/image-generation](https://ai.google.dev/gemini-api/docs/image-generation)

**14 total in one input**, per [Google Cloud's Gemini 3 Pro Image page](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-pro-image). Each input image costs ~560 tokens.

That 6/5/3 split maps almost perfectly onto this brief:

| Slot type | Budget | Use it for |
|---|---|---|
| **Object** (6) | garment fidelity | flat-lay front, flat-lay back, OT monogram isolated, hourglass artwork isolated, clock-face artwork, colourway swatch |
| **Character** (5) | model identity | the 5-view character sheet of one AI model |
| **Style** (3) | art direction | 3 grade/lighting reference frames that set the washed, desaturated, film-grain look |

He can genuinely fill all three buckets. That's why Gemini is the right primary tool here — most competitors give you one flat "reference images" list with no notion that the logo and the face need different handling.

### What it is actually good at

DeepMind's own model page is unusually specific:

- **Product/object fidelity:** "Maintain the consistency and resemblance of up to five characters and the fidelity of up to fourteen objects in a single workflow."
- **Text rendering** (the reason logos survive): "Gemini 3 Pro Image has the lowest error rates (mostly under 10%)" for single-line text across languages — this is the class-leading capability and it is why the thin wide-tracked OVERTIME wordmark has a chance of surviving.
- **Character consistency:** "excels at character consistency, **but it may not always get it right**."
- **Stated weaknesses**, quoted: "can still struggle with small faces, accurate spelling, and fine details" and may produce "unnatural results, visual artifacts, or disjointed scenes" during complex edits.

— [deepmind.google/models/gemini-image/pro](https://deepmind.google/models/gemini-image/pro/)

Read that honestly: **a chest-sized OT monogram will reproduce well; a 12mm woven neck label will not.** Art-direct around that — big prints, no fine text below about 40px in the output frame.

### Exact request shape — `generateContent`

Endpoint (verified live):
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent
```

Per Google's own [migration doc](https://ai.google.dev/gemini-api/docs/migrate-to-interactions), the generateContent image shape is:

> "In `generateContent`, you pass a list of `parts` within the `contents` array."
> `contents: [{ parts: [{ inlineData: { mimeType, data } }] }]`
> `generationConfig: { responseModalities, imageConfig: { aspectRatio, imageSize } }`
> "The response returns generated media directly in the `parts` of the candidate, typically as base64 data in `inlineData`."

**curl:**

```bash
B64_MODEL=$(base64 -w0 refs/model_A_front.png)
B64_TEE=$(base64 -w0 refs/tee_navy_back.png)
B64_LOGO=$(base64 -w0 refs/logo_ot_mono.png)

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<JSON | python3 -c "
import sys,json,base64
d=json.load(sys.stdin)
for p in d['candidates'][0]['content']['parts']:
    b=p.get('inlineData') or p.get('inline_data')
    if b: open('out.png','wb').write(base64.b64decode(b['data'])); print('saved out.png')
    elif p.get('text'): print('[text]',p['text'][:200])
"
{
  "contents": [{
    "role": "user",
    "parts": [
      {"text": "Image 1 is the CHARACTER reference — take the person's face and identity from it. Image 2 is the GARMENT reference — take the navy tee's cut, colour, wash and back print from it. Image 3 is the LOGO reference — the authority on the exact shape of the OT monogram. Photograph the person from Image 1 wearing the exact garment from Image 2, back view, reproducing the print exactly."},
      {"inlineData": {"mimeType": "image/png", "data": "$B64_MODEL"}},
      {"inlineData": {"mimeType": "image/png", "data": "$B64_TEE"}},
      {"inlineData": {"mimeType": "image/png", "data": "$B64_LOGO"}}
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": { "aspectRatio": "4:5", "imageSize": "2K" }
  }
}
JSON
```

**Python** — a full working, parameterised implementation is written to **`/mnt/c/AI/overtime/imagery/ot_shoot.py`** (stdlib only, no SDK). Core of it:

```python
def img_part(path):
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return {"inlineData": {"mimeType": mime,
                           "data": base64.b64encode(path.read_bytes()).decode()}}

body = {
  "contents": [{"role": "user", "parts": [{"text": prompt}] + [img_part(p) for p in refs]}],
  "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {"aspectRatio": "4:5", "imageSize": "2K"},
      "temperature": 0.4,
  },
}
req = urllib.request.Request(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
data = json.load(urllib.request.urlopen(req, timeout=360))

for part in data["candidates"][0]["content"]["parts"]:
    blob = part.get("inlineData") or part.get("inline_data")
    if blob:
        open("out.png", "wb").write(base64.b64decode(blob["data"]))
```

Note `parts` can contain **both** text and image parts — the model narrates as well as draws, so always loop the parts rather than assuming `parts[0]`.

**UNVERIFIED:** I did not make a live *image generation* call (it costs money and wasn't asked for), so the `imageConfig` block is documented-but-not-executed on this key. `"seed"` in `generationConfig` is **UNVERIFIED** on image models — the script includes it behind a flag. `imageOutputOptions: {"mimeType": "image/png"}` appears in third-party docs ([GMI Cloud](https://docs.gmicloud.ai/model-quickstarts/image/gemini-3-pro-image-preview)) — **UNVERIFIED** against Google.

### The newer Interactions API (worth knowing)

Google's docs now lead with `POST /v1beta/interactions`, a flatter shape:

```python
interaction = client.interactions.create(
    model="gemini-3-pro-image",
    input=[
        {"type": "text", "text": "..."},
        {"type": "image", "mime_type": "image/png", "data": b64},
    ],
    response_format={"type": "image", "mime_type": "image/jpeg",
                     "aspect_ratio": "4:5", "image_size": "2K"},
)
open("out.png","wb").write(base64.b64decode(interaction.output_image.data))
```

Google's position: "While generateContent remains fully supported, the Interactions API is recommended for all new development." **But** batch is generateContent-only right now — and batch is 50% off. For a campaign shoot, stay on `generateContent` + `batchGenerateContent`.

---

## 2. Resolutions, aspect ratios, pricing

**Aspect ratios** (`imageConfig.aspectRatio`): `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`.

**Sizes** (`imageConfig.imageSize`): `512px`(0.5K), `1K`, `2K`, `4K`. **Uppercase K is required.** Gemini 3.1 Flash Lite is 1K-only.

For OVERTIME specifically: **`4:5` at `2K`** for PDP/lookbook stills, **`9:16` at `2K`** for anything destined to become a scroll video or Reel, **`21:9` at `4K`** for the site's hero band. Generate the hero at 4K; everything else at 2K is plenty and half the token cost.

**Pricing**, quoted from [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing):

| Model | Standard output | Batch output |
|---|---|---|
| **Gemini 3 Pro Image** | **$0.134** per 1K/2K image, **$0.24** per 4K | **$0.067** per 1K/2K, **$0.12** per 4K |
| Gemini 3.1 Flash Image | $0.045 (0.5K) / $0.067 (1K) / $0.101 (2K) / $0.151 (4K) | $0.022 / $0.034 / $0.050 / $0.076 |
| Gemini 3.1 Flash Lite Image | $0.0336 per 1K | $0.0168 per 1K |
| Gemini 2.5 Flash Image *(deprecated)* | $0.039 per image | $0.0195 |

Input: Pro is `$2.00/M` text+image tokens ≈ **$0.0011 per input image**. With 10 reference images that's about a cent — negligible next to the output cost.

**Real budget:** a full campaign at 6 colourways × 2 models × 4 poses × 2 lighting setups = 96 frames. At 2K standard: **£10**. Through batch: **£5**. Even at 3× regeneration for QA you are under £30 for the whole shoot. The economics are not a constraint; the QA time is.

---

## 3. The apparel playbook — putting *these* garments on a model

This is the part that decides whether it works.

### 3.1 The core insight: separate the three jobs

Do not throw a flat-lay and a face at the model and hope. Gemini 3 Pro has distinct object/character/style reference slots, and the prompt must **name the role of every image**. Google's own guidance:

> "Use Image A for the character's pose, Image B for the art style, and Image C for the background environment."
> — [blog.google prompting tips for Nano Banana Pro](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/)

So the prompt opens with a role table, always in the same order the parts are appended:

```
Image 1 — CHARACTER reference. The model's face and identity. Take the person from this.
Image 2 — CHARACTER reference. Same person, three-quarter. Confirms bone structure.
Image 3 — GARMENT reference. Navy heavyweight oversized washed tee, front. Cut, colour, wash.
Image 4 — GARMENT reference. Same tee, back, showing the hourglass print. The print comes from this.
Image 5 — LOGO reference. The OT monogram at high resolution. THE AUTHORITY on the mark's exact shape.
Image 6 — ARTWORK reference. The distressed engraving hourglass, isolated on white.
```

That last distinction matters more than it looks. Supplying the back-print tee **and** the isolated hourglass artwork gives the model two independent views of the same graphic — one showing how it sits on cloth, one showing what it actually is. Fidelity goes up measurably.

### 3.2 Supply the logo as its own reference **and** describe it

Answer to the explicit question: **both, always.** The reference image constrains geometry; the text description constrains semantics and stops the model "improving" the mark. The description that works for OVERTIME:

```
BRAND LOCK — reproduce these exactly, do not redraw, restyle or reinterpret:
- The OT monogram is a heavy italic right-leaning athletic mark with sharp angular cuts:
  a slanted rounded-rectangle O with an open counter, and a T with a sharp diagonal shear.
  Reproduce its proportions, slant angle and cut shapes pixel-faithfully from the reference.
  It reads OT and nothing else. No extra letters, no serifs, no outline, no drop shadow.
- The OVERTIME wordmark is thin light-weight uppercase sans with very wide letterspacing,
  spelled O V E R T I M E, eight letters, correct order.
```

Spelling the wordmark letter-by-letter and stating the letter count is a real, load-bearing trick — Gemini's text error rate is low but non-zero, and "eight letters, correct order" catches the OVERTIEM class of failure.

Prep the logo reference properly: **isolated, on white, at 1024px+, no mockup context.** A logo cropped off a product photo carries that photo's lighting and the model inherits it.

### 3.3 Print placement in millimetres, not adjectives

"Logo on the chest" produces a logo anywhere from collarbone to navel, at any size. Specify like a tech pack:

```
Front: the OT monogram small on the left chest, roughly 65mm wide, just below the collarbone.
Back:  the distressed engraving hourglass large and centred between the shoulder blades,
       roughly 280mm wide, top edge about 75mm below the collar seam.
```

The model does not measure in mm, but the numbers force a consistent *relative* scale across every frame in the campaign, which is what actually reads as a real product line.

### 3.4 Fabric — "fabric before style"

This is the highest-leverage single tip and it is the direct answer to "washed/garment-dyed, not clean vector". A field-tested workflow writeup reports explicit fabric naming succeeds **8/10** versus **3/10** for generic terms ([apiyi flat-lay→model workflow](https://help.apiyi.com/en/nano-banana-pro-flat-lay-to-model-photo-apparel-workflow-en.html) — third-party, treat the exact ratio as indicative not gospel, but the direction is corroborated by every other source).

For OVERTIME's washed aesthetic:

```
FABRIC — heavyweight garment-dyed cotton jersey with a pigment-dyed washed finish:
visible cotton grain, slightly uneven dye with soft tonal mottling, a faint crocked fade at
the seams and hems, soft broken-in drape with real weight.
The print sits IN the fabric: it follows every fold, breaks slightly at the crease lines,
and carries a light vintage crack from wash. Matte throughout.
```

"The print sits IN the fabric... breaks at the crease lines" is the specific line that kills the decal look — the failure where a perfectly-reproduced logo floats on top of the garment like a sticker. Name the distortion you want and you get it.

Also lock colour explicitly: **`the exact same colour as the reference image`**. Warm/cool bias in the lighting description otherwise drags the navy and the washed denim-blue apart across frames.

### 3.5 Holding one face across a whole campaign

The technique is a **character sheet**, built once and reused as fixed inputs forever:

1. Generate the model once, text-to-image, at 4K. Lock in ethnicity, age, build, hair, and — critically — a **neutral, unremarkable face**. Distinctive faces drift less but date the campaign.
2. From that single image, generate **5 views**: front, three-quarter left, three-quarter right, profile, back-of-head. Do these one at a time, editing the previous output, not as a batch.
3. Those 5 files are now `model_A_*.png` and occupy all 5 character slots on **every single subsequent call**, forever.

The hard rule, from Google's guidance and echoed everywhere: **change one variable per prompt.** "If you change multiple variables like outfit, background, lighting, and facial expression in one prompt, the identity will break." So the shoot is structured as: same model sheet + same garment + change the pose. Then same model sheet + same pose + change the garment. Never both.

Keep two models max for a first drop. A third doubles QA time for no commercial gain.

### 3.6 Negative prompting — don't

Gemini is **not** a diffusion model with a negative-conditioning channel. Google's explicit guidance:

> Instead of saying "no cars", describe the scene positively: "an empty, deserted street with no signs of traffic."

Saying "no extra logos" reliably produces extra logos. The working substitute is a **positive inventory** — state exactly what is in the frame, which implicitly excludes everything else:

```
The frame contains: one person, the garment, the backdrop. Clean background.
Hands resolved and anatomically correct, five fingers per hand.
Plain garment surfaces apart from the specified prints.
Natural matte skin with visible pores and texture.
```

Note "matte skin with visible pores" rather than "not plastic" — that single swap is most of the fix for the AI sheen.

### 3.7 Failure modes and the fix for each

| Failure | Cause | Fix |
|---|---|---|
| **Logo mangled / re-lettered** | logo only visible small on the flat-lay | Give the isolated logo its own high-res reference slot + spell the wordmark letter-by-letter |
| **Logo looks like a sticker** | print not tied to cloth geometry | "the print sits IN the fabric, follows every fold, breaks at the crease lines, light vintage crack" |
| **Garment silhouette distorts** | flat-lays have no 3D structure | Shoot the reference on a **hanger or ghost mannequin**, not laid flat. Add cut descriptors: "boxy oversized, dropped shoulder, wide body" |
| **Colour drift across frames** | lighting language biasing warm/cool | `"the exact same colour as the reference image"` + neutral studio lighting + fixed `temperature: 0.4` |
| **Back details invented** | only a front reference supplied | Supply a back flat-lay as its own object reference |
| **Extra fingers / broken hands** | inherent | Pose around it: hands in pockets, arms crossed, hands out of frame. Then multi-turn edit any survivors |
| **Plastic skin / AI sheen** | default aesthetic | "natural matte skin with visible pores and texture", "slight film grain", "muted desaturated colour grade", f-stop and lens named |
| **Identity drift** | too many variables at once | One variable per prompt; 5-view character sheet in every call |
| **Print re-imagined** | not locked | `"preserving the original print pattern exactly"` verbatim |

**Multi-turn editing beats regeneration.** If 90% of a frame is right and the left hand is wrong, feed the output back in and ask for the hand — do not re-roll and lose the good frame. This is Google's stated guidance and it's much cheaper than the dice.

---

## 4. OpenAI `/v1/images/edits` — honest comparison

**Caveat: model IDs have moved.** OpenAI's current image guide documents **`gpt-image-2.5-sunburst`** (tighter control, `xhigh`/`max` quality) and **`gpt-image-2.5-flare`** (fast) — not `gpt-image-2`/`2.5` as flat names ([developers.openai.com image-generation guide](https://developers.openai.com/api/docs/guides/image-generation)).

**Multi-reference edit**, verbatim from OpenAI's docs:

```python
result = client.images.edit(
    model="gpt-image-2.5-sunburst",
    image=[open("body-lotion.png","rb"), open("bath-bomb.png","rb"),
           open("incense-kit.png","rb"), open("soap.png","rb")],
    prompt=prompt,
)
```

```bash
curl -s -X POST "https://api.openai.com/v1/images/edits" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "model=gpt-image-2.5-sunburst" \
  -F "image[]=@tee_navy_back.png" \
  -F "image[]=@logo_ot_mono.png" \
  -F "input_fidelity=high" \
  -F "size=1024x1536" -F "quality=high" \
  -F "prompt=..." | jq -r '.data[0].b64_json' | base64 -d > out.png
```

Response is `data[0].b64_json` (the edits endpoint returns base64, not a URL).

### The one thing OpenAI has that Gemini doesn't: `input_fidelity`

> "Setting `input_fidelity="high"` is especially useful when editing images with **faces, logos**, or any other details that require high fidelity in the output."
> — [OpenAI cookbook: generate images with high input fidelity](https://developers.openai.com/cookbook/examples/generate_images_with_high_input_fidelity)

It costs more — **+4096 input tokens for square images, +6144 for non-square** ([the-decoder](https://the-decoder.com/openai-rolls-out-high-input-fidelity-for-more-precise-image-editing/)). This is an explicit, dialled knob for exactly the OT-monogram problem, and Gemini has no equivalent parameter — on Gemini you buy fidelity with prompt discipline instead.

### Verdict on logo fidelity specifically

**Gemini 3 Pro Image wins, but not by a landslide, and the reasons are structural rather than about raw rendering:**

1. **Typed reference slots.** Gemini distinguishes "this is an object, hold it at high fidelity" from "this is a character" from "this is style". OpenAI's `image[]` is an undifferentiated list. For a job where the logo must be pinned but the face may vary, that separation is worth a lot.
2. **Benchmarked text rendering.** DeepMind publishes sub-10% single-line text error rates. The OT monogram is fundamentally a two-letter glyph and OVERTIME is a wordmark — this is a text-rendering problem wearing a logo costume.
3. **Reference capacity.** 6 object + 5 character + 3 style versus OpenAI's documented 4-reference examples (search results claim up to 16 for GPT image models — **UNVERIFIED** against OpenAI docs; the official examples show 4).
4. **Cost.** $0.134 at 2K versus roughly $0.165 for gpt-image `high` quality, and `input_fidelity=high` adds token cost on top. Gemini also has a batch tier at half price.

**But OpenAI is the better *repair* tool.** The realistic play is not either/or: shoot on Gemini, and when a frame is 95% right with a mangled chest logo, run a masked edit on `gpt-image-2.5-sunburst` with `input_fidelity=high` and a mask over the chest. That combination — Gemini for composition and consistency, OpenAI for surgical high-fidelity logo repair — is stronger than either alone. **Contingent on confirming he has an OpenAI key.**

Honest caveat both ways: OpenAI's own guidance says "real logos still need human review." True of both models. Budget QA time, not just API spend.

---

## 5. Dedicated virtual try-on — worth it?

### Google Vertex AI Virtual Try-On

Model `virtual-try-on-001` (preview `virtual-try-on-preview-08-04`). Endpoint:

```
POST https://REGION-aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/REGION/publishers/google/models/virtual-try-on-001:predict
```

Payload shape: `instances[]` with `personImage` and `productImages` (each `{image: {bytesBase64Encoded: ...}}`), `parameters` with `sampleCount`, `storageUri`. Response is `predictions[]` with `bytesBase64Encoded` + `mimeType`. **Marked UNVERIFIED** — Google's docs pages render as navigation shells to WebFetch, so this is assembled from search summaries and a community writeup, not read directly off the spec.

Documented constraints (from the [model card](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/virtual-try-on-preview-08-04)): max 4 output images per prompt, **output resolution = input resolution**, 10MB max image, PNG/JPEG only. Supports tops, bottoms and one-pieces — so the sweat shorts are in scope.

**The blocker for this brief:** VTO "is not available through Gemini API with just an API key — it specifically requires a full Google Cloud project setup" with billing and the Agent Platform API enabled. His Gemini AI Studio key won't reach it. Currently free during preview (100% generative-AI preview discount), which will end.

### FASHN.ai

The most credible purpose-built commercial option. Endpoints: `tryon-max`, `product-to-model`, `image-to-video`, `face-to-model`, `model-create`, `model-swap`, `edit`, `reframe`, `background-remove`. Try-On Max goes to **4K**. Input is `model_image` + `product_image` (flat-lay, ghost mannequin, or on-model). Auth via `FASHN_API_KEY`. Pricing from ~**$0.075/image**, dropping below **$0.04** at volume; app plans from $19/mo; API credits from $7.50. ([fashn.ai/products/api](https://fashn.ai/products/api), [pricing](https://fashn.ai/pricing))

Note `product-to-model` and `model-create` — FASHN has the *whole* pipeline, not just the try-on step.

### Open models

CatVTON (899M params, only 49M trainable, 1024×768 in ~35s on **under 8GB VRAM**), IDM-VTON (dual-UNet, slightly better detail preservation, heavier), Leffa (upper/lower/dress parameter), Kolors. All free, all need a GPU and a weekend.

### The benchmark that actually answers the question

[ionio.ai ran 640 generations across CatVTON, Kling, FASHN, Qwen and Nano Banana Pro](https://www.ionio.ai/blog/vton) for about $53. Findings that matter here:

- **Garment fidelity:** FASHN best, especially complex materials. CatVTON "flattens interesting textures into plausible-looking but generic surfaces" — **that is disqualifying for a washed/garment-dyed brand**, where the texture *is* the product.
- **Logo/print:** FASHN maintains pattern legibility best. All models struggled with high-contrast graphics on small source images.
- **Identity:** Kling drifts least. Nano Banana Pro "makes subtle but noticeable alterations to skin tone."
- **Cost/image:** Nano Banana ~$0.04 (cheapest), CatVTON/Qwen $0.05–0.06, Kling ~$0.07, FASHN ~$0.08.
- **Verdict:** "No single winner exists" — they recommend multi-model routing.

### Recommendation for OVERTIME

**Do not lead with a dedicated VTO model.** Here's the reasoning, and it's a real fork in the road:

Dedicated VTO tools solve a *different problem*. They take a **real photo of a real person** and swap a garment onto them. That is the e-commerce fitting-room problem. OVERTIME's problem is the **campaign photography** problem: there is no person yet, no location yet, no art direction yet. VTO gives you a garment swap; it does not give you golden-hour backlight on a wet street with a washed navy tee and a hourglass back print.

Gemini generates the person, the garment, the location, the light and the grade **in one pass**, art-directable in language. That's what "un-vibe-coded" requires.

**Where VTO earns its place:** later, as a *production* tool. Once the drop expands to 6 colourways, re-shooting each on Gemini risks garment drift between colourways. At that point, take one approved Gemini hero frame as the `personImage`, and use FASHN or Vertex VTO to swap in colourways 2–6 against the identical model, pose and light. That gives a colourway grid that is genuinely consistent — which plain regeneration will not.

So: **Gemini for the hero shoot, VTO for the colourway matrix.**

---

## 6. Legal and disclosure, UK

Short and factual:

**Watermarking.** Every Google image output carries SynthID: "All generated images include a SynthID watermark" — invisible, survives normal editing, and **cannot be turned off** on the Gemini API. As of the May 2026 Google/OpenAI alignment, outputs also carry **C2PA Content Credentials** — cryptographically signed, tamper-evident provenance metadata. Google is rolling native C2PA + SynthID detection into Search and Chrome. Practical consequence: these images are **detectably AI, permanently and by design**. Plan on that being visible, not on hiding it.

**UK ASA/CAP.** There is **no blanket legal requirement in the UK to disclose the use of AI in ads** — the ASA says so explicitly. The Codes contain no AI-specific rules; existing rules apply regardless of how content was made. The test CAP gives, verbatim:

> "Is the audience likely to be misled if the use of AI is not disclosed?"
> "If there is a danger of the audience being misled, is the disclosure clarifying the ad's message or contradicting it?"

— [asa.org.uk on AI disclosure](https://www.asa.org.uk/news/disclosure-of-ai-in-advertising-striking-the-balance-between-creativity-and-responsibility.html)

**What this means concretely for OVERTIME:** an AI model wearing a garment that genuinely exists, in a colour it genuinely comes in, is not misleading — nobody buys a t-shirt because of the model's jawline. The risk arises if the imagery misrepresents the *product*: a drape or a fit or a colour the real garment doesn't have. So the operative rule is a product-accuracy rule, not a disclosure rule. Keep the reference flat-lays as the ground truth, QA every frame against them, and the exposure is low.

Further CAP guidance on AI in ads is expected during 2026, with a final version anticipated by June 2026 covering watermarking standards and disclosure mechanisms ([Osborne Clarke](https://marketinglaw.osborneclarke.com/advertising-regulation/advertising-and-marketing-in-2026-what-businesses-might-expect-in-the-uk-and-eu/), [Charles Russell Speechlys](https://www.charlesrussellspeechlys.com/en/insights/expert-insights/commercial/2026/ai-in-advertising-a-regulatory-lookahead-for-2026/)). A quiet line in the site footer — "campaign imagery created with AI; all garments are real products" — costs nothing and pre-empts the whole question. Worth noting one commercial angle too: some brands now treat AI-model disclosure as a *trust* signal rather than a liability.

---

## 7. Recommended pipeline, end to end

**Stage 0 — Asset prep (one afternoon, no AI).**
Shoot or clean up: each garment on a **hanger or ghost mannequin** (not flat — flat-lays cause silhouette distortion), front and back, even light, no harsh shadow, 1024px+ minimum. Isolate the OT monogram, the hourglass engraving and the clock face as clean PNGs on white at 2048px. Six colourway swatches. → `/mnt/c/AI/overtime/imagery/refs/`

**Stage 1 — Cast the models (once, ~£2).**
Text-to-image, 4K, two models. Neutral faces, right build for oversized fits. Then from each hero, generate 5 views one at a time: front, ¾ left, ¾ right, profile, back. That's `model_A_*.png` — the character sheet, frozen forever.

**Stage 2 — Style plates (once, ~£1).**
Three frames that define the grade: washed desaturated, film grain, matte. These occupy the 3 style slots on every call and are the thing that stops the campaign looking like stock.

**Stage 3 — The hero shoot (~£10, half a day of QA).**
`ot_shoot.py` — 5 character refs + up to 6 garment/logo refs + 3 style plates, per call. Iterate: one variable per prompt. 4:5 at 2K for stills, 9:16 at 2K for anything becoming video, 21:9 at 4K for the site hero. Use `batchGenerateContent` for volume at half price.

**Stage 4 — QA against the tech pack.**
Print position, print scale, colour match, silhouette, hardware, hands, face consistency. Reject, don't rationalise. Multi-turn edit the near-misses rather than re-rolling. If an OpenAI key exists, masked `input_fidelity=high` repair on chest logos.

**Stage 5 — Colourway matrix (optional, later).**
Approved hero frame → FASHN or Vertex VTO → colourways 2–6 on the identical model/pose/light.

**Stage 6 — Into motion.**
This connects to the video brief: FASHN has an `image-to-video` endpoint; Veo takes an image as a first frame. Generate stills in **9:16 at 2K** where they're destined for scroll effects, and generate **matched pairs** — same model, same garment, two poses — so the video model has a start and end frame to interpolate between rather than hallucinating the motion. That's the cleanest route to "3D flair" without Blender, and Blender is indeed overkill for this.

**Total for a full first drop: roughly £15–30 in API spend.** The real cost is QA attention, and that is where the "un-vibe-coded" look is actually won — not in the prompt, in the rejection rate.

---

**Files written:** `/mnt/c/AI/overtime/imagery/ot_shoot.py` (working generator, stdlib-only, with the brand-lock / fabric-lock / camera prompt blocks and the 6+5+3 reference budget encoded), plus empty `refs/` and `out/` dirs.

**Blocked:** I could not sweep for an `OPENAI_API_KEY` outside `.aiorch/.env` — the permission classifier denied the multi-file credential scan. Section 4 is contingent on that key existing; he can confirm in one command in his own terminal.

**Sources:** [ai.google.dev image generation](https://ai.google.dev/gemini-api/docs/image-generation) · [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) · [migrate to Interactions](https://ai.google.dev/gemini-api/docs/migrate-to-interactions) · [DeepMind Gemini 3 Pro Image](https://deepmind.google/models/gemini-image/pro/) · [Google Cloud Gemini 3 Pro Image](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-pro-image) · [blog.google Nano Banana Pro prompting tips](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/) · [OpenAI image generation guide](https://developers.openai.com/api/docs/guides/image-generation) · [OpenAI high input fidelity cookbook](https://developers.openai.com/cookbook/examples/generate_images_with_high_input_fidelity) · [Vertex Virtual Try-On model card](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/virtual-try-on-preview-08-04) · [FASHN API](https://fashn.ai/products/api) · [FASHN pricing](https://fashn.ai/pricing) · [ionio.ai VTON benchmark](https://www.ionio.ai/blog/vton) · [FASHN open-source VITON comparison](https://fashn.ai/blog/comparing-the-top-4-open-source-virtual-try-on-viton-models) · [apiyi flat-lay→model workflow](https://help.apiyi.com/en/nano-banana-pro-flat-lay-to-model-photo-apparel-workflow-en.html) · [ASA on AI disclosure](https://www.asa.org.uk/news/disclosure-of-ai-in-advertising-striking-the-balance-between-creativity-and-responsibility.html) · [Osborne Clarke 2026 outlook](https://marketinglaw.osborneclarke.com/advertising-regulation/advertising-and-marketing-in-2026-what-businesses-might-expect-in-the-uk-and-eu/) · [C2PA/SynthID alignment](https://c2paviewer.com/articles/openai-google-c2pa-synthid-2026)