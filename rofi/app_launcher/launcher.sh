#!/usr/bin/env bash

## Author  : Aditya Shakya
## Mail    : adi1090x@gmail.com
## Github  : @adi1090x
## Twitter : @adi1090x

# Available Styles
# >> Created and tested on : rofi 1.6.0-1
#
# style_1     style_2     style_3     style_4     style_5     style_6     style_7

theme="pywal"

dir="$HOME/.config/rofi/app_launcher"
styles=($(ls -p --hide="colors.rasi" $dir/styles))
#olor="${styles[$(( $RANDOM % 10 ))]}"

# comment this line to disable random colors
#ed -i -e "s/@import .*/@import \"$color\"/g" $dir/styles/colors.rasi

# comment these lines to disable random style
#emes=($(ls -p --hide="launcher.sh" --hide="styles" $dir))
#heme="${themes[$(( $RANDOM % 7 ))]}"

rofi -no-lazy-grab -show drun \
-modi run,drun,window \
-icon-theme "Papirus-dark" \
-theme $dir/"$theme"

