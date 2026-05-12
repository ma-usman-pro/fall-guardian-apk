"""
utils/config.py
Fall detection thresholds and app-wide configuration
"""


class AppConfig:
    """
    Sensitivity thresholds for fall detection algorithm.
    Tune these based on testing.
    """

    # ── App Info ──
    APP_NAME    = "FallGuardian"
    APP_VERSION = "1.0.0"
    APP_TAGLINE = "Always watching. Always ready."

    # ── Accelerometer Thresholds ──
    # Free-fall: magnitude of acceleration vector drops near 0 (no gravity felt)
    # Impact:    sudden spike when body hits floor
    # Stillness: very little movement after impact (person unconscious/injured)

    THRESHOLDS = {
        "low": {
            "freefall_threshold":  3.0,    # m/s² - below this = free fall
            "impact_threshold":   25.0,    # m/s² - above this = hard impact
            "stillness_threshold": 2.0,    # m/s² - below this = no movement
            "stillness_duration":  4.0,    # seconds of stillness = emergency
            "detection_window":    2.5,    # seconds to detect fall sequence
        },
        "medium": {
            "freefall_threshold":  4.0,
            "impact_threshold":   20.0,
            "stillness_threshold": 2.5,
            "stillness_duration":  3.0,
            "detection_window":    2.0,
        },
        "high": {
            "freefall_threshold":  5.0,   # More sensitive = fewer false negatives
            "impact_threshold":   15.0,   # but more false positives
            "stillness_threshold": 3.0,
            "stillness_duration":  2.5,
            "detection_window":    1.5,
        },
    }

    # ── Sampling ──
    ACCELEROMETER_INTERVAL = 0.05   # 20 Hz sampling rate (seconds)
    LOCATION_INTERVAL      = 30     # GPS update every 30 seconds

    # ── Alert Message Templates ──
    SMS_TEMPLATE = (
        "🚨 EMERGENCY ALERT - FallGuardian 🚨\n\n"
        "{name} may have fallen and needs help!\n\n"
        "📍 Last known location:\n"
        "Lat: {lat}, Lon: {lon}\n"
        "Google Maps: https://maps.google.com/?q={lat},{lon}\n\n"
        "⏰ Time: {time}\n\n"
        "Please check on them immediately or call emergency services."
    )

    WHATSAPP_TEMPLATE = SMS_TEMPLATE  # Same format for WhatsApp

    # ── Colors (for programmatic use) ──
    COLORS = {
        "bg_dark":     "#0A0E1A",
        "bg_card":     "#111827",
        "bg_surface":  "#1C2333",
        "cyan":        "#00D4FF",
        "red":         "#FF3B5C",
        "green":       "#00E676",
        "amber":       "#FFB300",
        "text_primary":"#FFFFFF",
        "text_secondary": "#8892A4",
    }
