/* 全ページ共通のヘッダー。メニューの項目はここだけで管理する
   使い方：<header class="hd" id="hd" data-page="about"></header> の直後でこのファイルを読み込む（data-page は top / about / product / member / bizdev / recruit。お問い合わせの欄がないページは data-contact も付ける）
   ページの置き場所：トップは docs/index.html、ほかは docs/about/index.html のように「名前のフォルダ/index.html」 */
(() => {
  const hd = document.getElementById("hd"), page = hd.dataset.page || "top", top = page === "top";
  const R = top ? "" : "../"; // サイトの一番上（docs/）への道のり
  const t = top ? "" : R; // トップの中の欄へのリンク（トップではページ内移動）
  const ab = page === "about" ? "" : R + "about/", mb_ = page === "member" ? "" : R + "member/";
  const ct = hd.hasAttribute("data-contact") ? R : ""; // お問い合わせの欄がないページ（data-contact）はトップの欄へ
  // [リンク先, 名前, そのページの data-page, 追加のクラス, 子メニュー[[リンク先, 名前, 追加の属性]]]
  const items = [
    [R + "about/", "私たちについて", "about", "", [[ab + "#mission", "ミッション・ビジョン"], [ab + "#values", "行動指針"], [ab + "#style", "スタイル"], [ab + "#company", "会社概要"]]],
    [t + "#business", "事業", "", "", [[R + "product/", "プロダクト"], [R + "bizdev/", "新規事業開発支援"], [R + "recruit/", "採用支援"]]],
    [R + "member/", "メンバー", "member", "", [[mb_ + "#board", "ボードメンバー"], [mb_ + "#team", "チームメンバー"]]],
    [t + "#news", "ニュース", "", "md-hide"],
    [ct + "#contact-recruit", "採用"]
  ];
  const sub = ks => ks ? `<div class="sub"><ul>${ks.map(([h, l, x = ""]) => `<li><a href="${h}"${x}>${l}<span class="ar" aria-hidden="true">${x ? "↗" : "→"}</span></a></li>`).join("")}</ul></div>` : "";
  hd.innerHTML = `<div class="in">
    <a class="logo" href="${top ? "#top" : R}" aria-label="JIL トップへ">JIL<i></i></a>
    <nav class="nav" id="nav" aria-label="メインメニュー">
      ${items.map(([h, l, p, c, ks]) => `<div class="grp${ks ? " has" : ""}${c ? " " + c : ""}"><a class="p" href="${h}"${p && p === page ? ' aria-current="page"' : ""}>${l}${ks ? '<i class="cv" aria-hidden="true"></i>' : ""}</a>${sub(ks)}</div>`).join("")}
      <a class="pill" href="${ct}#contact">お問い合わせ<span class="dot">→</span></a>
    </nav>
    <button class="pill menu-btn" type="button" id="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>`;
  // 手元のファイルで開いたときは、フォルダへのリンク（about/ など）の先に index.html を足す（公開版ではフォルダだけで開く）
  if (location.protocol === "file:") addEventListener("DOMContentLoaded", () => document.querySelectorAll("a[href]").forEach(a => {
    const [p, x] = a.getAttribute("href").split("#");
    if (p && !/^[a-z]+:/i.test(p) && (p.endsWith("/") || p === "." || p === "..")) a.setAttribute("href", p.replace(/\/?$/, "/") + "index.html" + (x !== undefined ? "#" + x : ""));
  }));
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
