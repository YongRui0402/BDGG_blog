# BDGG 部落格

BDGG 的部落格:技術筆記、學習心得、專案紀錄與隨筆。
用 [Hugo](https://gohugo.io/) 產生,由 GitHub Actions 建置、GitHub Pages 託管。
原稿、版型、建置設定都在這個 repo 裡,沒有放在別處的部分。

- 站台:<https://yongrui0402.github.io/BDGG_blog/>
- RSS:<https://yongrui0402.github.io/BDGG_blog/index.xml>
- 作者:BDGG(筆名)。介紹與聯絡方式在[關於頁](https://yongrui0402.github.io/BDGG_blog/about/)

## 這個站有什麼

- **寫 Markdown、`git push` 就上線**。中間沒有其他步驟;做完 8 項功能時統計的 27 次部署,從 push 到部署完成是 22 到 94 秒。
- **文章頁**:程式碼上色與一鍵複製、目錄、文首重點與文末一句話、超過一年沒更新的過期提示。
  深淺色跟著系統設定,手機上(360px 寬)不會橫向捲動。
- **找文章**:六個分區、標籤、列出全部文章的「最新」頁、
  [站內搜尋](https://yongrui0402.github.io/BDGG_blog/search/)(中英文都可以;走錯網址時 404 頁也能搜)。
- **被找到與被訂閱**:全文 RSS、sitemap、貼到社群時的標題、摘要與圖。
- **自製版型**,沒有外部佈景主題。瀏覽器端只有三支小腳本(複製程式碼、排序、搜尋),沒有前端套件,也沒有建置用的 Node 相依。

沒有留言、分享按鈕與追蹤碼(GA4 的欄位留著,ID 是空的)。

## 在本機跑

需要 Linux、`make`、`curl`、`python3`(3.11 以上)。Hugo 不用自己裝 ——
第一次執行時會依 [`.hugo-version`](.hugo-version) 下載同一版到 `.hugo-bin/`。

```
make preview   # 本機預覽(含草稿),網址會印在終端機上,存檔即重新整理
make check     # 建置 + 成品檢查
make help      # 列出全部指令
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

push 之後通常半分鐘左右,文章會出現在 `https://yongrui0402.github.io/BDGG_blog/learning/my-post/`,中間沒有其他步驟。

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

## 這個 repo 裡有什麼

| 路徑 | 內容 |
|---|---|
| `content/` | 文章與單頁的 Markdown 原稿。一個目錄一個分區;根目錄的 `about.md`、`latest.md`、`search.md` 是單頁 |
| `layouts/` | 版型。`_default/` 是各種頁面,`partials/` 是共用的片段,`index.json` 產生搜尋索引,`rss.xml` 產生 feed |
| `assets/` | 兩份樣式(`main.css`、程式碼上色的 `syntax.css`)與三支腳本,建置時壓縮並加上指紋 |
| `static/` | 原樣複製的檔案:favicon 與預設的社群分享圖 |
| `archetypes/default.md` | `make new` 用的文章範本 |
| `hugo.toml` | 站台設定:網址、選單、分區的網址規則、輸出格式 |
| `Makefile`、`.hugo-version` | 建置指令,以及釘住的 Hugo 版本(只寫在這一個檔案) |
| `scripts/` | 成品檢查(`check_public.py`)與它的測試,以及重畫分享圖的腳本 |
| `.github/workflows/deploy.yml` | push 到 `main` → `make check` → 部署到 GitHub Pages |
| `docs/` | 開發紀錄,見下面 |

## 建置時檢查什麼

`make check` 依序做四件事,任何一件沒過就是失敗:

1. 刪掉上一次的 `public/`(Hugo 不會自己清掉已經不存在的頁面)
2. `hugo --gc --minify --panicOnWarning`:警告一律當成失敗,包含找不到版型與已棄用的寫法
3. 先測檢查器自己:54 個測試,拿假成品確認每一種要擋的情況真的會擋、不該擋的不會誤擋
4. 檢查成品:
   - 每個站內連結、圖片、樣式、腳本都在 `/BDGG_blog/` 底下,而且指向存在的檔案
   - 沒有草稿(頁面上與搜尋索引裡都不能有)
   - 給站外讀的網址(canonical、社群分享的 meta、RSS、sitemap、`robots.txt`)都是完整的 https 網址,而且指向存在的檔案
   - 每一頁的 canonical 是它自己的位置
   - 成品裡沒有 `192.168.` 開頭的位址

改了 `hugo.toml` 的站名、標語或 `baseURL`,要重畫分享圖並把新的圖一起 commit:
`python3 scripts/make_og_image.py`(需要 Pillow 與 Noto Sans CJK 字型;不在 `make check` 裡)。

## 開發紀錄

這個站的版型來自作者既有的部落格,這個 repo 是把它搬成「原稿、版型、建置、託管全部在 GitHub 上」的版本:
8 項功能一項一項加上來,直接提交到 `main`,每一筆都單獨建置過(唯一的例外是一筆刻意弄壞、
用來驗證「建置失敗時不會部署」的 commit,下一筆就還原)。過程同時用來試三支開發流程的 skill
(Double Diamond、Conventional Commits、Trunk-Based Development),所以留下的紀錄比一般的專案多:

- [`docs/requirements.md`](docs/requirements.md) —— 為什麼這樣做:需求怎麼收斂、考慮過哪些做法、驗收條件與驗收的結果
- [`docs/features.md`](docs/features.md) —— 一項一項怎麼做:每項功能的規格,以及過程中定下、之後要沿用的做法
- [`docs/skill-notes.md`](docs/skill-notes.md) —— 三支 skill 的試用心得:哪裡有幫助、哪裡卡住或多餘

要改版型或加功能,先讀 `docs/features.md` 的「已定下的做法」—— 站台在子路徑底下,連結的寫法有固定的規則。

## 授權

- 程式碼(版型、樣式、腳本、設定、workflow):[MIT](LICENSE)
- 文章(`content/`):[CC BY 4.0](LICENSE-content.md)
