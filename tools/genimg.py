#!/usr/bin/env python3
"""
genimg.py — reference-conditioned image generation / editing via the Gemini API.

aiorch's `image` command is text->image only (GPT Image 2, no reference input),
which cannot reproduce an exact logo or an exact garment. This does what that
cannot: send N reference images + a prompt, get an edited image back.

  genimg.py -o out.png -p "prompt" ref1.jpg ref2.jpg
  genimg.py -o out.png -p "prompt" --model gemini-3-pro-image --aspect 5:4 ref.jpg

Stdlib only. Reads GEMINI_API_KEY from the environment or from
C:\\AI\\AiOrchestrator-2\\.env.
"""
import argparse, base64, json, mimetypes, os, sys, time, urllib.error, urllib.request

ENV_PATHS = ["/mnt/c/AI/AiOrchestrator-2/.env", os.path.expanduser("~/.aiorch/.env")]
API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def load_key(name="GEMINI_API_KEY"):
    if os.environ.get(name):
        return os.environ[name]
    for p in ENV_PATHS:
        try:
            for line in open(p, encoding="utf-8", errors="replace"):
                line = line.strip()
                if line.startswith(name + "="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
        except OSError:
            continue
    sys.exit(f"genimg: no {name} found in env or {ENV_PATHS}")


def part_for(path):
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as fh:
        return {"inline_data": {"mime_type": mime, "data": base64.b64encode(fh.read()).decode()}}


def post(url, body, timeout):
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("refs", nargs="*", help="reference image paths")
    ap.add_argument("-p", "--prompt", required=True)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--model", default="gemini-3-pro-image")
    ap.add_argument("--aspect", default=None, help="e.g. 5:4, 4:3, 1:1, 16:9")
    ap.add_argument("--resolution", default=None, help="e.g. 1K, 2K, 4K")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--retries", type=int, default=2)
    a = ap.parse_args()

    key = load_key()
    parts = [part_for(p) for p in a.refs] + [{"text": a.prompt}]
    body = {"contents": [{"role": "user", "parts": parts}]}

    gen = {"responseModalities": ["TEXT", "IMAGE"]}
    img_cfg = {}
    if a.aspect:
        img_cfg["aspectRatio"] = a.aspect
    if a.resolution:
        img_cfg["imageSize"] = a.resolution
    if img_cfg:
        gen["imageConfig"] = img_cfg
    body["generationConfig"] = gen

    url = API.format(model=a.model) + "?key=" + key

    # Ladder of fallbacks: the exact generationConfig shape varies by model, so on a
    # 400 we progressively strip the optional config rather than failing outright.
    ladders = [body]
    if img_cfg:
        b2 = json.loads(json.dumps(body)); b2["generationConfig"].pop("imageConfig", None)
        ladders.append(b2)
    b3 = json.loads(json.dumps(body)); b3.pop("generationConfig", None)
    ladders.append(b3)

    last = None
    for attempt, b in enumerate(ladders):
        for retry in range(a.retries + 1):
            try:
                t0 = time.time()
                data = post(url, b, a.timeout)
                elapsed = time.time() - t0
                break
            except urllib.error.HTTPError as e:
                detail = e.read().decode()[:900]
                last = f"HTTP {e.code}: {detail}"
                if e.code in (429, 500, 503) and retry < a.retries:
                    time.sleep(5 * (retry + 1)); continue
                data = None; break
            except Exception as e:
                last = f"{type(e).__name__}: {e}"
                if retry < a.retries:
                    time.sleep(5 * (retry + 1)); continue
                data = None; break
        if data is not None:
            break
        print(f"genimg: attempt {attempt + 1}/{len(ladders)} failed -> {last}", file=sys.stderr)
    else:
        sys.exit(f"genimg: all attempts failed. Last error:\n{last}")

    if data is None:
        sys.exit(f"genimg: all attempts failed. Last error:\n{last}")

    cands = data.get("candidates") or []
    if not cands:
        sys.exit("genimg: no candidates. Raw:\n" + json.dumps(data)[:1500])

    saved, notes = [], []
    for i, c in enumerate(cands):
        for part in (c.get("content") or {}).get("parts") or []:
            blob = part.get("inlineData") or part.get("inline_data")
            if blob and blob.get("data"):
                out = a.out if len(cands) == 1 else a.out.replace(".", f"-{i+1}.", 1)
                os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
                with open(out, "wb") as fh:
                    fh.write(base64.b64decode(blob["data"]))
                saved.append(out)
            elif part.get("text"):
                notes.append(part["text"].strip())
        if c.get("finishReason") and c["finishReason"] not in ("STOP",):
            notes.append(f"[finishReason={c['finishReason']}]")

    usage = data.get("usageMetadata", {})
    print(json.dumps({
        "model": a.model, "saved": saved, "elapsed_s": round(elapsed, 1),
        "usage": usage, "notes": notes[:5],
        "prompt_feedback": data.get("promptFeedback"),
    }, indent=2))
    if not saved:
        sys.exit("genimg: model returned no image (see notes above)")


if __name__ == "__main__":
    main()
