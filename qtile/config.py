import pywal, json, os, subprocess, customwidgets
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget import modify
from qtile_extras.widget.decorations import RectDecoration, BorderDecoration

SUPER, ALT = "mod4", "mod1"
PYWAL_COLORS = json.load(open(pywal.settings.CACHE_DIR+"/colors.json","rb"))

terminal_application = guess_terminal()
web_browser_application = "librewolf"
app_launcher = os.path.expanduser('~/.config/qtile/scripts/app_launcher.sh')

amount_of_workspaces = 6

@lazy.function
def run_script_path(qtile,value):
    path = os.path.expanduser(value)
    subprocess.Popen(["sh", path])

@hook.subscribe.startup_complete
def autostart():
    autostart_path = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    subprocess.Popen(["sh",autostart_path])

def setup_keys(keys = []):
    system_keybindings = [
        Key([SUPER, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
        Key([SUPER, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

        Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+"), desc="Increase volume using XF86"),
        Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-"), desc="Decrease volume using XF86"),
        Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle"), desc="Switch mute"),

        Key([SUPER], "l", lazy.spawn("dm-tool switch-to-greeter"), desc="Switch to greeter (lock)")
    ]
    keys.extend(system_keybindings)

    workspace_keybindings = [
        Key([SUPER], "Left", lazy.layout.left(), desc="Move focus to left"),
        Key([SUPER], "Right", lazy.layout.right(), desc="Move focus to right"),
        Key([SUPER], "Down", lazy.layout.down(), desc="Move focus down"),
        Key([SUPER], "Up", lazy.layout.up(), desc="Move focus up")
    ]
    keys.extend(workspace_keybindings)

    window_keybindings = [
        Key([ALT], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
        Key([ALT], "F4", lazy.window.kill()),

        Key([SUPER, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
        Key([SUPER, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
        Key([SUPER, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
        Key([SUPER, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

        Key([SUPER, "shift", "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
        Key([SUPER, "shift", "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
        Key([SUPER, "shift", "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
        Key([SUPER, "shift", "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
        Key([SUPER], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

        Key([SUPER], "space", lazy.window.toggle_floating(), desc="Toggle window floating"),
        Key([SUPER], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
        Key([SUPER], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
        
        Key([SUPER], "w", lazy.to_screen(0)),
        Key([SUPER], "e", lazy.to_screen(1))
    ]
    keys.extend(window_keybindings)

    application_keybindings = [
        Key([SUPER], "Return", lazy.spawn(terminal_application), desc="Launch terminal"),
        Key([SUPER, "Shift"], "w", lazy.spawn(web_browser_application), desc="Launch web browser"),
        Key([SUPER], "d", run_script_path(app_launcher), desc="Launch rofi"),
        Key([], "Print", lazy.spawn("scrot 'Screenshot_%a-%d%b%y_%H.%M.png' -e 'mv $f ~/Screenshots/'"))
    ]
    keys.extend(application_keybindings)
    return keys

keys = setup_keys()

def setup_groups(groups = []):
    groups = [Group(str(i+1)) for i in range(0,amount_of_workspaces)]
    for i in groups:
        keys.extend([
            Key(
                [SUPER],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [SUPER, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ])

    return groups

groups = setup_groups()

layouts = [
    layout.Columns(
        border_normal=PYWAL_COLORS["special"]["background"],
        border_focus=PYWAL_COLORS["special"]["foreground"], 
        border_width=4, 
        margin=[10,10,10,10]
    )
]

widget_defaults = dict(
    font="SauceCodePro Nerd Font",
    fontsize=12,
    border_width=4,
    border_color=PYWAL_COLORS["special"]["foreground"],
    padding=20,
    foreground=PYWAL_COLORS["special"]["foreground"],
    decorations=[
        RectDecoration(clip=True, colour=PYWAL_COLORS["special"]["background"], radius=15, filled=True, padding_y=0),
    ]
)
extension_defaults = widget_defaults.copy()

def setup_top_bar():
    widgets = [
        modify(customwidgets.Button, default_text="", function=subprocess.Popen, function_args=['sh',app_launcher]),      
        widget.Spacer(length=5, background="#FFFF0000", decorations=[]),
        widget.GroupBox(highlight_method="line",highlight_color=['ff000000'], padding = 10, borderwidth=2, disable_drag=True, this_current_screen_border=PYWAL_COLORS["special"]["foreground"], active=PYWAL_COLORS["colors"]["color6"],inactive=PYWAL_COLORS["colors"]["color1"]),
        widget.Spacer(background="#FFFF0000", decorations=[]),
        widget.Mpris2(name="spotify", display_metadata=["xesam:title", "xesam:artist"]),
        widget.Spacer(background="#FFFF0000", decorations=[]),
        widget.Net(format='  {interface}: {down} ↓↑ {up}'),
        widget.Spacer(background="#FFFF0000", length=5, decorations=[]),
        widget.DF(visible_on_warn=False, format=" {p} ({uf}{m}B, {r:.0f}%)"),
        widget.Spacer(length=5, background="#FFFF0000", decorations=[]),
        widget.Clock(format=" %d.%m.%Y %a  %H:%M:%S"),
    ]
    result = bar.Bar(widgets=widgets, size=32, margin=[10,10,0,10], background="#FFFF0000")
    return result

def setup_bottom_bar():
    widgets = [
        widget.TextBox("- Steam wishlist widget coming soon... -", padding=10, decorations=[]),
        widget.Spacer(background="#FF000000", decorations=[]),
        widget.Systray(padding=10, icon_size=20, decorations=[]),
        widget.Spacer(length=5, background="#FF000000", decorations=[]),
        widget.QuickExit(default_text="", countdown_format="{}", countdown_start=6),
    ]
    result = bar.Bar(widgets=widgets, size=32, margin=[0,10,10,10], background="#00000000", opacity=1)
    return result

screens = [
    Screen(
        top = setup_top_bar(),
        bottom = setup_bottom_bar()
    )
]

mouse = [
    Drag([SUPER], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([SUPER], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([SUPER], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    border_normal=PYWAL_COLORS["special"]["background"],
    border_focus=PYWAL_COLORS["special"]["foreground"], 
    border_width=4, 
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True
wl_input_rules = None

wmname = "qtile"
