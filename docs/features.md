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
| 1 | push 就上線 | — | [x] | 2026-10-05 | `fb80377` |
| 2 | 基本版面 | 1 | [x] | 2026-10-05 | `5ce4506` |
| 3 | 文章頁的閱讀體驗 | 2 | [x] | 2026-10-05 | `5cf28ba` |
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
  功能 1 實測過:`relURL` 那一種在子路徑下確實不會補上 `/BDGG_blog/`,選單那一種 Hugo 會補。
  **全站的寫法記在下面的「已定下的做法」,之後每一項搬版型時都照那個寫法改。**

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

### 全站連結的寫法(功能 1 實測,2026-10-05)

在 Hugo 0.165.0、`baseURL = "https://yongrui0402.github.io/BDGG_blog/"` 下,各種寫法實際產出的網址:

| 寫法 | 產出 | 能用嗎 |
|---|---|---|
| `{{ "/projects/" \| relURL }}` | `/projects/` | ✗ 指到網域根目錄 |
| `{{ "projects/" \| relURL }}` | `/BDGG_blog/projects/` | ✓ |
| `{{ "/" \| relURL }}` | `/` | ✗ |
| `{{ "" \| relURL }}` | `/BDGG_blog/` | ✓ |
| `{{ "/projects/" \| absURL }}` | `https://yongrui0402.github.io/projects/` | ✗ |
| `{{ "projects/" \| absURL }}` | `https://yongrui0402.github.io/BDGG_blog/projects/` | ✓ |
| `.RelPermalink`、`site.Home.RelPermalink`、`(site.GetPage "/projects").RelPermalink` | `/BDGG_blog/…` | ✓ |
| 選單 `pageRef = "/projects"` 的 `.URL` | `/BDGG_blog/projects/` | ✓ |
| 選單 `url = "/projects/"` 的 `.URL` | `/BDGG_blog/projects/` | ✓(Hugo 會替設定檔裡的選單補上子路徑,和原先的推測相反) |
| 選單 `url = "projects/"` 的 `.URL` | `projects/` | ✗ 變成相對於目前頁面 |
| Markdown 內文 `[字](/projects/one/)` | `/projects/one/` | ✗ |
| Markdown 內文 `[字]({{< relref "/projects/one" >}})` | `/BDGG_blog/projects/one/` | ✓ |

`relLangURL` 的結果和 `relURL` 相同。

**定下的寫法**,之後每一項搬版型時照這個改:

1. **連到站內的頁面**:拿得到頁面物件就用 `.RelPermalink`(首頁是 `site.Home.RelPermalink`)。
2. **連到固定路徑或靜態檔**(標籤總覽、favicon、樣式、腳本、索引檔):`{{ "tags/" | relURL }}` ——
   **開頭不帶斜線**。原版型的 `"/x/" | relURL` 一律把開頭的斜線拿掉;寫死的 `/favicon.ico` 改成 `{{ "favicon.ico" | relURL }}`。
3. **站台根**(搜尋腳本要的 `data-baseurl`):`{{ "" | relURL }}`,不是 `"/" | relURL`。
4. **絕對網址**(canonical、社群分享圖、RSS):`.Permalink`,或 `{{ "og-default.png" | absURL }}`,同樣不帶開頭的斜線。
5. **選單**:一律 `pageRef`,不寫 `url`。`pageRef` 指到不存在的頁面時 Hugo 不報錯、只給空的連結 ——
   成品檢查會擋下空的 `href`。
6. **Markdown 內文的站內連結與圖片**(功能 3 定案):作者寫一般的 Markdown 連結,由 Hugo 解析。
   `hugo.toml` 設了 `markup.goldmark.renderHooks.link.useEmbedded = "always"`(圖片 `image` 同樣),
   `[字](/learning/one/)`、`[字](/learning/one)`、`[字](one.md)` 都會變成 `/BDGG_blog/learning/one/`。
   沒選 `relref` shortcode,是因為讀者在 GitHub 上看原稿時會看到一串 `{{< relref >}}`。
   - 指到不存在的頁面時 **Hugo 不報錯、原樣輸出**,靠成品檢查擋(實測:`/learning/nope/` 與 `nope.md` 都被擋下)
   - 頁內錨點 `[字](#標題)` 會被改寫成 `/BDGG_blog/learning/one/#標題`,仍然是同一頁,可以用
   - **圖片要放在文章旁邊**(文章改成 `content/<分區>/<檔名>/index.md`,圖放同一個目錄,寫 `![說明](圖.png)`)。
     放在 `static/` 再寫 `![](/img/x.png)` 不會被解析,成品檢查會擋

### 版面(功能 2,2026-10-05)

**站主這一項決定的事**

- **標語與說明換新的**,不沿用原架構的:標語「技術筆記、學習心得，與做過的專案」,
  說明「BDGG 的技術筆記、課程與學習心得、專案紀錄與隨筆。」(`hugo.toml` 的 `[params]`)。
- **分享圖重畫**:原圖印著舊網域與舊標語,不能搬。新圖同版面、同配色,字換成站名、標語與
  `yongrui0402.github.io/BDGG_blog`。
- **頁尾的「本機預覽版本」標記拿掉**,對應的樣式也沒搬。

**版型現在的樣子,以及之後各項要補的地方**

- 版型裡一律寫 `site.Title`、`site.Params.x`,不寫 `.Site.`。
- **`baseof`**:沒有 `data-baseurl`(功能 8 要加時寫 `data-baseurl="{{ "" | relURL }}"`);
  複製程式碼的腳本已在功能 3 加上;`{{ block "scripts" . }}` 已經在,
  功能 5、8 的版型直接 `{{ define "scripts" }}` 就會輸出。
- **`head`**:目前只有標題、作者、兩份樣式、favicon、GA4。說明文字、canonical、
  社群分享的 meta、feed 宣告、`article:published_time` 都留給功能 4。
  分享圖固定寫 `{{ "og-default.png" | absURL }}`;原版型依封面與 front matter `image` 換圖的那一段不搬。
- **`header`**:選單是空的時候不輸出 `<nav>`。目前選單只有「首頁」一項 ——
  原架構沒有這一項(站名本身就是回首頁的連結),這裡先放著讓選單看得到。
  功能 5 掛上分區時決定要不要留。
- **`footer`**:只有站名與 GitHub 連結。「標籤」連結功能 6 加,「RSS」連結功能 4 加。
- **`404`**:只有說明與回首頁。分區連結等功能 5、搜尋框等功能 8。
  這一頁會出現在任意深度的網址上,連結一定要是從網域根算起的路徑
  (`.RelPermalink`、`"x/" | relURL` 都是),不能寫相對路徑。
- **`single`** 已在功能 3 換成完整的文章頁;**`index`** 目前是「站名 + 暫時的文章清單」,功能 5 整份換掉。
- **`hugo.toml` 作者欄**:原架構那段匿名規則的註解沒有搬進來,功能 7 不必再處理它。

**`main.css`**

- 整份讀過後進來了。刪掉的段落:封面、閱讀進度條、分享、留言、相關文章、圖片(`.fig`)、
  喘息照、系列導覽、頁尾的預覽標記。之後各項搬版型時**不必再回來源拿樣式**。
- 還沒有版型在用、但留著等之後功能的段落:分類圖示、文章列表、排序、首頁的卡片、文章頁、
  目錄、標籤、分頁(功能 3、5、6);搜尋(功能 8);複製按鈕(功能 3);關於頁的技能標籤(功能 7)。
  **哪一項做完發現自己那一段有用不到的樣式,就在那一項刪掉** —— 收尾的驗收會查「沒有用不到的樣式」。
  關於頁的技能標籤(`.btn-inline`、`.btn-outline`)要在 Markdown 裡寫 HTML 才用得到
  (需要 `markup.goldmark.renderer.unsafe = true`),功能 7 不用的話整段刪。
- 文章列表(`.entry`、`.entry-tags`)已改成**沒有縮圖**的版本:拿掉縮圖的間距、標籤的左縮排、
  窄螢幕時改成直排的那一段。用一個假頁面照原版型的結構(去掉封面)在 360px 與深色下看過,
  功能 5 搬 `entry.html` 時再看一眼真的頁面。
- **`body` 多了 `overflow-wrap: break-word`**,原樣式沒有。實測 360px 寬時,內文一個很長的網址會把
  整頁撐出橫向捲軸(頁面寬度變成 1139px);加上之後長字串會從中間折行。
  `pre` 與表格不受影響,仍然是自己橫向捲。
- **表格在 360px 寬**:功能 3 已處理(表頭不換行、每一欄至少 5em),見「文章頁(功能 3)」。
- `syntax.css` 與 `markup.highlight.noClasses = false` 都已就位(功能 3),程式碼的顏色跟著深色模式切換。

**實測到的行為**

- **GitHub Pages 的 404**:`/BDGG_blog/` 底下任何不存在的網址(試過三種深度)都回 HTTP 404,
  內容就是成品的 `404.html`。子路徑以外的網址(`yongrui0402.github.io/別的`)是 GitHub 的通用 404,
  這個 repo 管不到。
- **GA4**:ID 留空時成品裡沒有追蹤碼;填一個假 ID,正式建置會輸出、`-e development` 不輸出。
  原版型的寫法 `{{ template "_internal/google_analytics.html" . }}` 在 0.165.0 沒有棄用警告,照搬。
- **選單**:掛滿 9 個項目(原架構全部分區加上最新、搜尋、關於)時,360px 寬會折成兩行,不會橫向捲。
  `pageRef` 的選單項目在自己那一頁會有 `class="active"`;404 頁上沒有任何一項是 active。
- **favicon** 副檔名是 `.ico`,內容其實是 32×32 的 PNG(原架構就是這樣),瀏覽器照樣顯示。圖上沒有文字。

**分享圖怎麼重畫**

- `python3 scripts/make_og_image.py` 會讀 `hugo.toml` 的站名、標語與 `baseURL`,寫出 `static/og-default.png`。
  **這三個值改了就要重跑,並把新的圖一起 commit** —— 建置時不會自動重畫。
  需要 Pillow 與 Noto Sans CJK 字型;不在 `make check` 裡,CI 不依賴它。
  同樣的輸入重跑,產出的檔案逐位元相同。
- 圖現在還沒有任何頁面引用。功能 4 加上 `og:image` 時,成品檢查要擴充到 `<meta content>` 裡的網址。

**怎麼驗「360px 沒有橫向捲動」與深淺色**

- 用本機的無頭 Chrome(遠端除錯埠)開頁面,設定視窗寬度與 `prefers-color-scheme`,
  比 `document.documentElement.scrollWidth` 與 `clientWidth`,順便記下所有回應碼 400 以上的請求。
  量測用的腳本只放在當次對話的暫存區,沒有進 repo。
- **先確認量得出問題**:這個方法在還沒加 `overflow-wrap` 時量到了 1139 / 360,所以它回報「沒有橫向捲動」是可信的。
  之後要驗時,記得用一個內容夠刁鑽的頁面(長網址、長程式碼、寬表格、很長的標題),只量首頁量不出東西。

### 文章頁(功能 3,2026-10-05)

**這一項定下的事**

- **第一篇文章**放在 `learning`(學習筆記):`content/learning/claude-mod-quick-test.md`。
  內容是當次對話實際做的測試(站主給題目,agent 起草,站主同意後發布)。
- **文章的 commit 用 `post:`**(例:`post: Claude mod 簡易測試與說明`),和改開發文件的 `docs:` 分開。
  這是自訂的 type,Conventional Commits 允許;檢查腳本會給一個「不在常見清單」的 WARN,可以忽略。
  站主若想改用別的寫法,從下一篇開始換即可,README 的「怎麼發一篇文」要跟著改。
- **文章網址** `/<分區>/<slug>/`,`[permalinks.page]` 六個分區都寫 `:slugorcontentbasename`。
  實測三種寫法:不設定時巢狀目錄會進網址(`/learning/nested/deep/`);原架構的 `:slug` 在沒寫 slug 時
  會退而用標題,中文標題就變成中文網址;`:slugorcontentbasename` 沒寫 slug 時用檔名。
- **分區列表頁還沒有**:`disableKinds` 多了 `"section"`。沒關的話 Hugo 找不到列表版型,
  `--panicOnWarning` 會讓建置失敗。關掉之後 `site.GetPage "/learning"` 仍然拿得到分區的 `title`,
  所以文章頁上的分區名稱照常顯示,只是**先顯示成文字**(`<span class="sect">`),不是連結。
- **標籤也先顯示成文字**(`<p class="tags"><span>#標籤</span>`)。
- **新增分區的做法**:一個分區第一次有文章時,先加 `content/<分區>/_index.md`(只要 `title`)。
  沒有它,文章頁上不會出現分區名稱(不會報錯)。目前只有 `learning` 有。
- **`make new POST=<分區>/<檔名>`**:規格沒列,加上是因為 Hugo 下載在 `.hugo-bin/`、不在 PATH 上,
  少了它範本用不到。
- **`hasCJKLanguage = true`**:原架構沒設。實測一篇八百多字的中文文章,沒設時字數算成 6、閱讀時間 1 分鐘;
  設了之後是 844 字、2 分鐘。功能 5 的摘要長度(`summaryLength`)也受這個設定影響。
- **`staleAfterMonths = 12`** 在 `hugo.toml` 的 `[params]`。過期提示用建置當下的時間算,
  所以一篇文章「過期」是在它滿 12 個月之後的下一次建置才會顯示,不是自動的。

**和原版型不同的地方(都是實測到問題才改的)**

- **深色模式下程式碼的標點看不見**。原 `syntax.css` 的淺色那份沒有包在媒體查詢裡,
  而 github-dark 那份沒有定義標點(`.p`)與 `.na`、`.nb`、`.bp` 的顏色,所以深色模式下這幾種
  留著淺色版的深色字。改成兩份各自包進 `prefers-color-scheme`。重新產生樣式時要記得兩份都包。
- **複製鈕會多複製空行**。原腳本用 `innerText`;上色後每一行是 `display:flex` 的區塊,
  `innerText` 會在行與行之間多補一個換行(實測:兩行的程式碼貼出來中間多一個空行)。
  改用 `textContent`,並拿掉結尾的換行(貼進終端機時不會直接執行)。
  沒有標語言的區塊不受影響,所以只測純文字區塊看不出這個問題。
- **表格**:表頭不換行、每一欄至少 `5em`。360px 寬時四欄的表格改成自己橫向捲(量到 400 / 320),
  不再把欄位擠成一行一兩個字;頁面本體仍然不捲。
- **`sect-name` 多一個判斷**:`content/` 根目錄的單頁沒有分區,原寫法會讓 `GetPage "/"` 拿到首頁、
  把站名當成分區名顯示。
- **空的區塊不輸出**:`toc: true` 但內文沒有 h2、h3 時不輸出目錄框;沒有上下篇時不輸出 `<nav class="pager">`。
- 版型裡一律 `site.Params`、`site.GetPage`(原版型是 `.Site.`)。

**之後各項要接的地方**

- **功能 4**:文章的 `description` 目前沒有任何版型在用,等 meta 與 RSS。
- **功能 5**:① 把 `"section"` 從 `disableKinds` 拿掉;② `single.html` 的分區從 `<span class="sect">` 改成連結,
  用 `(site.GetPage (printf "/%s" .Section)).RelPermalink`(原版型是 `"/x/" | relURL`,子路徑下會壞);
  ③ `index.html` 的暫時清單(`<section class="recent">`,只列分區底下的文章)整份換掉;
  ④ 其餘五個分區的 `_index.md`。原架構的 `_index.md` 還有 `blurb` 與一段內文,這次的 `learning/_index.md` 只有 `title`。
- **功能 6**:`single.html` 的標籤從 `<span>` 改成連結。`main.css` 的 `.tags a` 已經備好
  (顏色改成繼承 `.tags`,文字與連結同色)。
- **功能 7**:`single.html` 已經用 `.Section` 判斷 —— 沒有分區的單頁不輸出分區、日期、閱讀時間、
  過期提示與上下篇(用一個放在 `content/` 根目錄的假頁面看過)。關於頁直接用這份版型即可。
  要注意 front matter 的 `toc`、`key_points`、`takeaway`、`tags` 仍然會輸出,關於頁不要寫這幾個欄位。
- **功能 8**:搜尋索引要排除草稿以外,也留意 `where site.RegularPages "Section" "ne" ""` 這個條件
  (首頁清單用它排除根目錄的單頁)。

**實測到的行為**

- **發一篇文的時間**:`git push` 到公開網址回 200,**24 秒**(push 本身 2 秒)。零手動步驟。
  線上的 8 個檔案抓回來和本機 `make check` 的成品逐位元相同。
- **日期在未來的文章不會被建出來,而且沒有任何警告**。起草時把日期寫成半小時後,
  建置成功、成品檢查也通過,文章就是不在 —— 是用瀏覽器量測時拿到 404 才發現的。
  範本的 `date` 填的是開檔當下的時間,正常流程不會遇到;手改日期時要留意。README 有寫。
- **草稿**:`draft: true` 的文章 `make check` 之後不在 `public/` 裡;反過來用 `--buildDrafts` 建,
  成品檢查會因為 `draft-tag` 擋下來。兩個方向都試過。
- **未登入讀原稿**:GitHub 的 blob 頁回 200;raw 內容和本機檔案相同。
- **線上頁面**(無頭 Chrome,360 與 1280 寬、深淺色各一次):頁面本體沒有橫向捲動(360 / 360);
  12 個程式碼區塊在 360px 有 10 個自己橫向捲;深淺色的關鍵字顏色不同(淺 `rgb(207,34,46)`、深 `rgb(255,123,114)`);
  沒有 400 以上的請求、console 沒有錯誤;12 個複製鈕按下後剪貼簿的內容都等於原始碼。
- **手機上的複製鈕會蓋住第一行的右端**:觸控裝置沒有 hover,按鈕一律顯示(原設計)。
  程式碼可以橫向捲,被蓋住的字捲得出來。這次沒有改;要改的話是讓觸控裝置的 `pre` 上方多留一行。
- **`.TableOfContents`** 會輸出一個 `<nav id="TableOfContents">`,外面又包了一層 `<nav class="toc">`,
  是原版型的寫法,沒有動。

### 建置與成品檢查(功能 1)

- **`make check`** = 刪掉 `public/` → `hugo --gc --minify --panicOnWarning` → 檢查器的對照組測試 → 成品檢查。
  本機與 CI(`.github/workflows/deploy.yml`)跑的都是這一道。
- **建置前一定先刪 `public/`**:Hugo 不會清掉上一次留下的頁面(`--cleanDestinationDir` 只管 `static/`)。
  實測一篇用 `--buildDrafts` 建過的草稿,之後正常建置仍留在 `public/` 裡。
- **`--panicOnWarning`**:警告一律當成失敗。**已棄用的寫法也算** —— `languageCode` 與
  `.Language.LanguageCode` 在 0.158 起棄用,這個 repo 用 `locale` 與 `site.Language.Locale`。
  原版型裡若有 `.Site.LanguageCode`、`.Language.LanguageCode` 這類寫法,搬進來時要改。
- **`make preview`** 帶 `--buildDrafts --renderToMemory`:看得到草稿,而且不寫進 `public/`。
- **成品檢查**(`scripts/check_public.py`)看的是每個 HTML 的 `href` 與 `src`、class 含 `draft-tag` 的元素、
  以及所有檔案裡的 `192.168.`。之後的功能要注意:
  - 網址若放在別的屬性(`srcset`、`data-baseurl`、`<meta content>` 裡的分享圖),檢查器看不到,要跟著擴充
  - 草稿標記是 `layouts/_default/single.html` 裡 class 為 `draft-tag` 的元素;要改名就連檢查器與它的測試一起改
  - 新增一種要擋的情況,就在 `scripts/test_check_public.py` 加一個假成品,確認真的會擋
  - `--minify` 會拿掉屬性的引號(`class=draft-tag`),所以不能用 `grep 'class="draft-tag"'` 這種寫法檢查成品
- **還沒做到的頁面種類先關掉**(`hugo.toml` 的 `disableKinds`),輪到時再打開:
  RSS、sitemap、`robots.txt` → 功能 4;`section`(分區列表頁,功能 3 關上的)→ 功能 5;
  `taxonomy`、`term` → 功能 6。(`404` 已在功能 2 打開。)
- 功能 1 的測試頁 `content/link-test.md` 與選單的「連結測試」已在功能 2 拿掉。
- **workflow 只用 GitHub 官方的三個 action**(`checkout@v7`、`upload-pages-artifact@v5`、`deploy-pages@v5`),
  不覆蓋 `baseURL`(直接用 `hugo.toml` 的值)。
- **時區**寫在 `hugo.toml` 的 `timeZone = "Asia/Taipei"`(功能 3),不靠 CI 的環境變數,本機與 CI 的成品才會一樣。
- 本機需要 Python 3.11 以上(檢查器用標準函式庫的 `tomllib` 讀 `hugo.toml`)。
- **`main` 上有一筆故意建不起來的 commit**:`1e09eca`(功能 1 的失敗測試,站主選擇照驗收原文推到 `main`),
  下一筆 `fb80377` 還原。收尾檢查「`main` 每個 commit 都建得起來」時,這一筆是已知的例外。
- **GitHub 預告 `ubuntu-latest` 自 2026-10-19 起換成 Ubuntu 26**(Actions 的執行紀錄上有提示)。
  workflow 只靠 `make`、`curl`、`python3`,預期不受影響;那之後第一次 push 留意一下 Actions 是不是綠的。

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
