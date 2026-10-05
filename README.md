# BDGG 部落格

BDGG 的部落格,用 [Hugo](https://gohugo.io/) 產生,由 GitHub Actions 建置、GitHub Pages 託管。
原稿、版型、建置設定都在這個 repo 裡。

- 站台:<https://yongrui0402.github.io/BDGG_blog/>
- 開發紀錄:[`docs/requirements.md`](docs/requirements.md)(為什麼這樣做)、[`docs/features.md`](docs/features.md)(一項一項怎麼做)

站還在搭建中,功能照 `docs/features.md` 的順序一項一項加上來。目前可以發文與閱讀;分區列表、標籤、RSS、搜尋還沒做。

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

push 之後大約一分鐘,文章會出現在 `https://yongrui0402.github.io/BDGG_blog/learning/my-post/`,中間沒有其他步驟。

幾件要知道的事:

- **分區就是 `content/` 底下的目錄**:`pitfalls` 踩坑、`decisions` 架構決策、`projects` 專案、`notes` 速查、
  `learning` 學習筆記、`life` 生活紀錄。一個分區第一次有文章時,要先有 `content/<分區>/_index.md`
  (裡面只需要 `title`,文章頁上的分區名稱取自它)。
- **網址**是 `/<分區>/<slug>/`。`slug` 預設等於檔名,用英文小寫與連字號;發布之後不要再改。
- **`draft: true` 的文章不會上線**,但這個 repo 是公開的,原稿在 GitHub 上仍然看得到。
- **日期在未來的文章不會出現**,而且建置不會報錯。範本填的是開檔當下的時間,手改日期時留意這一點。
- **連到站內的其他文章**寫一般的 Markdown 連結,路徑從站台根算起或寫檔名都可以:
  `[字](/learning/other-post/)`、`[字](other-post.md)`。寫錯的連結 `make check` 會擋下來。
- **圖片**放在文章旁邊:把文章改成目錄 `content/learning/my-post/index.md`,圖放進同一個目錄,
  內文寫 `![說明](圖檔.png)`。
- **程式碼區塊**記得標語言(` ```bash `、` ```ts `),才會上色。
- front matter 各欄位的用途寫在範本 [`archetypes/default.md`](archetypes/default.md) 的註解裡。

## 授權

- 程式碼(版型、樣式、腳本、設定、workflow):[MIT](LICENSE)
- 文章(`content/`):[CC BY 4.0](LICENSE-content.md)
