"""
services/gps_service.py
GPS location tracking using plyer.
"""

from kivy.clock import Clock
from utils.config import AppConfig


class GPSService:
    """Manages GPS location updates"""

    def __init__(self):
        self.latitude  = None
        self.longitude = None
        self.accuracy  = None
        self._gps      = None
        self.is_active = False

    def start(self):
        """Start GPS tracking"""
        try:
            from plyer import gps
            self._gps = gps
            self._gps.configure(
                on_location=self._on_location,
                on_status=self._on_status
            )
            self._gps.start(
                minTime=AppConfig.LOCATION_INTERVAL * 1000,  # ms
                minDistance=10                                 # meters
            )
            self.is_active = True
            print("[GPS] Started tracking")
        except Exception as e:
            print(f"[GPS] Not available: {e}")
            # Fallback: use approximate location from IP (offline default)
            self._set_default_location()

    def stop(self):
        """Stop GPS tracking"""
        if self._gps:
            try:
                self._gps.stop()
            except Exception:
                pass
        self.is_active = False

    def get_location(self) -> dict:
        """Returns current location dict"""
        return {
            "lat": self.latitude  or 0.0,
            "lon": self.longitude or 0.0,
            "accuracy": self.accuracy or 0.0,
            "available": self.latitude is not None,
        }

    def get_maps_url(self) -> str:
        """Returns Google Maps URL for current location"""
        if self.latitude and self.longitude:
            return f"https://maps.google.com/?q={self.latitude},{self.longitude}"
        return "https://maps.google.com"

    # ──────────────────────────────────────────────
    #  CALLBACKS
    # ──────────────────────────────────────────────
    def _on_location(self, **kwargs):
        self.latitude  = kwargs.get('lat')
        self.longitude = kwargs.get('lon')
        self.accuracy  = kwargs.get('accuracy')
        print(f"[GPS] Updated: {self.latitude:.4f}, {self.longitude:.4f}")

    def _on_status(self, stype, status):
        print(f"[GPS] Status: {stype} — {status}")

    def _set_default_location(self):
        """Default coords if GPS unavailable (shows 0,0 on map)"""
        self.latitude  = 0.0
        self.longitude = 0.0
