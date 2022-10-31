#/usr/bin/env sh

## Author  : Aditya Shakya
## Mail    : adi1090x@gmail.com
## Github  : @adi1090x
## Twitter : @adi1090x

theme="style_7"

dir="$HOME/.config/rofi/launchers/text"
styles=($(ls -p --hide="nightly.rasi" $dir/styles))
color="${styles[$(( $RANDOM % 10 ))]}"

rofi -no-lazy-grab -show drun \
-modi drun,window \
-theme $dir/"$theme"
