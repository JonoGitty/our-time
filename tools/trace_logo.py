#!/usr/bin/env python3
"""
trace_logo.py — bitmap -> SVG path, stdlib only.

potrace isn't available here and there's no pip, so this does the job directly:
marching squares to pull isocontours off a thresholded bitmap, then
Ramer-Douglas-Peucker to drop the redundant vertices. The OT monogram is a
clean high-contrast geometric mark, which is the best possible case for this.

Output is a single <path> with fill-rule="evenodd", so the counter inside the O
falls out on its own without any winding bookkeeping.

  trace_logo.py in.jpg out.svg [--threshold 128] [--epsilon 0.6] [--width 880]
"""
import argparse, subprocess, sys

FFMPEG = "/home/jonogunix/bin/ffmpeg"


def load_gray(path, crop=None, scale=None):
    """Decode to raw 8-bit grayscale via ffmpeg and return (pixels, w, h)."""
    vf = []
    if crop:
        vf.append("crop=%s" % crop)
    if scale:
        vf.append("scale=%d:-1:flags=lanczos" % scale)
    cmd = [FFMPEG, "-v", "error", "-i", path]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += ["-f", "rawvideo", "-pix_fmt", "gray", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout

    probe = [FFMPEG.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0", path]
    w0, h0 = [int(v) for v in subprocess.run(probe, capture_output=True, check=True)
              .stdout.decode().strip().split(",")[:2]]
    if crop:
        cw, ch = crop.split(":")[:2]
        w0, h0 = int(cw), int(ch)
    if scale:
        h0 = round(h0 * scale / w0)
        h0 -= h0 % 2
        w0 = scale
    if len(raw) != w0 * h0:                      # ffmpeg rounded the height
        h0 = len(raw) // w0
    return raw, w0, h0


def marching_squares(bits, w, h):
    """Isocontour at 0.5 on a binary grid -> list of closed loops."""
    def at(x, y):
        if x < 0 or y < 0 or x >= w or y >= h:
            return 0
        return bits[y * w + x]

    segs = []
    # sample on a grid offset by half a pixel so contours sit between pixels
    for y in range(-1, h):
        for x in range(-1, w):
            tl, tr = at(x, y), at(x + 1, y)
            bl, br = at(x, y + 1), at(x + 1, y + 1)
            idx = (tl << 3) | (tr << 2) | (br << 1) | bl
            if idx in (0, 15):
                continue
            cx, cy = x + 0.5, y + 0.5
            N = (cx + 0.5, cy)
            S = (cx + 0.5, cy + 1.0)
            W = (cx, cy + 0.5)
            E = (cx + 1.0, cy + 0.5)
            # Oriented so the FILLED side is always on the left of travel.
            # That orientation is what makes each vertex have exactly one
            # outgoing edge, so the walk can never hop from the outer contour
            # onto the counter at a saddle (which collapsed 3 loops into 1).
            table = {
                1:  [(S, W)],            2:  [(E, S)],
                3:  [(E, W)],            4:  [(N, E)],
                5:  [(N, E), (S, W)],    6:  [(N, S)],
                7:  [(N, W)],            8:  [(W, N)],
                9:  [(S, N)],            10: [(W, N), (E, S)],
                11: [(E, N)],            12: [(W, E)],
                13: [(S, E)],            14: [(W, S)],
            }
            segs.extend(table[idx])
    return chain(segs)


def chain(segs):
    """Follow DIRECTED segments into closed loops.

    Because the marching-squares table is oriented (filled side on the left),
    every contour vertex has exactly one outgoing edge — so a directed walk
    recovers each loop separately. An undirected walk merges the O's counter
    into its outer contour wherever the two touch at a saddle.
    """
    def key(p):
        return (round(p[0] * 2), round(p[1] * 2))

    out = {}
    for i, (a, b) in enumerate(segs):
        out.setdefault(key(a), []).append(i)

    used = [False] * len(segs)
    loops = []
    for i0 in range(len(segs)):
        if used[i0]:
            continue
        loop = [segs[i0][0]]
        i = i0
        while i is not None and not used[i]:
            used[i] = True
            b = segs[i][1]
            loop.append(b)
            nxt = None
            for j in out.get(key(b), ()):
                if not used[j]:
                    nxt = j
                    break
            i = nxt
        if len(loop) > 8:
            loops.append(loop)
    return loops


def rdp(pts, eps):
    """Ramer-Douglas-Peucker."""
    if len(pts) < 3:
        return pts
    ax, ay = pts[0]
    bx, by = pts[-1]
    dx, dy = bx - ax, by - ay
    nrm = (dx * dx + dy * dy) ** 0.5
    worst, wi = -1.0, 0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        d = (abs(dy * px - dx * py + bx * ay - by * ax) / nrm) if nrm else \
            ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
        if d > worst:
            worst, wi = d, i
    if worst > eps:
        return rdp(pts[:wi + 1], eps)[:-1] + rdp(pts[wi:], eps)
    return [pts[0], pts[-1]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--threshold", type=int, default=128)
    ap.add_argument("--epsilon", type=float, default=0.6)
    ap.add_argument("--crop", default=None, help="ffmpeg crop, w:h:x:y")
    ap.add_argument("--work-width", type=int, default=880)
    ap.add_argument("--view", type=int, default=1000, help="viewBox width")
    a = ap.parse_args()

    px, w, h = load_gray(a.src, a.crop, a.work_width)
    bits = bytes(1 if v >= a.threshold else 0 for v in px)
    ink = sum(bits)
    print("grid %dx%d, ink %.1f%%" % (w, h, 100.0 * ink / (w * h)), file=sys.stderr)

    loops = marching_squares(bits, w, h)
    loops = [rdp(L + [L[0]], a.epsilon)[:-1] for L in loops]
    loops = [L for L in loops if len(L) >= 4]
    loops.sort(key=len, reverse=True)

    sx = a.view / float(w)
    vh = round(h * sx)
    parts, pts_total = [], 0
    for L in loops:
        pts_total += len(L)
        d = "M" + " L".join("%.2f %.2f" % (x * sx, y * sx) for x, y in L) + " Z"
        parts.append(d)

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'fill="currentColor" fill-rule="evenodd" aria-hidden="true">'
        '<path d="%s"/></svg>' % (a.view, vh, "".join(parts))
    )
    open(a.out, "w", encoding="utf-8").write(svg)
    print("loops %d, points %d, bytes %d -> %s"
          % (len(loops), pts_total, len(svg), a.out), file=sys.stderr)


if __name__ == "__main__":
    main()
