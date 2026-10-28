# 試作ページを配色ごと（#p=名前）に撮影し、横に並べた比較画像を作る
# 使い方: python scripts/shoot_palettes.py <出力フォルダ> <配色名1> <配色名2> ...
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
S=sys.argv[1]; src='file:///C:/Users/shino/dev/261016_HPリファレンス/docs/bizdev/service/index.html'
names=sys.argv[2:]
with sync_playwright() as p:
    b=p.chromium.launch()
    for n in names:
        pg=b.new_page(viewport={"width":1440,"height":900})
        pg.goto(src+'#p='+n); pg.wait_for_timeout(1200)
        pg.evaluate("document.querySelector('.pal').style.display='none'")
        pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(2200); pg.evaluate("window.scrollTo(0,0)")
        pg.screenshot(path=f'{S}/p_{n}.png',full_page=True); pg.close()
    b.close()
ims=[Image.open(f'{S}/p_{n}.png') for n in names]
w=560; ims=[i.resize((w,int(i.height*w/i.width))) for i in ims]
h=max(i.height for i in ims)
sheet=Image.new('RGB',(w*len(names)+10*len(names),h),'white')
for k,i in enumerate(ims): sheet.paste(i,(k*(w+10),0))
sheet.save(f'{S}/sheet_v9.jpg',quality=82)
# 最初の画面だけ大きめに
fv=[Image.open(f'{S}/p_{n}.png').crop((0,0,1440,1500)).resize((720,750)) for n in names]
s2=Image.new('RGB',(730*len(names),750),'white')
for k,i in enumerate(fv): s2.paste(i,(k*730,0))
s2.save(f'{S}/fv_v9.jpg',quality=82); print('ok')
