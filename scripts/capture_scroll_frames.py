# スクロールしながら1画面ずつ撮影する（スクロールで表示が出るサイト用）
# 使い方: python scripts/capture_scroll_frames.py <出力フォルダ> 名前,URL [名前,URL ...]
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
out = sys.argv[1]; targets = [a.split(',', 1) for a in sys.argv[2:]]
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}, locale="ja-JP")
    for name, url in targets:
        try:
            pg.goto(url, wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(name, 'warn', str(e)[:60])
        pg.wait_for_timeout(3000)
        for sel in ['text=Accept', 'text=Accept all', 'text=同意', 'text=OK', 'text=Allow all']:
            try: pg.click(sel, timeout=800); break
            except Exception: pass
        h = pg.evaluate("document.body.scrollHeight"); n = 0
        for y in range(0, min(h, 14000), 850):
            pg.mouse.wheel(0, 850 if y else 0); pg.wait_for_timeout(1400)
            pg.screenshot(path=f"{out}/{name}_{n:02d}.png"); n += 1
        print(name, h, n)
    b.close()
