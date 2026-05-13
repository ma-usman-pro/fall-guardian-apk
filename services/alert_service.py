"""
services/alert_service.py
Sends Native Background SMS using the phone's actual SIM card.
"""

import threading
from kivy.utils import platform
from kivy.clock import Clock

class AlertService:
    def __init__(self, storage):
        self.storage = storage

    def send_emergency_alerts(self, location: dict, on_complete=None):
        thread = threading.Thread(
            target=self._send_all_native,
            args=(location, on_complete),
            daemon=True
        )
        thread.start()

    def _send_all_native(self, location: dict, on_complete):
        contacts = self.storage.get_contacts()

        if not contacts:
            if on_complete: Clock.schedule_once(lambda dt: on_complete(0, 0), 0)
            return

        lat = location.get("lat", "Unknown")
        lon = location.get("lon", "Unknown")
        if lat != "Unknown":
            maps_url = f"http://maps.google.com/?q={lat},{lon}"
        else:
            maps_url = "Location Unavailable"

        message = (
            "🚨 EMERGENCY ALERT - FallGuardian 🚨\n\n"
            "I may have fallen and need help immediately!\n\n"
            f"📍 My Location: {maps_url}\n\n"
            "Please check on me or call emergency services."
        )

        success_count = 0
        fail_count = 0

        if platform == 'android':
            try:
                from jnius import autoclass
                SmsManager = autoclass('android.telephony.SmsManager')
                sms_manager = SmsManager.getDefault()
                
                for contact in contacts:
                    phone = contact.get("phone")
                    if phone:
                        try:
                            sms_manager.sendTextMessage(phone, None, message, None, None)
                            success_count += 1
                        except Exception as e:
                            print(f"SMS Failed for {phone}: {e}")
                            fail_count += 1
            except Exception as e:
                print(f"JNIUS SMS Setup Failed: {e}")
                fail_count = len(contacts)
        else:
            for contact in contacts:
                print(f"\n[DESKTOP TEST] Would send SMS to {contact.get('phone')}:\n{message}\n")
                success_count += 1

        if on_complete:
            Clock.schedule_once(lambda dt: on_complete(success_count, fail_count), 0)