"""
utils/storage.py
Local JSON storage for contacts, settings, alert history
"""

import json
import os
from datetime import datetime


class Storage:
    """Handles all local data persistence using JSON files"""

    def __init__(self):
        # On Android: use app storage dir; on desktop: use current dir
        try:
            from android.storage import app_storage_path  # type: ignore
            self.base_path = app_storage_path()
        except ImportError:
            self.base_path = os.path.join(os.path.dirname(__file__), '..', 'data')

        os.makedirs(self.base_path, exist_ok=True)

        self.contacts_file  = os.path.join(self.base_path, 'contacts.json')
        self.settings_file  = os.path.join(self.base_path, 'settings.json')
        self.history_file   = os.path.join(self.base_path, 'history.json')

        self._init_files()

    # ──────────────────────────────────────────────
    #  INIT
    # ──────────────────────────────────────────────
    def _init_files(self):
        """Create files with defaults if they don't exist"""
        if not os.path.exists(self.contacts_file):
            self._write(self.contacts_file, [])

        if not os.path.exists(self.settings_file):
            self._write(self.settings_file, {
                "sensitivity": "medium",      # low / medium / high
                "countdown_seconds": 15,       # seconds before auto-alert
                "twilio_sid": "",
                "twilio_token": "",
                "twilio_from": "",             # Your Twilio number
                "alert_mode": "sms",           # sms / whatsapp / both
                "monitoring_active": False,
                "user_name": "User",
            })

        if not os.path.exists(self.history_file):
            self._write(self.history_file, [])

    # ──────────────────────────────────────────────
    #  CONTACTS
    # ──────────────────────────────────────────────
    def get_contacts(self):
        return self._read(self.contacts_file) or []

    def add_contact(self, name: str, phone: str, relation: str = "Family"):
        contacts = self.get_contacts()
        contact = {
            "id": len(contacts) + 1,
            "name": name,
            "phone": phone,
            "relation": relation,
            "added": datetime.now().isoformat()
        }
        contacts.append(contact)
        self._write(self.contacts_file, contacts)
        return contact

    def delete_contact(self, contact_id: int):
        contacts = [c for c in self.get_contacts() if c["id"] != contact_id]
        self._write(self.contacts_file, contacts)

    # ──────────────────────────────────────────────
    #  SETTINGS
    # ──────────────────────────────────────────────
    def get_settings(self):
        return self._read(self.settings_file) or {}

    def update_setting(self, key: str, value):
        settings = self.get_settings()
        settings[key] = value
        self._write(self.settings_file, settings)

    def update_settings(self, updates: dict):
        settings = self.get_settings()
        settings.update(updates)
        self._write(self.settings_file, settings)

    # ──────────────────────────────────────────────
    #  HISTORY
    # ──────────────────────────────────────────────
    def get_history(self):
        history = self._read(self.history_file) or []
        return sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True)

    def add_history_event(self, event_type: str, location: dict = None,
                          contacts_alerted: list = None, cancelled: bool = False):
        history = self._read(self.history_file) or []
        event = {
            "id": len(history) + 1,
            "type": event_type,           # "fall_detected" / "manual_sos" / "cancelled"
            "timestamp": datetime.now().isoformat(),
            "location": location or {},
            "contacts_alerted": contacts_alerted or [],
            "cancelled": cancelled,
        }
        history.append(event)
        # Keep only last 50 events
        if len(history) > 50:
            history = history[-50:]
        self._write(self.history_file, history)
        return event

    def clear_history(self):
        self._write(self.history_file, [])

    # ──────────────────────────────────────────────
    #  HELPERS
    # ──────────────────────────────────────────────
    def _read(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def _write(self, filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
