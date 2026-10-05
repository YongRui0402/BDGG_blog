#!/usr/bin/env python3
"""重畫預設的社群分享圖 static/og-default.png(1200×630)。

圖上的字都從 hugo.toml 來:站名、標語(params.tagline)、站台網址(baseURL)。
這三個值改了就要重跑一次,並把新的圖一起 commit —— 圖不會在建置時自動重畫。

用法:
    python3 scripts/make_og_image.py [--font 字型檔] [--out 輸出路徑]

需要 Pillow,以及一個有繁體中文的粗體字型(預設用 Noto Sans CJK TC Bold)。
這支腳本不在 make check 裡,只有要換圖的時候才需要這兩樣東西。
"""

import argparse
import sys
import tomllib
from urllib.parse import urlsplit

from PIL import Image, ImageDraw, ImageFont

SIZE = (1200, 630)
# 顏色取自 assets/css/main.css 的深色模式
BG = (23, 23, 26)
FG = (228, 226, 222)
MUTED = (151, 146, 139)
ACCENT = (224, 151, 94)
BAR_WIDTH = 15
LEFT = 97
MAX_TEXT_WIDTH = SIZE[0] - LEFT * 2

DEFAULT_FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def load_font(path, size):
    """字型檔是 .ttc 時裡面有好幾個地區的字型,挑繁體中文(TC)那一個。"""
    index = 0
    while True:
        try:
            font = ImageFont.truetype(path, size, index=index)
        except OSError:
            return ImageFont.truetype(path, size)
        if " TC" in font.getname()[0]:
            return font
        index += 1


def tagline_lines(tagline):
    """標語有逗號就在最後一個逗號後面換行,一行太長時比較好讀。"""
    for comma in ("，", ","):
        head, sep, tail = tagline.rpartition(comma)
        if sep:
            return [head + sep, tail]
    return [tagline]


def main():
    parser = argparse.ArgumentParser(description="重畫預設的社群分享圖")
    parser.add_argument("--font", default=DEFAULT_FONT, help="有繁體中文的粗體字型檔")
    parser.add_argument("--out", default="static/og-default.png", help="輸出路徑")
    args = parser.parse_args()

    with open("hugo.toml", "rb") as f:
        config = tomllib.load(f)
    base = urlsplit(config["baseURL"])
    texts = [(config["title"], load_font(args.font, 128), FG, 345)]
    for i, line in enumerate(tagline_lines(config["params"]["tagline"])):
        texts.append((line, load_font(args.font, 44), MUTED, 406 + i * 62))
    texts.append((base.netloc + base.path.rstrip("/"), load_font(args.font, 36), ACCENT, 560))

    image = Image.new("RGB", SIZE, BG)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, BAR_WIDTH - 1, SIZE[1]), fill=ACCENT)
    for text, font, color, baseline in texts:
        if draw.textlength(text, font=font) > MAX_TEXT_WIDTH:
            print(f"這一行太長,畫不進圖裡:{text}", file=sys.stderr)
            return 1
        # anchor "ls":x 是左緣,y 是基線
        draw.text((LEFT, baseline), text, font=font, fill=color, anchor="ls")

    image.save(args.out, optimize=True)
    print(f"已寫入 {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
