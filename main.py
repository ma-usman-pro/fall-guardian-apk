"""
FallGuardian - Smart Fall Detection App
Main Entry Point
"""

import os
os.environ['KIVY_NO_ENV_CONFIG'] = '1'

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.clock import Clock
from kivy.metrics import dp

# Set window size for desktop testing (ignored on Android)
if platform not in ('android', 'ios'):
    Window.size = (400, 780)
    Window.minimum_width = 360
    Window.minimum_height = 640

from screens.splash_screen import SplashScreen
from screens.home_screen import HomeScreen
from screens.contacts_screen import ContactsScreen
from screens.settings_screen import SettingsScreen
from screens.history_screen import HistoryScreen
from utils.storage import Storage
from utils.config import AppConfig

KV = """
MDScreenManager:
    SplashScreen:
        name: "splash"
    HomeScreen:
        name: "home"
    ContactsScreen:
        name: "contacts"
    SettingsScreen:
        name: "settings"
    HistoryScreen:
        name: "history"
"""


class FallGuardianApp(MDApp):
    """Main Application Class"""

    def build(self):
        # ── Premium Dark Theme Setup ──
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.material_style = "M3"

        # ── App Metadata ──
        self.title = "FallGuardian"
        self.icon = "assets/images/icon.png"

        # ── Initialize Storage & Config ──
        self.storage = Storage()
        self.config_data = AppConfig()

        # ── Build Screen Manager ──
        sm = Builder.load_string(KV)
        return sm

    def on_start(self):
        """Called when app fully starts"""
        Clock.schedule_once(self._go_to_home, 3.0)

    def _go_to_home(self, dt):
        """Navigate from splash to home after delay"""
        self.root.current = "home"

    def on_pause(self):
        """Allow app to pause (important for Android)"""
        return True

    def on_resume(self):
        """Resume app"""
        pass


if __name__ == "__main__":
    FallGuardianApp().run()
