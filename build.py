#!/usr/bin/env python3
"""index.html（Artifact用の断片）に <head> を付けて docs/index.html を作る。

Artifact は <head> を自動で付けるため index.html には書けない。
GitHub Pages ではそれが無いと lang も meta も入らず、検索結果に出ない。
このスクリプトが両者の差を埋める。公開前に実行すること。

    python3 build.py
"""
import pathlib
import re

BASE = "https://shutsumi.github.io/tedori-taro/"
TITLE = "手取り計算シミュレーター｜手取り教えタロウ"
DESC = ("会社員・副業・フリーランスの手取りを月額で計算します。"
        "都道府県ごとの健康保険料率、配偶者控除・扶養控除、年収の壁、"
        "消費税（インボイス・簡易課税）まで含めた概算を無料で。令和8年度の料率に対応。")

HEAD = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{base}">
<meta name="theme-color" content="#C62828">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="手取り教えタロウ">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{base}">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebApplication","name":"手取り教えタロウ",
"url":"{base}","description":"{desc}","applicationCategory":"FinanceApplication",
"operatingSystem":"Web","inLanguage":"ja",
"offers":{{"@type":"Offer","price":"0","priceCurrency":"JPY"}},
"author":{{"@type":"Person","name":"うつみしょうた","url":"https://shutsumi.github.io/"}}}}
</script>
<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
'''

def main():
    here = pathlib.Path(__file__).parent
    src = (here / "index.html").read_text(encoding="utf-8")

    # 断片の先頭にある <title> / <link> / <style> は head に属するので切り出す
    m = re.match(r"(.*?</style>\n)(.*)$", src, flags=re.S)
    if not m:
        raise SystemExit("index.html の先頭に <style> が見つかりません")
    head_part, body_part = m.group(1), m.group(2)
    head_part = re.sub(r"<title>.*?</title>\n", "", head_part, count=1, flags=re.S)

    out = (HEAD.format(title=TITLE, desc=DESC, base=BASE)
           + head_part + "</head>\n<body>\n" + body_part + "</body>\n</html>\n")
    (here / "docs" / "index.html").write_text(out, encoding="utf-8")
    print("docs/index.html を書き出しました（{:,} バイト）".format(len(out.encode())))

if __name__ == "__main__":
    main()
