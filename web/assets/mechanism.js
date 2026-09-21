/**
 * THE MECHANISM — OUR TIME's motion primitive.
 *
 * Five concentric rings on FIXED INTEGER gear ratios (-1 : +2 : -3 : +6 : -12).
 * The integers are the whole point: whole-number ratios make the rings drift
 * apart and periodically realign, which is what a real gear train does. Ratios
 * that aren't integers just look like circles spinning at different speeds.
 *
 * The escapement ring is QUANTISED to 60 discrete steps. That single stepped
 * element is what sells the thing as clockwork; everything else glides.
 *
 * Taken from the Capaldi-era Doctor Who titles: concentricity, meshing rates,
 * the lock-into-place. Deliberately NOT taken: the gold/amber palette, the
 * density, the sci-fi. This stays bone on near-black.
 *
 * Canvas 2D at devicePixelRatio, not SVG and not a video file: it is sharp at
 * any size on any screen, weighs nothing, and can be driven by scroll.
 */
const TAU = Math.PI * 2;
const NUMERALS = ['XII', 'I', 'II', 'III', 'IIII', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI'];
const INK = '250,246,246';
const SLATE = '84,100,126';

export function createMechanism(canvas, opts = {}) {
  const o = Object.assign({
    detail: true,       // Roman numerals on the outer ring
    depth: 3,           // receding copies — implies the vortex without a 3D engine
    ambientMs: 26000,   // one slow revolution
    fps: null,          // optional callback(fpsString)
  }, opts);

  const ctx = canvas.getContext('2d');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let size = 0, running = false, turn = 0, introStart = 0, raf = 0;
  let frames = 0, fpsAt = 0;

  function fit() {
    const r = canvas.getBoundingClientRect();
    // cap dpr at 2.5 — 3x costs 44% more pixels for no visible gain on line art
    const dpr = Math.min(devicePixelRatio || 1, 2.5);
    size = Math.max(60, Math.round(r.width));
    canvas.width = Math.round(size * dpr);
    canvas.height = Math.round(size * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  const ring = (cx, cy, r, a, lw) => {
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, TAU);
    ctx.strokeStyle = `rgba(${INK},${a})`; ctx.lineWidth = lw; ctx.stroke();
  };

  /* One path for all N ticks, not N paths. The dial alone draws 60 + 120 + 60 +
     24 ticks and the gear 48 teeth, three depth layers deep — that was ~960
     beginPath/stroke pairs per frame. Batched it is 18. This is the single
     biggest thing standing between this and 60fps on a mid-range phone. */
  function ticks(cx, cy, r, count, len, a, lw, every, longLen) {
    ctx.beginPath();
    for (let i = 0; i < count; i++) {
      const ang = (i / count) * TAU;
      const co = Math.cos(ang), si = Math.sin(ang);
      const L = (every && i % every === 0) ? longLen : len;
      ctx.moveTo(cx + co * r, cy + si * r);
      ctx.lineTo(cx + co * (r - L), cy + si * (r - L));
    }
    ctx.strokeStyle = `rgba(${INK},${a})`; ctx.lineWidth = lw; ctx.stroke();
  }

  function teeth(cx, cy, r, count, depth, a, lw) {
    ctx.beginPath();
    for (let i = 0; i < count; i++) {
      const ang = (i / count) * TAU, w = (TAU / count) * 0.34;
      // moveTo is NOT optional when batching arcs: ctx.arc() draws a connecting
      // line from the current point, so without it every tooth is joined to the
      // last one and the gear renders as a fan of chords across the dial.
      ctx.moveTo(cx + Math.cos(ang - w) * r, cy + Math.sin(ang - w) * r);
      ctx.arc(cx, cy, r, ang - w, ang + w);
      ctx.arc(cx, cy, r + depth, ang + w, ang - w, true);
      ctx.closePath();
    }
    ctx.strokeStyle = `rgba(${INK},${a})`; ctx.lineWidth = lw; ctx.stroke();
  }

  /* counterRot cancels the parent ring's rotation so numerals ORBIT but stay
     upright — a rotating bezel, not a tumbling one. Radial orientation reads as
     upside-down nonsense ("IIIV") through the bottom half of the dial. */
  function numerals(cx, cy, r, a, px, counterRot) {
    ctx.font = `500 ${px}px "IBM Plex Mono", ui-monospace, monospace`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillStyle = `rgba(${INK},${a})`;
    for (let i = 0; i < 12; i++) {
      const ang = (i / 12) * TAU - Math.PI / 2;
      ctx.save();
      ctx.translate(cx + Math.cos(ang) * r, cy + Math.sin(ang) * r);
      ctx.rotate(counterRot || 0);
      ctx.fillText(NUMERALS[i], 0, 0);
      ctx.restore();
    }
  }

  function ellipse(cx, cy, rx, ry, rot, a, lw) {
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot);
    ctx.beginPath(); ctx.ellipse(0, 0, rx, ry, 0, 0, TAU);
    ctx.strokeStyle = `rgba(${INK},${a})`; ctx.lineWidth = lw; ctx.stroke();
    ctx.restore();
  }

  const spin = (cx, cy, r, fn) => { ctx.save(); ctx.translate(cx, cy); ctx.rotate(r); ctx.translate(-cx, -cy); fn(); ctx.restore(); };

  function assembly(cx, cy, R, T, a, detail) {
    const lw = Math.max(0.6, R * 0.0035);

    // R1 — dial: hairline, 60 minute ticks, 12 Roman numerals.  rate -1
    spin(cx, cy, -T, () => {
      ring(cx, cy, R, a * 0.34, lw);
      ticks(cx, cy, R, 60, R * 0.030, a * 0.34, lw, 5, R * 0.058);
      if (detail) numerals(cx, cy, R * 0.885, a * 0.60, Math.max(7, R * 0.062), T);
    });
    // R2 — gear ring, 48 teeth.  rate +2
    spin(cx, cy, T * 2, () => {
      ring(cx, cy, R * 0.775, a * 0.30, lw);
      teeth(cx, cy, R * 0.775, 48, R * 0.030, a * 0.42, lw);
    });
    // R3 — fine index, 120 ticks.  rate -3
    spin(cx, cy, -T * 3, () => {
      ring(cx, cy, R * 0.665, a * 0.22, lw);
      ticks(cx, cy, R * 0.665, 120, R * 0.016, a * 0.26, lw * 0.8, 10, R * 0.034);
    });
    // R4 — orbital ellipses, lifted off the globe tee.  rate +6
    spin(cx, cy, T * 6, () => {
      ellipse(cx, cy, R * 0.555, R * 0.200, 0.32, a * 0.30, lw);
      ellipse(cx, cy, R * 0.555, R * 0.200, TAU / 3 + 0.32, a * 0.22, lw);
      ellipse(cx, cy, R * 0.555, R * 0.200, 2 * TAU / 3 + 0.32, a * 0.22, lw);
    });
    // R5 — THE ESCAPEMENT. Quantised to 60 steps. The clockwork tell.
    const step = Math.floor(T * 12 / TAU * 60) / 60 * TAU;
    spin(cx, cy, -step, () => {
      ring(cx, cy, R * 0.415, a * 0.26, lw);
      ticks(cx, cy, R * 0.415, 60, R * 0.022, a * 0.34, lw, 15, R * 0.046);
      // the single slate mark — the brand's only saturated colour, used once
      ctx.beginPath();
      ctx.moveTo(cx, cy - R * 0.415); ctx.lineTo(cx, cy - R * 0.415 + R * 0.070);
      ctx.strokeStyle = `rgba(${SLATE},${a * 0.95})`; ctx.lineWidth = lw * 2.4; ctx.stroke();
    });
    // inner dial: 24 marks — the "24 / 7" off the tee.  rate +4
    spin(cx, cy, T * 4, () => {
      ring(cx, cy, R * 0.300, a * 0.18, lw);
      ticks(cx, cy, R * 0.300, 24, R * 0.020, a * 0.24, lw * 0.8, 6, R * 0.036);
    });
  }

  function draw(now) {
    if (!size) fit();
    const cx = size / 2, cy = size / 2, R = size * 0.46;
    ctx.clearRect(0, 0, size, size);

    // wind-up: fast, decelerating into lock. easeOutQuint.
    let intro = 1, windSpin = 0;
    if (introStart) {
      const e = Math.min(1, (now - introStart) / 2400);
      intro = 1 - Math.pow(1 - e, 5);
      windSpin = (1 - intro) * TAU * 2.2;
      if (e >= 1) introStart = 0;
    }

    const ambient = reduce.matches || !running ? 0 : (now / o.ambientMs) * TAU;
    const T = ambient + turn + windSpin;

    const DEPTH = [[1, 1, o.detail], [0.590, 0.24, false], [0.345, 0.10, false]].slice(0, o.depth);
    DEPTH.forEach((d, i) => assembly(cx, cy, R * d[0], T * (1 + i * 0.45) + i * 0.7, d[1] * intro, d[2]));

    // The hand ticks in 60 discrete steps and RECOILS into each one — a real
    // escapement overshoots and settles rather than arriving dead. A damped
    // sine over the fraction of a step is what makes it read mechanical.
    const stepF = (T * 3 / TAU) * 60;
    const idx = Math.floor(stepF), frac = stepF - idx;
    const recoil = Math.exp(-frac * 13) * Math.sin(frac * 26) * 0.010;
    const hand = (idx / 60) * TAU + recoil;
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(hand);
    ctx.beginPath(); ctx.moveTo(0, R * 0.055); ctx.lineTo(0, -R * 0.335);
    ctx.strokeStyle = `rgba(${INK},${0.70 * intro})`;
    ctx.lineWidth = Math.max(1, R * 0.008); ctx.lineCap = 'round'; ctx.stroke();
    ctx.restore();

    if (o.fps) {
      frames++;
      if (!fpsAt) { fpsAt = now; frames = 0; }
      else if (now - fpsAt > 1000) { o.fps(Math.round(frames * 1000 / (now - fpsAt)) + ' fps'); frames = 0; fpsAt = now; }
    }
  }

  const loop = (now) => { draw(now); if (running) raf = requestAnimationFrame(loop); };

  const api = {
    fit() { fit(); draw(performance.now()); return api; },
    start() { if (running || reduce.matches) { draw(performance.now()); return api; } running = true; raf = requestAnimationFrame(loop); return api; },
    stop() { running = false; cancelAnimationFrame(raf); return api; },
    /** drive the gear train from scroll progress, 0..1 */
    setTurn(t) { turn = t; if (!running) draw(performance.now()); return api; },
    replay() { introStart = performance.now(); api.start(); return api; },
    drawOnce() { draw(performance.now()); return api; },
    get reduced() { return reduce.matches; },
  };
  return api;
}
