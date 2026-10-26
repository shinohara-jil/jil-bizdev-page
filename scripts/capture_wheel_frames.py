# 画面が固定されたまま中身が切り替わるサイトを、ホイール操作で12コマ撮って縦につなぐ（*_full.png を作る）
# 使い方: python scripts/capture_wheel_frames.py <出力フォルダ> 名前,URL [名前,URL ...]
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
out = sys.argv[1]; targets = [a.split(',', 1) for a in sys.argv[2:]]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}, locale="ja-JP")
    for name, url in targets:
        try: pg.goto(url, wait_until="networkidle", timeout=60000)
        except Exception as e: print(name, 'warn', str(e)[:60])
        pg.wait_for_timeout(4000); pg.mouse.move(720, 450)
        frames = []
        for i in range(12):
            if i: pg.mouse.wheel(0, 900); pg.wait_for_timeout(1500)
            f = f"{out}/{name}_w{i:02d}.png"; pg.screenshot(path=f); frames.append(f)
        ims = [Image.open(f) for f in frames]
        full = Image.new('RGB', (1440, 900 * len(ims)), 'white')
        for i, im in enumerate(ims): full.paste(im.convert('RGB'), (0, 900 * i))
        full.save(f"{out}/{name}_full.png"); print(name, 'ok')
    b.close()
