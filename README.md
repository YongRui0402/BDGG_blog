# BDGG 部落格

BDGG 的部落格,用 [Hugo](https://gohugo.io/) 產生,由 GitHub Actions 建置、GitHub Pages 託管。
原稿、版型、建置設定都在這個 repo 裡。

- 站台:<https://yongrui0402.github.io/BDGG_blog/>
- 作者:BDGG(筆名)。介紹與聯絡方式在[關於頁](https://yongrui0402.github.io/BDGG_blog/about/)
- 開發紀錄:[`docs/requirements.md`](docs/requirements.md)(為什麼這樣做)、[`docs/features.md`](docs/features.md)(一項一項怎麼做)

站還在搭建中,功能照 `docs/features.md` 的順序一項一項加上來。目前可以發文、閱讀、依分區或標籤瀏覽、用[關鍵字搜尋](https://yongrui0402.github.io/BDGG_blog/search/),也可以用 RSS 訂閱(<https://yongrui0402.github.io/BDGG_blog/index.xml>)。

## 在本機跑

需要 Linux、`make`、`curl`、`python3`(3.11 以上)。Hugo 不用自己裝 ——
第一次執行時會依 [`.hugo-version`](.hugo-version) 下載同一版到 `.hugo-bin/`。

```
make preview   # 本機預覽(含草稿),網址會印在終端機上
make check     # 建置 + 成品檢查
```

push 到 `main` 之後,GitHub Actions 跑同一道 `make check`,通過才部署;沒過的話線上的站停在上一版。

## 怎麼發一篇文

```
make new POST=learning/my-post    # 依範本開一篇:content/learning/my-post.md
make preview                      # 邊寫邊看(草稿也看得到)
```

寫完之後把 front matter 的 `draft: true` 改成 `false`,然後:

```
make check
git add content/learning/my-post.md
git commit -m "post: 文章標題"
git push
```

push 之後一分鐘內(第一篇實測 24 秒),文章會出現在 `https://yongrui0402.github.io/BDGG_blog/learning/my-post/`,中間沒有其他步驟。

幾件要知道的事:

- **分區就是 `content/` 底下的目錄**:`pitfalls` 踩坑、`decisions` 架構決策、`projects` 專案、`notes` 速查、
  `learning` 學習筆記、`life` 生活紀錄。六個都可以直接發文。還沒有文章的分區不會出現在選單與首頁;
  發出第一篇之後它會自己出現,不必改設定。
- **分區的介紹**(選填)寫在 `content/<分區>/_index.md`:front matter 的 `blurb` 是首頁卡片上的一句話,
  內文會顯示在該分區列表頁的標題底下。
- **標籤**寫在 front matter 的 `tags`,中文、英文都可以:`tags: [Claude Code, 踩坑]`。每個標籤有自己的頁面,
  全部的標籤在 <https://yongrui0402.github.io/BDGG_blog/tags/>。畫面上顯示的就是你寫的樣子(大小寫不會被改)。
  **同一個標籤每一篇要寫得一樣**:`MCP` 與 `mcp`、`GitHub Pages` 與 `github-pages` 會被當成同一個標籤,
  兩種寫法並存時 `make check` 會失敗,並指出是哪兩篇。
- **網址**是 `/<分區>/<slug>/`。`slug` 預設等於檔名,用英文小寫與連字號;發布之後不要再改。
- **`draft: true` 的文章不會上線**,但這個 repo 是公開的,原稿在 GitHub 上仍然看得到。
- **日期在未來的文章不會出現**,而且建置不會報錯。範本填的是開檔當下的時間,手改日期時留意這一點。
- **連到站內的其他文章**寫一般的 Markdown 連結,路徑從站台根算起或寫檔名都可以:
  `[字](/learning/other-post/)`、`[字](other-post.md)`。寫錯的連結 `make check` 會擋下來。
- **圖片**放在文章旁邊:把文章改成目錄 `content/learning/my-post/index.md`,圖放進同一個目錄,
  內文寫 `![說明](圖檔.png)`。
- **`description` 寫一句話**:它會出現在搜尋結果、貼到社群時的預覽,以及 RSS 閱讀器裡。
  沒寫的話會取內文開頭的 160 個字。
- **程式碼區塊**記得標語言(` ```bash `、` ```ts `),才會上色。
- **內文不要直接寫 HTML 標籤**(例如 `<b>字</b>`):Hugo 會略過它並給一個警告,`make check` 把警告當成失敗。
  要在文章裡提到某個標籤,寫成行內程式碼。
- **站內搜尋**的索引每次建置重新產生,文章 push 上線之後就搜得到,不必另外做什麼。
  標題、標籤、`description` 與內文都會搜,標題命中的排最前面。
- **關於頁**是 [`content/about.md`](content/about.md),放在 `content/` 根目錄、不屬於任何分區,所以不會出現在首頁、
  「最新」頁與 RSS 裡。改它和改文章一樣:編輯、`make check`、push。它掛在選單上,不要把它設成草稿。
- front matter 各欄位的用途寫在範本 [`archetypes/default.md`](archetypes/default.md) 的註解裡。

## 授權

- 程式碼(版型、樣式、腳本、設定、workflow):[MIT](LICENSE)
- 文章(`content/`):[CC BY 4.0](LICENSE-content.md)
