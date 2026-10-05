---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
# 網址的最後一段:/<分區>/<slug>/。發布之後就不要再改,改了舊連結會失效。
slug: {{ .Name }}
tags: []
# 文首要不要放目錄(取內文的 h2、h3)。短文可以改成 false。
toc: true

# 一句話,寫事實。之後會用在文章列表、搜尋結果與社群分享的摘要。
description:

# 讀完只記得一句話的話,是哪一句。會顯示在文末。(選填)
takeaway:

# 2 到 5 條結論,每一條單獨看都成立。會顯示在文首。(選填)
key_points: []

# true 的時候只有 make preview 看得到,不會出現在線上的站。
# 寫完改成 false 再 push 才會發布。注意:這個 repo 是公開的,草稿的原稿在 GitHub 上仍然看得到。
draft: true
---
