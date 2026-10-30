# dotfiles

Ghostty + herdr 的終端機設定，加上一個切換深色／淺色的 `term-theme` 指令。

## 新電腦安裝

```sh
git clone https://github.com/<you>/dotfiles ~/dotfiles
~/dotfiles/install.sh
```

`install.sh` 會：

1. 用 Homebrew 安裝 herdr、gh、Ghostty 和 JetBrains Mono Nerd Font。
2. 把設定連到這個 repo（原本的檔案會改名成 `*.backup-時間`）：
   - `~/.config/ghostty` → `ghostty/`
   - `~/.config/herdr/config.toml` → `herdr/config.toml`
   - `~/.config/herdr/quota-status.py` → `herdr/quota-status.py`
   - `~/.local/bin/term-theme` → `bin/term-theme`
3. 安裝 herdr 外掛：usagebar、zoetrope、space-groups。
4. 套用深色配色。

因為是連結，改設定就是改這個 repo 裡的檔案，改完記得 commit。

## 切換配色

```sh
term-theme dark    # Tokyo Night Night
term-theme light   # Solarized Light
term-theme list    # 列出所有組合，* 是目前用的
```

一次切換 Ghostty 和 herdr，不用重開。配色組合寫在 `bin/term-theme` 最上面的 `PROFILES`，要加新組合就照格式多加一組。

`term-theme` 會覆蓋 `ghostty/term-theme.ghostty`，以及 herdr 設定裡的 `[theme]`、`[theme.custom]` 和左側 agent 列的 `fg` 顏色。這些部分請改 `PROFILES`，不要直接改設定檔。

Claude Code 的主題不在範圍內，切換後用 `/theme` 自己調。

## 注意

- `herdr/config.toml` 裡 tab bar 的用量指令寫的是絕對路徑（`/opt/homebrew/opt/python@3.13/...`、`/Users/xpizta/...`）。新電腦的使用者名稱或 Python 版本不同時要改。
- space-groups 的分組（`herdr plugin config-dir yojahny55.space-groups` 裡的 `groups.json`）沒有放進來，每台電腦各自設定。
