import { buildPath, headAt, posAt } from './geom.js';
import { SEGS, CELLS } from './scenes.js';
import { prepare, drawLine } from './ink.js';
import { makePaper, drawPaper, vignette, makeTooth, drawTooth } from './paper.js';
import { worldToScreen, BASE } from './cam.js';
import { penShadow } from './hands.js';
import { CUES } from './cues.js';
import { clamp, lerp, ss, eo, eio } from '/core/lib.js';
const q = new URLSearchParams(location.search), cv = document.getElementById('c'), ctx = cv.getContext('2d'), W = 1080, H = 1920, DUR = 139.4;
await document.fonts.load('600 80px Caveat'); await document.fonts.load('700 80px Caveat');
const P = prepare(buildPath(SEGS)), paper = makePaper(), tooth = makeTooth();
// ---- caméra : une composition par scène, resserrée à chaque phrase
const ids = Object.keys(CELLS), Z = { button: 2.75, crowd: 2.45, scales: 2.35, horizon: 2.3, phone: 2.5, cage: 2.5, hands: 2.6 };
const KEY = []; ids.forEach((id, i) => { const c = CELLS[id], n = CELLS[ids[i + 1]], e = n ? n.t0 + .1 : 121; KEY.push({ t: i ? c.t0 + .9 : -9, x: c.p[0], y: c.p[1] + 45, z: Z[id] || 2.6 }, { t: e, x: c.p[0], y: c.p[1] + 45, z: (Z[id] || 2.6) * 1.05 }); });
const OV = { x: 0, y: 30, z: .8 }; KEY.at(-1).t = 121.6; KEY.push({ t: 127.0, ...OV, z: .86 }, { t: 135.2, ...OV, z: .8 }, { t: 138.4, x: KEY[0].x, y: KEY[0].y, z: KEY[0].z * 1.3 }, { t: 150, x: KEY[0].x, y: KEY[0].y, z: KEY[0].z * 1.3 });
const PUNCH = [[-9, .3], [2.23, .04], [3.29, .12], [4.79, .34], [6.96, .22], [8.14, 0], [13.75, .1], [18.55, 0], [20.29, .12], [22.59, 0], [24.11, .16], [26.84, .28], [28.82, .1], [31.05, 0], [34.88, .16], [37.78, .04], [40.55, .34], [43, 0], [45.2, .1], [47.11, .3], [48.6, 0], [50.86, .14], [53.55, .24], [55.17, .06], [57.15, .22], [58.6, 0], [61.3, .1], [65.79, 0], [67.83, .15], [70.48, .32], [71.69, .05], [75.15, .16], [76.64, 0], [78.82, .16], [80.08, .3], [82.3, .1], [84.43, .34], [85.98, .12], [89.26, .42], [90.0, 0], [93.95, .1], [97.46, 0], [99, .12], [101.39, .02], [103.68, 0], [105.58, .14], [108.82, .4], [110.15, 0], [113.57, .12], [116.49, .3], [118.38, .1], [120.42, .2], [121.6, 0]];
const punch = t => { let v = 0; for (let i = 0; i < PUNCH.length; i++) { if (t < PUNCH[i][0]) break; const p = i ? PUNCH[i - 1][1] : 0; v = lerp(p, PUNCH[i][1], eo((t - PUNCH[i][0]) / .28)); const nx = PUNCH[i + 1]?.[0] ?? 1e9; if (nx > 900) continue; v += .035 * clamp((t - PUNCH[i][0]) / 4); } return v; };
function camFor(t) {
  let i = 0; while (i < KEY.length - 2 && t > KEY[i + 1].t) i++;
  const a = KEY[i], b = KEY[i + 1], u = eio((t - a.t) / (b.t - a.t)); const over = t > 121.6;
  let x = lerp(a.x, b.x, u), y = lerp(a.y, b.y, u), z = Math.exp(lerp(Math.log(a.z), Math.log(b.z), u)) * (1 + (over ? 0 : punch(t)));
  const roll = (Math.sin(t * .37) * .5 + (t > 52 && t < 58.5 ? (t - 52) * .5 : 0) - (t > 58.5 && t < 59.5 ? -3.2 * (1 - ss(t - 58.5)) : 0)) * clamp((138.4 - t) / 2) * clamp(t / 2);
  return { cx: x, cy: y, k: BASE * z, r: roll * Math.PI / 180, z };
}
// ---- l'intérieur de la machine : cercle d'encre qui inverse la page
const INV = [[24.0, 30.6], [84.35, 90.1]];
function inverse(t) { for (const [a, b] of INV) { if (t < a || t > b + .6) continue; const r = t < b ? eio((t - a) / .7) : 1 - eio((t - b) / .55); if (r <= .001) return;
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.beginPath(); ctx.arc(W / 2, 850, r * 1400, 0, 7); ctx.clip(); ctx.globalCompositeOperation = 'difference'; ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H);
  ctx.globalCompositeOperation = 'lighten'; ctx.fillStyle = '#12162a'; ctx.fillRect(0, 0, W, H); ctx.restore(); return; } }
// ---- texte
function halo(s, x, y, w) { ctx.lineJoin = 'round'; ctx.lineWidth = w; ctx.strokeStyle = 'rgba(244,239,228,.95)'; ctx.filter = 'blur(4px)'; ctx.strokeText(s, x, y); ctx.strokeText(s, x, y); ctx.filter = 'none'; }
const HOT = /^(parfait|vrai|appuies|Choisis|Maintenant|changer|rêves|cuve|piège|oublies|réel|refuser|plaisir|hésites|sauvé|quelqu’un|rien|forme|vaste|refusé|classée|retourne|erreur|machine|débrancher|perds|quoi|moitié|rester|reste|restent|riches|prison|vérité|connaît|déjà|statu|quo|main|vies|effleuré|question|sors|restes|raison)$/;
function subtitle(c, nextT, t) {
  const t1 = Math.min(Math.max(c.t1 + .45, c.t0 + 1.0), nextT - .04); if (t < c.t0 - .06 || t > t1) return;
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  const ws = c.text.split(' '), size = 92; ctx.font = `700 ${size}px Caveat`; const sp = ctx.measureText(' ').width, lines = [[]]; let x = 0;
  ws.forEach((w, i) => { const m = ctx.measureText(w).width; if (x + m > 850 && lines.at(-1).length) { lines.push([]); x = 0; } lines.at(-1).push({ w, m, i }); x += m + sp; });
  const N = c.text.length; let acc = 0; const at = ws.map(w => { const v = c.t0 + (c.t1 - c.t0) * acc / N; acc += w.length + 1; return v; });
  lines.forEach((ln, li) => { const tw = ln.reduce((s, o) => s + o.m, 0) + sp * (ln.length - 1); let xx = W / 2 - tw / 2; const y = 1435 + li * 98 - (lines.length > 2 ? 49 : 0);
    for (const o of ln) { const u = clamp((t - at[o.i] + .06) / .14); if (u > 0) { const hot = HOT.test(o.w.replace(/[.,?:;«»…\u00a0]/g, '')); ctx.globalAlpha = u; const yy = y + (1 - eo(u)) * 14; halo(o.w, xx, yy, 30); ctx.fillStyle = 'rgba(29,26,23,.95)'; ctx.fillText(o.w, xx, yy);
      if (hot) { ctx.strokeStyle = 'rgba(29,26,23,.9)'; ctx.lineWidth = 6; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(xx, yy + 16); ctx.quadraticCurveTo(xx + o.m * .5, yy + 22, xx + o.m * eo(u), yy + 12); ctx.stroke(); } } xx += o.m + sp; } });
  ctx.restore();
}
const BIG = [['FAUX', 3.3, 4.7, 190], ['1974', 32.6, 34.6, 150], ['1', 43.95, 46.3, 170], ['2', 48.7, 51.4, 170], ['3', 59.05, 61.6, 170], ['84 %', 67.83, 70.35, 250], ['2010', 71.9, 74.4, 150], ['46 %', 91.0, 93.8, 220], ['≈ 50 %', 97.46, 98.9, 220], ['87 %', 101.39, 103.4, 240], ['SORS', 127.2, 127.65, 0], ['?', 127.2, 127.2, 0]];
function big(t) { for (const [s, a, b, sz] of BIG) { if (!sz || t < a || t > b + .25) continue; const u = eo((t - a) / .25), o = 1 - clamp((t - b) / .25); ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = clamp((t - a) / .1) * o; ctx.translate(W / 2, 440); ctx.rotate(-.035); ctx.scale(1.35 - .35 * u, 1.35 - .35 * u); ctx.font = `700 ${sz}px Caveat`; ctx.textAlign = 'center'; halo(s, 0, 0, 44); ctx.fillStyle = 'rgba(29,26,23,.97)'; ctx.fillText(s, 0, 0); ctx.restore(); } }
// dix visages : combien restent
const HEADS = [-120, -60, 0, 60, 120].map(x => [x, -50]).concat([120, 60, 0, -60, -120].map(x => [x, 60]));
function heads(t, M, k) { const st = t < 93.9 ? [91.2, 4.6] : t < 99 ? [97.5, 5] : [101.4, 8.7]; if (t < st[0] || t > 103.6) return; const p = CELLS.scales.p; HEADS.forEach((h, i) => { const n = clamp(st[1] - i), u = eo((t - st[0] - i * .07) / .25) * n; if (u <= 0 || (t > 93.9 && t < 97.5)) return; const c = M(p[0] + h[0], p[1] + h[1]); ctx.beginPath(); ctx.ellipse(c[0], c[1], 14 * k * Math.sqrt(u), 16 * k * Math.sqrt(u), 0, 0, 7); ctx.fillStyle = 'rgba(29,26,23,.88)'; ctx.fill(); }); }
function scene(t, all) {
  const cam = all ? { cx: OV.x, cy: OV.y, k: BASE * OV.z, r: 0, z: 1 } : camFor(t), M = worldToScreen(cam, W, H), head = all ? P.N - 1 : headAt(P, t), i = Math.floor(head);
  drawPaper(ctx, paper, cam, W, H); drawLine(ctx, P, head, M, cam.k, { allDry: true }); heads(t, M, cam.k); drawTooth(ctx, tooth, cam, W, H); vignette(ctx, W, H);
  if (!all && t < 134) penShadow(ctx, M(...posAt(P, head)), [.56, .83], cam.k * .6, { lift: 0, alpha: clamp(t * 2) });
}
const snap = document.createElement('canvas'); snap.width = W; snap.height = H; let snapOk = false;
window.render = t => {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  if (t > 138.0 && !snapOk) { scene(0); snap.getContext('2d').drawImage(cv, 0, 0); snapOk = true; }
  scene(t, q.has('all')); if (q.has('all')) return;
  if (t > 138.3) { ctx.globalAlpha = ss((t - 138.3) / .5); ctx.drawImage(snap, 0, 0); ctx.globalAlpha = 1; }
  big(t); CUES.forEach((c, n) => subtitle(c, CUES[n + 1]?.t0 ?? 1e9, t)); inverse(t);
};
const tr = []; for (let t = 0; t <= DUR; t += .01) { const h = headAt(P, t), i = Math.floor(h); let mv = 0; for (const s of SEGS) if (t >= s.t[0] && t <= s.t[1]) mv = 1; const M = worldToScreen(camFor(t), W, H); tr.push([+t.toFixed(2), mv ? Math.round(Math.min(P.V[i], 2500)) : 0, +(M(...posAt(P, h))[0] / W).toFixed(2)]); }
window.EV = [{ t: 0, type: 'track', data: tr }]; window.DUR = DUR; window.READY = true;
