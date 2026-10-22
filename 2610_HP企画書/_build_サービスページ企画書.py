# サービスページ企画書（md v0.3）をPowerPointにする。デザインは design-jil スキル（白×墨＋黄色、Noto Sans JP）
# 使い方: python _build_サービスページ企画書.py   （作ったあと _preview/ に画像も書き出す）
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path.home() / '.claude' / 'skills' / 'design-jil'))
from jil_deck import *

HERE = Path(__file__).parent
IMG = HERE / '_img'
REF = HERE.parent / 'references'
OUT = HERE / '20261022_サービスページ企画書_v2.pptx'

prs = new_deck()
def slide(label_text, lead, marks=()):
    return new_slide(prs, label_text, lead, marks)

# ---------- 画像の下ごしらえ ----------
def prep_images():
    def crop(src, box, dst):
        Image.open(IMG / src).convert('RGB').crop(box).save(IMG / dst)
    crop('page_pc_concept.png', (905, 200, 1320, 590), 'venn.png')
    crop('page_pc_flow.png', (75, 365, 1365, 1360), 'flow_crop.png')
    crop('page_pc_feature.png', (370, 355, 460, 455), 'icon_eye.png')
    crop('page_pc_feature.png', (780, 355, 895, 455), 'icon_make.png')
    crop('page_pc_feature.png', (1205, 355, 1330, 455), 'icon_move.png')
    full = Image.open(IMG / 'page_pc_full.png').convert('RGB')
    cut = 2400   # 特徴の欄と流れの欄のすき間（見出しが切れない位置）
    full.crop((0, 0, 1440, cut)).save(IMG / 'full_top.png')
    full.crop((0, cut, 1440, full.height)).save(IMG / 'full_bottom.png')
    # AI欄の4つの図（文字は除き、図だけ。列の区切り線は含めない）
    ai = Image.open(IMG / 'page_pc_ai.png').convert('RGB')
    for i in range(4):
        part = ai.crop((80 + 320 * i + 8, 478, 80 + 320 * (i + 1) - 8, 608))
        box = Image.eval(part.convert('L'), lambda v: 255 if v < 235 else 0).getbbox()
        part.crop(box).save(IMG / f'ai_icon_{i}.png')
    # 手本の画像から撮影時の切れ端を除く
    Image.open(IMG / 'coral_02.jpg').crop((150, 62, 850, 499)).save(IMG / 'coral_02_crop.jpg', quality=92)
    Image.open(IMG / 'pksha_00.jpg').crop((200, 188, 900, 625)).save(IMG / 'pksha_00_crop.jpg', quality=92)
    # 同業の最初の画面（デザイン調査：上段 白×青、下段 ぼかし・球体／競合の捉え方：4タイプの代表）
    def thumb(src, dst, pre=None, th=450):
        im = Image.open(REF / src).convert('RGB')
        if pre:
            im = im.crop(pre)
        tw = 720
        im.resize((tw, int(im.height * tw / im.width))).crop((0, 0, tw, th)).save(IMG / dst, quality=90)
    comps = ['screenshots/alphadrive_fv.png', 'screenshots/bornrex_fv.png',
             'screenshots/01booster_fv.png', 'design/03_competitors/timeskip_fv.png',
             'design/03_competitors/algomatic_fv.png', 'design/03_competitors/newh_fv.png',
             'design/03_competitors/exawizards_fv.png', 'screenshots/sundred_fv.png']
    for i, c in enumerate(comps):
        thumb(c, f'comp_{i}.jpg', (300, 0, 1130, 519) if 'exawizards' in c else None)
    for i, c in enumerate(['screenshots/alphadrive_fv.png', 'design/03_competitors/algomatic_fv.png',
                           'design/03_competitors/zingth_fv.png', 'design/03_competitors/bundl_fv.png']):
        thumb(c, f'type_{i}.jpg', (0, 180, 1440, 900) if 'algomatic' in c else None, th=360)

# ---------- スライド ----------
def s_target():
    s = slide('誰に向けたページか', '大企業の新規事業部門の担当者・責任者', marks=['担当者・責任者'])
    lw = 4.8
    tb(s, L, TOP, lw, 0.3, '立場', size=14, bold=True, color=GRAY)
    hline(s, L, TOP + 0.45, lw, INK, 1.25)
    tb(s, L, TOP + 0.75, lw, 1.2, ['社内の審査や上司に、', '依頼先を説明する立場'], size=22, bold=True)
    tb(s, L, TOP + 2.25, lw, 0.3, 'ゴール', size=14, bold=True, color=GRAY)
    hline(s, L, TOP + 2.7, lw, LINE)
    tb(s, L, TOP + 3.0, lw, 1.2, ['30分の無料相談、', 'またはお問い合わせ'], size=22, bold=True)
    x = 6.4; w = R - x
    tb(s, x, TOP, w, 0.3, 'よくある悩み', size=14, bold=True, color=GRAY)
    hline(s, x, TOP + 0.45, w, INK, 1.25)
    for i, t in enumerate(['事業計画が、社内の審査を通らない', 'つくれる人が社内にいない', 'リリース後に、売る人・回す人が足りない']):
        yy = TOP + 0.45 + i * 1.15
        tb(s, x, yy, w, 1.15, t, size=20, anchor=MSO_ANCHOR.MIDDLE)
        hline(s, x, yy + 1.15, w)

def s_competitors():
    s = slide('競合の捉え方', '競合は4つのタイプに分かれる', marks=['4つのタイプ'])
    types = [('新規事業コンサル', '大企業の新規事業を、\n構想と検証から伴走する',
              'アルファドライブ／Relic\nquantum／ボーンレックス\nユニコーンファーム　ほか'),
             ('AI×事業開発', 'AIの開発力を軸に、\n事業づくりや業務を変える',
              'Algomatic／Sun*／AVILEN\nエクサウィザーズ\nリブ・コンサルティング　ほか'),
             ('実行の伴走支援', '立ち上げ後の営業・マーケ・\n業務を、実行まで担う',
              'Zingth／才流／セレブリックス\nSALES ROBOTICS\nAcrosstudio　ほか'),
             ('海外の事業スタジオ', '事業を一緒につくり、\n市場で試すところまで担う',
              'Bundl／IDEO／BCG X\nBoard of Innovation\nRainmaking　ほか')]
    gap = 0.3; cw = (W - gap * 3) / 4; th = cw / 2
    for i, (name, what, who) in enumerate(types):
        x = L + i * (cw + gap)
        pic(s, IMG / f'type_{i}.jpg', x, TOP, w=cw, border=True)
        y = TOP + th + 0.25
        tb(s, x, y, cw, 0.4, name, size=20, bold=True)
        tb(s, x, y + 0.5, cw, 0.7, what, size=15, color=GRAY, spacing=1.25)
        hline(s, x, y + 1.3, cw)
        tb(s, x, y + 1.42, cw, 0.3, '主な企業', size=12, bold=True, color=GRAY)
        tb(s, x, y + 1.7, cw, 0.9, who, size=14, spacing=1.3)
    source(s, '各タイプ10社・計39社を調査（アルファドライブは2タイプに該当）。画面は各タイプの1社目のサイト（2026/10/16・19 撮影）')

def s_norm():
    s = slide('業界の「当たり前」', 'どの会社も「一気通貫・伴走」を掲げている')
    tb(s, L, TOP, W, 0.9, ['実際は工程ごとに得意な会社が分かれている。',
                           '依頼する側は会社を分けて頼むことになり、つなぎ目で止まりやすい。'], size=18, color=GRAY)
    bw, gap, y = 3.3, (W - 3.3 * 3) / 2, 3.85
    items = [('STRATEGY', '戦略', 'コンサル'), ('DEVELOPMENT', '開発', '開発会社・AIベンダー'), ('EXECUTION', '実行', '営業・マーケ会社')]
    for i, (en, ja, who) in enumerate(items):
        x = L + i * (bw + gap)
        rect(s, x, y, bw, 1.75, fill=WHITE, line=CIRCLE, shape=MSO_SHAPE.ROUNDED_RECTANGLE).adjustments[0] = 0.08
        tb(s, x, y + 0.25, bw, 0.3, en, size=11, color=GRAY, align=PP_ALIGN.CENTER, name=MONO)
        tb(s, x, y + 0.5, bw, 0.4, ja, size=16, bold=True, align=PP_ALIGN.CENTER)
        tb(s, x, y + 0.95, bw, 0.5, who, size=20, bold=True, align=PP_ALIGN.CENTER)
        if i < 2:
            gx = x + bw
            tb(s, gx, y + 0.55, gap, 0.5, '→', size=24, color=CIRCLE, align=PP_ALIGN.CENTER)
            rect(s, gx + gap / 2 - 0.13, y + 2.05, 0.26, 0.26, fill=YELLOW, shape=MSO_SHAPE.OVAL)
            tb(s, gx + gap / 2 - 0.13, y + 2.05, 0.26, 0.26, '!', size=12, bold=True,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            tb(s, gx - 0.6, y + 2.4, gap + 1.2, 0.35, '止まりやすい', size=14, bold=True, align=PP_ALIGN.CENTER)

def s_position():
    s = slide('JILの立ち位置', '戦略・開発・実行を、ひとつのチームで受ける', marks=['ひとつのチーム'])
    h = 4.3; im = Image.open(IMG / 'venn.png'); w = h * im.width / im.height
    pic(s, IMG / 'venn.png', R - w, TOP - 0.05, h=h)
    y = TOP + 1.0
    hline(s, L, y, 6.4, INK, 1.25)
    tb(s, L, y + 0.35, 6.6, 0.5, '描いて終わり、つくって終わりにしない', size=22, bold=True)
    tb(s, L, y + 1.1, 6.4, 1.4, ['事業が立ち上がり、伸びるまで伴走する。',
                                 'ページでは3つの円の図で見せ、', '他社との比較表は使わない。'], size=18, color=GRAY)

def s_appeal():
    s = slide('訴求ポイント', '打ち出すのは「審査する側の目」と「人材まで」', marks=['審査する側の目', '人材まで'])
    cols = [(L, 2.6), (L + 2.7, 4.6), (L + 7.4, W - 7.4)]
    for (x, w), hd in zip(cols, ['他社もよく言うこと', 'JILの打ち出し', '根拠']):
        tb(s, x, TOP, w, 0.3, hd, size=14, bold=True, color=GRAY)
    hline(s, L, TOP + 0.45, W, INK, 1.25)
    rows = [('実践者が支援', '審査する側の目で見極める', '役員の事業審査 年1,500件超'),
            ('開発まで対応', '本番のプロダクトまでつくる', '新規サービスの立ち上げ 年10件以上'),
            ('伴走', '売る人・回す人までアサイン', '常駐・業務委託で参加'),
            ('AIを活用', 'AIは前に出さず、全工程で使う', '工程ごとの活用例')]
    rh = 0.92
    for i, row in enumerate(rows):
        y = TOP + 0.45 + i * rh
        for j, ((x, w), t) in enumerate(zip(cols, row)):
            tb(s, x, y, w, rh, t, size=20 if j == 1 else 18, bold=(j == 1),
               color=GRAY if j == 0 else INK, anchor=MSO_ANCHOR.MIDDLE)
        hline(s, L, y + rh, W)

def s_structure():
    s = slide('ページ全体の構成', '6つの欄で構成')
    items = [('最初の画面', 'キャッチとロゴ'), ('コンセプト', 'JILの立ち位置'),
             ('特徴', '見極める・つくる・動かす'), ('事業づくりの流れ', '支援の範囲'),
             ('事業開発×AI', '進め方'), ('ご相談', '30分の無料相談')]
    rh = 0.72; w = 6.4
    hline(s, L, TOP, w, INK, 1.25)
    for i, (n, d) in enumerate(items):
        y = TOP + i * rh
        tb(s, L, y, 0.5, rh, str(i + 1), size=16, color=GRAY, anchor=MSO_ANCHOR.MIDDLE, name=MONO)
        tb(s, L + 0.45, y, 2.9, rh, n, size=20, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, L + 3.35, y, w - 3.35, rh, d, size=18, color=GRAY, anchor=MSO_ANCHOR.MIDDLE)
        hline(s, L, y + rh, w)
    top = Image.open(IMG / 'full_top.png'); bot = Image.open(IMG / 'full_bottom.png')
    f = 4.32 / bot.height            # 2枚を同じ縮尺で
    pw = top.width * f
    x2 = R - pw; x1 = x2 - pw - 0.25
    pic(s, IMG / 'full_top.png', x1, TOP, w=pw, border=True)
    pic(s, IMG / 'full_bottom.png', x2, TOP, w=pw, border=True)

def s_omitted():
    s = slide('入れなかったもの', '同業の定番は使わない')
    tb(s, L, TOP, 4.8, 0.3, '使わないもの', size=14, bold=True, color=GRAY)
    tb(s, L + 5.6, TOP, 6, 0.3, '代わりに', size=14, bold=True, color=GRAY)
    hline(s, L, TOP + 0.45, W, INK, 1.25)
    rows = [('「お悩みありませんか」の箱', '流れの各ステップで答える'), ('他社との比較表', '3つの円の図'),
            ('実績数字の帯', 'ロゴと役員の経験の数字'), ('顔写真・料金', '相談の場で説明')]
    rh = 0.85
    for i, (a, b) in enumerate(rows):
        y = TOP + 0.45 + i * rh
        tb(s, L, y, 4.8, rh, a, size=18, color=GRAY, anchor=MSO_ANCHOR.MIDDLE, strike=True)
        tb(s, L + 4.85, y, 0.6, rh, '→', size=18, color=CIRCLE, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, L + 5.6, y, 6, rh, b, size=20, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        hline(s, L, y + rh, W)
    tb(s, L, TOP + 0.45 + 4 * rh + 0.3, W, 0.4, '※お客様インタビュー（5社）は、取材後に追加する', size=14, color=GRAY)

def s_fv():
    s = slide('最初の画面', '戦略から、実行まで。新規事業を、ひとつのチームで。')
    notes = [('写真', 'エスカレーターを\n行き交う人'), ('ロゴ', 'ご支援企業6社を\nすぐ下に'),
             ('ボタン', '30分の無料相談／\nお問い合わせ')]
    for i, (k, v) in enumerate(notes):
        y = TOP + i * 1.45
        hline(s, L, y, 3.6, INK if i == 0 else LINE, 1.25 if i == 0 else 0.75)
        tb(s, L, y + 0.2, 3.6, 0.3, k, size=14, bold=True, color=GRAY)
        tb(s, L, y + 0.5, 3.6, 0.9, v, size=18, spacing=1.2)
    h = 4.35; w = h * 1440 / 900
    pic(s, IMG / 'page_pc_fv.png', R - w, TOP, w=w, border=True)

def s_features():
    s = slide('JILの特徴', '見極める・つくる・動かす')
    rect(s, 0, TOP - 0.15, SW, 3.55, fill=PANEL)
    cols = [('戦略', '見極める', 'icon_eye.png', [('1,500', 54), ('件超／年', 18)], '役員が携わってきた事業審査'),
            ('開発', 'つくる', 'icon_make.png', [('10', 54), ('件以上／年', 18)], '立ち上げてきた新規サービス'),
            ('実行', '動かす', 'icon_move.png', [('人材まで', 36)], '仕組みづくりと人材のアサイン')]
    cw = W / 3
    for i, (en, ja, icon, num, sub) in enumerate(cols):
        x = L + i * cw; px = x + (0.3 if i else 0)
        if i:
            vline(s, x, TOP + 0.15, 3.0)
        tb(s, px, TOP + 0.15, 2, 0.3, en, size=13, bold=True, color=GRAY)
        tb(s, px, TOP + 0.5, 2.5, 0.6, ja, size=26, bold=True)
        ic = Image.open(IMG / icon); ih = 0.9
        pic(s, IMG / icon, x + cw - 0.35 - ih * ic.width / ic.height, TOP + 0.2, h=ih)
        tb(s, px, TOP + 1.35, cw - 0.5, 1.0, [[(t, {'size': sz, 'bold': True}) for t, sz in num]],
           spacing=1.0, anchor=MSO_ANCHOR.BOTTOM)
        tb(s, px, TOP + 2.55, cw - 0.6, 0.8, sub, size=16, color=GRAY)
    tb(s, L, 6.3, W, 0.4, '※数字は会社の実績ではなく、役員の経験として出す', size=14, color=GRAY)

def s_flow():
    s = slide('事業づくりの流れ', '4つのステップと土台で、立ち上げ全体を支援', marks=['立ち上げ全体'])
    lines = [('ステップ', '構想する → 確かめる\n→ つくる → 立ち上げ・伸ばす'),
             ('土台', '組織づくり\n起案制度・カルチャー・研修'), ('依頼の仕方', 'どのステップからでも依頼できる')]
    lw = 4.6
    for i, (k, v) in enumerate(lines):
        y = TOP + i * 1.45
        hline(s, L, y, lw, INK if i == 0 else LINE, 1.25 if i == 0 else 0.75)
        tb(s, L, y + 0.2, lw, 0.3, k, size=14, bold=True, color=GRAY)
        tb(s, L, y + 0.5, lw, 0.9, v, size=18, spacing=1.2)
    h = 4.35; im = Image.open(IMG / 'flow_crop.png'); w = h * im.width / im.height
    pic(s, IMG / 'flow_crop.png', R - w, TOP, h=h, border=True)

def s_ai():
    s = slide('事業開発×AI', 'AIは前に出さず、進め方として見せる')
    tb(s, L, TOP, W, 0.8, ['キャッチには入れず、ページの後半で「進め方」として紹介する。',
                           '同業はAIを新メニューとして足す形が多い。'], size=18, color=GRAY)
    items = [('高速に', '例：試作画面を\n翌日に'), ('大量に', '例：LP・広告を\n50パターンで検証'),
             ('網羅的に', '例：競合・市場を\n数百社規模で調査'), ('自動的に', '例：問い合わせ\n対応を自動で')]
    cw = W / 4; y = 3.6
    hline(s, L, y, W, INK, 1.25)
    for i, (k, ex) in enumerate(items):
        x = L + i * cw; px = x + (0.3 if i else 0)
        if i:
            vline(s, x, y, 3.0)
        pic(s, IMG / f'ai_icon_{i}.png', px, y + 0.35, h=0.95)
        tb(s, px, y + 1.55, cw - 0.4, 0.5, k, size=24, bold=True)
        tb(s, px, y + 2.1, cw - 0.3, 0.8, ex, size=18, color=GRAY, spacing=1.2)
    source(s, '※例は支援内容の一例。期間や数量は案件によって異なる')

def s_design_research():
    s = slide('デザイン調査', '同業の半分は「白×青」', marks=['白×青'])
    tb(s, L, TOP, W, 0.4, '同業24社と、デザインの評価が高いサイト30件を撮影して比較した。', size=18, color=GRAY)
    lw = 2.1; gap = 0.18
    tw = (W - lw - gap * 3) / 4; th = tw * 450 / 720
    for r, (k, v) in enumerate([('白×青', '24社中12社'), ('ぼかし・球体', 'AI系の会社に多い')]):
        y = 3.2 + r * (th + 0.3)
        tb(s, L, y - 0.05, lw - 0.2, 0.4, k, size=20, bold=True)
        tb(s, L, y + 0.45, lw - 0.2, 0.6, v, size=16, color=GRAY)
        for c in range(4):
            pic(s, IMG / f'comp_{r * 4 + c}.jpg', L + lw + c * (tw + gap), y, w=tw, border=True)
    source(s, '出典：アルファドライブ／ボーンレックス／ゼロワンブースター／TimeSkip／Algomatic／NEWh／エクサウィザーズ／SUNDRED 各社サイト（2026/10/16・19 撮影）')

def s_models():
    s = slide('手本にした4サイト', '手本はBundl・Hexa・Coral Capital・PKSHA')
    sites = [('bundl_05.jpg', 'Bundl', '文字と余白で\n見せる'),
             ('hexa_01.jpg', 'Hexa', '0→1→10を\n線画で'),
             ('coral_02_crop.jpg', 'Coral Capital', '3つの柱を\n重なる円で'),
             ('pksha_00_crop.jpg', 'PKSHA', '白黒の\n静かなトーン')]
    cw = (W - 0.5) / 2; iw = 2.8; ih = iw * 0.625
    for i, (f, n, d) in enumerate(sites):
        x = L + (i % 2) * (cw + 0.5); y = TOP + 0.1 + (i // 2) * (ih + 0.45)
        pic(s, IMG / f, x, y, w=iw, border=True)
        tb(s, x + iw + 0.3, y + 0.15, cw - iw - 0.3, 0.4, n, size=20, bold=True)
        tb(s, x + iw + 0.3, y + 0.65, cw - iw - 0.3, 0.9, d, size=18, color=GRAY, spacing=1.25)
    source(s, '出典：bundl.com／hexa.com／coralcap.co／pkshatech.com（2026/10/19 撮影）')

def s_design_policy():
    s = slide('デザインの方針', '白と黒に、黄色をひとつ', marks=['黄色'])
    for i, (c, n, code) in enumerate([(WHITE, '白', '#FFFFFF'), (INK, '墨', '#141414'), (YELLOW, '黄', '#FFF000')]):
        x = L + i * 1.75
        rect(s, x, TOP, 1.5, 1.0, fill=c, line=LINE)
        tb(s, x, TOP + 1.12, 1.5, 0.3, [[(n + '  ', {'bold': True, 'size': 14}), (code, {'size': 12, 'color': GRAY, 'name': MONO})]])
    rules = ['黄色は強調とボタンだけに使う', '写真は人が働く場面', '図は線で描く', 'スマホでも同じ内容']
    y0 = TOP + 1.8
    hline(s, L, y0, 7.6, INK, 1.25)
    for i, t in enumerate(rules):
        tb(s, L, y0 + i * 0.6, 7.6, 0.6, t, size=18, anchor=MSO_ANCHOR.MIDDLE)
        hline(s, L, y0 + (i + 1) * 0.6, 7.6)
    h = 4.5; im = Image.open(IMG / 'page_sp_fv.png'); sw = h * im.width / im.height
    pic(s, IMG / 'page_sp_fv.png', R - sw - 0.5, TOP, h=h, border=True)

SLIDES = [s_target, s_competitors, s_norm, s_position, s_appeal, s_structure, s_omitted,
          s_fv, s_features, s_flow, s_ai, s_design_research, s_models, s_design_policy]

if __name__ == '__main__':
    prep_images()
    for f in SLIDES:
        f()
    prs.save(OUT)
    print('saved', OUT.name, len(prs.slides), 'slides')
    render(OUT)
