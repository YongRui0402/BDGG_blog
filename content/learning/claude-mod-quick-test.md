---
title: "Claude mod 簡易測試與說明"
date: 2026-10-05T17:09:00+08:00
slug: claude-mod-quick-test
tags: [Claude Code, mod]
toc: true

description: 用一個 20 行的 mod 擋下 Claude Code 對建置成品的編輯，並用三種方式確認它真的有作用。

takeaway: mod 是用程式改寫 Claude Code 行為的地方；寫完不要只看「測試通過」，把它弄壞一次，確認測試真的會失敗。

key_points:
  - mod 是 Claude Code 的一種外掛：三個檔案，核心是一支掛在事件上的 TypeScript 模組
  - 每個 hook 的形狀都是 `($, e, next)`：不呼叫 `next` 就是自己回答，呼叫就是放行
  - "`claude plugin validate` 看結構、`claude plugin test` 跑測試、`claude -p --plugin-dir` 實際載入，三種檢查各看不同的事"
  - 這套 API 還在早期，版本之間會變；這篇的內容以 Claude Code 2.1.289 為準

draft: false
---

Claude Code 可以用 **mod** 改變它自己的行為：在提示框上面多一列資訊、開一個即時面板、加一個斜線指令，或是在它呼叫工具之前攔下來檢查。這篇用一個很小的 mod 走一遍「寫出來、檢查、實際載入」，並記下每一步真正看到的輸出。

測試環境是 Linux 上的 Claude Code 2.1.289，日期 2026-10-05。這個 mod 是我請 Claude Code 寫的，下面的指令也都是它在同一個工作階段裡實際跑的，輸出照貼，只把過長的絕對路徑縮短。

## mod 是什麼

mod 是一個資料夾，裡面是一個帶有「函式 hook」的外掛（plugin）。最少三個檔案：

```
public-guard/
├── .claude-plugin/
│   └── plugin.json      # 名稱、版本、一行說明
└── hooks/
    ├── hooks.json       # 指出 hook 模組是哪一個檔案
    └── register.ts      # hook 模組本體
```

`register.ts` 匯出一個 `register` 函式，用 `on(事件, 條件, hook)` 把函式掛到事件上。每個 hook 都收到同樣的三個參數：

| 參數 | 是什麼 |
|---|---|
| `$` | 引擎的介面：顯示、工具、檔案、時鐘等等，模組要碰外面的東西都得經過它 |
| `e` | 這次事件的輸入，例如工具名稱與參數 |
| `next` | 呼叫 `next(e)` 會交給下一層（其他外掛，最後是 Claude Code 自己的行為） |

所以一個 hook 能做的事只有三種：**不呼叫 `next`，自己回答**；**改一改 `e` 再呼叫 `next`**；或是**先 `await next(e)`，拿到結果之後再做事**。

模組跑在它自己的環境裡，沒有 DOM、也沒有 Node 的 API —— 不能直接 `import fs`，要讀檔就得用 `$` 提供的方法。

## 這次測的 mod：不准直接改建置成品

這個部落格用 Hugo 產生，`public/` 是建置出來的成品，每次建置都會整個重做。直接改裡面的檔案沒有意義，下一次建置就不見了。所以拿它當題目：**Claude Code 想用 Edit 工具改 `public/` 底下的檔案時，擋下來，並告訴它該去改哪裡。**

`.claude-plugin/plugin.json`：

```json
{
  "name": "public-guard",
  "version": "0.1.0",
  "description": "不讓 Claude 直接改 public/ 裡的建置成品"
}
```

`hooks/hooks.json`：

```json
{ "modules": ["./register.ts"] }
```

`hooks/register.ts`：

```ts
import type { Register } from 'claude-code'

// public/ 是 Hugo 的建置成品，每次建置都會整個重做，手改的內容留不住
const BUILD_OUTPUT = /(^|\/)public\//

export const register: Register = on => {
  let blocked = 0

  on('tool.call', { tool: 'Edit' }, ($, e, next) => {
    if (!BUILD_OUTPUT.test(e.file_path)) {
      return next(e)
    }

    blocked += 1
    $.ui.status(`public-guard：已擋下 ${blocked} 次`)

    return {
      deny: `${$.plugin.name}: ${e.file_path} 是建置成品，請改 content/ 或 layouts/ 裡的來源。`,
    }
  })
}
```

重點只有中間那個判斷：路徑不在 `public/` 底下就 `return next(e)` 放行；在的話回傳 `{ deny: 原因 }`，這次工具呼叫就不會執行，原因會回到模型手上。

## 檢查一：結構對不對

```bash
claude plugin validate ./public-guard
```

```
Validating plugin manifest: …/public-guard/.claude-plugin/plugin.json

⚠ Found 1 warning:

  ❯ author: No author information provided. Consider adding author details for plugin attribution

Validating hooks: …/public-guard/hooks/hooks.json

  ❯ ./register.ts hooks: tool.call{tool=Edit}
  ❯ ./register.ts calls: $.ui.status

✔ Validation passed with warnings
```

有用的是中間那兩行：它讀了模組的原始碼，列出**引擎認為這個模組掛了哪些事件、呼叫了 `$` 的哪些方法**。這裡列的和我想的一樣（掛在 `tool.call`、只管 Edit、會動到狀態列），代表引擎看到的就是我要的。唯一的警告是 `plugin.json` 沒填作者，不影響載入。

## 檢查二：行為對不對

mod 可以寫測試。測試檔放在 mod 的資料夾裡，檔名以 `.test.ts` 結尾，工具從 `claude-code/testing` 匯入：

```ts
import { expect, test } from 'claude-code/testing'

const EDIT = { tool: 'Edit', old_string: 'a', new_string: 'b' } as const

test('public/ 底下的檔案改不了', async ($, on) => {
  let reached = 0
  // 測試裡的這個 hook 站在 mod 的下面，代替引擎：走得到這裡就代表 mod 放行了
  on('tool.call', () => {
    reached += 1

    return { result: 'edited' }
  })

  const out = await $.tool.call({ ...EDIT, file_path: 'public/index.html' })

  expect(reached).toBe(0)
  expect(JSON.stringify(out)).toContain('建置成品')
})

test('其他檔案照常放行', async ($, on) => {
  let reached = 0
  on('tool.call', () => {
    reached += 1

    return { result: 'edited' }
  })

  await $.tool.call({ ...EDIT, file_path: 'content/learning/post.md' })

  expect(reached).toBe(1)
})
```

測試裡的 `on` 掛的 hook 位在所有外掛的**下面**，等於假扮引擎。所以「mod 有沒有放行」可以直接用「下面那一層有沒有被叫到」來判斷，不需要真的去改檔案。

```bash
claude plugin test ./public-guard
```

```
hooks/register.test.ts:
(pass) public/ 底下的檔案改不了 [34.48ms]
(pass) 其他檔案照常放行 [14.52ms]

 2 pass
 0 fail
Ran 2 tests across 1 file. [0.19s]
```

兩個都過。但只看到「通過」還不夠 —— 一份永遠通過的測試也會顯示通過。所以把 mod 故意弄壞一次：把判斷的目錄從 `public/` 改成 `dist/`，再跑同一道指令：

```
hooks/register.test.ts:
(fail) public/ 底下的檔案改不了 [34.40ms]
  AssertionError: expect(received).toBe()

  Expected: 0
  Received: 1
(pass) 其他檔案照常放行 [13.50ms]

 1 pass
 1 fail
```

第一個測試失敗了，而且失敗的原因正是「下面那一層被叫到了一次」，也就是 mod 沒擋住。這樣才能說這份測試真的在看我要它看的事。改回來之後又是 2 pass。

## 檢查三：真的載入跑一次

前兩步都沒有真的啟動 Claude Code。最後用 `--plugin-dir` 把 mod 載進一個不互動的工作階段，叫它去改 `public/` 裡的檔案。

先準備一個測試用的資料夾，裡面只有一個 `public/index.html`，內容是 `<h1>hello</h1>`。然後同一句提示跑兩次，一次不載入 mod、一次載入：

```bash
# 對照組：不載入 mod
claude -p "用 Edit 工具把 public/index.html 裡的 hello 改成 world。只試一次,不要改用別的工具或別的方法;失敗的話把工具回傳的訊息原文貼給我。" \
  --model haiku --permission-mode acceptEdits --allowedTools Read Edit

# 載入 mod：多一個 --plugin-dir
claude -p "（同一句提示）" \
  --model haiku --permission-mode acceptEdits --allowedTools Read Edit \
  --plugin-dir ./public-guard
```

| | Claude 的回答 | 跑完之後檔案的內容 |
|---|---|---|
| 不載入 mod | 完成。`hello` 已改成 `world`。 | `<h1>world</h1>` |
| 載入 mod | 貼出工具回傳的錯誤訊息（見下） | `<h1>hello</h1>`，沒有被改 |

載入 mod 那一次，模型拿到的訊息是：

```
public-guard: …/demo/public/index.html 是建置成品，請改 content/ 或 layouts/ 裡的來源。
```

就是 `register.ts` 裡寫的那一句。沒有 mod 的時候檔案被改了，有 mod 的時候沒有 —— 差別只在那個旗標，所以擋下它的確實是這個 mod。

## mod 還能做什麼

`tool.call` 只是其中一種事件。依 Claude Code 內建的說明，常見的需求大致對應到這些寫法（**這張表我只實測了第一列**）：

| 想做的事 | 寫法 |
|---|---|
| 擋下、改寫工具呼叫，或在它跑完之後做事 | `on('tool.call', { tool }, hook)` |
| 改寫或回應使用者送出的提示 | `on('prompt.submit', hook)` |
| 狀態列多一項資訊 | 在任何 hook 裡呼叫 `$.ui.status(文字)` |
| 跳一個通知 | 在任何 hook 裡呼叫 `$.ui.toast(文字)` |
| 提示框上面多一列 | 掛在 `ui.render`，條件是 `{ component: 'AbovePrompt' }` |
| 開一個面板 | `$.ui.open({ id, title })`，再用 `ui.render` 畫內容 |
| 加一個斜線指令 | 在 `session.start` 裡 `$.command.register(...)`，用 `command.run` 回應 |

想自己寫的話，最省事的做法是直接在 Claude Code 裡說「幫我做一個 mod」加上你要的行為。它會先載入內建的說明與這一版的型別定義再動手；這次就是這樣做的，上面那兩道檢查也是說明裡要求寫完要跑的。

## 這次沒有測到的

- **畫面上的東西**。狀態列那一行（`$.ui.status`）在不互動的工作階段裡看不到，所以我只確認了 `validate` 有列出這個呼叫，沒有親眼看到它顯示。面板、提示框上方那一列也都沒測。
- **熱重載**。依內建說明，在互動的工作階段裡同意開啟之後，mod 存檔會在那一輪結束時自動重新載入；這次用的是每次都從頭載入的 `claude -p`，沒有走到這一段。
- **Write 與 Bash**。這個 mod 只管 Edit。模型如果改用 Write 整份覆寫，或用 Bash 跑 `sed`，它擋不到 —— 真的要拿來用，得把這幾條路一起補上。上面的實測在提示裡要求「只試一次、不要換方法」，並且只開放 Read 與 Edit 兩種工具，就是為了不讓這件事干擾結果。

最後一點提醒：這套 API 官方標示為早期版本，不同版本之間會變動。這篇的事件名稱與指令以 2.1.289 為準，之後照抄跑不起來的話，先看那一版的型別定義。
