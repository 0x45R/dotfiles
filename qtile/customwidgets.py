from libqtile.widget import base
from libqtile import bar, hook
class Button(base._TextBox):
    defaults = [
        ("default_text", "Button")
    ]

    def __init__(self, width=bar.CALCULATED,**config):
        base._TextBox.__init__(self, "", width, **config)
        self.add_defaults(Button.defaults)
    
        self.text = self.default_text
        self.add_callbacks({"Button1": self.trigger})

    def trigger(self):
        self.text ="aaa"
        self.bar.draw()
