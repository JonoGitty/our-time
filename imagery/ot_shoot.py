#!/usr/bin/env python3
"""
OUR TIME — reference-conditioned apparel shoot generator.

Gemini 3 Pro Image ("Nano Banana Pro") via the classic generateContent endpoint.
Verified 2026-09-16: model `gemini-3-pro-image` is live on this key and lists
supportedGenerationMethods = [generateContent, countTokens, batchGenerateContent].

Reference budget for gemini-3-pro-image (per Google docs):
    up to  6 OBJECT images   (high-fidelity product/garment/logo)
    up to  5 CHARACTER images (identity consistency)
    up to  3 STYLE images
    14 images total in one input.

Usage:
    python ot_shoot.py --look navy_tee --model-sheet model_A --n 4

No SDK required — raw HTTPS + stdlib.
"""

import argparse, base64, json, mimetypes, os, pathlib, sys, time, urllib.request

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
MODEL = "gemini-3-pro-image"
REFS = pathlib.Path(__file__).parent / "refs"
OUT = pathlib.Path(__file__).parent / "out"


def key() -> str:
    k = os.environ.get("GEMINI_API_KEY")
    if k:
        return k
    env = pathlib.Path.home() / ".aiorch" / ".env"
    if not env.exists():
        env = pathlib.Path("/mnt/c/Users/jonog/.aiorch/.env")
    for line in env.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip()
    sys.exit("GEMINI_API_KEY not found")


def img_part(path: pathlib.Path) -> dict:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return {"inlineData": {"mimeType": mime, "data": base64.b64encode(path.read_bytes()).decode()}}


# ---------------------------------------------------------------- prompt build

BRAND_LOCK = (
    "BRAND LOCK — reproduce these exactly, do not redraw, restyle or reinterpret:\n"
    "- The OT monogram is a heavy italic right-leaning athletic mark with sharp angular cuts: "
    "a slanted rounded-rectangle O with an open counter, and a T with a sharp diagonal shear. "
    "Reproduce its proportions, slant angle and cut shapes pixel-faithfully from the reference. "
    "It reads OT and nothing else. No extra letters, no serifs, no outline, no drop shadow.\n"
    "- The OVERTIME wordmark is thin light-weight uppercase sans with very wide letterspacing, "
    "spelled O V E R T I M E, eight letters, correct order.\n"
    "- Garment colour matches the reference exactly. Same dye, same wash, same value.\n"
)

FABRIC_LOCK = (
    "FABRIC — heavyweight garment-dyed cotton jersey with a pigment-dyed washed finish: "
    "visible cotton grain, slightly uneven dye with soft tonal mottling, a faint crocked "
    "fade at the seams and hems, soft broken-in drape with real weight. "
    "The print sits IN the fabric: it follows every fold, breaks slightly at the crease lines, "
    "and carries a light vintage crack from wash. Matte throughout."
)

CAMERA = {
    "studio": "Shot on a full-frame body with an 85mm lens at f/4, one large softbox key camera-left "
              "plus a bounce fill, seamless warm-grey paper backdrop, soft contact shadow at the feet.",
    "street": "Shot on a full-frame body with a 35mm lens at f/2.0, overcast north-light diffused daylight, "
              "shallow depth of field, damp pavement and out-of-focus brick behind.",
    "golden": "Shot on a full-frame body with a 50mm lens at f/1.8, low golden-hour backlight raking across "
              "frame creating long shadows and a warm rim on the shoulders.",
}


def build_prompt(look: dict, shot: str, pose: str, n_refs: int) -> str:
    roles = "\n".join(f"Image {i+1} — {r}" for i, r in enumerate(look["ref_roles"]))
    return f"""Photograph, not illustration. Editorial e-commerce lookbook frame for a streetwear label.

REFERENCE IMAGE ROLES (use each only for its stated job):
{roles}

TASK
The person from the character reference images is wearing the exact garment(s) from the garment
reference images. Same person, same face, same hair, same build. Same garment, same cut, same colour,
same print, same placement, same scale relative to the body.

{BRAND_LOCK}
PRINT PLACEMENT
{look['print_spec']}

{FABRIC_LOCK}

POSE AND FRAMING
{pose}

LIGHT AND CAMERA
{CAMERA[shot]}

FINISH
Muted desaturated colour grade, slight film grain, natural matte skin with visible pores and texture,
true-to-life fabric, realistic contact shadows and ambient occlusion where cloth meets body.
Documentary honesty: real skin, real cloth, real light.

The frame contains: one person, the garment, the backdrop. Clean background. Hands resolved and
anatomically correct, five fingers per hand. Plain garment surfaces apart from the specified prints —
no additional logos, no additional text, no tags, no labels.
""".strip()


# ------------------------------------------------------------------ the looks

LOOKS = {
    "navy_tee": {
        "garment_refs": ["tee_navy_front.png", "tee_navy_back.png", "logo_ot_mono.png", "hourglass_backprint.png"],
        "ref_roles": [
            "CHARACTER reference — the model's face and identity. Take the person from this.",
            "CHARACTER reference — same person, three-quarter angle. Confirms bone structure.",
            "GARMENT reference — the navy heavyweight oversized washed tee, front. Take cut, colour and wash from this.",
            "GARMENT reference — the same tee, back, showing the hourglass back print. Take the print from this.",
            "LOGO reference — the OT monogram at high resolution. This is the authority on the mark's exact shape.",
            "ARTWORK reference — the distressed vintage-engraving hourglass, isolated. This is the authority on the back print artwork.",
        ],
        "print_spec": (
            "Front: the OT monogram small on the left chest, roughly 65mm wide, sitting just below the collarbone. "
            "Back: the distressed engraving-style hourglass large and centred between the shoulder blades, "
            "roughly 280mm wide, top edge about 75mm below the collar seam."
        ),
    },
    "shorts_grey": {
        "garment_refs": ["shorts_washed_grey.png", "logo_ot_mono.png"],
        "ref_roles": [
            "CHARACTER reference — the model's face and identity.",
            "CHARACTER reference — same person, three-quarter angle.",
            "GARMENT reference — the garment-dyed washed-grey sweat shorts. Take cut, length, hem, drawcord and wash from this.",
            "LOGO reference — the OT monogram at high resolution, authority on the mark's exact shape.",
        ],
        "print_spec": (
            "The OT monogram embroidered small on the left thigh, roughly 45mm wide, "
            "about 100mm above the hem. Tonal thread, one shade darker than the cloth."
        ),
    },
}

POSES = [
    "Full-body straight-on, standing square to camera, weight on the back foot, arms relaxed at the sides, "
    "chin level, neutral expression. Head to just below the shoes in frame.",
    "Three-quarter turn to camera-left, hands in pockets, shoulders dropped, looking just past the lens.",
    "Back view, standing square, arms at sides, head turned slightly right. The back print fully legible and flat to camera.",
    "Waist-up, arms crossed loosely, slight lean, looking straight down the lens.",
]


# --------------------------------------------------------------------- request

def generate(look_key: str, model_sheet: list, shot: str, pose: str, out_path: pathlib.Path,
             aspect: str = "4:5", size: str = "2K", seed: int | None = None) -> None:
    look = LOOKS[look_key]
    parts = [{"text": build_prompt(look, shot, pose, 0)}]
    for p in model_sheet:                       # CHARACTER refs first (max 5)
        parts.append(img_part(REFS / p))
    for p in look["garment_refs"]:              # OBJECT refs next (max 6)
        parts.append(img_part(REFS / p))

    body = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": aspect, "imageSize": size},
            "temperature": 0.4,
        },
    }
    if seed is not None:
        body["generationConfig"]["seed"] = seed   # UNVERIFIED on image models

    req = urllib.request.Request(
        API.format(model=MODEL),
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key()},
    )
    with urllib.request.urlopen(req, timeout=360) as r:
        data = json.load(r)

    saved = 0
    for part in data["candidates"][0]["content"]["parts"]:
        blob = part.get("inlineData") or part.get("inline_data")
        if blob:
            out_path.write_bytes(base64.b64decode(blob["data"]))
            print(f"  -> {out_path}")
            saved += 1
        elif part.get("text"):
            print(f"  [model] {part['text'][:200]}")
    if not saved:
        print("  !! no image in response:", json.dumps(data)[:600])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--look", default="navy_tee", choices=list(LOOKS))
    ap.add_argument("--model-sheet", default="model_A",
                    help="prefix of the character sheet files in refs/, e.g. model_A_front.png")
    ap.add_argument("--shot", default="studio", choices=list(CAMERA))
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--aspect", default="4:5")
    ap.add_argument("--size", default="2K", choices=["1K", "2K", "4K"])
    a = ap.parse_args()

    sheet = sorted(p.name for p in REFS.glob(f"{a.model_sheet}_*"))[:5]
    if not sheet:
        sys.exit(f"no character sheet files matching {a.model_sheet}_* in {REFS}")
    print(f"character sheet: {sheet}")

    OUT.mkdir(exist_ok=True)
    for i in range(a.n):
        pose = POSES[i % len(POSES)]
        dest = OUT / f"{a.look}_{a.model_sheet}_{a.shot}_{i:02d}.png"
        print(f"[{i+1}/{a.n}] {a.look} / {a.shot} / pose {i % len(POSES)}")
        try:
            generate(a.look, sheet, a.shot, pose, dest, a.aspect, a.size)
        except Exception as e:
            print(f"  !! {e}")
        time.sleep(1)


if __name__ == "__main__":
    main()
