#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Widgets - Reusable terminal widgets."""

class TerminalWidget:
    """Base class for terminal widgets."""

    def __init__(self, theme=None):
        from geex.core.config import Config
        from geex.core.theme import Theme
        self.theme = theme or Theme(Config())

    def render(self):
        """Render the widget. Override in subclasses."""
        return ""

class TextWidget(TerminalWidget):
    """Simple text widget."""

    def __init__(self, text, color=None, bold=False, theme=None):
        super().__init__(theme)
        self.text = text
        self.color = color
        self.bold = bold

    def render(self):
        t = self.theme
        style = ""
        if self.bold:
            style += t.bold()
        if self.color:
            style += t.hex_to_ansi(self.color) if self.color.startswith('#') else self.color
        return f"{style}{self.text}{t.reset()}"

class BarWidget(TerminalWidget):
    """Progress bar widget."""

    def __init__(self, value, max_value, width=20, theme=None):
        super().__init__(theme)
        self.value = value
        self.max_value = max_value
        self.width = width

    def render(self):
        t = self.theme
        pct = min(1.0, self.value / max(self.max_value, 1))
        filled = int(pct * self.width)

        if pct < 0.5:
            c = t.ok()
        elif pct < 0.8:
            c = t.warn()
        else:
            c = t.err()

        bar = f"{'█' * filled}{'░' * (self.width - filled)}"
        return f"[{c}{bar}{t.reset()}] {pct*100:.0f}%"

# Factory functions
def text(text, color=None, bold=False):
    """Quick text widget."""
    return TextWidget(text, color, bold).render()

def bar(value, max_value, width=20):
    """Quick bar widget."""
    return BarWidget(value, max_value, width).render()
