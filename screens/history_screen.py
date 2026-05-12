"""
screens/history_screen.py
Shows history of fall detections and SOS alerts.
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from datetime import datetime

KV = """
<HistoryScreen>:
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
                text: "Alert History"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

            MDIconButton:
                icon: "delete-sweep"
                theme_icon_color: "Custom"
                icon_color: 1, 0.231, 0.361, 0.7
                on_release: root.confirm_clear()

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: [dp(16), dp(12)]
                spacing: dp(10)
                adaptive_height: True

                MDLabel:
                    text: "RECENT EVENTS"
                    font_style: "Overline"
                    theme_text_color: "Custom"
                    text_color: 0.533, 0.573, 0.643, 1
                    size_hint_y: None
                    height: dp(24)

                MDLabel:
                    id: empty_label
                    text: "No events recorded yet.\\nFall detections and SOS alerts will appear here."
                    font_style: "Body1"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.533, 0.573, 0.643, 1
                    size_hint_y: None
                    height: dp(80)

                MDBoxLayout:
                    id: history_container
                    orientation: "vertical"
                    spacing: dp(8)
                    adaptive_height: True
"""

Builder.load_string(KV)


class HistoryScreen(Screen):

    def on_enter(self):
        self.app = App.get_running_app()
        Clock.schedule_once(lambda dt: self._refresh(), 0.1)

    def _refresh(self):
        container = self.ids.history_container
        container.clear_widgets()

        history = self.app.storage.get_history()
        self.ids.empty_label.opacity = 1 if not history else 0

        for event in history:
            self._add_event_widget(event)

    def _add_event_widget(self, event: dict):
        from kivymd.uix.card import MDCard
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel

        event_type  = event.get("type", "unknown")
        cancelled   = event.get("cancelled", False)
        timestamp   = event.get("timestamp", "")
        contacts    = event.get("contacts_alerted", [])
        location    = event.get("location", {})

        # Parse and format timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%d %b %Y, %I:%M %p")
        except Exception:
            time_str = timestamp[:16] if timestamp else "Unknown time"

        # Icon and color based on type
        if cancelled:
            icon, color, title = "cancel", (1, 0.702, 0, 1), "Fall Cancelled"
        elif event_type == "manual_sos":
            icon, color, title = "phone-alert", (1, 0.231, 0.361, 1), "Manual SOS"
        else:
            icon, color, title = "alert-circle", (1, 0.231, 0.361, 1), "Fall Detected"

        # Contact string
        if contacts:
            contact_str = f"Alerted: {', '.join(contacts)}"
        else:
            contact_str = "No contacts alerted"

        # Location string
        lat = location.get("lat", 0)
        lon = location.get("lon", 0)
        loc_str = f"📍 {lat:.4f}, {lon:.4f}" if (lat or lon) else "📍 Location unavailable"

        card = MDCard(
            md_bg_color=(0.067, 0.094, 0.161, 1),
            radius=[12],
            padding=[16, 12],
            size_hint_y=None,
            height=100,
        )

        row = MDBoxLayout(orientation="horizontal", spacing=12)

        from kivymd.uix.button import MDIconButton
        icon_btn = MDIconButton(
            icon=icon,
            theme_icon_color="Custom",
            icon_color=color,
            size_hint_x=None,
            width=44,
        )

        info = MDBoxLayout(orientation="vertical", spacing=2)
        title_lbl = MDLabel(
            text=title,
            bold=True,
            theme_text_color="Custom",
            text_color=color,
            font_style="Body1",
            size_hint_y=None,
            height=24,
        )
        time_lbl = MDLabel(
            text=time_str,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.9),
            font_style="Caption",
            size_hint_y=None,
            height=20,
        )
        contacts_lbl = MDLabel(
            text=contact_str,
            theme_text_color="Custom",
            text_color=(0.533, 0.573, 0.643, 1),
            font_style="Caption",
            size_hint_y=None,
            height=18,
        )
        loc_lbl = MDLabel(
            text=loc_str,
            theme_text_color="Custom",
            text_color=(0.533, 0.573, 0.643, 1),
            font_style="Caption",
            size_hint_y=None,
            height=18,
        )
        info.add_widget(title_lbl)
        info.add_widget(time_lbl)
        info.add_widget(contacts_lbl)
        info.add_widget(loc_lbl)

        row.add_widget(icon_btn)
        row.add_widget(info)
        card.add_widget(row)
        self.ids.history_container.add_widget(card)

    def confirm_clear(self):
        dialog = MDDialog(
            title="Clear History?",
            text="All recorded events will be permanently deleted.",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="CLEAR ALL",
                    md_bg_color=(1, 0.231, 0.361, 1),
                    on_release=lambda x: [
                        self.app.storage.clear_history(),
                        dialog.dismiss(),
                        self._refresh()
                    ]
                ),
            ]
        )
        dialog.open()

    def go_back(self):
        self.manager.current = "home"
