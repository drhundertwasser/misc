// Player + timeline. Builds every segment into #stage, exposes window.__seek(t) and __duration for capture.
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const { prog, pop, easeOut, easeIn, lerp, INK, OUT } = U;
  const SCENE_D = 6.5, TITLE_D = 5, END_D = 4.5;
  const stage = document.getElementById('stage');
  const params = new URLSearchParams(location.search);
  const capture = params.get('capture') === '1';

  function mk(html) { const g = document.createElementNS(NS, 'g'); g.innerHTML = html; g.style.display = 'none'; stage.appendChild(g); return g; }

  // ── cover ──
  function buildTitle() {
    let rays = ''; for (let i = 0; i < 18; i++) { const a = i * 20; rays += `<path d="M800 450 L${800 + 1400 * Math.cos(a * Math.PI / 180)} ${450 + 1400 * Math.sin(a * Math.PI / 180)} L${800 + 1400 * Math.cos((a + 10) * Math.PI / 180)} ${450 + 1400 * Math.sin((a + 10) * Math.PI / 180)}Z" fill="${i % 2 ? '#ff7b2e' : '#ffe14d'}"/>`; }
    const cast = ['hazen', 'horowitz', 'wright', 'sarcevic', 'lehner'].map((n, i) => figure({ ...CAST[n], name: 'c' + i, x: 330 + i * 235, y: 900, scale: .62 })).join('');
    const g = mk(`<rect x="0" y="0" width="1600" height="900" fill="#ffe14d"/><g data-id="rays">${rays}</g>` +
      `<g data-id="burst" data-pivot="800 400"><path d="${burst(800, 400, 560, 470, 24)}" fill="#fff" ${OUT} stroke-width="10"/>` +
      `<text x="800" y="400" text-anchor="middle" font-family="Bangers" font-size="190" fill="#e63946" stroke="${INK}" stroke-width="10" paint-order="stroke">UNKNOWNS</text>` +
      `<text x="800" y="490" text-anchor="middle" font-family="Bangers" font-size="54" fill="${INK}" letter-spacing="3">100 QUESTIONS. 100 SCIENTISTS.</text></g>` +
      `<g data-id="tag" data-pivot="1380 130"><circle cx="1380" cy="130" r="90" fill="#e63946" ${OUT}/><text x="1380" y="118" text-anchor="middle" font-family="Bangers" font-size="40" fill="#fff">SAMPLE</text><text x="1380" y="165" text-anchor="middle" font-family="Bangers" font-size="40" fill="#fff">ISSUE</text></g>` +
      `<g data-id="num" data-pivot="220 130"><rect x="120" y="70" width="200" height="120" fill="#fff" ${OUT}/><text x="220" y="118" text-anchor="middle" font-family="Bangers" font-size="34" fill="${INK}">No. 1</text><text x="220" y="168" text-anchor="middle" font-family="Comic Neue" font-weight="700" font-size="26" fill="${INK}">11 of 100</text></g>` +
      `<g data-id="castg">${cast}</g>` +
      `<rect x="30" y="30" width="1540" height="840" fill="none" stroke="${INK}" stroke-width="10"/>`);
    const P = U.collect(g);
    return { el: g, d: TITLE_D, update(t) {
      P.rays.setAttribute('transform', `rotate(${t * 6} 800 450)`);
      U.setPop(P.burst, pop(prog(t, .2, .7)));
      U.setPop(P.tag, pop(prog(t, 1.2, 1.6))); U.setPop(P.num, pop(prog(t, 1.5, 1.9)));
      for (let i = 0; i < 5; i++) { const p = easeOut(prog(t, 2.0 + i * .2, 2.6 + i * .2)); P['c' + i].setAttribute('transform', `translate(${330 + i * 235} ${lerp(1250, 900, p)}) scale(.62)`); window.setPart(P['c' + i + '.armR'], -140 * p + Math.sin(t * 6 + i) * 8); }
      g.setAttribute('transform', `translate(${-1600 * easeIn(prog(t, TITLE_D - .5, TITLE_D))} 0)`);
    } };
  }
  function burst(cx, cy, rx, ry, n) { let d = ''; for (let i = 0; i < n * 2; i++) { const a = (i / (n * 2)) * Math.PI * 2, r = i % 2 ? .82 : 1; d += (i ? 'L' : 'M') + (cx + rx * r * Math.cos(a)) + ' ' + (cy + ry * r * Math.sin(a)); } return d + 'Z'; }

  // ── end card ──
  function buildEnd() {
    const g = mk(`<rect x="0" y="0" width="1600" height="900" fill="#111"/><rect x="30" y="30" width="1540" height="840" fill="#ffe14d" stroke="${INK}" stroke-width="10"/>` +
      `<g data-id="tbc" data-pivot="800 380"><text x="800" y="400" text-anchor="middle" font-family="Bangers" font-size="150" fill="#e63946" stroke="${INK}" stroke-width="9" paint-order="stroke">TO BE CONTINUED...</text></g>` +
      `<g data-id="more"><text x="800" y="500" text-anchor="middle" font-family="Comic Neue" font-weight="700" font-size="44" fill="${INK}">89 unknowns to go.</text></g>` +
      `<g data-id="fine"><text x="800" y="740" text-anchor="middle" font-family="Comic Neue" font-size="24" fill="${INK}">Questions from "Unknowns," The New York Times Science desk, Oct. 5, 2026.</text>` +
      `<text x="800" y="776" text-anchor="middle" font-family="Comic Neue" font-size="24" fill="${INK}">Scientists are drawn as generic figures, not likenesses of the people credited.</text></g>`);
    const P = U.collect(g);
    return { el: g, d: END_D, update(t) {
      U.setPop(P.tbc, pop(prog(t, .2, .7))); P.more.setAttribute('opacity', prog(t, 1.0, 1.5)); P.fine.setAttribute('opacity', prog(t, 1.8, 2.4));
    } };
  }

  // ── scene ──
  function buildScene(s) {
    const f = s.fig, who = { ...CAST[f.who], name: f.who, x: f.x, y: f.y, scale: f.s, mouth: f.mouth, prop: f.prop };
    const figSvg = figure(who);
    let body = s.svg();
    if (f.inBoat) body = body.replace('<g data-id="figslot" transform="translate(550 440)"></g>', `<g transform="translate(550 440)">${figSvg}</g>`); else body += figSvg;
    const tail = s.bubble.tail || (f.inBoat ? [552, 440 - 352 * f.s] : [f.x, f.y - 352 * f.s]);
    const html = `<g data-id="slide">` + body + U.frame() +
      U.caption('cap', 50, 50, s.caption) +
      U.bubble('bub', s.bubble.x, s.bubble.y, s.bubble.w, s.bubble.h, tail[0], tail[1], s.bubble.lines, { size: s.bubble.size || 34 }) +
      s.sfx.map(x => U.sfx(x.id, x.x, x.y, x.text, x)).join('') +
      U.credit('cred', s.credit[0], s.credit[1]) + `</g>`;
    const g = mk(html);
    const P = U.collect(g);
    const bubbleT = s.bubbleT || 1.3;
    return { el: g, d: SCENE_D, update(t) {
      P.slide.setAttribute('transform', `translate(${lerp(1600, 0, easeOut(prog(t, 0, .5))) - 1600 * easeIn(prog(t, SCENE_D - .5, SCENE_D))} 0)`);
      P.cap.setAttribute('transform', `translate(50 50) scale(1 ${pop(prog(t, .45, .8))})`);
      U.setPop(P.bub, pop(prog(t, bubbleT, bubbleT + .4)));
      s.sfx.forEach(x => U.setPop(P[x.id], pop(prog(t, x.t, x.t + .3)) * (1 - easeIn(prog(t, x.t + 1.6, x.t + 2.1)))));
      P.cred.setAttribute('transform', `translate(0 ${lerp(120, 0, easeOut(prog(t, 4.6, 5.0)))})`);
      s.update(t, P);
    } };
  }

  const segs = [buildTitle(), ...SCENES.map(buildScene), buildEnd()];
  let starts = [], acc = 0; segs.forEach(s => { starts.push(acc); acc += s.d; });
  const DURATION = acc;
  let current = -1;
  function seek(t) {
    t = Math.max(0, Math.min(DURATION - 1e-3, t));
    let i = segs.length - 1; while (i > 0 && starts[i] > t) i--;
    if (i !== current) { segs.forEach((s, k) => s.el.style.display = k === i ? '' : 'none'); current = i; }
    segs[i].update(t - starts[i]);
    return t;
  }
  window.__seek = seek; window.__duration = DURATION;

  // ── playback UI ──
  let playing = false, t0 = 0, tStart = 0, cur = 0;
  const ui = document.getElementById('ui'), btn = document.getElementById('play'), rng = document.getElementById('scrub'), tm = document.getElementById('time');
  rng.max = DURATION;
  function frame(now) { if (!playing) return; cur = t0 + (now - tStart) / 1000; if (cur >= DURATION) { cur = DURATION - 1e-3; playing = false; btn.textContent = '▶'; } seek(cur); rng.value = cur; tm.textContent = cur.toFixed(1) + ' / ' + DURATION.toFixed(1) + 's'; if (playing) requestAnimationFrame(frame); }
  function play() { if (cur >= DURATION - 1e-2) cur = 0; playing = true; btn.textContent = '❚❚'; t0 = cur; tStart = performance.now(); requestAnimationFrame(frame); }
  function pause() { playing = false; btn.textContent = '▶'; }
  btn.onclick = () => playing ? pause() : play();
  rng.oninput = () => { pause(); cur = Number(rng.value); seek(cur); tm.textContent = cur.toFixed(1) + ' / ' + DURATION.toFixed(1) + 's'; };
  document.addEventListener('keydown', e => { if (e.code === 'Space') { e.preventDefault(); playing ? pause() : play(); } if (e.code === 'ArrowRight') { pause(); cur = Math.min(DURATION - 1e-3, cur + (e.shiftKey ? 6.5 : .5)); seek(cur); rng.value = cur; } if (e.code === 'ArrowLeft') { pause(); cur = Math.max(0, cur - (e.shiftKey ? 6.5 : .5)); seek(cur); rng.value = cur; } });
  function fit() { const s = Math.min(window.innerWidth / 1600, (window.innerHeight - (capture ? 0 : 60)) / 900); document.getElementById('wrap').style.transform = `scale(${s})`; }
  window.addEventListener('resize', fit); fit();
  if (capture) ui.style.display = 'none';
  cur = Number(params.get('t') || 0); seek(cur); rng.value = cur;
  if (params.get('autoplay') === '1') document.fonts.ready.then(play);
})();
