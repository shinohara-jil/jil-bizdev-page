/* 全ページ共通のヘッダー。メニューの項目はここだけで管理する
   使い方：<header class="hd" id="hd" data-page="about"></header> の直後でこのファイルを読み込む（data-page は top / about / product / member / bizdev / recruit。お問い合わせの欄がないページは data-contact も付ける）
   ページの置き場所：トップは docs/index.html、ほかは docs/about/index.html のように「名前のフォルダ/index.html」 */
(() => {
  const hd = document.getElementById("hd"), page = hd.dataset.page || "top", top = page === "top";
  const R = top ? "" : "../"; // サイトの一番上（docs/）への道のり
  const t = top ? "" : R; // トップの中の欄へのリンク（トップではページ内移動）
  const ab = page === "about" ? "" : R + "about/", mb_ = page === "member" ? "" : R + "member/";
  const ct = hd.hasAttribute("data-contact") ? R : ""; // お問い合わせの欄がないページ（data-contact）はトップの欄へ
  const biz = ["product", "bizdev", "recruit"];
  // [リンク先, 名前, そのページの data-page, 追加のクラス, 子メニュー[[リンク先, 名前, そのページの data-page]]]
  const items = [
    [R + "about/", "私たちについて", "about", "", [[ab + "#mission", "ミッション・ビジョン"], [ab + "#values", "行動指針"], [ab + "#style", "スタイル"], [ab + "#company", "会社概要"]]],
    [t + "#business", "事業", biz, "", [[R + "product/", "プロダクト", "product"], [R + "bizdev/", "新規事業開発支援", "bizdev"], [R + "recruit/", "採用支援", "recruit"]]],
    [R + "member/", "メンバー", "member", "", [[mb_ + "#board", "ボードメンバー"], [mb_ + "#team", "チームメンバー"]]],
    [t + "#news", "ニュース", "", "md-hide"],
    [ct + "#contact-recruit", "採用"]
  ];
  // 今いるページ：そのページ自身は aria-current="page"、事業の3ページにいるときの「事業」は aria-current="true"
  const cur = p => !p ? "" : p === page ? ' aria-current="page"' : Array.isArray(p) && p.includes(page) ? ' aria-current="true"' : "";
  const sub = ks => ks ? `<div class="sub"><ul>${ks.map(([h, l, p]) => `<li><a href="${h}"${cur(p)}>${l}<span class="ar" aria-hidden="true">→</span></a></li>`).join("")}</ul></div>` : "";
  hd.insertAdjacentHTML("beforebegin", `<a class="skip" href="#main">本文へ移動</a>`);
  hd.innerHTML = `<div class="in">
    <a class="logo" href="${top ? "#top" : R}" aria-label="JIL トップへ">JIL<i></i></a>
    <nav class="nav" id="nav" aria-label="メインメニュー">
      ${items.map(([h, l, p, c, ks]) => `<div class="grp${ks ? " has" : ""}${c ? " " + c : ""}"><a class="p" href="${h}"${cur(p)}>${l}${ks ? '<i class="cv" aria-hidden="true"></i>' : ""}</a>${sub(ks)}</div>`).join("")}
      <a class="pill" href="${ct}#contact">お問い合わせ<span class="dot" aria-hidden="true">→</span></a>
      <p class="m-note"><b>Japan Is Lovely<i>.</i></b>株式会社JIL　東京都渋谷区神宮前</p>
    </nav>
    <button class="pill menu-btn" type="button" id="menu-btn" aria-expanded="false" aria-controls="nav"><span class="hd-mlb">Menu</span><i class="bars" aria-hidden="true"></i></button>
    <i class="hd-pg" aria-hidden="true"></i>
  </div>`;
  // 本文へ移動の行き先（main に id がなければ付ける。ヘッダーの時点では本文がまだ読み込まれていないので、読み込み後に）
  addEventListener("DOMContentLoaded", () => { const m = document.querySelector("main"); if (!m) return; if (!m.id) m.id = "main"; hd.previousElementSibling.setAttribute("href", "#" + (top ? "about" : m.id)); });
  // 手元のファイルで開いたときは、フォルダへのリンク（about/ など）の先に index.html を足す（公開版ではフォルダだけで開く）
  if (location.protocol === "file:") addEventListener("DOMContentLoaded", () => document.querySelectorAll("a[href]").forEach(a => {
    const [p, x] = a.getAttribute("href").split("#");
    if (p && !/^[a-z]+:/i.test(p) && (p.endsWith("/") || p === "." || p === "..")) a.setAttribute("href", p.replace(/\/?$/, "/") + "index.html" + (x !== undefined ? "#" + x : ""));
  }));
  // 子メニューを押したら、開いていた子メニューを閉じる（ページ内移動のあともホバーで開いたままにならないように）
  hd.querySelectorAll(".sub a").forEach(a => a.addEventListener("click", () => { const g = a.closest(".grp"); a.blur(); g.classList.add("shut"); g.addEventListener("mouseleave", () => g.classList.remove("shut"), { once: true }); }));

  // スクロールしたら背景を敷く（トップは最初の画面を過ぎてから）。あわせて、読み進み具合の線を伸ばす
  const hero = document.getElementById("hero"), pg = hd.querySelector(".hd-pg");
  let ticking = false;
  const onScroll = () => {
    ticking = false;
    if (hd.classList.contains("open")) return;
    hd.classList.toggle("solid", scrollY > (hero ? hero.offsetHeight - 90 : 20));
    const max = document.documentElement.scrollHeight - innerHeight;
    pg.style.setProperty("--pg", max > 0 ? Math.min(1, scrollY / max).toFixed(4) : 0);
  };
  addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener("load", onScroll); addEventListener("resize", onScroll); onScroll();

  // スマホのメニュー
  const mb = document.getElementById("menu-btn"), lb = mb.querySelector(".hd-mlb");
  hd.querySelectorAll(".nav > *").forEach((el, i) => el.style.setProperty("--i", i));
  // 開いているあいだは後ろのページを止める。iPhone では overflow: hidden だけでは止まらないので、本文を今の位置のまま固定する
  let sy = 0;
  const others = () => [document.querySelector("main"), document.getElementById("ft"), document.querySelector(".nx")].filter(Boolean);
  const menu = o => {
    if (o === hd.classList.contains("open")) return;
    const b = document.body;
    if (o) {
      sy = scrollY;
      b.style.position = "fixed"; b.style.top = -sy + "px"; b.style.left = "0"; b.style.right = "0";
    } else {
      b.style.position = b.style.top = b.style.left = b.style.right = "";
      scrollTo({ top: sy, behavior: "instant" });
    }
    hd.classList.toggle("open", o); b.classList.toggle("lock", o);
    // 開いているあいだは、メニューの外（本文・フッター）にキーボードや読み上げが移らないように
    others().forEach(el => el.inert = o);
    mb.setAttribute("aria-expanded", String(o)); mb.setAttribute("aria-label", o ? "メニューを閉じる" : "メニューを開く"); lb.textContent = o ? "Close" : "Menu";
    if (o) { hd.classList.add("solid"); const f = hd.querySelector(".nav a"); f && f.focus({ preventScroll: true }); } else onScroll();
  };
  mb.setAttribute("aria-label", "メニューを開く");
  mb.addEventListener("click", () => menu(!hd.classList.contains("open")));
  hd.querySelectorAll(".nav a").forEach(a => a.addEventListener("click", () => menu(false)));
  addEventListener("keydown", e => {
    if (!hd.classList.contains("open")) return;
    if (e.key === "Escape") { menu(false); mb.focus(); }
    // Tab でメニューの中を一周する（最後の次はボタンへ戻る）
    if (e.key === "Tab") {
      const fs = [mb, ...hd.querySelectorAll(".nav a")], i = fs.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); fs[fs.length - 1].focus(); }
      else if (!e.shiftKey && i === fs.length - 1) { e.preventDefault(); fs[0].focus(); }
    }
  });
  addEventListener("resize", () => { if (innerWidth > 720 && hd.classList.contains("open")) menu(false); });
})();
