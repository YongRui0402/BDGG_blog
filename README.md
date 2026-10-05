# BDGG 部落格

BDGG 的部落格,用 [Hugo](https://gohugo.io/) 產生,由 GitHub Actions 建置、GitHub Pages 託管。
原稿、版型、建置設定都在這個 repo 裡。

- 站台:<https://yongrui0402.github.io/BDGG_blog/>
- 開發紀錄:[`docs/requirements.md`](docs/requirements.md)(為什麼這樣做)、[`docs/features.md`](docs/features.md)(一項一項怎麼做)

站還在搭建中,功能照 `docs/features.md` 的順序一項一項加上來。

## 在本機跑

需要 Linux、`make`、`curl`、`python3`(3.11 以上)。Hugo 不用自己裝 ——
第一次執行時會依 [`.hugo-version`](.hugo-version) 下載同一版到 `.hugo-bin/`。

```
make preview   # 本機預覽(含草稿),網址會印在終端機上
make check     # 建置 + 成品檢查
```

push 到 `main` 之後,GitHub Actions 跑同一道 `make check`,通過才部署;沒過的話線上的站停在上一版。

## 授權

- 程式碼(版型、樣式、腳本、設定、workflow):[MIT](LICENSE)
- 文章(`content/`):[CC BY 4.0](LICENSE-content.md)
