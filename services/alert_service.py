"""
services/alert_service.py
Sends emergency alerts via Twilio SMS / WhatsApp.

Setup:
  1. Create free account at https://www.twilio.com
  2. Get Account SID, Auth Token, and a Phone Number
  3. For WhatsApp: join Twilio Sandbox (free, just send a WhatsApp message)
  4. Enter credentials in Settings screen of the app
"""

import threading
from datetime import datetime
from utils.config import AppConfig


class AlertService:
    """Handles sending SMS and WhatsApp alerts via Twilio"""

    def __init__(self, storage):
        self.storage = storage

    # ──────────────────────────────────────────────
    #  PUBLIC API
    # ──────────────────────────────────────────────
    def send_emergency_alerts(self, location: dict, on_complete=None):
        """
        Send alerts to all contacts in a background thread.
        
        Args:
            location: dict with 'lat', 'lon' keys
            on_complete: callback(success_count, fail_count)
        """
        # Run in thread so UI doesn't freeze
        thread = threading.Thread(
            target=self._send_all,
            args=(location, on_complete),
            daemon=True
        )
        thread.start()

    def test_alert(self, phone: str, on_complete=None):
        """Send a test SMS to verify credentials work"""
        settings = self.storage.get_settings()
        message = (
            "✅ FallGuardian Test Alert\n"
            "Your emergency contact setup is working correctly!"
        )
        thread = threading.Thread(
            target=self._send_single,
            args=(phone, message, settings, "sms", on_complete),
            daemon=True
        )
        thread.start()

    # ──────────────────────────────────────────────
    #  INTERNAL
    # ──────────────────────────────────────────────
    def _send_all(self, location: dict, on_complete):
        settings  = self.storage.get_settings()
        contacts  = self.storage.get_contacts()
        user_name = settings.get("user_name", "Someone")
        alert_mode = settings.get("alert_mode", "sms")

        if not contacts:
            print("[Alert] No contacts configured!")
            if on_complete:
                on_complete(0, 0)
            return

        # Build message
        lat  = location.get('lat', 0.0)
        lon  = location.get('lon', 0.0)
        time_str = datetime.now().strftime("%I:%M %p, %d %b %Y")
        message = AppConfig.SMS_TEMPLATE.format(
            name=user_name,
            lat=lat,
            lon=lon,
            time=time_str
        )

        success = 0
        failure = 0
        alerted_names = []

        for contact in contacts:
            phone = contact.get("phone", "")
            name  = contact.get("name", "Contact")

            ok = self._send_single(phone, message, settings, alert_mode)
            if ok:
                success += 1
                alerted_names.append(name)
                print(f"[Alert] ✅ Sent to {name} ({phone})")
            else:
                failure += 1
                print(f"[Alert] ❌ Failed for {name} ({phone})")

        # Log to history
        self.storage.add_history_event(
            event_type="fall_detected",
            location={"lat": lat, "lon": lon},
            contacts_alerted=alerted_names
        )

        if on_complete:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: on_complete(success, failure), 0)

    def _send_single(self, phone: str, message: str, settings: dict,
                     mode: str = "sms", on_complete=None) -> bool:
        """Send one message. Returns True on success."""
        try:
            from twilio.rest import Client

            sid   = settings.get("twilio_sid", "").strip()
            token = settings.get("twilio_token", "").strip()
            from_ = settings.get("twilio_from", "").strip()

            if not all([sid, token, from_]):
                print("[Alert] Twilio credentials missing!")
                return False

            client = Client(sid, token)

            if mode in ("sms", "both"):
                client.messages.create(
                    body=message,
                    from_=from_,
                    to=phone
                )

            if mode in ("whatsapp", "both"):
                # Twilio WhatsApp sandbox: prefix numbers with 'whatsapp:'
                wa_from = f"whatsapp:{from_}"
                wa_to   = f"whatsapp:{phone}"
                client.messages.create(
                    body=message,
                    from_=wa_from,
                    to=wa_to
                )

            if on_complete:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: on_complete(True), 0)
            return True

        except ImportError:
            print("[Alert] Twilio library not installed. Run: pip install twilio")
            return False
        except Exception as e:
            print(f"[Alert] Send error: {e}")
            if on_complete:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: on_complete(False), 0)
            return False
