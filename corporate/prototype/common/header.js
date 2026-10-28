/* 全ページ共通のヘッダー。メニューの項目はここだけで管理する
   使い方：<header class="hd" id="hd" data-page="about"></header> の直後でこのファイルを読み込む（data-page は top / about / product / member） */
(() => {
  const hd = document.getElementById("hd"), page = hd.dataset.page || "top", top = page === "top";
  const t = top ? "" : "index.html"; // トップの中の欄へのリンク（トップではページ内移動）
  const ab = page === "about" ? "" : "about.html", mb_ = page === "member" ? "" : "member.html";
  const ext = ' target="_blank" rel="noopener" data-local="../../prototype/index.html"'; // 新規事業開発の支援は専用サイトを別タブで
  // [リンク先, 名前, そのページの data-page, 追加のクラス, 子メニュー[[リンク先, 名前, 追加の属性]]]
  const items = [
    ["about.html", "私たちについて", "about", "", [[ab + "#mission", "ミッション・ビジョン・バリュー"], [ab + "#style", "スタイル"], [ab + "#company", "会社概要"]]],
    [t + "#business", "事業", "", "", [["product.html", "プロダクト"], ["service.html", "新規事業開発支援", ext], [t + "#biz-3", "採用支援"]]],
    ["member.html", "メンバー", "member", "", [[mb_ + "#board", "ボードメンバー"], [mb_ + "#team", "チームメンバー"]]],
    [t + "#news", "ニュース", "", "md-hide"],
    ["#contact-recruit", "採用"]
  ];
  const sub = ks => ks ? `<div class="sub"><ul>${ks.map(([h, l, x = ""]) => `<li><a href="${h}"${x}>${l}<span class="ar" aria-hidden="true">${x ? "↗" : "→"}</span></a></li>`).join("")}</ul></div>` : "";
  hd.innerHTML = `<div class="in">
    <a class="logo" href="${top ? "#top" : "index.html"}" aria-label="JIL トップへ">JIL<i></i></a>
    <nav class="nav" id="nav" aria-label="メインメニュー">
      ${items.map(([h, l, p, c, ks]) => `<div class="grp${ks ? " has" : ""}${c ? " " + c : ""}"><a class="p" href="${h}"${p && p === page ? ' aria-current="page"' : ""}>${l}${ks ? '<i class="cv" aria-hidden="true"></i>' : ""}</a>${sub(ks)}</div>`).join("")}
      <a class="pill" href="#contact">お問い合わせ<span class="dot">→</span></a>
    </nav>
    <button class="pill menu-btn" type="button" id="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>`;
  if (location.protocol === "file:") hd.querySelectorAll("a[data-local]").forEach(a => a.href = a.dataset.local);
  // 子メニューを押したら、開いていた子メニューを閉じる（ページ内移動のあともホバーで開いたままにならないように）
  hd.querySelectorAll(".sub a").forEach(a => a.addEventListener("click", () => { const g = a.closest(".grp"); a.blur(); g.classList.add("shut"); g.addEventListener("mouseleave", () => g.classList.remove("shut"), { once: true }); }));

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
