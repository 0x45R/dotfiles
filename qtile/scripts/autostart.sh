xrandr --output DP-1 --noprimary --auto --left-of HDMI-1
xrandr --output HDMI-1 --mode "1920x1080" --primary
wal -R
picom &
blueman-tray &
syncthing & 
discord &
pa-applet &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
setxkbmap -model pc104 -layout us,pl -variant ,, -option grp:alt_shift_toggle &

