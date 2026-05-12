import threading
import urllib.request
import urllib.parse
import base64
from datetime import datetime
from utils.config import AppConfig

class AlertService:
    """Handles sending SMS and WhatsApp alerts via Twilio API natively"""

    def __init__(self, storage):
        self.storage = storage

    def send_emergency_alerts(self, location: dict, on_complete=None):
        thread = threading.Thread(
            target=self._send_all,
            args=(location, on_complete),
            daemon=True
        )
        thread.start()

    def test_alert(self, phone: str, on_complete=None):
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

    def _send_all(self, location: dict, on_complete):
        settings  = self.storage.get_settings()
        contacts  = self.storage.get_contacts()
        user_name = settings.get("user_name", "Someone")
        alert_mode = settings.get("alert_mode", "sms")

        if not contacts:
            print("[Alert] No contacts configured!")
            if on_complete:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: on_complete(0, 0), 0)
            return

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
            else:
                failure += 1

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
        try:
            sid   = settings.get("twilio_sid", "").strip()
            token = settings.get("twilio_token", "").strip()
            from_ = settings.get("twilio_from", "").strip()

            if not all([sid, token, from_]):
                print("[Alert] Twilio credentials missing!")
                return False

            url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
            auth_str = f"{sid}:{token}"
            auth_b64 = base64.b64encode(auth_str.encode('utf-8')).decode('ascii')

            def send_req(to_num, from_num):
                data = urllib.parse.urlencode({
                    'To': to_num,
                    'From': from_num,
                    'Body': message
                }).encode('utf-8')
                
                req = urllib.request.Request(url, data=data)
                req.add_header("Authorization", f"Basic {auth_b64}")
                req.add_header("Content-Type", "application/x-www-form-urlencoded")
                
                try:
                    urllib.request.urlopen(req)
                    return True
                except Exception as e:
                    print(f"[Alert] Twilio API Error: {e}")
                    return False

            overall_success = True
            if mode in ("sms", "both"):
                if not send_req(phone, from_):
                    overall_success = False

            if mode in ("whatsapp", "both"):
                wa_from = f"whatsapp:{from_}"
                wa_to   = f"whatsapp:{phone}"
                if not send_req(wa_to, wa_from):
                    overall_success = False

            if on_complete:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: on_complete(overall_success), 0)
            return overall_success

        except Exception as e:
            print(f"[Alert] General send error: {e}")
            if on_complete:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: on_complete(False), 0)
            return False