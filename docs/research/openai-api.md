# OVERTIME — OpenAI Image + Video API Integration Brief
*Verified against OpenAI docs on 2026-09-16. Every claim below is either sourced or explicitly marked UNVERIFIED.*

---

## 0. STOP — READ THIS FIRST: Sora 2 is being switched off in 8 days

**The Videos API and every Sora 2 model are removed from the OpenAI API on 2026-09-24.** Today is 2026-09-16.

From the official deprecations page (verbatim table):

| Shutdown date | Model / system | Recommended replacement |
|---|---|---|
| 2026-09-24 | Videos API | --- |
| 2026-09-24 | `sora-2` | --- |
| 2026-09-24 | `sora-2-pro` | --- |
| 2026-09-24 | `sora-2-2025-10-06` | --- |
| 2026-09-24 | `sora-2-2025-12-08` | --- |
| 2026-09-24 | `sora-2-pro-2025-10-06` | --- |

Source: https://developers.openai.com/api/docs/deprecations.md — section "2026-03-24: Sora 2 video generation models and Videos API". **The "Recommended replacement" column is literally `---`. OpenAI has named no successor video product.**

### What this means for the OVERTIME build

1. **Any Sora clip you want, generate it before 24 Sep and archive the MP4s.** Download URLs expire 1 hour after generation and OpenAI deletes stored videos — pull every MP4 to local/S3 immediately, do not treat `/videos/{id}/content` as a CDN.
2. **Do not architect the site around a live Sora call.** Build the site to consume static `.mp4`/`.webm` files from your own storage. A "generate on demand" video pipeline dies on 24 Sep.
3. **Budget the render sprint now.** Realistically you have ~6 working days to lock a shot list, generate, QC and re-roll. See §4 for the numbers — this is cheap ($4–$30), the constraint is time, not money.
4. **gpt-image-2.5 is NOT deprecated.** The image side of the plan is safe and long-lived. If you miss the Sora window, the fallback is: generate stills with gpt-image-2.5, animate them with CSS/WebGL/Three.js scroll effects (parallax, mask reveals, a rotating hourglass), or a non-OpenAI video model. Stills + good scroll motion is the un-vibe-coded look anyway.

---

## 1. SORA 2 VIDEO API — exact shapes

### Endpoints (all prefixed `https://api.openai.com/v1`)

| Method | Path | Purpose |
|---|---|---|
| POST | `/videos` | Create a render job |
| GET | `/videos/{video_id}` | Poll status |
| GET | `/videos/{video_id}/content` | Download the MP4 (`?variant=video\|thumbnail\|spritesheet`) |
| GET | `/videos` | List (`?limit=&after=&order=`) |
| DELETE | `/videos/{video_id}` | Delete |
| POST | `/videos/characters` | Upload a reusable character clip |
| POST | `/videos/extensions` | Continue a completed video |
| POST | `/videos/edits` | Edit an existing video (replaces the deprecated remix endpoint) |

Source: https://developers.openai.com/api/docs/guides/video-generation.md

> **UNVERIFIED — path conflict on video edits.** The guide says `POST /v1/videos/edits`. The March-2026 cookbook prompting guide says `POST /v1/videos/{video_id}/edits`. The guide is the newer, more detailed page, so use `/v1/videos/edits`, but if you get a 404, try the other form. This does not affect the core generate→poll→download path, which is consistent across all sources.

### `POST /v1/videos` request body

Accepts **either** `multipart/form-data` **or** `application/json`. Batch is JSON-only.

| Field | Type | Required | Values / default |
|---|---|---|---|
| `prompt` | string | **yes** | Free text |
| `model` | string | no | `sora-2` (default), `sora-2-pro`, `sora-2-2025-10-06`, `sora-2-pro-2025-10-06`, `sora-2-2025-12-08` |
| `seconds` | string | no | `"4"` (default), `"8"`, `"12"`, `"16"`, `"20"` — **sent as a STRING, not an int** |
| `size` | string | no | `"720x1280"` (default), `"1280x720"`, `"1024x1792"`, `"1792x1024"`, `"1080x1920"`, `"1920x1080"` |
| `input_reference` | file (multipart) or object (JSON) | no | JSON form: `{"file_id": "..."}` **or** `{"image_url": "..."}` — exactly one |
| `characters` | array | no | `[{"id": "char_123"}]`, max 2 per video |

> **UNVERIFIED — the auto-generated API reference page is STALE.** https://developers.openai.com/api/reference/resources/videos/methods/create.md still lists `seconds` as only `"4" | "8" | "12"` and `size` as only the four non-1080p values. This contradicts (a) the guide, (b) the changelog, (c) the pricing page, and (d) the cookbook — all four of which document 16s/20s and 1080p. **Trust the guide; the typed enum page lags.** Verify empirically with the free 400 probe in §8 before spending money on a 20s pro render.

### Job lifecycle

`queued` → `in_progress` → `completed` | `failed`

The create call returns immediately with `status: "queued"` and `progress: 0`. The response object:

```json
{
  "id": "video_68d7512d07848190b3e45da0ecbebcde004da08e1e0678d5",
  "object": "video",
  "created_at": 1758941485,
  "status": "queued",
  "model": "sora-2-pro",
  "progress": 0,
  "seconds": "8",
  "size": "1280x720"
}
```

Full object fields: `id`, `object`, `created_at`, `completed_at`, `expires_at`, `status`, `model`, `progress`, `prompt`, `seconds`, `size`, `remixed_from_video_id`, `error` (`{code, message, misalignment}`).

**Poll every 10–20s with exponential backoff.** A single render "may take several minutes"; 1080p and 20s jobs take materially longer. Alternatively register a webhook — events are `video.completed` and `video.failed`, payload `{"id":"evt_...","type":"video.completed","data":{"id":"video_..."}}`.

**Download URLs are valid for a maximum of 1 hour after generation.** Copy to your own storage immediately.

### Working curl

```bash
# 1. CREATE
curl -X POST "https://api.openai.com/v1/videos" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F prompt="Wide tracking shot of a teal coupe driving through a desert highway, heat ripples visible, hard sun overhead." \
  -F model="sora-2-pro" \
  -F size="1280x720" \
  -F seconds="8"

# 2. POLL
curl "https://api.openai.com/v1/videos/video_abc123" \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.status, .progress'

# 3. DOWNLOAD (note -L, it redirects)
curl -L "https://api.openai.com/v1/videos/video_abc123/content" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  --output video.mp4

# 3b. Supporting assets
curl -L "https://api.openai.com/v1/videos/video_abc123/content?variant=thumbnail" \
  -H "Authorization: Bearer $OPENAI_API_KEY" --output thumbnail.webp
curl -L "https://api.openai.com/v1/videos/video_abc123/content?variant=spritesheet" \
  -H "Authorization: Bearer $OPENAI_API_KEY" --output spritesheet.jpg
```

### Working Python (verbatim pattern from the OpenAI guide, extended)

```python
from openai import OpenAI
import sys, time

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)
print("Video generation started:", video)

progress = getattr(video, "progress", 0)
bar_length = 30

while video.status in ("in_progress", "queued"):
    video = openai.videos.retrieve(video.id)
    progress = getattr(video, "progress", 0)
    filled_length = int((progress / 100) * bar_length)
    bar = "=" * filled_length + "-" * (bar_length - filled_length)
    status_text = "Queued" if video.status == "queued" else "Processing"
    sys.stdout.write(f"\r{status_text}: [{bar}] {progress:.1f}%")
    sys.stdout.flush()
    time.sleep(2)

sys.stdout.write("\n")

if video.status == "failed":
    message = getattr(getattr(video, "error", None), "message", "Video generation failed")
    raise RuntimeError(message)

content = openai.videos.download_content(video.id, variant="video")
content.write_to_file("video.mp4")
print("Wrote video.mp4")
```

There is also a convenience helper on the async client:

```python
from openai import AsyncOpenAI
client = AsyncOpenAI()
video = await client.videos.create_and_poll(model="sora-2", prompt="...")
```

*(`create_and_poll` is documented on the async client only. UNVERIFIED whether the sync client exposes it — the manual loop above is the safe path.)*

---

## 2. IMAGE-TO-VIDEO / `input_reference` — the critical bit

**Yes. Sora 2 takes an input image and uses it as the FIRST FRAME of the video.** This is exactly the "generate a hero image, then animate it" workflow, and OpenAI's own docs demonstrate it with a GPT Image still fed into Sora.

> "You can guide a generation with an input image, which acts as **the first frame of your video**. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment."

### Constraints (all verbatim from the guide)

| Constraint | Value |
|---|---|
| **Resolution** | **"The image must match the target video's resolution (`size`)."** Exact match — a 1280x720 image for `size="1280x720"`. Not "same aspect ratio". Same pixels. |
| **File types** | `image/jpeg`, `image/png`, `image/webp` |
| **Multipart form** | `-F input_reference="@sample_720p.jpeg;type=image/jpeg"` |
| **JSON form** | `"input_reference": {"file_id": "file_..."}` or `{"image_url": "https://..."}` (fully qualified URL or base64 data URL) |
| **Batch API** | JSON form only. Multipart `input_reference` uploads are **not supported** in Batch. |
| **File size** | UNVERIFIED — no limit stated for `input_reference` specifically. |

```bash
curl -X POST "https://api.openai.com/v1/videos" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F prompt="She turns around and smiles, then slowly walks out of the frame." \
  -F model="sora-2-pro" \
  -F size="1280x720" \
  -F seconds="8" \
  -F input_reference="@sample_720p.jpeg;type=image/jpeg"
```

### ⚠️ THE ONE THAT WILL BITE YOU

The guardrails section states, verbatim:

> **"Input images with faces of humans are currently rejected."**

**This kills the naive plan.** You cannot generate a beautiful AI model wearing the OVERTIME tee facing camera and then feed that image to Sora to animate it. It will be rejected at input.

Note that OpenAI's own demo is consistent with this: the reference image is a woman shot **from behind** on a skyline, and the prompt is *"She turns around and smiles…"* — the face appears in the *output*, never in the *input*.

**Workarounds, in order of reliability:**
1. **Back-of-head / over-shoulder hero frames.** Model facing away, walking away, looking down. The Sora prompt then drives the turn. This is also the strongest streetwear film language — it reads as considered, not as an AI limitation.
2. **Crop to torso/garment.** Frame from shoulders to hip. No face in frame at all. Perfect for a scroll-triggered product reveal: fabric moving, drawstring swinging, hand into pocket.
3. **Face obscured by design.** Hood up and turned, hair across face, back of a cap, motion blur.
4. **Object-only clips.** The hourglass turning, sand falling, a clock second hand sweeping, tessellated OT pattern rippling on fabric. Zero human risk, 100% on-theme, and these are the clips that actually carry the TIME concept.
5. **Text-to-video without `input_reference`** for anything needing a face, accepting you lose exact garment/logo control.

**My recommendation for OVERTIME:** use `input_reference` for the *product and motif* clips (hourglass, fabric texture, pattern, clock), and text-to-video for the *atmosphere* clips. Put the on-model garment work entirely in gpt-image-2.5 stills, where faces are allowed and reference fidelity is far higher, and animate those stills in-browser with CSS/WebGL rather than Sora.

---

## 3. LIMITS

### Durations
`"4"`, `"8"`, `"12"`, `"16"`, `"20"` — default `"4"`. Both `sora-2` and `sora-2-pro` support up to 20s (added 2026-03-12 per changelog).

**Craft note from OpenAI's own cookbook:** *"The model generally follows instructions more reliably in shorter clips… you may see better results by stitching together two 4 second clips in editing instead of generating a single 8 second clip."* For scroll-triggered web loops, 4s is usually the right unit anyway.

### Resolutions (verbatim from the Sora 2 prompting guide)

| Model | Supported `size` |
|---|---|
| `sora-2` | `720x1280`, `1280x720` **only** |
| `sora-2-pro` | `720x1280`, `1280x720`, `1024x1792`, `1792x1024`, `1080x1920`, `1920x1080` |

There is no square or 1:1 output. For a square web hero you render 1280x720 or 720x1280 and crop.

### Extensions
Each extension adds up to 20s; a video can be extended up to 6 times, max total 120s. Extensions accept only a source video + prompt — **no characters, no image references.**

### Content policy — what matters for fashion

Verbatim from the guide's "Guardrails and restrictions":

> - Only content suitable for audiences under 18 (a setting to bypass this restriction will be available in the future).
> - Copyrighted characters and copyrighted music will be rejected.
> - **Real people—including public figures—cannot be generated.**
> - Character uploads that depict human likeness are blocked by default.
> - **Input images with faces of humans are currently rejected.**

**Translated for OVERTIME:**
- ✅ **Photorealistic synthetic humans in output: yes, allowed.** Sora generates people; the restriction is on *real/identifiable* people and on *input images containing faces*.
- ❌ No real person, no celebrity, no "in the style of [named athlete]", no likeness of your cousin or a friend.
- ❌ No minors — do not prompt ages, do not prompt "teen", "youth", "school". Say "adult", "in their twenties".
- ❌ Nothing suggestive. Streetwear shoots drift here easily: avoid "wet", "sweaty", "cropped", "bare", "sultry", "lingerie-like". Keep it "athletic", "utilitarian", "relaxed fit".
- ❌ No real brand marks in frame other than your own — no Nike swooshes on shoes in the background, no Supreme-style references. Say "unbranded footwear", "no visible logos other than the OT monogram".
- ❌ No copyrighted music. Sora generates audio; for a web loop you'll mute it anyway. Add "no music, ambient sound only" and strip the audio track in post.
- ⚠️ "Character uploads that depict human likeness are blocked by default" — so the `characters` feature cannot give you a consistent human model across shots. It works for **objects and animals**. For OVERTIME that means: you *can* make the hourglass a reusable character, you *cannot* make "the OVERTIME girl" one.

Rejections surface as a `failed` job with `error.code`, `error.message`, and an optional `error.misalignment.detailed_explanation`. Log all three.

---

## 4. PRICING — verified against the official pricing page

Source: https://developers.openai.com/api/docs/pricing.md — "Video generation models · Prices per second"

**Standard tier**

| Model | Size | Portrait | Landscape | Price per second |
|---|---|---|---|---|
| `sora-2` | 720p | 720x1280 | 1280x720 | **$0.10** |
| `sora-2-pro` | 720p | 720x1280 | 1280x720 | **$0.30** |
| `sora-2-pro` | 1024p | 1024x1792 | 1792x1024 | **$0.50** |
| `sora-2-pro` | 1080p | 1080x1920 | 1920x1080 | **$0.70** |

**Batch tier (50% off, jobs complete within 24h, JSON-only requests)**

| Model | Size | Price per second |
|---|---|---|
| `sora-2` | 720p | **$0.05** |
| `sora-2-pro` | 720p | **$0.15** |
| `sora-2-pro` | 1024p | **$0.25** |
| `sora-2-pro` | 1080p | **$0.35** |

Note the pricing table has **no row for `sora-2` above 720p** — consistent with the cookbook. Treat 1024p/1080p as pro-only.

### The requested calculation: 5 clips × 8 seconds × 720p

Total billable = 5 × 8 = **40 seconds**.

| Model / tier | Maths | **Cost** |
|---|---|---|
| `sora-2`, standard | 40 × $0.10 | **$4.00** |
| `sora-2`, batch | 40 × $0.05 | **$2.00** |
| `sora-2-pro`, standard | 40 × $0.30 | **$12.00** |
| `sora-2-pro`, batch | 40 × $0.15 | **$6.00** |

For reference, the same 5-clip set at **1080p on pro**: 40 × $0.70 = **$28.00** standard, **$14.00** batch.

**Real-world budget.** Generative video has a high re-roll rate — plan 3× the shot count. A realistic sprint: ~15 `sora-2` 720p takes to land 5 keepers = **$12**, then re-render the 5 winners on `sora-2-pro` at 1080p = **$28**. **Total ≈ $40.** This is not a budget problem. The deadline is the problem.

---

## 5. GPT IMAGE — `/generations` vs `/edits`

### The difference

| | `POST /v1/images/generations` | `POST /v1/images/edits` |
|---|---|---|
| Input images | **None.** Text prompt only. | **Yes — up to 16 images for GPT image models.** |
| `mask` | Not available | Optional |
| `input_fidelity` | Not available | `"high"` \| `"low"` |
| `response_format` | Present but **"isn't supported for the GPT image models, which always return base64-encoded images"** | n/a — always b64 |
| `style` | `vivid`/`natural` — **dall-e-3 only** | n/a |
| Use it for | Concepts, backgrounds, motifs from scratch | **Everything OVERTIME actually needs** |

### ✅ THE ANSWER YOU NEEDED: yes, `/v1/images/edits` takes MULTIPLE reference images with NO mask

Verbatim from the API reference for `POST /images/edits`:

> `images: array of object { file_id, image_url }` — Input image references to edit. **For GPT image models, you can provide up to 16 images.**

And from the image generation guide, section "Create a new image using image references":

> "You can use one or more images as a reference to generate a new image. In this example, we'll use 4 input images to generate a new image of a gift basket containing the items in the reference images."

The mask is **entirely optional** and only used for local inpainting. Multi-reference compositing needs no mask. (If you *do* pass a mask with multiple images: *"If you provide multiple input images, the mask will be applied to the first image."*)

### Exact multipart request shape (verbatim from OpenAI docs, adapted)

**Note the field name: `image[]` in multipart, `images` in JSON.** This trips people up.

```bash
curl -s -D >(grep -i x-request-id >&2) \
  -o >(jq -r '.data[0].b64_json' | base64 --decode > ot-hero.png) \
  -X POST "https://api.openai.com/v1/images/edits" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "model=gpt-image-2.5-sunburst" \
  -F "image[]=@ot-monogram-white-on-black.png" \
  -F "image[]=@tee-navy-flatlay.png" \
  -F "image[]=@shorts-washed-grey-flatlay.png" \
  -F "image[]=@model-pose-reference.png" \
  -F "quality=high" \
  -F "size=1024x1536" \
  -F "input_fidelity=high" \
  -F 'prompt=Image 1 is the exact OT monogram logo. Image 2 is the exact navy heavyweight oversized washed tee. Image 3 is the exact washed grey sweat shorts. Image 4 is the pose and body reference. Photorealistic editorial fashion photograph of an adult model wearing the garments from images 2 and 3, in the pose of image 4. Reproduce the OT monogram from image 1 exactly as shown, correct proportions and italic shear, no redrawing. Preserve the exact garment colour, wash, seam placement, ribbing and drape from images 2 and 3. Near-black seamless studio background, soft large-source key light from camera left, muted desaturated grade. Full body visible, feet included, hands relaxed at sides and fully visible. No extra text, no watermarks, no other logos.'
```

**JSON form** (uses `images`, not `image[]`):

```bash
curl https://api.openai.com/v1/images/edits \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "images": [
      {"image_url": "https://cdn.overtime.example/ot-monogram.png"},
      {"file_id": "file_abc123"}
    ],
    "prompt": "…",
    "model": "gpt-image-2.5-sunburst",
    "quality": "high",
    "size": "1024x1536",
    "input_fidelity": "high"
  }'
```

**Python:**

```python
import base64
from openai import OpenAI

client = OpenAI()

result = client.images.edit(
    model="gpt-image-2.5-sunburst",
    image=[
        open("ot-monogram.png", "rb"),
        open("tee-navy.png", "rb"),
        open("shorts-grey.png", "rb"),
    ],
    prompt=PROMPT,
    size="1024x1536",
    quality="high",
    input_fidelity="high",
)

with open("ot-hero.png", "wb") as f:
    f.write(base64.b64decode(result.data[0].b64_json))
```

### Full `POST /v1/images/edits` parameter list (verbatim enums)

| Param | Type / allowed values |
|---|---|
| `images` (JSON) / `image[]` (multipart) | up to 16 images for GPT image models |
| `prompt` | string, required |
| `model` | `gpt-image-2.5-sunburst`, `gpt-image-2.5-sunburst-2026-09-08`, `gpt-image-2.5-flare`, `gpt-image-2.5-flare-2026-09-08`, `gpt-image-2`, `gpt-image-2-2026-04-21`, `gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini`, `chatgpt-image-latest` |
| `quality` | `low`, `medium`, `high`, `xhigh`, `max`, `auto` (default `auto`; `xhigh`/`max` are 2.5-only) |
| `size` | `auto`, `1024x1024`, `1536x1024`, `1024x1536`, or any `WIDTHxHEIGHT` |
| `background` | `transparent`, `opaque`, `auto` |
| `input_fidelity` | `high`, `low` — **omit for `gpt-image-2`** (always high, not settable) |
| `mask` | `{file_id}` or `{image_url}`, exactly one |
| `output_format` | `png`, `jpeg`, `webp` |
| `output_compression` | 0–100, jpeg/webp only |
| `moderation` | `auto` (default), `low` |
| `n` | number |
| `partial_images` | 0–3 (streaming) |
| `stream` | boolean |
| `user` | string |

**Custom size constraints (2.5 models):** both edges multiple of 16; aspect ratio between 1:3 and 3:1; neither edge > 3840px; total pixels between 655,360 and 8,294,400; above `2560x1440` is **experimental**.

**Useful sizes for OVERTIME:** `1536x864` (16:9 desktop hero), `2048x1152` (2K landscape), `1024x1536` (portrait on-model), `1080x1920`→ nearest legal is `1088x1920` (multiple of 16) for a Sora-matched portrait reference. **For any still destined for Sora `input_reference`, generate it at the exact Sora size** — `1280x720` and `720x1280` are both multiples of 16, so gpt-image-2.5 can produce them natively. Do this and you skip a resize step and the associated quality loss.

**Response** includes a `usage` block — `input_tokens`, `output_tokens`, `input_tokens_details.{image_tokens,text_tokens}`, `output_tokens_details`. **Log this on every call**; it is the only reliable way to know what a 2.5 image actually costs (see §6).

**Prerequisite:** GPT Image models may require **API Organization Verification** on your account before they'll run. https://help.openai.com/en/articles/10910291-api-organization-verification

---

## 6. THE 2.5 MODELS — documented, no guessing needed

Good news: these **are** documented. No empirical probe required for the basics.

### What they are

> "GPT Image 2.5 includes two model choices. **GPT Image 2.5 Flare is the small model, optimized for speed**, with image quality comparable to GPT Image 2. **GPT Image 2.5 Sunburst is the base model, optimized for quality**, with higher image quality than GPT Image 2. Both models offer improvements in precise editing and subject preservation."
> — https://developers.openai.com/api/docs/guides/image-prompting.md

| | `gpt-image-2.5-flare` | `gpt-image-2.5-sunburst` |
|---|---|---|
| Positioning | "Fast, high-quality everyday image generation" | "Our most capable model for image generation and editing" |
| Size class | Small model | Base model |
| Optimised for | Speed | Quality / **editing precision** |
| Quality vs gpt-image-2 | Comparable | Higher |
| Default snapshot | `gpt-image-2.5-flare-2026-09-08` | `gpt-image-2.5-sunburst-2026-09-08` |
| Quality settings | `low`, `medium`, `high`, `xhigh`, `max`, `auto` | same |
| Endpoints | `/v1/images/generations`, `/v1/images/edits` only | same |
| Batch API | **Not supported** | **Not supported** |
| Features | inpainting | inpainting |

**It is not a different aesthetic — it is the same family, small vs base.** They share identical token prices, so "cheaper" is only true via lower token consumption, and OpenAI explicitly warns: *"Confirm current pricing rather than assuming the faster model costs less."*

### Pricing (identical rates for both, and identical to gpt-image-2)

| Metric | Price |
|---|---|
| Text input | $5.00 / 1M tokens |
| Cached text input | $1.25 / 1M tokens |
| Image input | $8.00 / 1M tokens |
| Cached image input | $2.00 / 1M tokens |
| **Image output** | **$30.00 / 1M tokens** |
| Text output | Not billed (image-only output) |

### ⚠️ EXPLICIT GAP — per-image cost is NOT published for 2.5

OpenAI's docs deliberately do **not** publish a per-image token table for GPT Image 2.5. The guide says, verbatim:

> "Use the response's `usage` to measure token consumption for your prompts, sizes, and quality settings. **Equal token rates don't mean equal cost per image: token consumption can differ by model and quality setting.**"

and on both model pages:

> "**The GPT Image 2 calculator does not estimate GPT Image 2.5 token consumption.**"

The only per-image token table OpenAI still publishes is for models *prior to* `gpt-image-2` (1024×1024 low 272 / medium 1056 / high 4160 tokens; 1024×1536 low 408 / medium 1584 / high 6240). At $30/1M that's roughly **$0.008 (low) to $0.19 (high)** per image — **use that only as an order-of-magnitude anchor for budgeting, not as a 2.5 figure.**

**RECOMMENDED EMPIRICAL PROBE (do this, it is cheap and definitive):**

```python
import base64, itertools, json
from openai import OpenAI
client = OpenAI()

rows = []
for model, quality, size in itertools.product(
    ["gpt-image-2.5-flare", "gpt-image-2.5-sunburst"],
    ["medium", "high", "xhigh", "max"],
    ["1024x1536", "1536x864"],
):
    r = client.images.generate(
        model=model, prompt="A plain matte navy cotton swatch, studio lighting.",
        size=size, quality=quality, n=1,
    )
    u = r.usage
    rows.append({
        "model": model, "quality": quality, "size": size,
        "output_tokens": u.output_tokens,
        "input_tokens": u.input_tokens,
        "usd": u.output_tokens / 1e6 * 30 + u.input_tokens / 1e6 * 5,
    })
print(json.dumps(rows, indent=2))
```

That's 16 calls, almost certainly under $2 total, and it gives you the exact cost-per-image grid for your real sizes. **Run it before you commit to a model for the shoot.** Also time each call — latency is the actual Flare-vs-Sunburst decision axis.

### Two documented contradictions to be aware of

1. **Responses API support.** Both model pages list `v1/responses` as **"Not supported"** in the endpoint table, yet the same pages' prose says *"Select it directly in the Image API **or as the model of the Responses API image generation tool**,"* and the image generation guide shows exactly that with `tools: [{type: "image_generation", model: "gpt-image-2.5-sunburst"}]` under `model: "gpt-6-astra"`. **UNVERIFIED which is correct. Use the Image API directly** (`/v1/images/edits`) — it's documented consistently everywhere and it's what the OVERTIME pipeline needs.
2. **Batch.** Both model pages say Batch is "Not supported" for 2.5. If you need batch image pricing, `gpt-image-2` does support it at $15/1M output. UNVERIFIED whether this changes.

### Which to use for OVERTIME

- **Sunburst** for anything where the OT monogram or the exact garment must survive — on-model shots, the hourglass back-print mockup, the pocket clock print, anything with letterforms. It is explicitly *"for workflows where editing precision matters most."*
- **Flare** for volume: background plates, texture studies, palette exploration, 30 quick composition roughs.
- OpenAI's own selection method: establish quality on Sunburst first, then test Flare with identical prompts/inputs/dimensions; switch only if quality holds and latency improves.

---

## 7. KNOWN FAILURE MODES FOR PRODUCT / APPAREL WORK

OpenAI's own stated limitations, verbatim:

> - **Latency:** Complex prompts may take up to 2 minutes to process.
> - **Text Rendering:** Although significantly improved, the model can still struggle with precise text placement and clarity.
> - **Consistency:** While capable of producing consistent imagery, the model may occasionally struggle to maintain visual consistency for **recurring characters or brand elements** across multiple generations.
> - **Composition Control:** …may have difficulty placing elements precisely in structured or layout-sensitive compositions.

### 7.1 Logo / wordmark fidelity — your biggest risk

The OT monogram has *sharp angular cuts and a specific diagonal shear*. Models redraw logos they are asked to "include". The wide-tracked `O V E R T I M E` wordmark is even more fragile — letterspacing is the first thing to collapse.

**Mitigations, strongest first:**
1. **Never ask the model to draw the logo. Ask it to reproduce a supplied one.** Always pass the monogram as a reference image with `input_fidelity="high"` and an explicit role: *"Image 1 is the exact OT monogram. Reproduce it exactly as shown — same proportions, same italic shear, same angular cuts. Do not redesign, restyle or reinterpret it."*
2. **Composite the logo in post, not in the model.** OpenAI says this outright: *"If a region must remain pixel-identical, **composite the approved edit into the original image instead of relying on prompting alone**."* For OVERTIME this is the professional answer — generate the garment on the model with a **blank chest panel**, then overlay the real vector OT in Photoshop/Figma/Sharp with a multiply/displacement pass for fabric wrap. Guaranteed-correct logo, every time.
3. **For the wordmark, don't generate type at all.** Generate the image, set `O V E R T I M E` in real type in the browser/CSS. Web type is crisper, is selectable, is a11y-correct, and can never be misspelt. This is also part of the "un-vibe-coded" look — AI-rendered type is the #1 tell.
4. If you must render text: quote it exactly, state how many times it appears, use `quality="high"` or above. From the guide: *"Put required wording in quotes and describe its position and typography. **Spell unusual words or brand names letter by letter** when needed. Ask for no extra text, then check spelling and legibility."* e.g. `Render the wordmark exactly once, spelled O-V-E-R-T-I-M-E, uppercase, thin weight, very wide letterspacing. No other text.`
5. **Always append the negative clause:** `No extra text, no watermarks, no unrelated logos.` OpenAI uses this verbatim in their own streetwear example.

### 7.2 Hands

Not called out by name in OpenAI's docs, but the mitigation is:

> "Specify people and actions. Describe body framing, relative scale, gaze, and interaction with objects. Instructions such as '**full body visible, feet included**,' 'looking down at the open book,' or '**hands naturally gripping the handlebars**' make the intended pose and action clearer."

**Give hands a job.** `hands relaxed in the shorts pockets`, `one hand adjusting the hood, fingers clearly separated`, `hands at sides, palms inward, five fingers visible on each hand`. Ambiguous hands = broken hands. Also: `feet included` prevents the classic crop-at-the-ankle artefact, which matters because you're selling shorts.

### 7.3 Garment detail drift across generations

This is the documented "Consistency" limitation, and it's severe in multi-shot campaigns: the washed grey drifts to blue, the drawstring vanishes, the ribbing changes.

**Mitigations:**
1. **Always use `/edits` with the flat-lay as a reference image.** Never `/generations` for a garment you actually sell.
2. **Name the invariants explicitly, every single time.** OpenAI's clothing-swap prompt is the template — adapt it directly:

   > *"Edit the image to dress the woman using the provided clothing images. Do not change her face, facial features, skin tone, body shape, pose, or identity in any way. Preserve her exact likeness, expression, hairstyle, and proportions. Replace only the clothing, fitting the garments naturally to her existing pose and body geometry with realistic fabric behavior. Match lighting, shadows, and color temperature to the original photo so the outfit integrates photorealistically, without looking pasted on. Do not change the background, camera angle, framing, or image quality, and do not add accessories, text, logos, or watermarks."*

   For OVERTIME, add the garment invariants: *"Preserve the exact garment-dyed wash, colour value, seam placement, ribbed cuff detail, drawstring and drape from the reference. Do not change the colour temperature of the fabric."*
3. **`input_fidelity="high"`** on every edit (omit it for `gpt-image-2`, which is always high and rejects the param).
4. **"Separate changes from constraints."** Say *"change only X"* and then list what must be preserved. One change per call.
5. **Iterate by chaining, not by re-prompting.** Pass the previous output as the next edit input, request one change, and restate the preservation list. *"Repeated edits can still change details you intended to preserve. Restate those constraints and inspect each result."*
6. **Assign numbered roles to references:** *"Identify each input by number and purpose: subject, style, clothing, or background."* This is the single highest-leverage prompt habit for multi-reference product work.

### 7.4 The "un-vibe-coded" look — anti-generic prompt patterns

OpenAI's own streetwear example is almost your brief, and it's worth copying its shape:

> *"Give me a cool in culture ad / fashion shot for a brand called Thread. It's a hip young street brand… Make it feel like a polished campaign image for a youth streetwear audience: stylish, contemporary, energetic, and tasteful. Use clean composition, strong color direction, natural poses, and premium fashion photography cues. Render the tagline exactly once, clearly and legibly, integrated into the ad layout. No extra text, no watermarks, no unrelated logos."*

Add OVERTIME's specific anti-AI guardrails:
- **Name the palette as explicit anchors, 3–5 colours.** From the Sora guide: *"Naming three to five colours helps keep the palette stable across shots."* → `Palette anchors: near-black, bone, navy, washed denim blue, warm sand. Muted and desaturated throughout. No neon, no saturated accents.`
- **Describe the medium, not the mood.** `Shot on 35mm film, fine grain, slight halation, matte blacks` beats "cinematic".
- **Ban the AI tells explicitly:** `No gradients, no lens flare, no bokeh orbs, no glossy plastic skin, no HDR, no clip art, no stock-photo treatment, no decorative clutter.` (OpenAI uses `Avoid clip art, stock photography, gradients, shadows, decorative elements, or anything that feels generic or overdesigned` in their own slide example.)
- **Specify light physically:** `single large soft key from camera left, hard shadow falloff to near-black on the right, no fill` beats "moody lighting".
- **Organise as labelled sections.** *"For complex requests, organize the prompt as scene, subject, details, and constraints, using labeled sections."*

### 7.5 Sora-specific failure modes

- **Motion:** one camera move, one subject action, per clip. Describe in beats with counts: *"Actor takes four steps to the window, pauses, and pulls the curtain in the final second"* — not *"actor walks across the room."*
- **Lighting continuity across a cut sequence:** repeat the identical lighting + palette-anchor block in every clip's prompt, or the edit won't cut together.
- **Same prompt ≠ same result.** *"Using the same prompt multiple times will lead to different results — this is a feature, not a bug."* Budget re-rolls (§4).
- **Audio:** Sora generates sound. For web loops, add `No music, ambient sound only` and strip the audio track with ffmpeg anyway (`-an`) — autoplaying audio on a storefront is a bounce generator.
- **Prompt template that works** (from OpenAI's cookbook, adapt per shot):
  ```
  [Prose scene description: characters, costumes, scenery, weather.]

  Cinematography:
  Camera shot: [framing and angle]
  Lens: [e.g. 35mm, shallow depth of field]
  Lighting + palette: [quality of light + 3-5 colour anchors]
  Mood: [overall tone]

  Actions:
  - [beat 1]
  - [beat 2]
  - [beat 3]
  ```

### 7.6 Moderation errors — handle them properly

Blocked requests return `error.type = "image_generation_user_error"` with `error.code = "moderation_blocked"` and an optional:

```json
{"error": {"type": "image_generation_user_error", "code": "moderation_blocked",
  "moderation_details": {"moderation_stage": "input", "categories": ["harassment"]}}}
```

`moderation_stage` ∈ `input` | `output` | `unknown`; `categories` are coarse labels like `harassment`, `self-harm`, `sexual`, `violence`.

**Use `error.code` as the stable discriminator, not the message. Never auto-retry a user error without changing the request.** Log `x-request-id` on every call. You may also set `moderation: "low"` on image calls for less restrictive filtering — but note there is no equivalent parameter on `/v1/videos`.

---

## 8. FREE EMPIRICAL PROBES — run these before spending money

All of these cost $0 (auth/validation errors bill nothing) and settle every UNVERIFIED item above.

```bash
# A. Confirm the Videos API is still alive on your key (and not yet 410 Gone)
curl -s "https://api.openai.com/v1/models/sora-2" \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq .

# B. Discover the REAL `seconds` enum — deliberate 400, zero cost.
#    The error message enumerates accepted values.
curl -s -X POST "https://api.openai.com/v1/videos" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F prompt="probe" -F model="sora-2-pro" -F size="1920x1080" -F seconds="99" | jq .

# C. Discover the REAL `size` enum per model — same trick.
curl -s -X POST "https://api.openai.com/v1/videos" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F prompt="probe" -F model="sora-2" -F size="9999x9999" -F seconds="4" | jq .

# D. Confirm sora-2 rejects 1080p (should 400) — tells you if pro is mandatory
curl -s -X POST "https://api.openai.com/v1/videos" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F prompt="probe" -F model="sora-2" -F size="1920x1080" -F seconds="4" | jq .

# E. Confirm the video-edits path (404 vs 400 tells you which form is right)
curl -s -o /dev/null -w "%{http_code}\n" -X POST "https://api.openai.com/v1/videos/edits" \
  -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" -d '{}'

# F. Confirm input_reference size-match enforcement CHEAPLY:
#    send a deliberately mismatched image. Expect a 400 before any billing.
curl -s -X POST "https://api.openai.com/v1/videos" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F prompt="probe" -F model="sora-2" -F size="1280x720" -F seconds="4" \
  -F input_reference="@wrong_size_512x512.png;type=image/png" | jq .

# G. Confirm the human-face rejection behaviour BEFORE building the shoot around it
curl -s -X POST "https://api.openai.com/v1/videos" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F prompt="She turns and walks out of frame." -F model="sora-2" \
  -F size="1280x720" -F seconds="4" \
  -F input_reference="@face_forward_720p.jpg;type=image/jpeg" | jq '.status, .error'
```

**Probe G is the most important call in this document.** Run it today. If faces are hard-rejected, the entire on-model video plan changes shape, and you have 8 days.

---

## 9. RECOMMENDED PIPELINE FOR OVERTIME

```
Real flat-lays + vector OT  ──┐
                              ├─► /v1/images/edits (sunburst, input_fidelity=high,
AI model/pose reference    ───┘      size = 1280x720 or 720x1280 exactly)
                                      │
                                      ├─► composite real vector OT in post  ──► on-model stills (site)
                                      │
                                      └─► face-free hero frame (back/torso/object)
                                              │
                                              └─► POST /v1/videos  input_reference + 4s prompt
                                                      │ poll → GET /content
                                                      └─► archive MP4 to your own storage
                                                              │
                                                              └─► ffmpeg -an → .mp4 + .webm
                                                                      → scroll-scrubbed <video> on site
```

**Priority order for the next 8 days:**
1. Today: run probe G and probe B. (10 minutes, $0.)
2. Today: lock a 5–8 shot list. Weight it toward object/motif clips — hourglass, falling sand, clock hand, pattern on fabric, drawstring in slow motion. These are policy-safe, on-theme, and loop beautifully.
3. Days 1–3: generate hero stills at exact Sora resolutions with `gpt-image-2.5-sunburst`.
4. Days 3–6: Sora renders at `sora-2` 720p for selects ($4–12), then final passes on `sora-2-pro`. **Download and archive everything within the hour.**
5. Day 7: buffer for re-rolls.
6. After 24 Sep: image generation continues indefinitely; all video work is now static-file editing and in-browser motion.

---

## Sources

- [Video generation with Sora — OpenAI API guide](https://developers.openai.com/api/docs/guides/video-generation)
- [Create a video — API reference](https://developers.openai.com/api/reference/resources/videos/methods/create) *(note: `seconds`/`size` enums on this page are stale)*
- [Sora 2 Prompting Guide — OpenAI Cookbook, updated March 2026](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide)
- [Deprecations — OpenAI API](https://developers.openai.com/api/docs/deprecations)
- [API changelog](https://developers.openai.com/api/docs/changelog)
- [Pricing — OpenAI API](https://developers.openai.com/api/docs/pricing)
- [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [Image prompting guide (GPT Image 2.5)](https://developers.openai.com/api/docs/guides/image-prompting)
- [Images API reference](https://developers.openai.com/api/reference/resources/images)
- [GPT-Image-2.5 Flare model page](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare)
- [GPT-Image-2.5 Sunburst model page](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)
- [Images and vision — input requirements](https://developers.openai.com/api/docs/guides/images-vision)
- [API Organization Verification](https://help.openai.com/en/articles/10910291-api-organization-verification)

Working copies of every source markdown are saved at `/tmp/claude-1000/-mnt-c-Users-jonog/ab01cf7a-8049-4ea4-83af-8ecfa89c04cc/scratchpad/` (`video-gen.md`, `ref-videos-create.md`, `sora-prompting.md`, `image-generation.md`, `image-prompting.md`, `R-images.md`, `pricing.md`, `deprecations.md`, `changelog.md`, `gpt-image-2.5-flare.md`, `gpt-image-2.5-sunburst.md`).