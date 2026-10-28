# 使い方: docs/ で python -m http.server 8765 を起動し、final/ フォルダを作ってから実行
# スマホのメニュー：途中までスクロールして開く／閉じると元の位置に戻る／メニューのリンクで移動できる、を全ページで確かめる
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
BASE = "http://127.0.0.1:8765/"
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    for p in ["", "about/", "product/", "member/", "bizdev/", "recruit/"]:
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + p, wait_until="networkidle"); pg.wait_for_timeout(500)
        pg.evaluate("scrollTo({top: 2200, behavior: 'instant'})"); pg.wait_for_timeout(500)
        y0 = pg.evaluate("scrollY")
        pg.tap("#menu-btn"); pg.wait_for_timeout(900)
        nav = pg.evaluate("(() => { const r = document.getElementById('nav').getBoundingClientRect(); return [Math.round(r.top), Math.round(r.height)]; })()")
        inert = pg.evaluate("document.querySelector('main').inert")
        focus = pg.evaluate("document.activeElement.textContent.trim().slice(0,10)")
        name = (p.strip('/') or 'top')
        pg.screenshot(path=f"final/menu_{name}.png")
        pg.tap("#menu-btn"); pg.wait_for_timeout(500)
        y1 = pg.evaluate("scrollY")
        # メニューから「ニュース」（トップの欄）へ
        pg.tap("#menu-btn"); pg.wait_for_timeout(700)
        pg.click("#nav a[href$='#news']"); pg.wait_for_timeout(1800)
        url = pg.evaluate("location.pathname + location.hash"); ny = pg.evaluate("Math.round(document.getElementById('news') ? document.getElementById('news').getBoundingClientRect().top : -1)")
        print(json.dumps({"page": name, "navTopHeight": nav, "mainInert": inert, "focus": focus, "scrollBefore": y0, "scrollAfterClose": y1, "newsLink": url, "newsTop": ny, "errors": errs}, ensure_ascii=False))
        pg.close()
    b.close()
