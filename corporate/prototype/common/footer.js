/* 全ページ共通のフッター。リンクと、人の線とAIの線の動き（もとは採用の欄の動き）はここだけで管理する
   使い方：<footer class="ft" id="ft" data-page="top"></footer> の直後でこのファイルを読み込む（data-page は top / about / product / member / bizdev / recruit） */
(() => {
  const ft = document.getElementById("ft"), page = ft.dataset.page || "top";
  const t = page === "top" ? "" : "index.html", ab = page === "about" ? "" : "about.html";
  const ct = ft.dataset.contact || ""; // お問い合わせの欄がないページはトップの欄へ
  const li = (h, l, x = "") => `<li><a href="${h}"${x}>${l}</a></li>`;
  ft.innerHTML = `<canvas class="ft-cv" aria-hidden="true"></canvas>
  <div class="in">
    <div class="top">
      <dl><dt>会社名</dt><dd>株式会社JIL（JIL Inc.）</dd><dt>設立</dt><dd>2024年5月</dd><dt>所在地</dt><dd>〒150-0001 東京都渋谷区神宮前六丁目23番4号 桑野ビル2階</dd></dl>
      <div><h4>私たちについて</h4><ul>${li(ab + "#mission", "ミッション・ビジョン")}${li(ab + "#values", "行動指針")}${li(ab + "#style", "スタイル")}${li(ab + "#company", "会社概要")}</ul></div>
      <div><h4>事業</h4><ul>${li("product.html", "プロダクト")}${li("bizdev.html", "新規事業開発支援")}${li("recruit.html", "採用支援")}</ul></div>
      <div><h4>組織</h4><ul>${li("member.html", "メンバー")}${li(t + "#news", "ニュース")}${li(ct + "#contact", "事業のお問い合わせ")}${li(ct + "#contact-recruit", "採用のお問い合わせ")}</ul></div>
    </div>
    <div class="mark" aria-hidden="true">Japan Is Lovely<i>.</i></div>
    <div class="bt"><span>© 2026 JIL Inc.</span><span class="r"><a href="#" id="ft-top">Page Top ↑</a></span></div>
  </div>`;
  document.getElementById("ft-top").addEventListener("click", e => { e.preventDefault(); scrollTo({ top: 0, behavior: "smooth" }); });

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const ss = (a, b, v) => { const t = clamp((v - a) / (b - a)); return t * t * (3 - 2 * t); };
  const eo = t => 1 - Math.pow(1 - t, 3);
  const TAU = Math.PI * 2;
  const rnd = s => () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const mob = () => innerWidth < 720;
  const fit = cv => {
    const r = cv.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1, 2);
    cv.width = Math.max(1, Math.round(r.width * d)); cv.height = Math.max(1, Math.round(r.height * d));
    const ctx = cv.getContext("2d"); ctx.setTransform(d, 0, 0, d, 0, 0); return { ctx, w: r.width, h: r.height };
  };
  const bez = (P, t) => { const u = 1 - t, a = u * u * u, b = 3 * u * u * t, c = 3 * u * t * t, e = t * t * t; return [a * P[0][0] + b * P[1][0] + c * P[2][0] + e * P[3][0], a * P[0][1] + b * P[1][1] + c * P[2][1] + e * P[3][1]]; };

  /* ===== 人の線とAIの線 =====
     太い1本＝人。途中から細い線が筒状にからみつき、ねじれながら右へ伸びる＝AI */
  function Ribbon(cv, o) {
    let ctx, w, h, S = [], wMax = 0, t0 = null, mx = .5, tmx = .5, twk = 1;
    const K = 220;
    const resize = () => {
      ({ ctx, w, h } = fit(cv)); const m = mob(); const P = o.spine(w, h, m); wMax = o.width(w, h, m); twk = m ? .5 : 1; S = [];
      for (let k = 0; k <= K; k++) S.push(bez(P, k / K));
      for (let k = 0; k <= K; k++) { const a = S[Math.max(0, k - 1)], b = S[Math.min(K, k + 1)]; const dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1; S[k][2] = -dy / l; S[k][3] = dx / l; }
    };
    const pt = (k, th, tau, el) => {
      const t = k / K, env = ss(o.from, o.from + o.grow, t);
      const tw = th + t * o.twist * twk * TAU + tau * .16 + (mx - .5) * 1.4;
      const wd = wMax * env * (.78 + .22 * Math.sin(t * 5 + tau * .35));
      const off = wd * Math.sin(tw); const s = S[k];
      return [s[0] + s[2] * off, s[1] + s[3] * off, Math.cos(tw)];
    };
    const draw = now => {
      if (t0 === null) t0 = now;
      const el = reduce ? 9 : (now - t0) / 1000, tau = reduce ? 2 : el;
      const rh = eo(clamp(el / 1.5)), rf = eo(clamp((el - .8) / 2.6));
      mx += (tmx - mx) * .04;
      ctx.clearRect(0, 0, w, h);
      const n = mob() ? o.n * .7 | 0 : o.n, step = 2;
      const k0 = Math.floor(K * o.from), kEnd = Math.floor(K * (o.from + (1 - o.from) * rf));
      // 奥と手前、濃さの段階ごとにまとめて描く
      const B = [[], []].map(() => Array.from({ length: 5 }, () => new Path2D()));
      const A = [new Path2D(), new Path2D()];
      for (let i = 0; i < n; i++) {
        const th = i / n * TAU, acc = i % o.accEvery === 0;
        let prev = pt(k0, th, tau), lastP = null;
        for (let k = k0 + step; k <= kEnd; k += step) {
          const cur = pt(k, th, tau), z = (prev[2] + cur[2]) / 2, layer = z >= 0 ? 1 : 0;
          const p = acc ? A[layer] : B[layer][Math.min(4, Math.floor((Math.abs(z)) * 5))];
          // 同じ濃さが続くあいだは1本の線としてつなぐ（つなぎ目の点が縦じまに見えないように）
          if (p !== lastP) p.moveTo(prev[0], prev[1]);
          p.lineTo(cur[0], cur[1]); prev = cur; lastP = p;
        }
      }
      const fine = (layer) => {
        for (let q = 0; q < 5; q++) { ctx.strokeStyle = o.fine(layer ? .1 + q * .05 : .05 + (4 - q) * .012); ctx.lineWidth = .7; ctx.stroke(B[layer][q]); }
        ctx.strokeStyle = o.acc(layer ? .55 : .18); ctx.lineWidth = .9; ctx.stroke(A[layer]);
      };
      fine(0);
      // 人の線
      const kh = Math.floor(K * rh);
      if (kh > 1) {
        ctx.beginPath(); ctx.moveTo(S[0][0], S[0][1]);
        for (let k = 1; k <= kh; k++) ctx.lineTo(S[k][0], S[k][1]);
        ctx.strokeStyle = o.thick; ctx.lineWidth = o.thickW; ctx.lineCap = "round"; ctx.stroke();
      }
      fine(1);
      // 線の上を流れる点
      if (o.dots && rf > .2) for (let q = 0; q < 9; q++) {
        const sp = .05 + (q % 3) * .018, f = (tau * sp + q / 9) % 1, k = Math.floor(k0 + f * (K - k0));
        if (k > kEnd) continue;
        const c = pt(k, (q * 7 % o.n) / o.n * TAU, tau);
        ctx.fillStyle = o.acc(c[2] > 0 ? .9 : .3); ctx.beginPath(); ctx.arc(c[0], c[1], c[2] > 0 ? 2.4 : 1.6, 0, TAU); ctx.fill();
      }
    };
    resize();
    return { el: cv, draw, resize, point: x => { tmx = x; }, reset: () => { t0 = null; } };
  }

  const foot = Ribbon(ft.querySelector(".ft-cv"), {
    spine: (w, h, m) => m ? [[-.1 * w, .3 * h], [.3 * w, .5 * h], [.62 * w, .02 * h], [1.1 * w, .22 * h]] : [[-.04 * w, .44 * h], [.32 * w, .76 * h], [.6 * w, .2 * h], [1.04 * w, .5 * h]],
    width: (w, h, m) => m ? .08 * h : .13 * h,
    from: .16, grow: .45, twist: 1.3, n: 70, accEvery: 14, dots: false, // 線の上を流れる青い点は出さない
    fine: a => `rgba(251,251,252,${a * .9})`, acc: a => `rgba(120,140,255,${a})`, thick: "#FBFBFC", thickW: 2
  });
  // 見えているときだけ動かす
  let on = false;
  new IntersectionObserver(es => es.forEach(e => { on = e.isIntersecting; if (on) foot.reset(); }), { rootMargin: "80px" }).observe(foot.el);
  if (reduce) foot.draw(performance.now());
  else { const loop = now => { if (on && !document.hidden) foot.draw(now); requestAnimationFrame(loop); }; requestAnimationFrame(loop); }
  let rt; addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { foot.resize(); if (reduce) foot.draw(performance.now()); }, 150); });
})();
