import pywal, json, os, subprocess, customwidgets
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget import modify
from qtile_extras.widget.decorations import RectDecoration

SUPER, ALT = "mod4", "mod1"
PYWAL_COLORS = json.load(open(pywal.settings.CACHE_DIR+"/colors.json","rb"))

terminal_application = guess_terminal()
web_browser_application = "librewolf"

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
        Key([SUPER], "Tab", lazy.next_layout(), desc="Toggle between layouts")
    ]
    keys.extend(window_keybindings)

    application_keybindings = [
        Key([SUPER], "Return", lazy.spawn(terminal_application), desc="Launch terminal"),
        Key([SUPER, "Shift"], "w", lazy.spawn(web_browser_application), desc="Launch web browser"),
        Key([SUPER], "d", run_script_path('~/.config/qtile/scripts/app_launcher.sh'), desc="Launch rofi")
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
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ])

    return groups

groups = setup_groups()

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=0, margin=[10,10,10,10])
]

widget_defaults = dict(
    font="Inconsolata",
    fontsize=14,
    padding=20,
    foreground=PYWAL_COLORS["special"]["foreground"],
    decorations=[
        RectDecoration(colour=PYWAL_COLORS["special"]["background"], radius=10, filled=True, padding_y=0)
    ]
)
extension_defaults = widget_defaults.copy()

def setup_top_bar():
    widgets = [
        modify(customwidgets.Button, default_text=""),      
        widget.Spacer(length=10, background="#FFFF0000", decorations=[]),
        widget.GroupBox(highlight_method="line", padding = 10),
        widget.Spacer(background="#FFFF0000", decorations=[]),
        widget.Mpris2(display_metadata=["xesam:title", "xesam:artist"]),
        widget.Spacer(background="#FFFF0000", decorations=[]),
        widget.Net(format=' {interface}: {down} ↓↑ {up}'),
        widget.Spacer(background="#FFFF0000", length=10, decorations=[]),
        widget.DF(visible_on_warn=False, format=" {p} ({uf}{m}B, {r:.0f}%)"),
        widget.Spacer(length=10, background="#FFFF0000", decorations=[]),
        widget.Clock(format=" %d.%m.%Y %a  %H:%M:%S", font="Inconsolata bold"),
    ]
    result = bar.Bar(widgets=widgets, size=32, margin=[10,10,10,10], background="#FFFF0000") # PYWAL_COLORS["special"]["background"])
    return result

def setup_bottom_bar():
    widgets = [
        widget.TextBox("- Steam wishlist widget coming soon... -", padding=0),
        widget.Spacer(background="#FF000000", decorations=[]),
        widget.Systray(padding=10),
        widget.Spacer(length=10, background="#FF000000", decorations=[]),
        widget.QuickExit(padding=10, default_text="", countdown_format="{}", countdown_start=6),
    ]
    result = bar.Bar(widgets=widgets, size=20, margin=[10,10,10,10], background="#00000000", opacity=1)
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

wmname = "LG3D"