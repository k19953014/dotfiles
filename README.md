# dotfiles

Ghostty + herdr 的終端機設定，加上一個切換深色／淺色的 `term-theme` 指令。

## 新電腦安裝

```sh
git clone https://github.com/k19953014/dotfiles ~/dotfiles
~/dotfiles/install.sh
```

`install.sh` 會：

1. 用 Homebrew 安裝 herdr、gh、Ghostty 和 JetBrains Mono Nerd Font。
2. 把設定連到這個 repo（原本的檔案會改名成 `*.backup-時間`）：
   - `~/.config/ghostty` → `ghostty/`
   - `~/.config/herdr/config.toml` → `herdr/config.toml`
   - `~/.local/bin/term-theme` → `bin/term-theme`
3. 安裝 herdr 外掛：zoetrope、space-groups，並把 space-groups 的分組設定
   `~/.config/herdr/plugins/config/yojahny55.space-groups/groups.json` 連到 `herdr/space-groups/groups.json`。
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
- 如果之後發現 `groups.json` 變回一般檔案（不是連結），代表外掛存檔時把連結換掉了，把它搬回 repo 再重跑 `install.sh` 即可。

## Codex 壓縮設定與續做規則

`install.sh` 會以 Python 3.11 以上版本執行 `codex/install.py`，合併以下內容：

- `codex/config.toml`：自動壓縮門檻 217,600 tokens（gpt-6-astra 的 272,000 容量 × 80%）、計算完整上下文，以及保留目標、限制、進度、驗證結果與下一步的摘要指令。這是固定 token 值，換不同容量的模型時需重新計算；不會自動切換模型。
- `codex/AGENTS.md`：壓縮後恢復狀態並接續工作，不將壓縮視為完成。

只同步這些選定設定，保留本機其他設定與 AGENTS.md 規則，不複製登入憑證、MCP 設定、工作區絕對路徑、對話紀錄或快取。修改來源檔後需要重新執行合併；這兩個檔案不使用符號連結。變更前會在目標目錄產生 `*.backup-時間` 備份，重複執行不會重複加入規則。

只套用 Codex 設定：

```sh
python3 ~/dotfiles/codex/install.py
# 自訂位置：
python3 ~/dotfiles/codex/install.py --codex-home /path/to/codex-home
```

需要 Python 3.11 以上（使用標準函式庫 tomllib）；主安裝腳本會透過 Homebrew 安裝 Python 3.13。重新啟動 Codex 並開啟新對話，以確保設定重新載入。
