#!/usr/bin/env bash
# 在新電腦上安裝 Ghostty + herdr + term-theme 設定。
# 用法：git clone https://github.com/<you>/dotfiles ~/dotfiles && ~/dotfiles/install.sh
set -euo pipefail

DOTFILES="$(cd "$(dirname "$0")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"

# 把 target 換成指向 repo 的連結；原本有檔案就先改名備份
link() {
  local src="$DOTFILES/$1" target="$2"
  mkdir -p "$(dirname "$target")"
  if [ -L "$target" ] && [ "$(readlink "$target")" = "$src" ]; then
    echo "ok      $target"
    return
  fi
  if [ -e "$target" ] || [ -L "$target" ]; then
    mv "$target" "$target.backup-$STAMP"
    echo "backup  $target -> $target.backup-$STAMP"
  fi
  ln -s "$src" "$target"
  echo "link    $target -> $src"
}

if command -v brew >/dev/null; then
  brew install herdr gh
  brew install --cask ghostty font-jetbrains-mono-nerd-font
else
  echo "沒有 Homebrew，跳過安裝程式。請先裝 https://brew.sh 再重跑一次。"
fi

link ghostty ~/.config/ghostty
link herdr/config.toml ~/.config/herdr/config.toml
link herdr/quota-status.py ~/.config/herdr/quota-status.py
link bin/term-theme ~/.local/bin/term-theme

# macOS 上 Ghostty 也會讀 Application Support 裡的設定，先移開以免蓋掉 repo 的設定
GA="$HOME/Library/Application Support/com.mitchellh.ghostty"
for f in config config.ghostty; do
  if [ -f "$GA/$f" ]; then
    mv "$GA/$f" "$GA/$f.backup-$STAMP"
    echo "backup  $GA/$f"
  fi
done

if command -v herdr >/dev/null; then
  herdr plugin install -y senna-lang/herdr-agent-usage || true
  herdr plugin install -y furkankly/zoetrope/herdr-plugin || true
  herdr plugin install -y yojahny55/herdr-space-groups || true
fi

# 沒有選過配色就先用深色
[ -f "$DOTFILES/ghostty/term-theme.ghostty" ] || "$DOTFILES/bin/term-theme" dark || true

echo
echo "完成。若 ~/.local/bin 不在 PATH，請在 ~/.zshrc 加上：export PATH=\"\$HOME/.local/bin:\$PATH\""
