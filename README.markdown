# Presentation Controller 🎥✨

Welcome to the **Presentation Controller**—an innovative tool to control your PowerPoint presentations using **hand gestures** or **voice commands**! No more fumbling with a clicker—whether you're in a boardroom, classroom, or virtual meeting, this app makes presenting effortless and fun. Check out the demo below to see it in action! 🚀

## 🎬 Demo Video

See the Presentation Controller in action! Open the link and watch the demo video 

[![Demo Video](thumbnail.png)](https://drive.google.com/file/d/1zPdrTwPOjcT9rHNB2oHIsiq_YBQs1DH-/view?usp=sharing)


## 🎉 User Guide for Presentation Controller

Hey there, presenter extraordinaire! Ready to take your PowerPoint game to the next level? With the **Presentation Controller**, you can control your slides using **hand gestures** or **voice commands**—no more fumbling with a clicker! Whether you're in a boardroom, classroom, or virtual meeting, this app has got your back. Let’s dive in and get you started! 🚀

### 🌟 Getting Started
### 🎮 Using the Presentation Controller

#### Mode 1: Sign Mode (Gesture Control) ✋
In Sign Mode, you control your slides with simple hand gestures. It’s like magic! First, you need to activate the system with a gesture, then use other gestures to navigate your slides.

##### How to Activate Sign Mode
- **Gesture to Activate:** Show a **Thumbs Up** 👍 to the camera.
- You’ll see a message in the camera window: `System: ON`. The status bar will turn green, meaning the system is ready to listen to your gestures.

##### Gesture Commands
Here’s a table of all the gestures you can use in Sign Mode:

| **Gesture** | **Action** | **Description** |
| --- | --- | --- |
| **Thumbs Up** 👍 | Activate System | Turns on gesture control (status bar turns green). |
| **Thumbs Down** 👎 | Deactivate System | Turns off gesture control (status bar turns red). |
| **One Finger Right** 👆➡️ | Next Slide (x1) | Show the index finger of your **right hand** pointing right to move to the next slide. |
| **One Finger Left** 👆⬅️ | Previous Slide (x1) | Show the index finger of your **left hand** pointing left to move to the previous slide. |
| **Two Fingers Right** ✌️➡️ | Next Slide (x2) | Show two fingers (index and middle) of your **right hand** pointing right to skip forward 2 slides. |
| **Two Fingers Left** ✌️⬅️ | Previous Slide (x2) | Show two fingers (index and middle) of your **left hand** pointing left to skip backward 2 slides. |
| **Three Fingers Right** | Next Slide (x3) | Show three fingers (index, middle, ring) of your **right hand** pointing right to skip forward 3 slides. |
| **Three Fingers Left**  | Previous Slide (x3) | Show three fingers (index, middle, ring) of your **left hand** pointing left to skip backward 3 slides. |
| **Four Fingers Right** | Next Slide (x4) | Show four fingers (index, middle, ring, pinky) of your **right hand** pointing right to skip forward 4 slides. |
| **Four Fingers Left** | Previous Slide (x4) | Show four fingers (index, middle, ring, pinky) of your **left hand** pointing left to skip backward 4 slides. |
| **Right Hand Fist** ✊ | Zoom In | Make a fist with your **right hand** to zoom in on the slide (like `Ctrl + Plus`). |
| **Right Hand Palm** 🖐️ | Zoom Out | Show an open palm with your **right hand** to zoom out on the slide (like `Ctrl + Minus`). |

##### Tips for Sign Mode
- **Gesture Timing:** Wait about 1 second between gestures to avoid accidental repeats.
- **Camera Window:** A small camera window will show what the app sees. Use it to ensure your hand is in view.
- **Restarting:** To switch modes or restart, close the app and reopen it to return to the mode selection window.

---
#### Mode 2: Voice Mode (Voice Control) 🗣️
In Voice Mode, you control your slides by speaking commands. It’s as easy as talking to a friend! First, you need to activate the system with a voice command, then use other commands to navigate your slides.

##### How to Activate Voice Mode
- When you select Voice Mode, the app will calibrate your microphone.
- You’ll see a message: `Microphone calibrated. Say 'On' to activate commands.`
- Say **"On"** to activate the system. You’ll hear a beep, and the app will log: `System: ON`. Now it’s listening for your commands!

##### Voice Commands
Here’s a table of all the voice commands you can use in Voice Mode:

| **Command Group** | **Example Phrases** | **Action** | **Description** |
| --- | --- | --- | --- |
| **On** | "On", "Start", "Enable", "Begin" | Activate System | Turns on voice control (you’ll hear a beep). |
| **Off** | "Off", "Stop", "Disable", "End" | Deactivate System | Turns off voice control (you’ll hear a different beep). |
| **Next** | "Next slide", "Next", "Go next", "Forward" | Next Slide (x1 or more) | Moves to the next slide. Say "Next 3 slide" or "Next three slide" to skip 3. |
| **Previous** | "Previous slide", "Previous", "Go back" | Previous Slide (x1 or more) | Moves to the previous slide. Say "Previous 2 slide" to skip back 2. |
| **Zoom In** | "Zoom in", "Increase zoom", "Zoom bigger" | Zoom In | Zooms in on the slide (like `Ctrl + Plus`). |
| **Zoom Out** | "Zoom out", "Decrease zoom", "Zoom smaller" | Zoom Out | Zooms out on the slide (like `Ctrl + Minus`). |
| **Go To** | "Go to slide 5", "Jump to slide three" | Go to Specific Slide | Jumps to the specified slide number (e.g., "Go to slide 5" jumps to slide 5). |
| **Switch to Sign** | "Switch to sign", "Gesture mode", "Sign" | Switch to Sign Mode | Switches to Sign Mode (you’ll need to restart gesture control with Thumbs Up). |
| **Exit** | "Exit system" | Exit Voice Mode | Stops Voice Mode and returns to the mode selection window. |

##### Tips for Voice Mode
- **Speak Clearly:** Use a clear, natural voice. Avoid background noise for best results.
- **Numbers in Commands:** You can use numbers (e.g., "Next 3 slide") or number words (e.g., "Next three slide") to skip multiple slides.
- **Network Requirement:** Voice Mode requires an internet connection for speech recognition.
- **Restarting:** Use the "Exit system" command to return to the mode selection window, then choose a mode to restart.

---
### 🛠️ Running the Code on Your System

Want to run the Presentation Controller directly from the source code on your own system? Follow these steps to set up and run the project from the GitHub repository. Let’s get started! 🚀

#### Prerequisites
Before you begin, ensure your system meets these requirements:
- **Operating System:** Windows (the app uses Windows-specific libraries like `pywin32`).
- **Hardware:**
  - A webcam (for Sign Mode).
  - A microphone (for Voice Mode).
- **Software:**
  - **Python 3.10 or higher:** Download and install from [python.org](https://www.python.org/downloads/).
  - **Git:** Install Git to clone the repository. Download from [git-scm.com](https://git-scm.com/downloads).
  - **Microsoft PowerPoint:** Installed on your system to control presentations.
- **Internet Connection:** Required for Voice Mode (speech recognition) and to install dependencies.

#### Step 1: Clone the Repository
1. Open a terminal (e.g., Command Prompt, PowerShell, or Git Bash).
2. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/surbhi-guptav/PresentationController-v1.git
   ```
3. Navigate into the project directory:
   ```bash
   cd PresentationController-v1
   ```

#### Step 2: Set Up a Virtual Environment
It’s best to use a virtual environment to manage dependencies and avoid conflicts.
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   You should see `(venv)` in your terminal prompt.

#### Step 3: Install Dependencies
The project includes a `requirements.txt` file listing all required Python libraries.
1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   - **Note on PyAudio:** If `PyAudio` fails to install, you may need to install it manually:
     - Download the appropriate wheel file for your Python version and system from [PyPi](https://pypi.org/project/PyAudio/#files) (e.g., `PyAudio-0.2.14-cp310-cp310-win_amd64.whl` for Python 3.10 on 64-bit Windows).
     - Install it with:
       ```bash
       pip install path\to\PyAudio-0.2.14-cp310-cp310-win_amd64.whl
       ```

#### Step 4: Verify the Directory Structure
Ensure your project directory has the following structure:
```
PresentationController-v1/
│
├── src/
│   ├── app.py # Main application script
|   ├── sign / slide_controller.py
│   ├── voice / voice_controller.py   # Voice Mode logic
│   ├── Ui_images/
│   │   ├── sign_mode.png     # Image for Sign Mode button
│   │   └── voice.png         # Image for Voice Mode button
│
├── models/
│   └── model_updated.p       # Pre-trained model for Sign Mode
│
├── demo.mp4              # Demo video (optional, if hosted in repo)
│
├── requirements.txt          # List of dependencies
│
└── README.md                 # This user guide
```
- If any files are missing (e.g., `sign_mode.png`, `voice.png`, or `model_updated.p`), you won’t be able to run the app. Contact the repository owner to obtain these files or check the repository for updates.

#### Step 5: Run the Application
1. Run the main script:
   ```bash
   python src/app.py
   ```
2. The welcome window should appear, allowing you to select Sign Mode or Voice Mode.
3. Follow the usage instructions in this user guide to use Sign Mode or Voice Mode.

### 🎈 Thankyou for using my application
