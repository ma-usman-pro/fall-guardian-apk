"""
services/fall_detector.py
Core fall detection algorithm using phone accelerometer.

Algorithm:
  1. Read accelerometer at 20 Hz
  2. Compute vector magnitude: √(x² + y² + z²)
  3. PHASE 1 - Free Fall:  magnitude < freefall_threshold (gravity disappears)
  4. PHASE 2 - Impact:     magnitude > impact_threshold   (body hits ground)
  5. PHASE 3 - Stillness:  magnitude stays low for N seconds (person not moving)
  → All 3 phases in sequence within detection_window = FALL DETECTED
"""

import math
from collections import deque
from datetime import datetime
from kivy.clock import Clock
from utils.config import AppConfig


class FallDetector:
    """
    Monitors accelerometer and fires callback when fall is detected.
    """

    def __init__(self, sensitivity: str = "medium", on_fall_detected=None):
        self.sensitivity     = sensitivity
        self.on_fall_detected = on_fall_detected  # Callback function
        self.thresholds      = AppConfig.THRESHOLDS[sensitivity]
        self.is_running      = False

        # ── State machine ──
        self.phase           = "IDLE"   # IDLE → FREEFALL → IMPACT → STILLNESS
        self.phase_timestamp = None

        # ── Rolling window of recent magnitudes ──
        self.magnitude_history = deque(maxlen=100)  # ~5 seconds at 20Hz

        # ── Accelerometer ──
        self._accel = None
        self._clock_event = None

        # ── Debug/test mode ──
        self.debug_mode = False

    # ──────────────────────────────────────────────
    #  PUBLIC API
    # ──────────────────────────────────────────────
    def start(self):
        """Start monitoring"""
        if self.is_running:
            return

        try:
            from plyer import accelerometer
            self._accel = accelerometer
            self._accel.enable()
            self.is_running = True
            self.phase = "IDLE"
            self._clock_event = Clock.schedule_interval(
                self._read_sensor,
                AppConfig.ACCELEROMETER_INTERVAL
            )
            print("[FallDetector] Started monitoring")
        except Exception as e:
            print(f"[FallDetector] Accelerometer not available: {e}")
            # On desktop/emulator, run in test mode
            self._start_simulation()

    def stop(self):
        """Stop monitoring"""
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None

        if self._accel:
            try:
                self._accel.disable()
            except Exception:
                pass

        self.is_running = False
        self.phase = "IDLE"
        print("[FallDetector] Stopped monitoring")

    def update_sensitivity(self, sensitivity: str):
        """Update sensitivity level"""
        if sensitivity in AppConfig.THRESHOLDS:
            self.sensitivity = sensitivity
            self.thresholds  = AppConfig.THRESHOLDS[sensitivity]

    def simulate_fall(self):
        """Manually trigger a fall detection (for testing)"""
        print("[FallDetector] ⚠️  Simulated fall triggered")
        if self.on_fall_detected:
            self.on_fall_detected()

    # ──────────────────────────────────────────────
    #  SENSOR READING
    # ──────────────────────────────────────────────
    def _read_sensor(self, dt):
        """Read accelerometer data and run detection algorithm"""
        try:
            values = self._accel.acceleration  # (x, y, z) in m/s²
            if values is None or values == (None, None, None):
                return

            x, y, z = values
            magnitude = math.sqrt(x**2 + y**2 + z**2)
            self.magnitude_history.append((datetime.now(), magnitude))
            self._run_detection(magnitude)

        except Exception as e:
            print(f"[FallDetector] Sensor read error: {e}")

    # ──────────────────────────────────────────────
    #  DETECTION ALGORITHM
    # ──────────────────────────────────────────────
    def _run_detection(self, magnitude: float):
        """
        3-phase fall detection state machine.
        Normal gravity = ~9.8 m/s²
        Free fall      = ~0 m/s²
        Hard impact    = 20-40+ m/s²
        """
        T = self.thresholds
        now = datetime.now()

        if self.phase == "IDLE":
            # Watch for free fall (gravity disappears)
            if magnitude < T["freefall_threshold"]:
                self.phase = "FREEFALL"
                self.phase_timestamp = now
                print(f"[FallDetector] PHASE 1: Free fall detected (mag={magnitude:.2f})")

        elif self.phase == "FREEFALL":
            elapsed = (now - self.phase_timestamp).total_seconds()

            # Check if still in detection window
            if elapsed > T["detection_window"]:
                print("[FallDetector] Detection window expired, resetting")
                self.phase = "IDLE"
                return

            # Watch for impact (sudden spike)
            if magnitude > T["impact_threshold"]:
                self.phase = "IMPACT"
                self.phase_timestamp = now
                print(f"[FallDetector] PHASE 2: Impact detected (mag={magnitude:.2f})")

        elif self.phase == "IMPACT":
            elapsed = (now - self.phase_timestamp).total_seconds()

            # Check if person became still (no movement after impact)
            if magnitude < T["stillness_threshold"]:
                if elapsed >= T["stillness_duration"]:
                    # ✅ FALL CONFIRMED
                    print("[FallDetector] ✅ FALL CONFIRMED — alerting!")
                    self.phase = "IDLE"
                    if self.on_fall_detected:
                        Clock.schedule_once(lambda dt: self.on_fall_detected(), 0)
            else:
                # Person is moving — they're okay, reset
                if elapsed > T["detection_window"] * 3:
                    print("[FallDetector] Person is moving after impact — OK, resetting")
                    self.phase = "IDLE"

    # ──────────────────────────────────────────────
    #  DESKTOP SIMULATION
    # ──────────────────────────────────────────────
    def _start_simulation(self):
        """Simulated monitoring for desktop testing (no real sensor)"""
        self.is_running = True
        self.debug_mode = True
        print("[FallDetector] Running in SIMULATION mode (no real accelerometer)")

    def get_current_magnitude(self):
        """Get the most recent acceleration magnitude"""
        if self.magnitude_history:
            return self.magnitude_history[-1][1]
        return 9.8  # default gravity

    def get_activity_level(self):
        """
        Returns activity level string based on recent movement.
        Used for UI display.
        """
        if not self.magnitude_history or len(self.magnitude_history) < 5:
            return "unknown"

        recent = [m for _, m in list(self.magnitude_history)[-20:]]
        avg = sum(recent) / len(recent)
        variance = sum((m - avg)**2 for m in recent) / len(recent)

        if variance < 1.0:
            return "still"
        elif variance < 5.0:
            return "walking"
        else:
            return "active"
