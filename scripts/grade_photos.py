# 写真の色調を統一する（素材写真を差し替えたときも同じ加工をかける）
#   warm : 暖かく・少し暗め・彩度控えめ・薄い粒子（v2で使用）
#   mono : 暖かいセピア寄りのモノクロ（ダブルトーン）＋薄い粒子（v3で使用）
#   natural : カラーのまま、彩度とコントラストを少し抑えて落ち着かせる（v4で使用）
# 使い方: python scripts/grade_photos.py <入力画像> <出力画像> [横幅px] [warm|mono|natural]
import sys, random
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageEnhance, ImageOps

def add_grain(im, amount=0.035):
    random.seed(1)
    noise = Image.effect_noise(im.size, 18).convert('RGB')
    return Image.blend(im, noise, amount)

def grade_warm(im):
    im = ImageEnhance.Color(im).enhance(0.78)
    im = ImageEnhance.Brightness(im).enhance(0.93)
    im = ImageEnhance.Contrast(im).enhance(0.94)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.04 + 4)))
    b = b.point(lambda v: int(v * 0.90))
    im = Image.merge('RGB', (r, g, b))
    return im.point(lambda v: int(14 + v * (236 / 255)))

def grade_mono(im):
    g = ImageOps.grayscale(im)
    g = ImageOps.autocontrast(g, cutoff=1)
    g = ImageEnhance.Contrast(g).enhance(1.05)
    # 影は暖かい墨色、明るい部分は生成り色に寄せる
    return ImageOps.colorize(g, black=(30, 27, 24), mid=(128, 118, 106), white=(241, 236, 228))

def grade_natural(im):
    im = ImageEnhance.Color(im).enhance(0.84)
    im = ImageEnhance.Contrast(im).enhance(0.96)
    return im.point(lambda v: int(6 + v * (247 / 255)))  # 黒をわずかに持ち上げる

def grade(src, dst, width=2000, mode='warm'):
    im = Image.open(src).convert('RGB')
    if im.width > width:
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    im = {'mono': grade_mono, 'natural': grade_natural}.get(mode, grade_warm)(im)
    im = add_grain(im, {'mono': 0.04, 'natural': 0.02}.get(mode, 0.035))
    im.save(dst, quality=82, optimize=True, progressive=True)
    print(dst, im.size)

if __name__ == "__main__":
    grade(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2000,
          sys.argv[4] if len(sys.argv) > 4 else 'warm')
