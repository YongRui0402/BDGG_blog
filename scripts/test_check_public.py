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
        self.assertEqual(stats, {"files": 2, "html": 2, "links": 2, "site_urls": 0})

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

    def test_same_host_link_over_http_is_blocked(self):
        self.write(
            "about/index.html",
            '<link rel="canonical" href="http://example.github.io/blog/about/">',
        )
        self.assert_blocked("about/index.html", "http://", "應該")

    def test_share_meta_with_site_urls_passes(self):
        self.write("og.png", "圖")
        self.write(
            "about/index.html",
            '<link rel="canonical" href="https://example.github.io/blog/about/">'
            '<meta property="og:url" content="https://example.github.io/blog/about/">'
            '<meta property="og:image" content="https://example.github.io/blog/og.png">'
            # 不是網址的 meta 不檢查
            '<meta property="og:title" content="/tags/">',
        )
        stats, problems = check(self.public, BASE_URL)
        self.assertEqual(problems, [])
        self.assertEqual(stats["site_urls"], 2)

    def test_unquoted_share_meta_is_still_checked(self):
        # --minify 之後的樣子
        self.write("about/index.html", "<meta property=og:image content=/blog/og.png>")
        self.assert_blocked("分享用的 meta", "完整網址")

    def test_share_image_outside_subpath_is_blocked(self):
        self.write(
            "about/index.html",
            '<meta property="og:image" content="https://example.github.io/og.png">',
        )
        self.assert_blocked("about/index.html", "分享用的 meta", "之外")

    def test_share_image_missing_is_blocked(self):
        self.write(
            "about/index.html",
            '<meta property="og:image" content="https://example.github.io/blog/og.png">',
        )
        self.assert_blocked("分享用的 meta", "不存在")

    def test_share_url_over_http_is_blocked(self):
        self.write(
            "about/index.html",
            '<meta property="og:url" content="http://example.github.io/blog/about/">',
        )
        self.assert_blocked("分享用的 meta", "完整網址")

    def test_empty_share_meta_is_blocked(self):
        self.write("about/index.html", '<meta property="og:image" content="">')
        self.assert_blocked("分享用的 meta", "完整網址")

    def write_feed(self, *, self_href=None, link=None, content=""):
        """一份最小的 feed,裡面有一篇指向 about 頁的文章。"""
        self_href = self_href or "https://example.github.io/blog/index.xml"
        link = link or "https://example.github.io/blog/about/"
        self.write(
            "index.xml",
            '<?xml version="1.0" encoding="utf-8"?>'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"'
            ' xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel>'
            "<link>https://example.github.io/blog/</link>"
            f'<atom:link href="{self_href}" rel="self"/>'
            f'<item><link>{link}</link><guid isPermaLink="true">{link}</guid>'
            "<description>A&amp;amp;B &amp;lt;b&amp;gt; 純文字</description>"
            f"<content:encoded>{content}</content:encoded></item>"
            "</channel></rss>",
        )

    def test_feed_with_site_urls_passes(self):
        self.write("pic.png", "圖")
        self.write_feed(
            content="&lt;a href=&quot;https://example.github.io/blog/about/#top&quot;&gt;站內&lt;/a&gt;"
            "&lt;img src=&quot;https://example.github.io/blog/pic.png&quot;&gt;"
            "&lt;a href=&quot;https://example.com/&quot;&gt;外站&lt;/a&gt;"
        )
        stats, problems = check(self.public, BASE_URL)
        self.assertEqual(problems, [])
        # 頻道連結、feed 自己、文章的 link 與 guid、內文兩個站內網址
        self.assertEqual(stats["site_urls"], 6)

    def test_feed_self_link_pointing_at_home_is_blocked(self):
        # 原版型的寫法:rss.xml 裡的 .Permalink 是首頁,不是 feed
        self.write_feed(self_href="https://example.github.io/blog/")
        self.assert_blocked("index.xml", "feed 自己的網址", "blog/index.xml")

    def test_feed_item_link_outside_subpath_is_blocked(self):
        self.write_feed(link="https://example.github.io/about/")
        problems = self.problems()
        self.assertEqual(len(problems), 2, problems)  # <link> 與 <guid> 各一
        self.assertIn("<link>", problems[0])
        self.assertIn("之外", problems[0])

    def test_feed_item_link_to_missing_page_is_blocked(self):
        self.write_feed(link="https://example.github.io/blog/nope/")
        problems = self.problems()
        self.assertEqual(len(problems), 2, problems)
        self.assertIn("不存在", problems[1])

    def test_feed_content_with_root_relative_link_is_blocked(self):
        self.write_feed(content="&lt;a href=&quot;/blog/about/&quot;&gt;站內&lt;/a&gt;")
        self.assert_blocked("index.xml", "'/blog/about/'", "不是完整網址")

    def test_feed_content_with_anchor_only_link_is_blocked(self):
        self.write_feed(content="&lt;a href=&quot;#top&quot;&gt;頁內&lt;/a&gt;")
        self.assert_blocked("'#top'", "不是完整網址")

    def test_feed_content_with_missing_image_is_blocked(self):
        self.write_feed(
            content="&lt;img src=&quot;https://example.github.io/blog/nope.png&quot;&gt;"
        )
        self.assert_blocked("內文裡的", "不存在")

    def test_broken_xml_is_blocked(self):
        # 原版型在摘要含引號時的產出:沒有宣告過的實體
        self.write("index.xml", "<rss><channel><description>it&rsquo;s</description></channel></rss>")
        self.assert_blocked("index.xml", "不是合法的 XML")

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
