# Morse Code Blink Authentication System

A novel authentication system using **Morse code-inspired blink patterns** for secure, hands-free login.

- **Quick blink (< 0.4s)** = "dit" (dot) = **0**
- **Long blink (≥ 0.4s)** = "dah" (dash) = **1**

Register a 4-bit PIN using blink patterns and authenticate with the same Morse-like timing logic.

## Requirements

- Python 3.10 – 3.12
- OpenCV: `opencv-python`
- MediaPipe: `mediapipe`
- NumPy: `numpy`

## Install

```powershell
pip install opencv-python mediapipe numpy
```

## Register a user PIN

```powershell
python register_pin.py
```

- Enter a username when prompted.
- Perform 4 blinks to set your PIN:
  - Quick blink (< 0.4s) = 0
  - Long blink (≥ 0.4s) = 1
- Press `r` to reset or `q` to quit.
- The PIN is stored as a SHA-256 hash in `users.json` in this folder.

## Authenticate

```powershell
python blink_pin_fixed.py
```

- Enter the same username used during registration.
- Blink the same 4-bit sequence.
- Success/failure will be shown in the console and on-screen.

## Notes

- Thresholds and logic are shared via `blink_utils.py`.
- The system uses MediaPipe FaceMesh and an Eye Aspect Ratio (EAR)-based blink detector.
- Camera defaults to 640x480; adjust if needed.

---

## 🎯 Use Cases

### 1. **Emergency & Covert Communication**
- **Hostage situations**: Authenticate identity or send distress signals without speaking
- **Undercover operations**: Law enforcement can verify identity silently
- **Silent alarms**: Trigger security alerts through blink patterns without alerting threats
- **Kidnapping scenarios**: Victims can signal SOS using Morse-coded blinks

### 2. **Military & Defense Applications**
- **Tactical authentication**: Soldiers authenticate in radio-silent operations
- **POW identification**: Verify identity through blink codes in videos
- **Secure facility access**: Authenticate without physical tokens in classified areas
- **Covert messaging**: Send Morse-encoded messages through security cameras

### 3. **Medical & Healthcare**
- **Locked-in syndrome patients**: Communication for patients who can only control eye movement
- **Post-stroke rehabilitation**: Assess blink control and cognitive function
- **ICU patient authentication**: Verify patient identity when they cannot speak
- **Anesthesia awareness**: Monitor patient consciousness through blink responses

### 4. **Accessibility & Assistive Technology**
- **ALS/Motor Neuron Disease**: Alternative input for users who retain eye control
- **Severe paralysis**: Authentication for users with limited voluntary movement
- **Speech impairment**: Non-verbal authentication and communication
- **Brain-computer interface training**: Learn to control blink patterns for device control

### 5. **Privacy & Anti-Surveillance**
- **Public authentication**: No visible PIN pad for observers to record
- **Counter-surveillance**: Authenticate without leaving traces on input devices
- **Photographic evidence**: Verify identity in photos/videos through blink patterns
- **Deepfake detection**: Challenge-response blink patterns harder to fake in real-time

### 6. **Educational & Training**
- **Morse code learning**: Interactive way to practice Morse code (dit/dah as blinks)
- **Signal training**: First responders, pilots, military learn visual communication
- **STEM education**: Demonstrate computer vision, pattern recognition, cryptography
- **Accessibility awareness**: Train professionals on alternative communication methods

### 7. **Aviation & Maritime**
- **Pilot distress signals**: Detect blink-based SOS from incapacitated pilots
- **Submarine communications**: Silent authentication in sound-sensitive environments
- **Aircraft hijacking**: Pilots signal duress through pre-arranged blink codes
- **Naval operations**: Radio-silent authentication protocols

### 8. **Banking & Financial Security**
- **ATM anti-coercion**: Blink a "duress PIN" to silently alert authorities
- **High-value transactions**: Multi-factor authentication using blink-Morse code
- **Elderly banking**: Alternative for customers who struggle with PIN pads
- **Biometric vault access**: Combined face recognition + blink-code verification

### 9. **IoT & Smart Devices**
- **Smart glasses authentication**: Unlock AR glasses through eye-tracking cameras
- **Bathroom smart mirrors**: Authenticate to load personalized settings
- **Car driver identification**: Verify driver through dashboard cameras
- **Smart home security**: Alternative for users who forget traditional passwords

### 10. **Research & Development**
- **Cognitive load studies**: Measure user attention during blink authentication
- **Liveness detection**: Distinguish real blinks from replayed videos
- **Pattern recognition AI**: Train models to detect intentional vs. involuntary blinks
- **Human-computer interaction**: Study alternative input modalities

---

## ✅ Unique Advantages

- **Universally recognizable**: Morse code timing (dit/dah) is internationally known
- **Cultural/historical significance**: Military, maritime, emergency responders trained in Morse
- **Dual-purpose**: Works for both authentication AND communication
- **Timing-based security**: Harder to replay (requires precise timing replication)
- **No language barrier**: Binary encoding works across all languages
- **Hands-free**: Perfect for situations where hands are occupied or unavailable
- **Privacy-enhanced**: No physical keyboard input to observe or record

---

## ⚠️ Limitations

- **Timing precision**: Requires consistent dit/dah duration control
- **Learning curve**: Users need to remember their blink pattern
- **Eye fatigue**: Extended use can cause eye strain
- **Lighting dependent**: Requires adequate lighting for face detection
- **Speed trade-off**: Slower than traditional PIN entry
- **Medical conditions**: Not suitable for users with certain eye/neurological conditions

---

## 🚨 Critical Use Case: Distress Signaling

The most powerful application is **silent distress communication**:

- Hostages can blink **SOS** (`... --- ...` = short-short-short-long-long-long-short-short-short)
- Undercover agents verify identity through pre-arranged Morse patterns
- Medical patients signal **YES** or **NO** responses
- Covert operations require silent authentication without verbal/physical interaction

This transforms authentication into a **multi-purpose covert communication tool** with historical precedent and universal recognition! 🎖️
