# capture_scroll_frames.py で撮った画面を、サイトごとに3列の一覧画像にまとめる
# 使い方: python scripts/make_contact_sheet.py <フォルダ> 名前 [名前 ...]
import sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
d = sys.argv[1]
for name in sys.argv[2:]:
    fs = sorted(glob.glob(f"{d}/{name}_[0-9][0-9].png")); cw, chh, cols = 640, 400, 3
    rows = (len(fs) + cols - 1) // cols
    sh = Image.new('RGB', (cols * cw + (cols - 1) * 8, rows * chh + (rows - 1) * 8), 'white')
    for i, f in enumerate(fs):
        im = Image.open(f).convert('RGB').resize((cw, chh))
        sh.paste(im, ((i % cols) * (cw + 8), (i // cols) * (chh + 8)))
    sh.save(f"{d}/{name}_sheet.jpg", quality=82); print(name, sh.size)
