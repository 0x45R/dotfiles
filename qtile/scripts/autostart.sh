xrandr --output DisplayPort-0 --noprimary --auto --left-of HDMI-A-0
xrandr --output HDMI-A-0 --mode "1920x1080" --primary
picom &
wal -R &
setxkbmap -model pc104 -layout us,pl -variant ,, -option grp:alt_shift_toggle &

