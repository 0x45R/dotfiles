#/usr/bin/env sh

theme="pywal"
dir="$HOME/.config/rofi/app_launcher"

rofi -no-lazy-grab -show drun \
-modi drun \
-theme $dir/"$theme"
