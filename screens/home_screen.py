"""
screens/home_screen.py
Main monitoring dashboard — the heart of the app.
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.app import App
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.toast import toast

from services.fall_detector import FallDetector
from services.gps_service    import GPSService
from services.alert_service  import AlertService

KV = """
<HomeScreen>:
    canvas.before:
        Color:
            rgba: 0.039, 0.055, 0.102, 1
        Rectangle:
            pos: self.pos
            size: self.size

    MDBoxLayout:
        orientation: "vertical"
        spacing: 0
        padding: 0

        # ══ TOP BAR ══
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(60)
            padding: [dp(16), dp(8)]
            spacing: dp(8)
            md_bg_color: 0.067, 0.094, 0.161, 1

            MDIconButton:
                icon: "shield-check"
                theme_text_color: "Custom"
                text_color: 0, 0.831, 1, 1

            MDLabel:
                text: "FallGuardian"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_x: 1

            MDIconButton:
                icon: "history"
                theme_text_color: "Custom"
                text_color: 0.533, 0.573, 0.643, 1
                on_release: root.go_to_history()

            MDIconButton:
                icon: "cog"
                theme_text_color: "Custom"
                text_color: 0.533, 0.573, 0.643, 1
                on_release: root.go_to_settings()

        # ══ SCROLLABLE CONTENT ══
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: [dp(16), dp(12)]
                spacing: dp(14)
                adaptive_height: True

                # ── STATUS CARD ──
                MDCard:
                    md_bg_color: 0.067, 0.094, 0.161, 1
                    radius: [dp(20)]
                    padding: dp(20)
                    size_hint_y: None
                    height: dp(200)
                    elevation: 4

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(10)

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(30)
                            MDLabel:
                                text: "MONITORING STATUS"
                                font_style: "Overline"
                                theme_text_color: "Custom"
                                text_color: 0.533, 0.573, 0.643, 1
                            Widget:
                            MDLabel:
                                id: status_badge
                                text: "● OFF"
                                font_style: "Caption"
                                bold: True
                                halign: "right"
                                theme_text_color: "Custom"
                                text_color: 1, 0.231, 0.361, 1
                                size_hint_x: None
                                width: dp(60)

                        MDLabel:
                            id: status_label
                            text: "Protection OFF"
                            font_style: "H5"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            size_hint_y: None
                            height: dp(50)

                        MDLabel:
                            id: activity_label
                            text: "Tap the shield to activate protection"
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: 0.533, 0.573, 0.643, 1
                            size_hint_y: None
                            height: dp(30)

                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(50)
                            Widget:
                            MDRaisedButton:
                                id: toggle_btn
                                text: "ACTIVATE SHIELD"
                                md_bg_color: 0, 0.831, 1, 1
                                on_release: root.toggle_monitoring()
                                size_hint_x: None
                                width: dp(200)
                            Widget:

                # ── PULSE ANIMATION CARD ──
                MDCard:
                    id: pulse_card
                    md_bg_color: 0.067, 0.094, 0.161, 1
                    radius: [dp(20)]
                    padding: dp(20)
                    size_hint_y: None
                    height: dp(150)
                    elevation: 4

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)
                        MDLabel:
                            text: "SENSOR READINGS"
                            font_style: "Overline"
                            theme_text_color: "Custom"
                            text_color: 0.533, 0.573, 0.643, 1
                            size_hint_y: None
                            height: dp(20)

                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: dp(16)
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(4)
                                MDLabel:
                                    id: accel_value
                                    text: "9.8"
                                    font_style: "H4"
                                    bold: True
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: 0, 0.831, 1, 1
                                MDLabel:
                                    text: "m/s² (accel)"
                                    font_style: "Caption"
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: 0.533, 0.573, 0.643, 1

                            Widget:
                                size_hint_x: None
                                width: dp(1)
                                canvas:
                                    Color:
                                        rgba: 0.2, 0.2, 0.3, 1
                                    Rectangle:
                                        pos: self.pos
                                        size: dp(1), self.height

                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(4)
                                MDLabel:
                                    id: phase_label
                                    text: "IDLE"
                                    font_style: "H5"
                                    bold: True
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: 0, 0.902, 0.463, 1
                                MDLabel:
                                    text: "detection phase"
                                    font_style: "Caption"
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: 0.533, 0.573, 0.643, 1

                        MDProgressBar:
                            id: magnitude_bar
                            value: 50
                            color: 0, 0.831, 1, 1

                # ── QUICK ACTIONS ──
                MDLabel:
                    text: "QUICK ACTIONS"
                    font_style: "Overline"
                    theme_text_color: "Custom"
                    text_color: 0.533, 0.573, 0.643, 1
                    size_hint_y: None
                    height: dp(24)
                    padding_x: dp(4)

                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(12)
                    size_hint_y: None
                    height: dp(100)

                    MDCard:
                        md_bg_color: 1, 0.231, 0.361, 0.15
                        radius: [dp(16)]
                        padding: dp(12)
                        ripple_behavior: True
                        on_release: root.manual_sos()
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(4)
                            MDIconButton:
                                icon: "phone-alert"
                                theme_text_color: "Custom"
                                text_color: 1, 0.231, 0.361, 1
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 1
                            MDLabel:
                                text: "SOS Alert"
                                font_style: "Caption"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: 1, 0.231, 0.361, 1

                    MDCard:
                        md_bg_color: 0, 0.831, 1, 0.1
                        radius: [dp(16)]
                        padding: dp(12)
                        ripple_behavior: True
                        on_release: root.go_to_contacts()
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(4)
                            MDIconButton:
                                icon: "account-group"
                                theme_text_color: "Custom"
                                text_color: 0, 0.831, 1, 1
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 1
                            MDLabel:
                                text: "Contacts"
                                font_style: "Caption"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: 0, 0.831, 1, 1

                    MDCard:
                        md_bg_color: 1, 0.702, 0, 0.1
                        radius: [dp(16)]
                        padding: dp(12)
                        ripple_behavior: True
                        on_release: root.test_detection()
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(4)
                            MDIconButton:
                                icon: "test-tube"
                                theme_text_color: "Custom"
                                text_color: 1, 0.702, 0, 1
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 1
                            MDLabel:
                                text: "Test Fall"
                                font_style: "Caption"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: 1, 0.702, 0, 1

                # ── LOCATION CARD ──
                MDCard:
                    md_bg_color: 0.067, 0.094, 0.161, 1
                    radius: [dp(16)]
                    padding: [dp(16), dp(12)]
                    size_hint_y: None
                    height: dp(80)
                    elevation: 2
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(12)
                        MDIconButton:
                            icon: "map-marker"
                            theme_text_color: "Custom"
                            text_color: 0, 0.831, 1, 1
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(2)
                            MDLabel:
                                text: "LOCATION"
                                font_style: "Overline"
                                theme_text_color: "Custom"
                                text_color: 0.533, 0.573, 0.643, 1
                                size_hint_y: None
                                height: dp(20)
                            MDLabel:
                                id: location_label
                                text: "Waiting for GPS..."
                                font_style: "Body2"
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 1
                Widget:
                    size_hint_y: None
                    height: dp(20)

    # ══ EMERGENCY OVERLAY ══
    MDBoxLayout:
        id: emergency_overlay
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(30)
        # THE FIX: Start it far off-screen so it doesn't block clicks!
        pos_hint: {"center_x": 0.5, "center_y": 5.0} 
        size_hint: None, None
        size: dp(340), dp(400)
        opacity: 0
        canvas.before:
            Color:
                rgba: 0.039, 0.055, 0.102, 0.95
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(24)]
        MDLabel:
            text: "⚠️"
            font_size: dp(60)
            halign: "center"
            size_hint_y: None
            height: dp(80)
        MDLabel:
            text: "Fall Detected!"
            font_style: "H4"
            bold: True
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 0.231, 0.361, 1
            size_hint_y: None
            height: dp(50)
        MDLabel:
            id: countdown_label
            text: "Sending alert in 15s..."
            font_style: "H6"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            size_hint_y: None
            height: dp(40)
        MDLabel:
            text: "Are you okay? Press CANCEL to stop the alert."
            font_style: "Body2"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.533, 0.573, 0.643, 1
        MDRaisedButton:
            text: "I'M OKAY — CANCEL"
            md_bg_color: 0, 0.831, 1, 1
            on_release: root.cancel_alert()
            size_hint_x: 1
            height: dp(52)
        MDRaisedButton:
            text: "SEND ALERT NOW"
            md_bg_color: 1, 0.231, 0.361, 1
            on_release: root.send_alert_now()
            size_hint_x: 1
            height: dp(52)
"""
Builder.load_string(KV)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app              = None
        self.fall_detector    = None
        self.gps_service      = None
        self.alert_service    = None
        self.is_monitoring    = False
        self.countdown        = 0
        self._countdown_event = None
        self._ui_event        = None

    def on_enter(self):
        try:
            self.app           = App.get_running_app()
            self.gps_service   = GPSService()
            self.alert_service = AlertService(self.app.storage)
            self.fall_detector = FallDetector(
                sensitivity=self.app.storage.get_settings().get("sensitivity", "medium"),
                on_fall_detected=self._on_fall_detected
            )
            self._start_ui_updates()
        except Exception as e:
            toast(f"Init Error: {str(e)}")

    def on_leave(self):
        if self._ui_event: self._ui_event.cancel()

    def toggle_monitoring(self):
        try:
            if self.is_monitoring: self._stop_monitoring()
            else: self._start_monitoring()
        except Exception as e:
            toast(f"Monitor Error: {str(e)}")

    def _start_monitoring(self):
        self.is_monitoring = True
        self.fall_detector.start()
        self.gps_service.start()
        self.ids.status_label.text        = "Protection ACTIVE"
        self.ids.status_badge.text        = "● ON"
        self.ids.status_badge.text_color  = (0, 0.902, 0.463, 1)
        self.ids.activity_label.text      = "Monitoring your movement..."
        self.ids.toggle_btn.text          = "DEACTIVATE SHIELD"
        self.ids.toggle_btn.md_bg_color   = (1, 0.231, 0.361, 1)
        toast("Shield Activated")

    def _stop_monitoring(self):
        self.is_monitoring = False
        self.fall_detector.stop()
        self.gps_service.stop()
        self.ids.status_label.text        = "Protection OFF"
        self.ids.status_badge.text        = "● OFF"
        self.ids.status_badge.text_color  = (1, 0.231, 0.361, 1)
        self.ids.activity_label.text      = "Tap the shield to activate protection"
        self.ids.toggle_btn.text          = "ACTIVATE SHIELD"
        self.ids.toggle_btn.md_bg_color   = (0, 0.831, 1, 1)
        toast("Shield Deactivated")

    def _start_ui_updates(self):
        self._ui_event = Clock.schedule_interval(self._update_ui, 0.5)

    def _update_ui(self, dt):
        if self.fall_detector and self.is_monitoring:
            mag = self.fall_detector.get_current_magnitude()
            activity = self.fall_detector.get_activity_level()
            self.ids.accel_value.text = f"{mag:.1f}"
            phase = self.fall_detector.phase
            phase_colors = {"IDLE": (0, 0.902, 0.463, 1), "FREEFALL": (1, 0.702, 0, 1), "IMPACT": (1, 0.231, 0.361, 1), "STILLNESS": (1, 0.231, 0.361, 1)}
            self.ids.phase_label.text = phase
            self.ids.phase_label.text_color = phase_colors.get(phase, (1,1,1,1))
            self.ids.magnitude_bar.value = min(100, (mag / 40.0) * 100)
            activity_map = {"still": "Standing still or resting", "walking": "Walking — monitoring active", "active": "Active movement detected", "unknown": "Analyzing movement..."}
            self.ids.activity_label.text = activity_map.get(activity, "Monitoring...")

        if self.gps_service:
            loc = self.gps_service.get_location()
            if loc.get("available"):
                self.ids.location_label.text = f"Lat: {loc['lat']:.4f}, Lon: {loc['lon']:.4f}"
            else:
                self.ids.location_label.text = "Acquiring GPS signal..."

    def _on_fall_detected(self):
        settings = self.app.storage.get_settings()
        self.countdown = int(settings.get("countdown_seconds", 15))
        self._show_emergency_overlay()

    def _show_emergency_overlay(self):
        overlay = self.ids.emergency_overlay
        overlay.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        Animation(opacity=1, duration=0.3).start(overlay)
        self._update_countdown_label()
        self._countdown_event = Clock.schedule_interval(self._tick_countdown, 1.0)

    def _tick_countdown(self, dt):
        self.countdown -= 1
        self._update_countdown_label()
        if self.countdown <= 0:
            self._countdown_event.cancel()
            self.send_alert_now()

    def _update_countdown_label(self):
        self.ids.countdown_label.text = f"Sending alert in {self.countdown}s..."
        if self.countdown <= 5: self.ids.countdown_label.text_color = (1, 0.231, 0.361, 1)

    def _hide_emergency_overlay(self):
        if self._countdown_event: self._countdown_event.cancel()
        overlay = self.ids.emergency_overlay
        anim = Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=lambda *_: setattr(overlay, 'pos_hint', {"center_x": 0.5, "center_y": 5.0}))
        anim.start(overlay)

    def cancel_alert(self):
        self._hide_emergency_overlay()
        self.ids.countdown_label.text_color = (1, 1, 1, 1)
        self.app.storage.add_history_event("fall_detected", cancelled=True)

    def send_alert_now(self):
        self._hide_emergency_overlay()
        location = self.gps_service.get_location() if self.gps_service else {}
        self.alert_service.send_emergency_alerts(location=location, on_complete=self._on_alerts_sent)

    def _on_alerts_sent(self, success: int, fail: int):
        try:
            dialog = MDDialog(
                title="🚨 Alerts Sent",
                text=f"Successfully sent to {success} contact(s).\\nFailed: {fail}.",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
        except Exception:
            toast(f"Alert Sent: {success} successes, {fail} failures.")

    def manual_sos(self):
        try:
            dialog = MDDialog(
                title="🆘 Send Manual SOS?",
                text="This will immediately alert all your emergency contacts.",
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=lambda x: dialog.dismiss()),
                    MDRaisedButton(text="SEND SOS", md_bg_color=(1, 0.231, 0.361, 1), 
                                   on_release=lambda x: [dialog.dismiss(), self._do_manual_sos()]),
                ]
            )
            dialog.open()
        except Exception:
            toast("Sending SOS...")
            self._do_manual_sos()

    def _do_manual_sos(self):
        toast("Sending SOS...")
        location = self.gps_service.get_location() if self.gps_service else {}
        self.alert_service.send_emergency_alerts(location=location, on_complete=self._on_alerts_sent)
        self.app.storage.add_history_event("manual_sos", location=location)

    def test_detection(self):
        try:
            if not self.is_monitoring:
                dialog = MDDialog(
                    title="Monitoring Off",
                    text="Please activate monitoring first, then test fall detection.",
                    buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
                )
                dialog.open()
                return
            self.fall_detector.simulate_fall()
        except Exception as e:
            toast(f"Error: {str(e)}")

    def go_to_contacts(self): self.manager.current = "contacts"
    def go_to_settings(self): self.manager.current = "settings"
    def go_to_history(self): self.manager.current = "history"