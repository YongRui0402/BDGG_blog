# 功能需求清單(一次開發一項)

> 這份檔案是**每次開發的入口**。8 項功能需求照順序做,每一項開一個新對話。
> 背景、範圍、驗收條件的來龍去脈在 [`requirements.md`](requirements.md);這裡只放「這一項要做什麼」。
> 建立日期:2026-10-05。

## 怎麼用

每次開發前,在新對話裡依序啟用三支 skill:

```
/double-diamond-principle
/git-conventional-commit
/trunk-based-development
```

接著把該項功能底下「貼上這段」的內容整段貼進去。裡面有 `<…>` 的地方先換成你的內容。

## 進度

做完一項就把 `[ ]` 改成 `[x]`,並填上完成日期與最後一筆 commit。

| # | 功能需求 | 前置 | 狀態 | 完成日期 | commit |
|---|---|---|---|---|---|
| 1 | push 就上線 | — | [ ] | | |
| 2 | 基本版面 | 1 | [ ] | | |
| 3 | 文章頁的閱讀體驗 | 2 | [ ] | | |
| 4 | 被找到與被訂閱 | 3 | [ ] | | |
| 5 | 分區與首頁列表 | 3 | [ ] | | |
| 6 | 標籤 | 5 | [ ] | | |
| 7 | 關於頁 | 3 | [ ] | | |
| 8 | 站內搜尋 | 5 | [ ] | | |
| — | 收尾(不算功能) | 全部 | [ ] | | |

第 7 項只依賴第 3 項,資料備齊就可以往前移。第 4、5 項彼此獨立,順序可以互換。

## 每一項都適用的規則

**來源**

- 版型來自站主既有部落格的 Hugo 專案。正本在站主的私有 repo;
  其中 `layouts/`、`assets/css/`、`assets/js/`、`static/` 和公開的 `YongRui0402/blog` 在 commit `9e7ed55` 的內容
  只差 `footer.html` 與 `robots.txt` 兩處文字,任一邊都可以當來源。
  `Makefile`、`.hugo-version`、`archetypes/`、`config/` 只有正本有。
- 來源抓到對話的暫存區,**不要放進這個 repo 的目錄裡**。
- 不動正本、不動 `YongRui0402/blog`、不動現有的站。

**搬的方式**

- **白名單、逐檔**:這個 repo 是公開的,歷史收不回。每個檔案進 commit 之前要整份讀過,
  清掉提到內網、staging、舊產線、匿名規則的字眼與註解。
- **絕對不搬**:`drafts/`、`tools/`、`docs/`、`deploy/`、`content/`、`assets/photos/`、`static/CNAME`、`.gitlab-ci.yml`。
- **不在範圍內的功能,引用直接拿掉、不留半截**:留言(`comments.html`、giscus 設定)、
  閱讀進度條(`progress.js`)、分享(`share.html`、`share.js`)、系列文導覽(`series-nav.html`)、
  相關文章(`[related]` 設定)、封面與穿插照片(`cover.html`、`cover-res.html`、`photo-breather.html`、`defaultCover`)、
  圖片 shortcode(`fig.html`)。對應的樣式也一併刪掉。
- 文章 front matter 不使用 `publish` 與 `hook`(版型沒讀,是舊產線的欄位)。
- 在範圍內、但還沒輪到的功能:版型先以精簡的形式進來,輪到那一項時再補上引用。
  **選單項目跟著功能進來**,不要先掛一個點了會 404 的連結。

**網址**

- 站台網址 `https://yongrui0402.github.io/BDGG_blog/`,是子路徑,不綁自訂網域。
- 原版型有至少 16 處寫成 `{{ "/tags/" | relURL }}`(開頭帶斜線),選單網址也是 `/projects/` 這種寫法。
  依 Hugo 文件,這在子路徑下不會補上 `/BDGG_blog/`。**功能 1 會實測並定下全站的寫法**,
  記在下面的「已定下的做法」;之後每一項搬版型時都照那個寫法改。

**建置與整合**

- Hugo extended **0.165.0**,版本只釘在 `.hugo-version`。搬家期間不升級。
- 本機與 CI 跑**同一道指令**(`make check`:建置 + 成品檢查)。push 之前先在本機跑過。
- 直接 commit 到 `main`,不開長期 branch。`main` 上每一筆都要建得起來、可以發布。
- commit 作者已在這個 repo 設好(`BDGG` + GitHub noreply 信箱),不要改。
- `.claude/` 不進 repo(已在 `.gitignore`)。

**其他**

- 身分:BDGG 是筆名,可以連回本人。站名與作者欄是 BDGG。
- 授權:程式碼 MIT,文章 CC BY 4.0。
- GA4:設定欄位保留,ID 留空。
- 文章範本預設 `draft: true`,作者改成 `false` 才上線。
- 只用上面三支專案 skill;不查站主的個人知識庫。

**每一項做完時**

1. 更新上面的進度表
2. 後面的功能會用到的決定,記到「已定下的做法」
3. 在 `docs/skill-notes.md` 記一筆這次三支 skill 的試用心得:哪裡有幫助、哪裡卡住或多餘

## 已定下的做法

> 開發過程中定下、後面會沿用的事記在這裡。

- **GitHub Pages**:來源已設為 GitHub Actions(2026-10-05,站主同意後以 `gh` 設定)。不需要再到網頁上改。
- **成品檢查**要包含「成品不得出現 `192.168.`」這一項(站主 2026-10-05 決定)。
- 全站連結的寫法:_功能 1 實測後填_

---

## 功能 1:push 就上線

**貼上這段**

```
請幫我開發「功能 1:push 就上線」。
需求、範圍與驗收在 docs/features.md 的「功能 1」,共用規則在同一份檔案的「每一項都適用的規則」,背景在 docs/requirements.md。
目標:我 push 到 main 之後,GitHub Actions 自動建置,一個最簡單的頁面出現在 https://yongrui0402.github.io/BDGG_blog/。
這次只做這一項,不要搬任何原架構的版型。做完更新 docs/features.md 的進度表與「已定下的做法」。
```

**為什麼先做**:GitHub 建置部署與子路徑是整個專案最不確定的兩件事,先用最小的東西驗掉。

**範圍內**

- 鋪路(單獨一筆 commit,先於其他變更):`docs/`、`.gitignore`(補上 `public/`、`.hugo-bin/`、`resources/`、`.hugo_build.lock`)、
  MIT 授權檔、文章的 CC BY 4.0 授權聲明、最簡 README
- `.hugo-version`、`Makefile`(下載同版 Hugo 到 `.hugo-bin/`、`preview`、`build`、`check`)
- 最小的 `hugo.toml`:`baseURL`、站名、語系
- 最小的版面與兩個互相連結的頁面(用來測連結,不需要樣式)
- `.github/workflows/deploy.yml`:push 到 `main` → 建置 → 成品檢查 → 部署。
  可參考 `YongRui0402/blog@9e7ed55` 的同名檔案;其中針對自訂網域的 https 檢查不適用
- 成品檢查腳本:站內連結都落在 `/BDGG_blog/` 底下且指向存在的頁面、沒有草稿標記、成品不得出現 `192.168.`
- **實測子路徑下的連結寫法**:`"/x/" | relURL`、`"x/" | relURL`、選單的 `.URL` 各產出什麼,
  定下全站寫法並記到「已定下的做法」

**範圍外**:樣式、任何原架構的版型、文章。

**驗收**

- 公開網址打得開,兩個頁面互相點得到,網址都在 `/BDGG_blog/` 底下
- workflow 裡沒有 self-hosted runner 或外部主機
- 故意推一個會讓建置失敗的變更,公開站仍是上一版;之後還原
- 本機 `make check` 的成品與 CI 的成品逐檔一致
- 成品檢查腳本對「連結指到網域根目錄」「成品含 `192.168.`」兩種情況各用一個假例子驗過,確認真的會擋

**需要站主**:同意第一次 push 到公開 repo。

---

## 功能 2:基本版面

**貼上這段**

```
請幫我開發「功能 2:基本版面」。
需求、範圍與驗收在 docs/features.md 的「功能 2」,共用規則與「已定下的做法」在同一份檔案,背景在 docs/requirements.md。
目標:站有完整的外觀 —— 頁首選單、頁尾、深色模式、手機版面,以及一個基本的 404 頁。
這次只做這一項。做完更新 docs/features.md 的進度表與「已定下的做法」。
```

**範圍內**

- `layouts/_default/baseof.html`、`partials/head.html`、`partials/header.html`、`partials/footer.html`
- `assets/css/main.css`(整份讀過,刪掉不在範圍內的功能所用的樣式)、`assets/css/syntax.css`
- `static/favicon.ico`、`static/og-default.png`(先看圖上有沒有舊網域或舊站名的字樣)
- `layouts/404.html` 的基本版(先不含搜尋框,功能 8 再補)
- `hugo.toml` 的站台參數:作者、標語、說明、GitHub 帳號;GA4 欄位保留、ID 留空
- 連結全部改成「已定下的做法」裡的寫法;favicon 那一處寫死的 `/favicon.ico` 一併處理

**要拿掉的引用**:`baseof` 裡的進度條與分享腳本;`head` 裡的封面解析(社群分享圖固定用預設那一張)。
複製程式碼的腳本留到功能 3。頁尾的「本機預覽版本」標記是否保留、文字怎麼寫,這一項決定。

**範圍外**:文章頁、列表、標籤、搜尋、RSS。選單先只放已經存在的頁面。

**驗收**

- 360px 寬沒有橫向捲動
- 深色與淺色模式都正常
- favicon 與預設分享圖在子路徑下載得到
- 不存在的網址會顯示自己的 404 頁
- 成品檢查通過;成品裡沒有不在範圍內功能的殘留(腳本、樣式、空的區塊)

**需要站主**:看一眼外觀對不對。

---

## 功能 3:文章頁的閱讀體驗

**貼上這段**

```
請幫我開發「功能 3:文章頁的閱讀體驗」。
需求、範圍與驗收在 docs/features.md 的「功能 3」,共用規則與「已定下的做法」在同一份檔案,背景在 docs/requirements.md。
目標:我可以發第一篇文章,讀者讀得舒服 —— 程式碼有上色、可以一鍵複製,長文有目錄,手機上好讀。
第一篇文章的題目與內容:<填題目;內容可以貼上,或寫「請依 docs/requirements.md 的過程起草,我再改」>
這次只做這一項。做完更新 docs/features.md 的進度表與「已定下的做法」。
```

**範圍內**

- `layouts/_default/single.html`:標題、日期、分區、目錄、內文、標籤顯示、文首重點(`key_points`)、
  文末一句話(`takeaway`)、過期提示(`staleAfterMonths`)、草稿標記
- `partials/sect-icon.html`、`partials/sect-name.html`
- 程式碼高亮設定、`assets/js/copy-code.js` 與它在 `baseof` 的引用
- `archetypes/default.md`:說明文字改寫(原檔提到 `drafts/` 與 `make publish`,都不適用),預設 `draft: true`
- 文章網址規則(`[permalinks]`)
- 第一篇文章,以及它所屬的那一個分區目錄
- 首頁暫時列出文章連結,讓讀者點得到(正式的首頁在功能 5)
- README 補上「怎麼發一篇文」

**要拿掉的引用**:留言、封面、穿插照片、系列文導覽、分享、文末的相關文章。

**範圍外**:分區列表頁、標籤頁(文章上的標籤先顯示成文字,功能 6 再變成連結)。

**驗收**

- 實際發一篇:從 push 到公開網址看得到,5 分鐘內、零手動步驟(計時)
- 未登入的瀏覽器能在 GitHub 上讀到該篇的 Markdown 原稿
- 程式碼區塊在深淺色下都有上色、複製鈕可用、手機上可橫向捲動而頁面本身不捲
- `draft: true` 的文章不會出現在成品裡(用一篇假草稿驗,驗完移除)

**需要站主**:第一篇文章的題目與內容。

---

## 功能 4:被找到與被訂閱

**貼上這段**

```
請幫我開發「功能 4:被找到與被訂閱」。
需求、範圍與驗收在 docs/features.md 的「功能 4」,共用規則與「已定下的做法」在同一份檔案,背景在 docs/requirements.md。
目標:搜尋引擎拿到正確的網址,讀者能用 RSS 閱讀器訂閱,文章貼到社群時有標題、摘要與圖。
這次只做這一項。做完更新 docs/features.md 的進度表與「已定下的做法」。
```

**範圍內**

- `layouts/_default/rss.xml`、首頁輸出格式加上 RSS、頁尾的 RSS 連結、頁首的 feed 宣告
- `layouts/robots.txt`(註解改寫)、sitemap
- 頁首的說明文字、canonical 網址、社群分享用的 meta(圖固定用預設那一張)

**範圍外**:搜尋索引(`index.json`,功能 8)。

**驗收**

- RSS feed 通過 W3C Feed Validator
- sitemap、robots、canonical、分享圖的網址都是 https 且帶 `/BDGG_blog/`
- 成品檢查多一項:sitemap 與 robots 不得含 `http://` 的絕對網址
- 草稿不出現在 feed 與 sitemap 裡

---

## 功能 5:分區與首頁列表

**貼上這段**

```
請幫我開發「功能 5:分區與首頁列表」。
需求、範圍與驗收在 docs/features.md 的「功能 5」,共用規則與「已定下的做法」在同一份檔案,背景在 docs/requirements.md。
目標:讀者能依六個分區瀏覽文章,首頁與「最新」頁會列出文章,文章多了可以分頁與排序。
這次只做這一項。做完更新 docs/features.md 的進度表與「已定下的做法」。
```

**範圍內**

- 六個分區與各自的 `_index.md`:`pitfalls` 踩坑、`decisions` 架構決策、`projects` 專案、
  `notes` 速查、`learning` 學習筆記、`life` 生活紀錄
- `layouts/_default/list.html`、`layouts/index.html`、`layouts/_default/latest.html` 與 `content/latest.md`
- `partials/entry.html`(文章摘要卡)、`partials/paginator.html`、`partials/sort-bar.html`、`assets/js/sort.js`
- 選單、分頁設定
- 取代功能 3 留下的暫時首頁

**要拿掉的引用**:摘要卡裡的封面。

**範圍外**:標籤頁(`list.html` 裡給標籤用的部分留到功能 6)。
沒有文章的分區要不要放進選單,這一項決定 —— 原架構的做法是空的分區不掛選單。

**驗收**

- 每個分區頁只列自己的文章;空的分區有合理的顯示,不是空白頁
- 分頁與排序可用(文章不夠多時用假文章驗,驗完移除)
- 首頁、六個分區頁、「最新」頁的樣式與連結在子路徑下全部正常,瀏覽器 console 沒有 404

---

## 功能 6:標籤

**貼上這段**

```
請幫我開發「功能 6:標籤」。
需求、範圍與驗收在 docs/features.md 的「功能 6」,共用規則與「已定下的做法」在同一份檔案,背景在 docs/requirements.md。
目標:讀者能從文章上的標籤點進去,看到同一個標籤的所有文章,也能看到全部標籤的總覽。
這次只做這一項。做完更新 docs/features.md 的進度表與「已定下的做法」。
```

**範圍內**

- `[taxonomies]` 設定、`layouts/_default/terms.html`、`partials/term-name.html`、`content/tags/_index.md`
- 文章頁與摘要卡上的標籤改成連結;頁尾的「標籤」連結
- `list.html` 裡標籤頁用到的部分

**驗收**

- 每個標籤有自己的頁面,只列該標籤的文章
- 標籤總覽頁列出全部標籤
- 中文標籤的網址在子路徑下打得開
- 標籤名稱的大小寫顯示正確(原架構用 `term-name` 處理這件事)

---

## 功能 7:關於頁

**貼上這段**

```
請幫我開發「功能 7:關於頁」。
需求、範圍與驗收在 docs/features.md 的「功能 7」,共用規則與「已定下的做法」在同一份檔案,背景在 docs/requirements.md。
目標:看作品集的人點進「關於」,知道 BDGG 是誰、做過什麼、怎麼聯絡。
要放的資料 —— 真名:<填> / 聯絡方式:<填> / 想呈現的經歷與技能:<填,或寫「請先列大綱問我」>
這次只做這一項。做完更新 docs/features.md 的進度表與「已定下的做法」。
```

**範圍內**

- 新寫的 `content/about.md`(不搬舊的內文)
- 選單加上「關於」
- `hugo.toml` 作者欄旁的註解改寫(原本寫的是匿名規則)
- README 的作者資訊

**範圍外**:履歷下載、聯絡表單。

**驗收**

- 內容經站主確認後才把 `draft` 改成 `false`
- 關於頁不出現文章才有的元素(日期、過期提示、分區標示)
- 頁面上的對外連結都打得開

**需要站主**:真名、聯絡方式、想呈現的經歷。

---

## 功能 8:站內搜尋

**貼上這段**

```
請幫我開發「功能 8:站內搜尋」。
需求、範圍與驗收在 docs/features.md 的「功能 8」,共用規則與「已定下的做法」在同一份檔案,背景在 docs/requirements.md。
目標:讀者能用關鍵字(中文或英文)找到文章;走錯網址時,404 頁也有搜尋框可以用。
這次只做這一項。做完更新 docs/features.md 的進度表與「已定下的做法」。
```

**範圍內**

- `layouts/index.json`(搜尋索引)、首頁輸出格式加上 JSON
- `layouts/_default/search.html`、`content/search.md`、`assets/js/search.js`
- `404.html` 補上搜尋框
- 選單加上「搜尋」

**要拿掉的引用**:搜尋索引裡的封面欄位。

**要特別看的地方**:`search.js` 從 `<html data-baseurl>` 取站台根來組索引檔的網址,
而 `baseof` 產生這個屬性的寫法正是子路徑下有疑慮的那一種 —— 確認它照「已定下的做法」改過。

**驗收**

- 中文、英文各搜一個只出現在單篇的詞,都找得到對應文章
- 子路徑下索引檔載得到,瀏覽器 console 沒有 404
- 草稿不出現在索引裡
- 成品檢查涵蓋 `index.json`(不得出現 `192.168.`)

---

## 收尾(不算功能)

**貼上這段**

```
請幫我做這個專案的收尾。
項目在 docs/features.md 的「收尾」,驗收條件在 docs/requirements.md 的「成功的樣子」。
把 14 項驗收條件逐項跑一遍並附上證據,補完 README,彙整 docs/skill-notes.md 的試用心得。
```

- README 完整版:這是什麼、怎麼在本機預覽、怎麼發一篇文、授權
- `requirements.md` 的驗收條件逐項跑,每一項附證據(第 10 項已取消)
- 對整個 repo 與 `git log -p` 搜尋內網 IP、內網網域、token、舊產線殘留
- 彙整 `docs/skill-notes.md`:三支 skill 各自哪裡有幫助、哪裡卡住或多餘
- `requirements.md` 補上 Deliver 段:測了什麼、淘汰了什麼、最後怎麼做
