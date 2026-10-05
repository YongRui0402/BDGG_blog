#!/usr/bin/env python3
"""check_public.py 的對照組:餵它已知有問題的成品,確認它真的會擋。

檢查器只跑過「會過」的成品是不夠的 —— 一支永遠回報通過的腳本也會過。
這裡每一種要擋的情況各做一個假成品。`make check` 每次都先跑這一支。
"""

import tempfile
import unittest
from pathlib import Path

from check_public import check

BASE_URL = "https://example.github.io/blog/"
# 拆開寫,這個檔案本身才不會被當成「repo 裡出現了內網位址」
PRIVATE_IP = "192." + "168." + "0.1"


class CheckPublicTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.public = Path(tmp.name)
        # 一個沒有問題的最小成品;各個測試再往裡面加東西
        self.write("index.html", '<a href="/blog/about/">關於</a>')
        self.write("about/index.html", '<a href="/blog/">首頁</a>')

    def write(self, rel, text):
        path = self.public / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def problems(self):
        return check(self.public, BASE_URL)[1]

    def assert_blocked(self, *fragments):
        problems = self.problems()
        self.assertEqual(len(problems), 1, problems)
        for fragment in fragments:
            self.assertIn(fragment, problems[0])

    def test_clean_site_passes(self):
        stats, problems = check(self.public, BASE_URL)
        self.assertEqual(problems, [])
        self.assertEqual(stats, {"files": 2, "html": 2, "links": 2})

    def test_link_to_domain_root_is_blocked(self):
        self.write("about/index.html", '<a href="/tags/">標籤</a>')
        self.assert_blocked("about/index.html", "'/tags/'", "之外")

    def test_unquoted_attribute_is_still_checked(self):
        # --minify 會把屬性的引號拿掉
        self.write("about/index.html", "<a href=/tags/>標籤</a>")
        self.assert_blocked("'/tags/'", "之外")

    def test_absolute_link_to_own_host_outside_subpath_is_blocked(self):
        self.write("about/index.html", '<a href="https://example.github.io/tags/">x</a>')
        self.assert_blocked("之外")

    def test_relative_link_climbing_out_of_subpath_is_blocked(self):
        self.write("about/index.html", '<a href="../../tags/">x</a>')
        self.assert_blocked("之外")

    def test_link_to_missing_page_is_blocked(self):
        self.write("about/index.html", '<a href="/blog/nope/">x</a>')
        self.assert_blocked("'/blog/nope/'", "不存在")

    def test_missing_asset_is_blocked(self):
        self.write("about/index.html", '<img src="/blog/photo.png">')
        self.assert_blocked("'/blog/photo.png'", "不存在")

    def test_empty_link_is_blocked(self):
        self.write("about/index.html", '<a href="">不存在的選單項目</a>')
        self.assert_blocked("about/index.html", "空的")

    def test_relative_and_percent_encoded_links_resolve(self):
        self.write("tags/中文/index.html", '<a href="../../about/">關於</a>')
        self.write("about/index.html", '<a href="/blog/tags/%E4%B8%AD%E6%96%87/">中文</a>')
        self.assertEqual(self.problems(), [])

    def test_external_and_non_page_links_are_ignored(self):
        self.write(
            "about/index.html",
            '<a href="https://example.com/tags/">外站</a>'
            '<a href="mailto:someone@example.com">信箱</a>'
            '<a href="#top">頁內</a>',
        )
        self.assertEqual(self.problems(), [])

    def test_draft_marker_is_blocked(self):
        self.write("about/index.html", '<p class="note draft-tag">草稿</p>')
        self.assert_blocked("about/index.html", "草稿標記")

    def test_unquoted_draft_marker_is_blocked(self):
        self.write("about/index.html", "<p class=draft-tag>草稿</p>")
        self.assert_blocked("草稿標記")

    def test_private_ip_in_html_is_blocked(self):
        self.write("about/index.html", f"<p>連到 {PRIVATE_IP} 就好</p>")
        self.assert_blocked("about/index.html:1", "192.168.")

    def test_private_ip_in_non_html_file_is_blocked(self):
        self.write("index.json", f'[\n{{"content": "ssh {PRIVATE_IP}"}}\n]')
        self.assert_blocked("index.json:2", "192.168.")

    def test_empty_output_is_blocked(self):
        (self.public / "index.html").unlink()
        self.assert_blocked("index.html 不存在")


if __name__ == "__main__":
    unittest.main()
