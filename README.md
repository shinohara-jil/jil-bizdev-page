# JIL コーポレートサイト・新規事業開発支援サイト

公開ページ：https://shinohara-jil.github.io/jil-bizdev-page/ （GitHub Pages。`docs/` の中身だけが公開される）

## 公開しているページ（`docs/`）

| 住所 | ファイル | 中身 |
|---|---|---|
| `/` | `docs/index.html` | コーポレートサイトのトップ |
| `/about/` | `docs/about/index.html` | 私たちについて |
| `/product/` | `docs/product/index.html` | プロダクト |
| `/member/` | `docs/member/index.html` | メンバー |
| `/bizdev/` | `docs/bizdev/index.html` | 新規事業開発支援（紹介） |
| `/bizdev/service/` | `docs/bizdev/service/index.html` | 新規事業開発支援の専用サイト（サービスページ） |
| `/recruit/` | `docs/recruit/index.html` | 採用支援 |
| `/prototype/` | `docs/prototype/index.html` | 以前の住所。`/bizdev/service/` へ自動で移動する |

- `docs/common/`：全ページ共通のヘッダー・フッター（メニューの項目はここで管理）
- `docs/img/`：コーポレートサイトの画像。サービスサイトの画像・ロゴ・書体は `docs/bizdev/service/` の中
- ページ同士のリンクはフォルダの形（`../about/` など）。手元でファイルを直接開いたときは、共通ヘッダーが自動で `index.html` を補う

## 公開ページに出さないもの（リポジトリには入っている）

- `archive/`：以前の試作（コーポレートサイトの v1・v3 案、サービスページのデザインコンセプト）と、今は使っていない画像
- `corporate/references/`・`references/`：参考サイトの調査
- `00_〜04_*.md`、`2610_HP企画書/`：分析・設計のメモ、企画書
- `scripts/`：画面の撮影などの作業用スクリプト
