# VEO 3.1 — GEMINI API INTEGRATION BRIEF (OVERTIME site b-roll)

All shapes below are copied from Google's own REST samples on ai.google.dev. Anything not in the docs is marked **UNVERIFIED**.
Working script (syntax-checked, stdlib only): `/tmp/claude-1000/-mnt-c-Users-jonog/ab01cf7a-8049-4ea4-83af-8ecfa89c04cc/scratchpad/veo_gen.py`

---

## 1. The `predictLongRunning` request

**Endpoint**
```
POST https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predictLongRunning
```
`{MODEL}` ∈ `veo-3.1-generate-preview` | `veo-3.1-fast-generate-preview` | `veo-3.1-lite-generate-preview`

**Auth:** header `x-goog-api-key: $GEMINI_API_KEY`. Every official sample uses the header, **not** `?key=`. (`?key=` is UNVERIFIED for this endpoint — use the header.)

**Body:** a Vertex-style predict envelope — `instances` (an array, but only one entry; "Output video: 1" per request) + `parameters`.

```json
{
  "instances": [{
    "prompt": "string, max 1,024 tokens",
    "image":           { "inlineData": { "mimeType": "image/png", "data": "<base64>" } },
    "lastFrame":       { "inlineData": { "mimeType": "image/png", "data": "<base64>" } },
    "referenceImages": [ { "image": { "inlineData": {...} }, "referenceType": "asset" } ],
    "video":           { "inlineData": { "mimeType": "video/mp4", "data": "<base64>" } }
  }],
  "parameters": {
    "aspectRatio": "16:9",
    "durationSeconds": "8",
    "resolution": "720p",
    "personGeneration": "allow_adult"
  }
}
```

**CRITICAL GOTCHA:** on the **Gemini API** images are `{"inlineData": {"mimeType", "data"}}`. `bytesBase64Encoded` is the **Vertex AI** shape and will not work here. Do not mix the two — most blog examples online are Vertex. Also note `durationSeconds` is a **string** (`"8"`, not `8`) in every official sample.

**Working curl** (verbatim structure from the docs, OVERTIME prompt substituted):

```bash
BASE_URL="https://generativelanguage.googleapis.com/v1beta"

operation_name=$(curl -s "${BASE_URL}/models/veo-3.1-fast-generate-preview:predictLongRunning" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -X "POST" \
  -d '{
    "instances": [{
      "prompt": "Slow 180-degree orbit around a folded heavyweight washed-navy tee on a bone plinth, hard raking key light across the cotton slub, deep matte-black seamless background, dust motes drifting, shallow depth of field, locked-off studio product cinematography, no text, no logos, no people."
    }],
    "parameters": {
      "aspectRatio": "16:9",
      "durationSeconds": "8",
      "resolution": "1080p"
    }
  }' | jq -r .name)

while true; do
  status_response=$(curl -s -H "x-goog-api-key: $GEMINI_API_KEY" "${BASE_URL}/${operation_name}")
  if [ "$(echo "${status_response}" | jq .done)" = "true" ]; then
    video_uri=$(echo "${status_response}" | jq -r '.response.generateVideoResponse.generatedSamples[0].video.uri')
    curl -L -o ot_hero_01.mp4 -H "x-goog-api-key: $GEMINI_API_KEY" "${video_uri}"
    break
  fi
  sleep 10
done
```

**Working Python (raw REST, stdlib only, no SDK)** — the load-bearing parts:

```python
import base64, json, mimetypes, os, time, urllib.request
BASE = "https://generativelanguage.googleapis.com/v1beta"
KEY  = os.environ["GEMINI_API_KEY"]
HDR  = {"x-goog-api-key": KEY, "Content-Type": "application/json"}

def inline(path):                      # Gemini API part — NOT bytesBase64Encoded
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return {"inlineData": {"mimeType": mime,
                           "data": base64.b64encode(open(path,"rb").read()).decode()}}

def start(prompt, model="veo-3.1-fast-generate-preview", image=None, last_frame=None,
          refs=None, aspect="16:9", duration="8", resolution="720p", person=None):
    inst = {"prompt": prompt}
    if image:      inst["image"]     = inline(image)
    if last_frame: inst["lastFrame"] = inline(last_frame)
    if refs:       inst["referenceImages"] = [{"image": inline(p), "referenceType": "asset"}
                                              for p in refs[:3]]
    params = {"aspectRatio": aspect, "durationSeconds": duration, "resolution": resolution}
    if person: params["personGeneration"] = person
    req = urllib.request.Request(f"{BASE}/models/{model}:predictLongRunning",
            data=json.dumps({"instances":[inst], "parameters":params}).encode(),
            headers=HDR, method="POST")
    return json.load(urllib.request.urlopen(req))["name"]

def wait(op_name, every=10, timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        op = json.load(urllib.request.urlopen(
                urllib.request.Request(f"{BASE}/{op_name}", headers={"x-goog-api-key": KEY})))
        if op.get("done"):
            if "error" in op: raise RuntimeError(op["error"])
            return op
        time.sleep(every)
    raise TimeoutError(op_name)

def download(op, out):
    uri = op["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
    r = urllib.request.urlopen(urllib.request.Request(uri, headers={"x-goog-api-key": KEY}))
    open(out, "wb").write(r.read())   # urlopen follows the redirect; keep the key header
```

---

## 2. LRO lifecycle

- **Initial response:** JSON whose `.name` is the operation resource name. Poll `GET {BASE_URL}/{name}` — i.e. **concatenate the returned name onto the v1beta base, do not build the path yourself**. (The literal string format, believed to be `models/veo-3.1-…/operations/<id>`, is **UNVERIFIED** — docs never print it. Treat `.name` as opaque.)
- **Poll:** `GET` with the same `x-goog-api-key` header. Docs poll every 10s. Latency: **min 11s, max ~6 min at peak.**
- **`done: true`:** the result is on the same object at
  `.response.generateVideoResponse.generatedSamples[0].video.uri`
  A failure surfaces as `.error` on the operation (shape **UNVERIFIED** — treat as standard google.rpc.Status).
- **Retrieval:** yes — it is a **separate authenticated download**. The `uri` is not public. `curl -L -H "x-goog-api-key: …"` (follow redirects; the header must survive the redirect — in Python, `urllib`/`requests` carry it).
- **Retention: 2 days.** Videos are deleted server-side after 48h. Download immediately in the same script run; never store the URI as your asset reference.
- All output is **SynthID-watermarked** (invisible). Fine for commercial use, worth knowing.

---

## 3. Image-to-video, end frame, reference images — all supported, and this is the win

| Input | Field (in `instances[0]`) | Veo 3.1 / Fast | Veo 3.1 Lite |
|---|---|---|---|
| First frame | `image` | ✔ | ✔ |
| **Last frame** (interpolation) | `lastFrame` — *must* be used with `image` | ✔ | ✔ |
| **Reference images** (subject consistency) | `referenceImages`, up to **3**, each `{image, referenceType:"asset"}` | ✔ | ✖ **n/a** |
| Video extension (+7s, up to 20×) | `video` | ✔ | ✖ |

This is exactly the OVERTIME workflow:

1. **Hero animation:** Nano Banana (`gemini-3-pro-image` / `gemini-3.1-flash-image`) generates the still → pass as `image` → Veo animates it. Docs literally ship this as the canonical pipeline.
2. **Perfect loop:** pass the **same PNG** as both `image` and `lastFrame`. Veo interpolates start→end, so the clip returns to frame 1 — a seamless CSS loop with no crossfade hack. (Same-image loop trick is an inference from the documented interpolation behaviour, **UNVERIFIED** as an explicit Google recommendation, but it is the documented mechanism.)
3. **Garment + model consistency across clips:** `referenceImages` is designed for exactly this — Google's own worked example is *a dress + sunglasses + a woman*, i.e. a fashion look-book. Feed it (a) the OT garment flat-lay, (b) the AI model's face, (c) a set/lighting reference, and you get the same model in the same fit across the whole site. **Requires `veo-3.1-generate-preview` or `-fast`; Lite cannot do it.**
4. `referenceImages` **forces `durationSeconds: "8"`**.

---

## 4. Capabilities and limits (Veo 3.1 on the Gemini API)

| | Veo 3.1 / Fast | Veo 3.1 Lite |
|---|---|---|
| Duration | `"4"`, `"6"`, `"8"` — **must be `"8"`** for 1080p, 4k, reference images, or extension | `"4"`,`"6"`,`"8"`; must be `"8"` for 1080p or refs |
| Resolution | `720p` (default), `1080p` (8s only), `4k` (8s only); 720p only when extending | `720p`, `1080p` (8s only); **no 4k** |
| Aspect ratio | **`16:9` (default) and `9:16`** — vertical fully supported | same |
| Frame rate | **24 fps** | 24 fps |
| Videos per request | 1 | 1 |
| Prompt length | 1,024 tokens | 1,024 tokens |
| Status | Preview | Preview |

**Audio: "✔️ Always on" for all three tiers.** There is **no `generateAudio` parameter in the Gemini API Veo parameter table** — you cannot disable it and you are billed the "video with audio" price regardless. (Whether Vertex AI exposes `generateAudio` for Veo 3.1 is **UNVERIFIED** — its docs are JS-rendered and unreachable from here.) **For a silent site loop, strip it in post:** `ffmpeg -i in.mp4 -an -c:v copy out.mp4` — zero re-encode, and you should be re-encoding to web H.264/VP9/AV1 anyway. Also put `muted playsinline loop` on the `<video>`.

**Known audio failure mode, quoted:** *"Veo 3.1 will sometimes block a video from generating because of safety filters or other processing issues with the audio. You will not be charged if your video is blocked."* Build retry-on-empty into the batch runner.

**Rate limits:** Google **no longer publishes per-model Veo RPM in the docs** — the rate-limits page now says "View your active rate limits in AI Studio" (aistudio.google.com/rate-limit). So specific Veo RPM/RPD numbers are **UNVERIFIED**. What *is* documented and will bite you:

> **Spend-based rate limit, rolling 10-minute window: Free N/A · Tier 1 $10 · Tier 2 $50 · Tier 3 $200.** Exceeding it returns `429 RESOURCE_EXHAUSTED`.

At Tier 1 that caps you at roughly **3 × Standard-1080p 8s clips per 10 minutes** ($3.20 each) — but **12 × Fast-720p** or **25 × Lite-720p**. Batch generation overnight on Fast/Lite, not Standard, or you will spend the night sitting in 429s.

Other limits: English fully supported (others unevaluated); no multi-video prompting; extension input ≤141s.

---

## 5. Tier differences

- **`veo-3.1-generate-preview` (Standard)** — top quality, 4k, reference images, extension. 8× the price of Fast.
- **`veo-3.1-fast-generate-preview`** — Google's framing, quoted: *"create videos with sound while maintaining high quality and optimizing for speed and business use cases… ideal for backend services that programmatically generate ads, tools for rapid A/B testing of creative concepts."* Full feature set (refs + extension + 4k). **This is the OVERTIME workhorse.**
- **`veo-3.1-lite-generate-preview`** — cheapest, 720p/1080p only. **No reference images, no extension, no 4k.** Fine for abstract texture/atmosphere plates; useless for consistent models or garments.

Exact latency deltas between tiers are **UNVERIFIED** (docs give only the global 11s–6min range).

---

## 6. Pricing — 5 × 8-second clips (= 40 billed seconds)

Source: [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing). Paid tier only — **all three Veo 3.1 variants are "Not available" on the free tier.** Prices are per second, video-with-audio (the default and only mode).

| Model | 720p | 1080p | 4k |
|---|---|---|---|
| Veo 3.1 Standard | $0.40/s | $0.40/s | $0.60/s |
| Veo 3.1 Fast | $0.10/s | $0.12/s | $0.30/s |
| Veo 3.1 Lite | $0.05/s | $0.08/s | not supported |

**5 × 8s = 40s:**

| Tier / res | Per clip | **5 clips** |
|---|---|---|
| Standard 720p or 1080p | $3.20 | **$16.00** |
| Standard 4k | $4.80 | **$24.00** |
| **Fast 720p** | $0.80 | **$4.00** |
| **Fast 1080p** | $0.96 | **$4.80** |
| Fast 4k | $2.40 | **$12.00** |
| Lite 720p | $0.40 | **$2.00** |
| Lite 1080p | $0.64 | **$3.20** |

Practical read: a full site's worth of hero + scroll b-roll — say 30 accepted clips at Fast 1080p — is **~$29**, and with a realistic 3× reject rate on art-directed fashion work, **~$85–90 all-in**. That is a rounding error against the design time. Budget for rejects, not for clips.

---

## 7. People, clothing, and `personGeneration`

Yes — photorealistic human models wearing clothing is a **first-class, documented use case**. Google's own reference-image showcase is a woman in a couture dress and sunglasses. Generated video passes safety filters plus memorisation checks for privacy/copyright/bias.

`personGeneration` is **mode-dependent and effectively not a free choice**:

| Mode | Allowed value |
|---|---|
| Text-to-video (and extension) | **`"allow_all"` only** |
| **Image-to-video, interpolation, reference images** | **`"allow_adult"` only** |

There is no `"dont_allow"` on Veo 3.1 in the Gemini API docs — that value is **UNVERIFIED** here (it exists on other/older Google image-gen surfaces).

**Regional restriction, and it applies to the user:** *"In EU, UK, CH, MENA locations, `allow_adult` is the only allowed value for `personGeneration`."* The cousin and the user are UK-based → **`allow_all` is unavailable**, so **pure text-to-video with people will be constrained/refused**. The unblocked path for UK is exactly the one you want anyway: generate the model as a still with Nano Banana, then drive Veo via `image` / `referenceImages` with `personGeneration: "allow_adult"`. Set it explicitly; do not rely on defaults.

`allow_adult` also means **no minors** — brief the model prompts as adult, 20s–30s.

---

## 8. Veo 3.1 vs Sora 2 for this job — and there is no contest

**Sora 2 is dead in 8 days.** From OpenAI's own [deprecations page](https://platform.openai.com/docs/deprecations): on 24 March 2026 OpenAI notified developers that the **Videos API and all Sora 2 models are removed from the API on 2026-09-24** — `sora-2`, `sora-2-pro`, `sora-2-2025-10-06`, `sora-2-2025-12-08`, `sora-2-pro-2025-10-06`. **Recommended replacement: none ("---").** Today is 16 September 2026.

For completeness, Sora pricing while it lasts ([OpenAI pricing](https://platform.openai.com/docs/pricing)): `sora-2` 720p $0.10/s (5×8s = $4.00); `sora-2-pro` 720p $0.30/s ($12.00), 1024p $0.50/s ($20.00), 1080p $0.70/s ($28.00). So Veo 3.1 Fast matches `sora-2` on price at 720p and undercuts `sora-2-pro` by 3–6×.

**Pick: `veo-3.1-fast-generate-preview`, 1080p, 8s.** Reasons, in order:

1. **Sora 2 is removed from the API next week.** Building the OVERTIME pipeline on it would be malpractice.
2. **Reference images.** Three-image subject locking is the single feature that makes a *brand* site possible rather than five unrelated pretty clips — same model, same garment, same lighting across the whole scroll. Sora 2's equivalent subject-consistency guarantees are **UNVERIFIED** and moot.
3. **`lastFrame` interpolation** gives true seamless loops, which is precisely what a scroll-driven web hero needs. This is a hard problem to fake in post.
4. **9:16 native** covers the mobile half of the brief without cropping a 16:9 master.
5. **Cost headroom to iterate.** At $0.96 a clip you can reject nine takes and still be under a fiver — which is how you get the "un-vibe-coded" look. Art direction is an iteration count, not a model choice.

**Use Standard (`veo-3.1-generate-preview`) only for the one or two hero clips** where the garment texture has to read — washed cotton slub and garment-dye mottling are exactly where Fast will soften. $3.20 a take is affordable for two shots and not for thirty.

Two things to plan around regardless of model: **audio is unavoidable and billed** (strip with `-an`), and **the 2-day retention window** means the generation script must download-and-archive in the same run.

---

Sources:
- [Generate videos with Veo 3.1 in Gemini API](https://ai.google.dev/gemini-api/docs/veo) (last updated 2026-09-09)
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) (last updated 2026-09-02)
- [Gemini API video overview](https://ai.google.dev/gemini-api/docs/video)
- [OpenAI pricing](https://platform.openai.com/docs/pricing)
- [OpenAI deprecations](https://platform.openai.com/docs/deprecations)
- [Introducing Veo 3.1 in the Gemini API](https://developers.googleblog.com/introducing-veo-3-1-and-new-creative-capabilities-in-the-gemini-api/)

One flag for the parent: the Veo docs page carries a header note — *"This feature is currently only available with the generateContent API"* — while the entire page's REST samples use `predictLongRunning`, and the video-overview page now pitches **Gemini Omni Flash** as the default video model with Veo 3.1 reachable "through the `generateContent` API". These contradict each other and the note reads as stale or misplaced. `predictLongRunning` is what every code sample on the page uses, and the user's key confirms the three Veo models expose *only* `predictLongRunning` — so that is the correct path for this build. A future `generateContent` path for Veo is **UNVERIFIED**, and Gemini Omni Flash video is **not on the user's key**.