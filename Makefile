# 本機與 CI 跑同一道指令:make check。
# Hugo 的版本只寫在 .hugo-version,這裡依它下載同一版到 .hugo-bin/。
#
# 自動下載只支援 Linux(amd64 / arm64)。其他平台請自己裝同一版的 Hugo extended,
# 照 build 與 check 底下的指令手動跑。

HUGO_VERSION := $(shell cat .hugo-version)
HUGO_ARCH    := $(shell uname -m | sed -e 's/x86_64/amd64/' -e 's/aarch64/arm64/')
HUGO_TARBALL := hugo_extended_$(HUGO_VERSION)_linux-$(HUGO_ARCH).tar.gz
HUGO_SUMS    := hugo_$(HUGO_VERSION)_checksums.txt
HUGO_RELEASE := https://github.com/gohugoio/hugo/releases/download/v$(HUGO_VERSION)
HUGO         := .hugo-bin/hugo-$(HUGO_VERSION)

.PHONY: help preview build check clean

help:
	@echo "make preview  本機預覽(含草稿),存檔即重新整理"
	@echo "make build    建置到 public/"
	@echo "make check    建置 + 成品檢查;push 之前跑這個,CI 跑的也是這個"
	@echo "make clean    刪掉 public/ 與 Hugo 的快取"

# 檔名帶版本號,所以改了 .hugo-version 就會重新下載
$(HUGO):
	mkdir -p .hugo-bin
	cd .hugo-bin && curl -fL --retry 3 -O $(HUGO_RELEASE)/$(HUGO_TARBALL) -O $(HUGO_RELEASE)/$(HUGO_SUMS)
	cd .hugo-bin && grep ' $(HUGO_TARBALL)$$' $(HUGO_SUMS) | sha256sum -c -
	tar -xzf .hugo-bin/$(HUGO_TARBALL) -C .hugo-bin hugo
	mv .hugo-bin/hugo $@
	rm .hugo-bin/$(HUGO_TARBALL) .hugo-bin/$(HUGO_SUMS)

# --renderToMemory:預覽不寫進 public/,免得帶草稿的頁面留在成品目錄裡
preview: $(HUGO)
	$(HUGO) server --buildDrafts --renderToMemory

# 先刪 public/:Hugo 不會清掉上一次建置留下的頁面(--cleanDestinationDir 只管 static/),
# 不刪的話,改過名或刪掉的文章會留在本機成品裡,和 CI 從零建出來的不一樣。
# --panicOnWarning:Hugo 的警告(找不到版型、用了已棄用的寫法)一律當成建置失敗。
build: $(HUGO)
	rm -rf public
	$(HUGO) --gc --minify --panicOnWarning

# 先確認檢查器自己會擋,再拿它檢查成品
check: build
	python3 scripts/test_check_public.py
	python3 scripts/check_public.py public

clean:
	rm -rf public resources .hugo_build.lock
