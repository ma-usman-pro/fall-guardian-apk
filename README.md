# 🛡️ FallGuardian — Smart Fall Detection App

> **Always watching. Always ready.**
> Python mobile app that detects falls using phone sensors and alerts family members via SMS/WhatsApp.

---

## 📱 What This App Does

1. **Monitors** your phone's accelerometer (motion sensor) continuously
2. **Detects** a fall using a 3-phase algorithm:
   - Phase 1: Free-fall (gravity disappears briefly)
   - Phase 2: Impact (sudden spike when hitting ground)
   - Phase 3: Stillness (no movement = person may be injured)
3. **Shows** a 15-second countdown so you can cancel if it's a false alarm
4. **Sends** SMS/WhatsApp alert with GPS location to all family contacts

---

## 🗂️ File Structure

```
fall_guardian/
├── main.py                    ← App entry point (start here)
├── requirements.txt           ← Python packages
├── buildozer.spec             ← Android build config
│
├── screens/
│   ├── splash_screen.py       ← Animated loading screen
│   ├── home_screen.py         ← Main dashboard + fall detection
│   ├── contacts_screen.py     ← Add/remove emergency contacts
│   ├── settings_screen.py     ← Twilio keys + sensitivity
│   └── history_screen.py      ← Past alerts log
│
├── services/
│   ├── fall_detector.py       ← Core fall detection algorithm
│   ├── gps_service.py         ← GPS location tracking
│   └── alert_service.py       ← Twilio SMS/WhatsApp sender
│
├── utils/
│   ├── storage.py             ← JSON file storage
│   └── config.py              ← Thresholds & configuration
│
└── assets/
    └── images/                ← App icon, splash screen
```

---

## 🚀 Step-by-Step Setup Guide (for Beginners)

### STEP 1 — Install Python

Download Python 3.10 or 3.11 from: https://www.python.org/downloads/
During install, **check "Add Python to PATH"**.

Verify installation:
```bash
python --version
```

---

### STEP 2 — Install Project Dependencies

Open terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This will install Kivy, KivyMD, Twilio, and Plyer.

---

### STEP 3 — Get Twilio Account (FREE)

Twilio gives you a free trial with $15 credit — enough for hundreds of SMS.

1. Go to https://www.twilio.com/try-twilio
2. Sign up for free account
3. Verify your phone number
4. From the Console Dashboard, copy:
   - **Account SID** (looks like: ACxxxxxxxxxxxxxxxx)
   - **Auth Token** (long secret key)
5. Click "Get a Trial Number" to get your Twilio phone number

**For WhatsApp alerts (optional):**
1. In Twilio Console → Messaging → Try it out → Send a WhatsApp message
2. Follow instructions to join the WhatsApp sandbox
3. Ask your family members to also join the sandbox (one time setup)

---

### STEP 4 — Test on Desktop First

```bash
cd fall_guardian
python main.py
```

On desktop, the accelerometer won't work (it's a phone sensor), but you can:
- Add contacts
- Configure Twilio credentials
- Press "Test Fall" button to simulate a fall
- See the emergency countdown overlay

---

### STEP 5 — Configure the App

In the app's Settings screen:
1. Enter your name
2. Paste your Twilio Account SID
3. Paste your Twilio Auth Token
4. Enter your Twilio phone number (format: +1XXXXXXXXXX)
5. Choose alert mode: SMS, WhatsApp, or Both
6. Set sensitivity (Medium is recommended)
7. Tap Save (💾 icon)

In the Contacts screen:
1. Tap + button
2. Add family members with their phone numbers
3. Use international format: +92XXXXXXXXXX (for Pakistan)

---

### STEP 6 — Build Android APK

**Requirements for building APK:**
- Linux OS (Ubuntu recommended) OR use Google Colab/Docker
- Python 3.10
- Java JDK 17

**Install Buildozer:**
```bash
pip install buildozer
sudo apt-get install -y git zip unzip openjdk-17-jdk
```

**Build the APK:**
```bash
cd fall_guardian
buildozer android debug
```

First build takes 20-30 minutes (downloads Android SDK/NDK).
APK will be in: `fall_guardian/bin/fallguardian-1.0-debug.apk`

**Deploy to phone:**
```bash
buildozer android deploy run
```
Or manually copy APK to phone and install (enable "Unknown Sources" first).

---

## 📋 Twilio Quick Reference

| What you need | Where to find it |
|--------------|------------------|
| Account SID | twilio.com/console (Dashboard) |
| Auth Token | twilio.com/console (Dashboard, click reveal) |
| Phone number | twilio.com/console → Phone Numbers |
| WhatsApp sandbox | twilio.com/console → Messaging → Try it out |

---

## 🔧 Troubleshooting

**App crashes on startup:**
- Make sure all packages are installed: `pip install -r requirements.txt`

**Accelerometer not working on desktop:**
- Normal! Sensors only work on actual Android device
- Use "Test Fall" button for desktop testing

**Twilio not sending messages:**
- Check credentials are correct in Settings
- Verify phone numbers are in international format (+923001234567)
- For WhatsApp: make sure contacts have joined the sandbox
- Check Twilio Console → Monitor → Logs for errors

**False alarms:**
- Lower sensitivity to "Low" in Settings
- The 15-second countdown lets you cancel accidental detections

**GPS location not available:**
- Make sure Location permission is granted
- Go outside or near a window for better signal

---

## 🛠️ Customization Tips

**Change alert message** → Edit `utils/config.py`, look for `SMS_TEMPLATE`

**Adjust fall detection sensitivity** → Edit `utils/config.py`, look for `THRESHOLDS`

**Add more screens** → Create file in `screens/`, import in `main.py`

---

## 📞 Support

If you face any issues:
1. Check the Troubleshooting section above
2. Search on Stack Overflow for Kivy/KivyMD specific issues
3. Kivy Discord: https://chat.kivy.org/
