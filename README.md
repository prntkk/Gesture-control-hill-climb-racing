

<!-- Banner -->
<p align="center">
  <img src="https://i.imgur.com/dhZ6frG.png" alt="Gesture Control Banner" width="100%">
</p>

<h1 align="center">🖐️ Gesture-Controlled Racing Game</h1>
<p align="center">
  Control racing games with your hands using MediaPipe + OpenCV + Python <br />
  Works with browser-based games like <strong>Hill Climb Racing</strong>, <strong>Slow Roads</strong>, and more.
</p>

---

## 🎮 Features

- ✋ Open Palm → Accelerate (Right Arrow)
- ✊ Fist → Brake / Reverse (Left Arrow)
- 🎥 Real-time webcam detection
- 🧠 Hand landmark tracking with MediaPipe
- 🎮 Works with games that use arrow keys or WASD

---

## 🚀 Getting Started

### 📁 Clone the Repo

```bash
git clone https://github.com/yourusername/gesture-control.git
cd gesture-control
```

### 🧪 Create a Virtual Environment (Recommended)

```bash
conda create -n gesture-env python=3.10 -y
conda activate gesture-env
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install opencv-python mediapipe pynput
```

---

## ▶️ Run It

```bash
python gesture_control.py
```

Keep your webcam on and launch any racing game (browser/emulator) in the background.

---

## 🧠 How It Works

- 📷 Captures live video feed using OpenCV
- ✋ Detects hand and finger positions via MediaPipe
- 🧠 Recognizes gestures like palm/fist
- ⌨️ Sends keypresses (← / →) using `pynput` to control any game

---

## 🗂️ Project Structure

```bash
gesture-control/
│
├── gesture_control.py       # Main controller script
├── requirements.txt         # Required Python packages
└── README.md                
```

---

## ✅ Tested With

- Python 3.10
- Hill Climb Racing (browser)
- Windows 10/11

---




