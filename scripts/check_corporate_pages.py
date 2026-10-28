# 使い方: docs/ で python -m http.server 8765 を起動してから python scripts/check_corporate_pages.py <出力フォルダ>
# 各ページをPC幅・スマホ幅で撮影し、スマホのメニューを途中までスクロールしてから開いたときの状態を調べる
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8765/"
OUT = sys.argv[1] if len(sys.argv) > 1 else "shots"
PAGES = ["", "about/", "product/", "member/", "bizdev/", "recruit/"]
SHOW = ".js .rise:not(.in-view){transform:none!important;opacity:1!important}"
import os
os.makedirs(OUT, exist_ok=True)

def name(p):
    return (p.strip("/") or "top").replace("/", "_")

with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    report = {}
    for vw, vh, tag, mobile in [(1440, 900, "pc", False), (390, 844, "sp", True)]:
        ctx = b.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
        for p in PAGES:
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.goto(BASE + p, wait_until="networkidle")
            pg.wait_for_timeout(2200)
            pg.screenshot(path=f"{OUT}/{name(p)}_{tag}_fv.png")
            # 横はみ出し
            ov = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
            r = {"overflowX": ov, "errors": errs}
            if mobile:
                # 途中までスクロールしてからメニューを開く
                pg.evaluate("scrollTo(0, 1600)"); pg.wait_for_timeout(600)
                pg.click("#menu-btn"); pg.wait_for_timeout(700)
                r["menu_after_scroll"] = pg.evaluate("(() => { const n = document.getElementById('nav').getBoundingClientRect(); const h = document.getElementById('hd'); return { top: n.top, height: n.height, hdSolid: h.classList.contains('solid'), backdrop: getComputedStyle(h).backdropFilter }; })()")
                pg.screenshot(path=f"{OUT}/{name(p)}_{tag}_menu_scrolled.png")
                pg.click("#menu-btn"); pg.wait_for_timeout(400)
                pg.evaluate("scrollTo(0, 0)"); pg.wait_for_timeout(600)
                pg.click("#menu-btn"); pg.wait_for_timeout(700)
                r["menu_at_top"] = pg.evaluate("(() => { const n = document.getElementById('nav').getBoundingClientRect(); return { top: n.top, height: n.height }; })()")
                pg.screenshot(path=f"{OUT}/{name(p)}_{tag}_menu_top.png")
                pg.click("#menu-btn"); pg.wait_for_timeout(300)
            pg.add_style_tag(content=SHOW)
            # 下まで流して、スクロール連動の処理を一通り動かす
            h = pg.evaluate("document.body.scrollHeight")
            for y in range(0, h, 500):
                pg.evaluate(f"scrollTo(0,{y})"); pg.wait_for_timeout(60)
            pg.wait_for_timeout(800)
            pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(400)
            pg.screenshot(path=f"{OUT}/{name(p)}_{tag}_full.png", full_page=True)
            r["height"] = h
            report[f"{name(p)}_{tag}"] = r
            pg.close()
        ctx.close()
    b.close()
    print(json.dumps(report, ensure_ascii=False, indent=1))
