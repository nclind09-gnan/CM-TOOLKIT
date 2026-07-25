# -*- coding: utf-8 -*-
"""
CM Toolkit - merged launcher

Combines three independent Kivy apps as tabs/screens in one APK, each
keeping its own internal logic untouched:
  - CM/DX          (cmdx_tab.py)   - condition monitoring diagnostics
  - Rotor Balance  (rotor_tab.py)  - single-plane balancing calculator
  - Bearing Freq   (bearing_tab.py)- bearing defect frequency scope

Each original app's App subclass is instantiated and .build() is called
directly (never .run()), so each contributes only its root widget. Kivy
only allows one App to actually "run" per process, which is this one.
"""
import traceback

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.scrollview import ScrollView

# Background color to restore for each tab (matches that app's own design)
TAB_BG = {
    "cmdx": (0.078, 0.09, 0.102, 1),      # CM/DX dark theme
    "rotor": (1, 1, 1, 1),                # Rotor Balance white theme
    "bearing": (0.957, 0.969, 0.984, 1),  # Bearing Freq Scope light theme
}

ACCENT = (0.145, 0.388, 0.922, 1)   # active tab highlight (blue)
INACTIVE = (0.2, 0.22, 0.26, 1)     # inactive tab background
NAV_TEXT = (1, 1, 1, 1)


def _safe_build(build_fn, label):
    """Build a sub-app's root widget, catching any exception so one
    broken tab can't take down the whole merged app."""
    try:
        return build_fn()
    except Exception:
        err = traceback.format_exc()
        box = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))
        box.add_widget(Label(
            text=f"{label} failed to load - screenshot this and send it in chat:",
            color=(1, 0.4, 0.4, 1), bold=True, font_size=sp(15),
            size_hint_y=None, height=dp(50), halign="left", valign="top",
        ))
        scroll = ScrollView()
        err_label = Label(
            text=err, color=(1, 1, 1, 1), font_size=sp(12),
            size_hint_y=None, halign="left", valign="top",
        )
        err_label.bind(width=lambda w, val: setattr(w, "text_size", (val, None)))
        err_label.bind(texture_size=lambda w, ts: setattr(w, "height", ts[1]))
        scroll.add_widget(err_label)
        box.add_widget(scroll)
        return box


class CMToolkitApp(App):
    title = "CM Toolkit"
    icon = "icon.png"

    def build(self):
        Window.clearcolor = TAB_BG["cmdx"]

        # --- lazy imports so a broken tab module doesn't block the others ---
        try:
            import cmdx_tab
            cmdx_root = _safe_build(lambda: cmdx_tab.CMDXApp().build(), "CM/DX")
        except Exception:
            cmdx_root = _safe_build(lambda: (_ for _ in ()).throw(Exception(traceback.format_exc())), "CM/DX")

        try:
            import rotor_tab
            rotor_root = _safe_build(lambda: rotor_tab.BalanceApp().build(), "Rotor Balance")
        except Exception:
            rotor_root = _safe_build(lambda: (_ for _ in ()).throw(Exception(traceback.format_exc())), "Rotor Balance")

        try:
            import bearing_tab
            bearing_root = _safe_build(lambda: bearing_tab.BearingScopeApp().build(), "Bearing Freq")
        except Exception:
            bearing_root = _safe_build(lambda: (_ for _ in ()).throw(Exception(traceback.format_exc())), "Bearing Freq")

        self.sm = ScreenManager(transition=NoTransition())
        for name, widget in (("cmdx", cmdx_root), ("rotor", rotor_root), ("bearing", bearing_root)):
            screen = Screen(name=name)
            screen.add_widget(widget)
            self.sm.add_widget(screen)

        nav = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(2), padding=[dp(2), dp(2)])
        self.nav_buttons = {}
        for name, label in (("cmdx", "CM/DX"), ("rotor", "Rotor Balance"), ("bearing", "Bearing Freq")):
            btn = Button(text=label, bold=True, font_size=sp(13),
                         background_normal="", background_color=INACTIVE, color=NAV_TEXT)
            btn.bind(on_release=lambda inst, n=name: self.switch(n))
            nav.add_widget(btn)
            self.nav_buttons[name] = btn

        root = BoxLayout(orientation="vertical")
        root.add_widget(nav)
        root.add_widget(self.sm)

        self.switch("cmdx")
        return root

    def switch(self, name):
        Window.clearcolor = TAB_BG[name]
        self.sm.current = name
        for n, btn in self.nav_buttons.items():
            btn.background_color = ACCENT if n == name else INACTIVE


if __name__ == "__main__":
    CMToolkitApp().run()
