/* 全ページ共通のヘッダー。メニューの項目はここだけで管理する
   使い方：<header class="hd" id="hd" data-page="about"></header> の直後でこのファイルを読み込む（data-page は top / about / product / member） */
(() => {
  const hd = document.getElementById("hd"), page = hd.dataset.page || "top", top = page === "top";
  const t = top ? "" : "index.html"; // トップの中の欄へのリンク（トップではページ内移動）
  const items = [
    ["about.html", "私たちについて", "about"],
    [t + "#business", "事業"],
    ["product.html", "プロダクト", "product"],
    ["member.html", "メンバー", "member"],
    [t + "#news", "ニュース", "", "md-hide"],
    ["#contact-recruit", "採用"]
  ];
  hd.innerHTML = `<div class="in">
    <a class="logo" href="${top ? "#top" : "index.html"}" aria-label="JIL トップへ">JIL<i></i></a>
    <nav class="nav" id="nav" aria-label="メインメニュー">
      ${items.map(([h, l, p, c]) => `<a href="${h}"${c ? ` class="${c}"` : ""}${p && p === page ? ' aria-current="page"' : ""}>${l}</a>`).join("")}
      <a class="pill" href="#contact">お問い合わせ<span class="dot">→</span></a>
    </nav>
    <button class="pill menu-btn" type="button" id="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>`;

  // スクロールしたら背景を敷く（トップは最初の画面を過ぎてから）
  const hero = document.getElementById("hero");
  const onScroll = () => hd.classList.toggle("solid", scrollY > (hero ? hero.offsetHeight - 90 : 20));
  addEventListener("scroll", onScroll, { passive: true }); addEventListener("load", onScroll); onScroll();

  // スマホのメニュー
  const mb = document.getElementById("menu-btn");
  const menu = o => { hd.classList.toggle("open", o); document.body.classList.toggle("lock", o); mb.setAttribute("aria-expanded", String(o)); mb.textContent = o ? "Close" : "Menu"; };
  mb.addEventListener("click", () => menu(!hd.classList.contains("open")));
  hd.querySelectorAll(".nav a").forEach(a => a.addEventListener("click", () => menu(false)));
  addEventListener("keydown", e => { if (e.key === "Escape" && hd.classList.contains("open")) { menu(false); mb.focus(); } });
  addEventListener("resize", () => { if (innerWidth >= 720 && hd.classList.contains("open")) menu(false); });
})();
