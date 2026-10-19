# 手元のHTMLファイルを指定の画面幅で撮影する（最初の画面と全体）。自作ページの見た目確認用
# 使い方: python scripts/shoot_local_html.py <HTMLのパス> <出力png> <画面幅px>
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
src, out, w = sys.argv[1], sys.argv[2], int(sys.argv[3])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": 900})
    pg.goto('file:///' + src.replace(chr(92), '/')); pg.wait_for_timeout(2500)
    pg.screenshot(path=out.replace('.png', '_fv.png'))
    pg.screenshot(path=out, full_page=True); b.close(); print('ok')
