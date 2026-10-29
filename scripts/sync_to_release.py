# 制作フォルダの docs/ を本番フォルダ（GitHub: JIL-inc-development/corporate_site）へ写す。
# 写すときに、ロゴの帯を外す・住所を本番用に直す・GTMを入れる・旧ページの転送とsitemapを作る
# 使い方: python scripts/sync_to_release.py [本番フォルダ]（省略時は C:\Users\shino\Release\corporate_site）
import sys, os, re, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')
DST = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\shino\Release\corporate_site'
SITE = 'https://jilinc.co.jp/'
TEST_SITE = 'https://shinohara-jil.github.io/jil-bizdev-page/'
GTM_ID = 'GTM-MJ5MSNVB'

# 本番フォルダで残すもの（自動公開の設定など）。それ以外は消してから写し直す
KEEP = {'.git', '.github', 'README.md', 'robots.txt'}
# 写さないもの（テスト公開用・掲載許可待ち）
SKIP = {'prototype', '.nojekyll', os.path.join('bizdev', 'service', 'logos')}

PAGES = ['', 'about/', 'product/', 'member/', 'bizdev/', 'bizdev/service/', 'recruit/']

GTM_HEAD = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
"""
GTM_BODY = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""

REDIRECT = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- 旧サイトの住所（/client-solution/）。新サイトでは新規事業開発支援（/bizdev/）に当たるので、そこへ自動で移動する -->
<meta http-equiv="refresh" content="0; url=/bizdev/">
<link rel="canonical" href="https://jilinc.co.jp/bizdev/">
<meta name="robots" content="noindex">
<title>移動しました｜株式会社JIL</title>
<script>location.replace("/bizdev/" + location.hash);</script>
</head>
<body>
<p>このページは移動しました。<a href="/bizdev/">新規事業開発支援のページへ</a></p>
</body>
</html>
"""


def must_sub(pattern, repl, text, label, flags=0):
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        sys.exit(f'止めました：「{label}」の場所が見つかりません。元のページの形が変わった可能性があります')
    return new


def add_gtm(html):
    if GTM_ID in html:
        return html
    html = must_sub(r'(<head[^>]*>\n)', lambda m: m.group(1) + GTM_HEAD, html, 'GTMを入れる場所（head）')
    if re.search(r'<body[^>]*>\n', html):
        return must_sub(r'(<body[^>]*>\n)', lambda m: m.group(1) + GTM_BODY, html, 'GTMを入れる場所（body）')
    # <body> を省略しているページは、本文の最初の要素の直前に入れる
    return must_sub(r'^(?=<(header|a|div|main|section|nav)\b)', GTM_BODY, html, 'GTMを入れる場所（本文の先頭）', re.M)


def remove_logos(html):
    # ご支援企業のロゴの帯は、掲載許可が取れるまで本番では外す
    html = must_sub(r'<div class="clients-band">.*?\n</div>\n\n', '', html, 'ロゴの帯', re.S)
    return must_sub(r'@media \(min-width:901px\)\{\.hero\{min-height:max\(560px,calc\(100svh - 101px\)\)\}\}',
                    '@media (min-width:901px){.hero{min-height:max(560px,100svh)}}', html, '最初の画面の高さ')


# 1. 本番フォルダを片付ける
if not os.path.isdir(os.path.join(DST, '.git')):
    sys.exit(f'止めました：{DST} は本番フォルダ（gitの管理下）ではありません')
for name in os.listdir(DST):
    if name in KEEP:
        continue
    p = os.path.join(DST, name)
    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

# 2. docs/ を写す
src_root = os.path.abspath(SRC)
def ignore(d, names):
    rel = os.path.relpath(d, src_root)
    return [n for n in names if os.path.normpath(os.path.join(rel, n)) in SKIP]
shutil.copytree(src_root, DST, ignore=ignore, dirs_exist_ok=True)

# 3. ページを本番用に直す
for root, _, files in os.walk(DST):
    if '.git' in root.split(os.sep):
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        p = os.path.join(root, f)
        html = open(p, encoding='utf-8').read()
        html = html.replace(TEST_SITE, SITE)
        if os.path.normpath(os.path.relpath(p, DST)) == os.path.join('bizdev', 'service', 'index.html'):
            html = remove_logos(html)
        html = add_gtm(html)
        open(p, 'w', encoding='utf-8', newline='\n').write(html)

# 4. 旧ページの転送と sitemap
os.makedirs(os.path.join(DST, 'client-solution'), exist_ok=True)
open(os.path.join(DST, 'client-solution', 'index.html'), 'w', encoding='utf-8', newline='\n').write(REDIRECT)
today = datetime.date.today().isoformat()
urls = ''.join(f'  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n' for p in PAGES)
open(os.path.join(DST, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

print(f'写しました：{src_root} → {DST}')
