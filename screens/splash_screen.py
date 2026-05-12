"""
screens/splash_screen.py
Premium animated splash screen
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock

KV = """
<SplashScreen>:
    canvas.before:
        Color:
            rgba: 0.039, 0.055, 0.102, 1   # #0A0E1A
        Rectangle:
            pos: self.pos
            size: self.size

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(16)
        padding: [dp(40), 0]
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: None, None
        size: dp(280), dp(300)

        # ── Shield Icon ──
        MDLabel:
            id: icon_label
            text: "🛡️"
            font_size: dp(80)
            halign: "center"
            opacity: 0

        # ── App Name ──
        MDLabel:
            id: title_label
            text: "FallGuardian"
            font_style: "H4"
            bold: True
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0, 0.831, 1, 1   # cyan
            opacity: 0

        # ── Tagline ──
        MDLabel:
            id: tagline_label
            text: "Always watching. Always ready."
            font_style: "Caption"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.533, 0.573, 0.643, 1
            opacity: 0

        Widget:
            size_hint_y: None
            height: dp(30)

        # ── Loading bar ──
        MDProgressBar:
            id: progress_bar
            value: 0
            color: 0, 0.831, 1, 1
"""

Builder.load_string(KV)


class SplashScreen(Screen):

    def on_enter(self):
        """Start animations when screen shows"""
        Clock.schedule_once(self._animate, 0.2)

    def _animate(self, dt):
        icon    = self.ids.icon_label
        title   = self.ids.title_label
        tagline = self.ids.tagline_label
        bar     = self.ids.progress_bar

        # Stagger fade-ins
        Animation(opacity=1, duration=0.6).start(icon)

        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(title), 0.4
        )
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(tagline), 0.7
        )
        Clock.schedule_once(
            lambda dt: Animation(value=100, duration=1.8, t='in_out_cubic').start(bar),
            0.9
        )
