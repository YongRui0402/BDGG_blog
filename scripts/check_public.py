#!/usr/bin/env python3
"""成品檢查:建好的 public/ 放到 GitHub Pages 的子路徑底下會不會壞。

檢查三件事:

1. 站內連結(href 與 src)都落在站台的子路徑底下,指向成品裡真的存在的檔案,而且不是空的。
   子路徑從 hugo.toml 的 baseURL 取,例如 /BDGG_blog/。
   寫成 href="/tags/" 的連結建置時不會報錯,放上子路徑才會壞,所以要在這裡擋。
2. 成品裡沒有草稿標記(class 含 draft-tag 的元素)。
   正式建置本來就不會產出草稿;這是 --buildDrafts 被誤加時的保險。
3. 成品的任何檔案都不含 192.168. 這個字串。

用法:
    python3 scripts/check_public.py [成品目錄] [--base-url 網址]

只用 Python 標準函式庫。有問題就逐條列出並以 1 結束。
"""

import argparse
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

DRAFT_CLASS = "draft-tag"
PRIVATE_IP = b"192.168."
# 不是「連到某個頁面」的網址,不檢查
SKIP_SCHEMES = {"mailto", "tel", "data", "javascript"}


class PageScan(HTMLParser):
    """收集一個 HTML 檔裡所有的 href / src,以及有沒有草稿標記。"""

    def __init__(self):
        super().__init__()
        self.urls = []
        self.has_draft = False

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is None:
                continue
            if name in ("href", "src"):
                self.urls.append(value.strip())
            elif name == "class" and DRAFT_CLASS in value.split():
                self.has_draft = True


def target_exists(public, rel):
    """rel 是去掉子路徑之後的路徑。目錄要有 index.html 才算存在。"""
    target = public / rel
    if rel == "" or rel.endswith("/") or target.is_dir():
        return (target / "index.html").is_file()
    return target.is_file()


def check_links(public, html_file, urls, host, base_path):
    """回傳 (站內連結數, 問題清單)。"""
    rel_file = html_file.relative_to(public).as_posix()
    # 這個檔案在站上的網址;相對連結要以它為基準解析
    page_path = base_path + rel_file.removesuffix("index.html")
    internal = 0
    problems = []

    for url in urls:
        if not url:
            # 選單的 pageRef 指向不存在的頁面時,Hugo 不報錯,只給空字串
            problems.append(f"{rel_file}: 有一個空的 href 或 src")
            continue
        if url.startswith("#"):
            continue
        parts = urlsplit(url)
        if parts.scheme in SKIP_SCHEMES:
            continue
        if parts.netloc:
            if parts.netloc != host:
                continue  # 站外連結
            path = parts.path or "/"
        else:
            path = urlsplit(urljoin(page_path, url)).path

        internal += 1
        path = unquote(path)
        if path == base_path.rstrip("/"):
            path = base_path
        if not path.startswith(base_path):
            problems.append(
                f"{rel_file}: 站內連結 {url!r} 落在 {base_path} 之外"
            )
        elif not target_exists(public, path.removeprefix(base_path)):
            problems.append(f"{rel_file}: 連結 {url!r} 指向不存在的檔案")

    return internal, problems


def check(public, base_url):
    """回傳 (統計, 問題清單)。"""
    public = Path(public)
    base = urlsplit(base_url)
    base_path = base.path if base.path.endswith("/") else base.path + "/"
    stats = {"files": 0, "html": 0, "links": 0}
    problems = []

    if not (public / "index.html").is_file():
        return stats, [f"{public}/index.html 不存在 —— 還沒建置,或建置沒有產出首頁"]

    for path in sorted(p for p in public.rglob("*") if p.is_file()):
        stats["files"] += 1
        rel = path.relative_to(public).as_posix()
        data = path.read_bytes()

        for lineno, line in enumerate(data.splitlines(), 1):
            if PRIVATE_IP in line:
                problems.append(f"{rel}:{lineno}: 含有 {PRIVATE_IP.decode()}")

        if path.suffix != ".html":
            continue
        stats["html"] += 1
        scan = PageScan()
        scan.feed(data.decode("utf-8", errors="replace"))
        if scan.has_draft:
            problems.append(f"{rel}: 有草稿標記(class 含 {DRAFT_CLASS})")
        count, found = check_links(public, path, scan.urls, base.netloc, base_path)
        stats["links"] += count
        problems.extend(found)

    return stats, problems


def base_url_from_config(config="hugo.toml"):
    with open(config, "rb") as f:
        return tomllib.load(f)["baseURL"]


def main():
    parser = argparse.ArgumentParser(description="檢查 Hugo 的建置成品")
    parser.add_argument("public", nargs="?", default="public", help="成品目錄")
    parser.add_argument("--base-url", help="站台網址;省略時讀 hugo.toml 的 baseURL")
    args = parser.parse_args()

    base_url = args.base_url or base_url_from_config()
    stats, problems = check(args.public, base_url)

    if problems:
        print(f"成品檢查沒過({len(problems)} 個問題):", file=sys.stderr)
        for problem in problems:
            print(f"  ✗ {problem}", file=sys.stderr)
        return 1

    print(
        f"成品檢查通過:{stats['files']} 個檔案、{stats['html']} 個 HTML、"
        f"{stats['links']} 個站內連結,都在 {urlsplit(base_url).path} 底下"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
