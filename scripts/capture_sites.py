# Webサイトのファーストビュー・全体の画面写真と、フォント・色などのデザイン情報をまとめて取得する
# 使い方: python scripts/capture_sites.py <名前,URL を1行ずつ書いたテキスト> <出力フォルダ>
import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

STYLE_JS = """
() => {
  const pick = (el) => {
    if (!el) return null;
    const s = getComputedStyle(el);
    return {text: (el.innerText || '').trim().slice(0, 80), font: s.fontFamily, size: s.fontSize,
            weight: s.fontWeight, lineHeight: s.lineHeight, letterSpacing: s.letterSpacing, color: s.color};
  };
  const firstVisible = (sel) => [...document.querySelectorAll(sel)].find(e => e.offsetHeight > 0 && (e.innerText || '').trim());
  const colors = {};
  [...document.querySelectorAll('body *')].slice(0, 3000).forEach(e => {
    if (e.offsetHeight === 0) return;
    const s = getComputedStyle(e);
    [s.backgroundColor, s.color].forEach(c => {
      if (c && c !== 'rgba(0, 0, 0, 0)') colors[c] = (colors[c] || 0) + 1;
    });
  });
  const topColors = Object.entries(colors).sort((a, b) => b[1] - a[1]).slice(0, 10).map(x => x[0]);
  const fonts = [...new Set([...document.querySelectorAll('h1,h2,h3,p,a,span')].slice(0, 400)
                  .map(e => getComputedStyle(e).fontFamily))].slice(0, 8);
  return {title: document.title, h1: pick(firstVisible('h1')), h2: pick(firstVisible('h2')),
          body: pick(firstVisible('p')), bodyBg: getComputedStyle(document.body).backgroundColor,
          fonts, topColors, height: document.body.scrollHeight,
          imgCount: document.querySelectorAll('img').length, videoCount: document.querySelectorAll('video').length,
          canvasCount: document.querySelectorAll('canvas').length};
}
"""

def make_thumb(full_path, thumb_path, w=400, colh=1400):
    im = Image.open(full_path).convert('RGB')
    im = im.resize((w, int(im.height * w / im.width)))
    n = max(1, (im.height + colh - 1) // colh)
    out = Image.new('RGB', (w * n + 10 * (n - 1), colh), 'white')
    for i in range(n):
        out.paste(im.crop((0, i * colh, w, min((i + 1) * colh, im.height))), (i * (w + 10), 0))
    out.save(thumb_path, quality=80)

def main(list_file, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    targets = [l.strip().split(',', 1) for l in open(list_file, encoding='utf-8') if ',' in l and not l.startswith('#')]
    meta = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 900}, locale="ja-JP")
        for name, url in targets:
            name, url = name.strip(), url.strip()
            try:
                pg.goto(url, wait_until="networkidle", timeout=45000)
            except Exception as e:
                print(name, "load warn", str(e)[:80])
            try:
                pg.wait_for_timeout(3000)
                pg.screenshot(path=f"{out_dir}/{name}_fv.png")
                h = pg.evaluate("document.body.scrollHeight")
                for y in range(0, min(h, 20000), 700):
                    pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(200)
                pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(800)
                pg.screenshot(path=f"{out_dir}/{name}_full.png", full_page=True)
                make_thumb(f"{out_dir}/{name}_full.png", f"{out_dir}/{name}_thumb.jpg")
                meta[name] = {"url": url, **pg.evaluate(STYLE_JS)}
                print(name, "ok", h)
            except Exception as e:
                print(name, "err", str(e)[:120])
                meta[name] = {"url": url, "error": str(e)[:200]}
        b.close()
    path = f"{out_dir}/_design_meta.json"
    old = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
    old.update(meta)
    json.dump(old, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
