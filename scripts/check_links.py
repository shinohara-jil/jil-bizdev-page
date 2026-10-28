# 使い方: docs/ で python -m http.server 8765 を起動してから実行
# 全ページのリンクを集め、行き先のページが開けるか・#の欄が実在するかを確かめる
import sys, json, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
BASE = "http://127.0.0.1:8765/"
PAGES = ["", "about/", "product/", "member/", "bizdev/", "recruit/"]
bad, ext = [], set()
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    ids = {}
    for p in PAGES:
        pg.goto(BASE + p, wait_until="networkidle")
        ids[BASE + p] = set(pg.evaluate("[...document.querySelectorAll('[id]')].map(e => e.id)"))
    for p in PAGES:
        pg.goto(BASE + p, wait_until="networkidle")
        hrefs = pg.evaluate("[...document.querySelectorAll('a[href]')].map(a => [a.href, a.textContent.trim().slice(0,20), a.target])")
        for h, t, tg in hrefs:
            u = urllib.parse.urldefrag(h)
            if not h.startswith(BASE):
                ext.add((h[:70], tg)); continue
            if u.url.rstrip("/") + "/" not in [k.rstrip("/") + "/" for k in ids] and u.url not in ids:
                if "service" not in u.url: bad.append((p, h, t, "page?"))
                continue
            key = u.url if u.url in ids else u.url.rstrip("/") + "/"
            if u.fragment and key in ids and u.fragment not in ids[key]:
                bad.append((p, h, t, "no id"))
    b.close()
print("BAD:", json.dumps(bad, ensure_ascii=False, indent=0))
print("EXTERNAL:"); [print(" ", e) for e in sorted(ext)]
