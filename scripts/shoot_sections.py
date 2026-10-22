# 試作ページを欄ごと（コンセプト・特徴・流れ・AI・ご相談）に撮影する。固定ヘッダーは隠し、動きは止めた状態で撮る。資料に貼る画像用
# 使い方: python scripts/shoot_sections.py <HTMLの絶対パス> <出力フォルダ>
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
src, outdir = sys.argv[1], sys.argv[2]
url = 'file:///' + src.replace(chr(92), '/')
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion='reduce')
    pg.goto(url); pg.wait_for_timeout(2000)
    pg.screenshot(path=f'{outdir}/page_pc_fv.png')
    pg.add_style_tag(content='header.hd,a.skip{display:none!important}')
    pg.evaluate('document.querySelectorAll("body *").forEach(e=>{const p=getComputedStyle(e).position;if(p=="fixed"||p=="sticky")e.style.setProperty("visibility","hidden","important")})')
    for sid in ['concept', 'feature', 'flow', 'ai', 'contact']:
        el = pg.locator(f'#{sid}'); el.scroll_into_view_if_needed(); pg.wait_for_timeout(800)
        el.screenshot(path=f'{outdir}/page_pc_{sid}.png')
    pg.evaluate('document.querySelectorAll("style").forEach(s=>{if(s.textContent.includes("header.hd,a.skip"))s.remove()});window.scrollTo(0,0)'); pg.wait_for_timeout(500)
    pg.screenshot(path=f'{outdir}/page_pc_full.png', full_page=True)
    sp = b.new_page(viewport={"width": 390, "height": 844}, reduced_motion='reduce', device_scale_factor=2)
    sp.goto(url); sp.wait_for_timeout(2000)
    sp.screenshot(path=f'{outdir}/page_sp_fv.png')
    b.close(); print('ok')
