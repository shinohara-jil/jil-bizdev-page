/* 下層ページ共通の冒頭の線：大きな英字の見出し（About. など）のピリオドから人の線（墨）が伸び、途中からAIの細い線（青・灰）が分かれて広がる
   使い方：.ph-top の中に <div class="ph-bg ph-lines" aria-hidden="true"><canvas></canvas></div> を置き、ページの最後でこのファイルを読み込む */
(() => {
  const hero = document.querySelector(".ph-top"), cv = hero && hero.querySelector(".ph-lines canvas"), period = hero && hero.querySelector(".en-t i");
  if (!cv || !period) return;
  cv.style.cssText = "position:absolute;inset:0;width:100%;height:100%";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const mob = () => innerWidth < 720;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const ss = (a, b, v) => { const t = clamp((v - a) / (b - a)); return t * t * (3 - 2 * t); };
  const eo = t => 1 - Math.pow(1 - t, 3);
  const fit = () => { const r = cv.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1, 2); cv.width = Math.max(1, Math.round(r.width * d)); cv.height = Math.max(1, Math.round(r.height * d)); const c = cv.getContext("2d"); c.setTransform(d, 0, 0, d, 0, 0); return { c, w: r.width, h: r.height }; };
  const INK = a => `rgba(14,16,19,${a})`, BLUE = a => `rgba(45,68,224,${a})`;

  // [分かれる位置, 広がり（マイナスは上へ）, 青か]
  const BR = [[.05, -.48, 1], [.11, -.24, 0], [.17, .24, 0], [.24, -.6, 0], [.31, .42, 1], [.39, -.36, 0], [.47, .12, 0], [.56, -.5, 1], [.64, .3, 0]];
  // スマホはピリオドから右端までが短いので、本数を減らし、早めに分かれて上下へ小さく広がる形にする（急に跳ね上がって絡まって見えないように）
  const BR_SP = [[.08, -.55, 1], [.16, .5, 0], [.26, -.25, 0], [.36, .85, 1], [.46, -.85, 0], [.56, .2, 0]];
  const draw = (c, w, h, t, p) => {
    // 起点はピリオドの点の中心（文字の箱の下寄り）
    const r = period.getBoundingClientRect(), hr = hero.getBoundingClientRect(), m = mob();
    const ox = r.left + r.width / 2 - hr.left, oy = r.top + r.height * .755 - hr.top, L = w - ox, X = ox + (L + 20) * p;
    // 広がりの大きさ。スマホはごく控えめに。タブレット幅では上のメニューにかからない高さまでに抑える
    const S = m ? Math.min(L * .2, 32) : Math.min(h * .42, 250, oy - 90);
    const main = m
      ? u => oy - S * .12 * ss(0, 1, u) + S * .04 * Math.sin(u * 4 + t * .4) * ss(0, .3, u)
      : u => oy - S * .35 * ss(0, 1, u) + S * .05 * Math.sin(u * 5 + t * .4) * ss(0, .2, u);
    c.clearRect(0, 0, w, h);
    (m ? BR_SP : BR).forEach(([u0, sp, blue], k) => {
      const x0 = ox + L * u0; if (x0 > X) return;
      c.beginPath();
      for (let x = x0; x <= X; x += 5) {
        const u = (x - ox) / L, v = (u - u0) / (1 - u0);
        const y = main(u) + S * sp * ss(0, 1, v) + S * .035 * Math.sin(v * 4 + t * .5 + k) * v;
        x === x0 ? c.moveTo(x, y) : c.lineTo(x, y);
      }
      c.strokeStyle = blue ? BLUE(.7) : INK(.26); c.lineWidth = blue ? .9 : .8; c.stroke();
    });
    c.beginPath();
    for (let x = ox; x <= X; x += 5) { const y = main((x - ox) / L); x === ox ? c.moveTo(x, y) : c.lineTo(x, y); }
    c.strokeStyle = INK(.92); c.lineWidth = 1.6; c.lineCap = "round"; c.stroke();
  };

  let F = fit(), tShow = performance.now(), on = true;
  const frame = now => { const { c, w, h } = F; draw(c, w, h, reduce ? 20 : now / 1000, reduce ? 1 : eo(clamp((now - tShow) / 2600))); };
  new IntersectionObserver(es => es.forEach(e => { on = e.isIntersecting; })).observe(hero);
  // 書体が読み込まれるとピリオドの位置が変わるので、測り直して線を伸ばし直す
  document.fonts && document.fonts.ready.then(() => { F = fit(); tShow = performance.now(); if (reduce) frame(0); });
  if (reduce) frame(0);
  else { const loop = now => { if (on && !document.hidden) frame(now); requestAnimationFrame(loop); }; requestAnimationFrame(loop); }
  let rt; addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { F = fit(); if (reduce) frame(0); }, 150); });
})();
