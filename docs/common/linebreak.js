/* スマホで日本語の改行を整える：言葉の途中（「つく／る。」など）で折り返さないようにする
   文節の切れ目にだけ改行の目印（<wbr>）を入れ、そこでしか折り返さない（「ます。」なども前の言葉と一緒に送られる）
   iPhoneのSafariは「文節で改行する」CSS（word-break: auto-phrase）に対応していないため、ブラウザの辞書（Intl.Segmenter）で区切る
   使い方：各ページで footer.js の直後に読み込む。効くのはスマホ幅（720px以下）だけ。
   改行の指定は各文に直接付ける（CSSファイルが古いまま残っていたり、ほかの改行の指定が優先されたりしても効くように） */
(() => {
  if (!matchMedia("(max-width: 720px)").matches || !(window.Intl && Intl.Segmenter)) return;
  const seg = new Intl.Segmenter("ja", { granularity: "word" });
  const JA = /[\u3040-\u30ff\u3400-\u9fff]/;
  const SKIP = "script, style, svg, canvas, .stmt, .js-fill, [data-to]";
  // 前の言葉にくっつけるもの：句読点・閉じかっこ・長音・小さい文字で始まる語、ひらがなだけの短い語（助詞・助動詞など）、空白
  const glue = s => /^[\s、。，．・：；！？!?」』）)〕】ー〜…ぁぃぅぇぉっゃゅょゎ]/.test(s) || (/^[ぁ-ん]{1,3}$/.test(s) && !/^[ごお]$/.test(s));
  // 数字と単位（1,500件・300社）、漢字の続く言葉（事業＋開発、上場＋企業）、動詞のつながり（立ち＋上げ、掛け＋合わせ）、
  // 「ご」「お」と後ろの言葉（ご＋相談、お＋見積り）も離さない
  const join = (raw, s) => (/[0-9０-９]$/.test(raw) && /^[件社名年月日人回円万億倍号階%％]/.test(s))
    || (/^[\u4e00-\u9fff]+$/.test(raw) && /^[\u4e00-\u9fff]/.test(s))
    || (/^[\u4e00-\u9fff]+[ぁ-ん]$/.test(raw) && !/[をにがはのでともへやか]$/.test(raw) && /^[\u4e00-\u9fff]/.test(s))
    || /^[ごお]$/.test(raw) || (/[番目]$/.test(raw) && /^[0-9０-９]/.test(s));
  const phrases = text => {
    const out = [];
    let raw = "";
    for (const { segment: s } of seg.segment(text)) {
      const prev = out[out.length - 1];
      if (prev !== undefined && (glue(s) || join(raw, s) || /[「『（(〔【]$/.test(prev))) out[out.length - 1] = prev + s;
      else out.push(s);
      raw = s;
    }
    return out;
  };
  const disp = el => getComputedStyle(el).display;
  const blockOf = node => { let el = node.parentElement; while (el && disp(el).startsWith("inline")) el = el.parentElement; return el; };

  const nodes = [];
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = tw.nextNode());) if (JA.test(n.textContent) && !n.parentElement.closest(SKIP)) nodes.push(n);
  nodes.forEach(n => {
    const ps = phrases(n.textContent), b = blockOf(n);
    if (ps.length < 2 || !b) return;
    const f = document.createDocumentFragment();
    ps.forEach((p, i) => { if (i) f.appendChild(document.createElement("wbr")); f.appendChild(document.createTextNode(p)); });
    // 横並び・格子の枠に直接入っている文は、区切ると別々の段になってしまうので、ひとつの span にまとめてから差し込む
    if (/flex|grid/.test(disp(n.parentElement))) { const s = document.createElement("span"); s.appendChild(f); n.replaceWith(s); }
    else n.replaceWith(f);
    b.classList.add("lb-p"); b.style.wordBreak = "keep-all"; b.style.overflowWrap = "break-word";
  });
})();
