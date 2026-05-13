"""
screens/settings_screen.py
Configure sensitivity, and alert preferences.
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton

KV = """
<SettingsScreen>:
    canvas.before:
        Color:
            rgba: 0.039, 0.055, 0.102, 1
        Rectangle:
            pos: self.pos
            size: self.size

    MDBoxLayout:
        orientation: "vertical"

        # ── Top Bar ──
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(60)
            padding: [dp(8), dp(8)]
            md_bg_color: 0.067, 0.094, 0.161, 1

            MDIconButton:
                icon: "arrow-left"
                theme_icon_color: "Custom"
                icon_color: 0, 0.831, 1, 1
                on_release: root.go_back()

            MDLabel:
                text: "Settings"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

            MDIconButton:
                icon: "content-save"
                theme_icon_color: "Custom"
                icon_color: 0, 0.902, 0.463, 1
                on_release: root.save_settings()

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: [dp(16), dp(12)]
                spacing: dp(16)
                adaptive_height: True

                # ── PROFILE SECTION ──
                MDLabel:
                    text: "PROFILE"
                    font_style: "Overline"
                    theme_text_color: "Custom"
                    text_color: 0.533, 0.573, 0.643, 1
                    size_hint_y: None
                    height: dp(24)

                MDCard:
                    md_bg_color: 0.067, 0.094, 0.161, 1
                    radius: [dp(16)]
                    padding: [dp(16), dp(16)]
                    size_hint_y: None
                    height: dp(100)

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)
                        MDLabel:
                            text: "Your Name (sent in alerts)"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.533, 0.573, 0.643, 1
                            size_hint_y: None
                            height: dp(20)
                        MDTextField:
                            id: user_name_field
                            hint_text: "Enter your name"
                            mode: "rectangle"
                            text: ""

                # ── SENSITIVITY ──
                MDLabel:
                    text: "FALL DETECTION SENSITIVITY"
                    font_style: "Overline"
                    theme_text_color: "Custom"
                    text_color: 0.533, 0.573, 0.643, 1
                    size_hint_y: None
                    height: dp(24)

                MDCard:
                    md_bg_color: 0.067, 0.094, 0.161, 1
                    radius: [dp(16)]
                    padding: [dp(16), dp(16)]
                    size_hint_y: None
                    height: dp(180)

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(12)

                        MDLabel:
                            text: "Higher sensitivity = detects more falls but may have false alarms"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.533, 0.573, 0.643, 1
                            size_hint_y: None
                            height: dp(36)

                        MDSlider:
                            id: sensitivity_slider
                            min: 1
                            max: 3
                            step: 1
                            value: 2
                            color: 0, 0.831, 1, 1
                            size_hint_y: None
                            height: dp(40)

                        MDLabel:
                            id: sensitivity_label
                            text: "Medium — Recommended"
                            font_style: "Body2"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0, 0.831, 1, 1
                            size_hint_y: None
                            height: dp(30)

                # ── COUNTDOWN ──
                MDLabel:
                    text: "ALERT COUNTDOWN (seconds)"
                    font_style: "Overline"
                    theme_text_color: "Custom"
                    text_color: 0.533, 0.573, 0.643, 1
                    size_hint_y: None
                    height: dp(24)

                MDCard:
                    md_bg_color: 0.067, 0.094, 0.161, 1
                    radius: [dp(16)]
                    padding: [dp(16), dp(16)]
                    size_hint_y: None
                    height: dp(120)

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)

                        MDLabel:
                            text: "Time to cancel alert before sending"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.533, 0.573, 0.643, 1
                            size_hint_y: None
                            height: dp(24)

                        MDSlider:
                            id: countdown_slider
                            min: 5
                            max: 30
                            step: 5
                            value: 15
                            color: 0, 0.831, 1, 1

                        MDLabel:
                            id: countdown_label
                            text: "15 seconds"
                            font_style: "Body2"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0, 0.831, 1, 1
                            size_hint_y: None
                            height: dp(24)

                Widget:
                    size_hint_y: None
                    height: dp(20)
"""

Builder.load_string(KV)


class SettingsScreen(Screen):

    def on_enter(self):
        self.app = App.get_running_app()
        Clock.schedule_once(lambda dt: self._load_settings(), 0.1)
        # Bind sliders
        self.ids.sensitivity_slider.bind(value=self._on_sensitivity_change)
        self.ids.countdown_slider.bind(value=self._on_countdown_change)

    def _load_settings(self):
        s = self.app.storage.get_settings()

        self.ids.user_name_field.text = s.get("user_name", "")

        sens_map = {"low": 1, "medium": 2, "high": 3}
        self.ids.sensitivity_slider.value = sens_map.get(
            s.get("sensitivity", "medium"), 2
        )
        self.ids.countdown_slider.value = s.get("countdown_seconds", 15)

    def _on_sensitivity_change(self, slider, value):
        labels = {1: "Low — Fewer false alarms",
                  2: "Medium — Recommended",
                  3: "High — Most sensitive"}
        self.ids.sensitivity_label.text = labels.get(int(value), "Medium")

    def _on_countdown_change(self, slider, value):
        self.ids.countdown_label.text = f"{int(value)} seconds"

    def save_settings(self):
        sens_map = {1: "low", 2: "medium", 3: "high"}

        self.app.storage.update_settings({
            "user_name":         self.ids.user_name_field.text.strip(),
            "sensitivity":       sens_map.get(int(self.ids.sensitivity_slider.value), "medium"),
            "countdown_seconds": int(self.ids.countdown_slider.value),
        })

        dialog = MDDialog(
            title="✅ Settings Saved",
            text="Your settings have been saved successfully.",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def go_back(self):
        self.manager.current = "home"