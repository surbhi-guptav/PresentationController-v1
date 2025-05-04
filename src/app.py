import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
import threading
import tkinter as tk
from tkinter import ttk
import warnings
from sign.slide_controller import SlideController
from voice.voice_controller import VoiceController
from PIL import Image, ImageTk
import sys
import os

# Function to handle paths for PyInstaller
def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Suppress all UserWarnings (including protobuf deprecation)
warnings.filterwarnings("ignore", category=UserWarning)

# Simple class to hold shared state
class SystemState:
    def __init__(self):
        self.mode = None
        self.running = True  # To control the main loop
        self.system_running = True  # To control whether the system is fully running or stopped
        self.system_active = False
        self.last_gesture_time = 0
        self.last_detected_action = None
        self.last_detected_gesture = None  # To track the last detected gesture for debouncing
        self.cooldown = 1.0
        self.action_delay = 0  # Delay before executing the action

state = SystemState()
mode_selected = threading.Event()

def create_welcome_window():
    """Create a centered welcome window for mode selection with modern UI and colorful icons."""
    root = tk.Tk()
    root.title("Presentation Controller")
    root.geometry("700x420")
    root.configure(bg="#F5F7FA")
    root.resizable(False, False)

    def select_sign_mode(event=None):
        state.mode = "gesture"
        mode_selected.set()
        root.destroy()

    def select_voice_mode(event=None):
        state.mode = "voice"
        mode_selected.set()
        root.destroy()

    def apply_hand_cursor(widget):
        widget.configure(cursor="hand2")
        for child in widget.winfo_children():
            child.configure(cursor="hand2")

    # Load and resize icons using resource_path
    hand_img = Image.open(resource_path(r"src\Ui_images\sign_mode.png")).resize((64, 64), Image.Resampling.LANCZOS)
    hand_icon = ImageTk.PhotoImage(hand_img)

    mic_img = Image.open(resource_path(r"src\Ui_images\voice.png")).resize((64, 64), Image.Resampling.LANCZOS)
    mic_icon = ImageTk.PhotoImage(mic_img)

    # Title
    icon_label = tk.Label(root, text="", bg="#F5F7FA")
    icon_label.pack(pady=(30, 10))

    title = tk.Label(root, text="Presentation Controller", font=("Helvetica", 24, "bold"), fg="#2C3E50", bg="#F5F7FA")
    title.pack()

    subtitle = tk.Label(
        root,
        text="Choose how you'd like to interact with our system—via gestures or voice commands.",
        font=("Helvetica", 12),
        fg="#555555",
        bg="#F5F7FA"
    )
    subtitle.pack(pady=(5, 20))

    # Button container
    button_frame = tk.Frame(root, bg="#F5F7FA")
    button_frame.pack()

    # Sign Mode Box
    sign_card = tk.Frame(button_frame, bg="white", bd=2, relief="groove", padx=20, pady=10)
    sign_card.grid(row=0, column=0, padx=20)
    sign_card.bind("<Button-1>", select_sign_mode)
    apply_hand_cursor(sign_card)

    sign_icon_label = tk.Label(sign_card, image=hand_icon, bg="white")
    sign_icon_label.pack()

    sign_title = tk.Label(sign_card, text="Sign Mode", font=("Helvetica", 14, "bold"), fg="#2C3E50", bg="white")
    sign_title.pack(pady=(10, 2))

    sign_desc = tk.Label(sign_card, text="Use gesture or manual input to sign in.", font=("Helvetica", 10), fg="#777777", bg="white")
    sign_desc.pack()

    # Voice Mode Box
    voice_card = tk.Frame(button_frame, bg="white", bd=2, relief="groove", padx=20, pady=10)
    voice_card.grid(row=0, column=1, padx=20)
    voice_card.bind("<Button-1>", select_voice_mode)
    apply_hand_cursor(voice_card)

    voice_icon_label = tk.Label(voice_card, image=mic_icon, bg="white")
    voice_icon_label.pack()

    voice_title = tk.Label(voice_card, text="Voice Mode", font=("Helvetica", 14, "bold"), fg="#2C3E50", bg="white")
    voice_title.pack(pady=(10, 2))

    voice_desc = tk.Label(voice_card, text="Use your voice for hands-free interaction.", font=("Helvetica", 10), fg="#777777", bg="white")
    voice_desc.pack()

    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()

def initialize_system():
    """Initialize or reset the system state and resources."""
    global cap, hands, segmentation, model
    # Reset state variables (except mode, which is set by create_welcome_window)
    state.system_active = False
    state.system_running = True
    state.last_gesture_time = 0
    state.last_detected_action = None
    state.last_detected_gesture = None

    # Release existing camera resources if they exist
    if 'cap' in globals() and cap is not None:
        cap.release()
        cv2.destroyAllWindows()

    # Reinitialize camera and other resources for Sign Mode
    if state.mode == "gesture":
        
        model_dict = pickle.load(open(resource_path('models/model_updated.p'), 'rb'))
        model = model_dict['model']
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
        mp_selfie_segmentation = mp.solutions.selfie_segmentation
        segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Initialize SlideController and VoiceController
slide_controller = SlideController()
print(f"[{time.strftime('%H:%M:%S')}] Loaded SlideController with methods: {dir(slide_controller)}")
voice_controller = VoiceController(slide_controller, state)

# Load gesture model and initialize webcam only for Sign Mode
model = None
cap = None
hands = None
segmentation = None

# Initialize MediaPipe drawing utilities globally
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Define the gesture names in the same order as collect_data.py
gestures = [
    'one_finger_left', 'one_finger_right', 'thumbs_up', 'thumbs_down',
    'zoom_in', 'zoom_out', 'two_next', 'two_previous',
    'three_next', 'three_previous', 'four_next', 'four_previous'
]
print(f"[{time.strftime('%H:%M:%S')}] Gesture mapping: {dict(enumerate(gestures))}")

# Gesture to SlideController action mapping
gesture_action_map = {
    'one_finger_right': 'fist_right_1',
    'one_finger_left': 'fist_left_1',
    'two_next': 'fist_right_2',
    'three_next': 'fist_right_3',
    'four_next': 'fist_right_4',
    'two_previous': 'fist_left_2',
    'three_previous': 'fist_left_3',
    'four_previous': 'fist_left_4',
    'zoom_in': 'zoom_in',
    'zoom_out': 'zoom_out'
}

def run_voice_controller():
    """Run the voice controller in a separate thread."""
    print(f"[{time.strftime('%H:%M:%S')}] Starting voice controller thread...")
    while state.running:
        try:
            if state.mode == "voice" and state.system_running:
                print(f"[{time.strftime('%H:%M:%S')}] Voice mode active. Listening...")
                voice_controller.listen()
                time.sleep(0.5)  # Avoid CPU overload
            else:
                time.sleep(1)  # Wait while in gesture mode or system is stopped
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Voice controller error: {e}")
            time.sleep(2)  # Wait before retrying

# Start voice controller in a separate thread
voice_thread = threading.Thread(target=run_voice_controller, daemon=True)
voice_thread.start()

try:
    while state.running:
        # Run the welcome window to select mode
        mode_selected.clear()
        create_welcome_window()
        mode_selected.wait()  # Wait for the user to select a mode

        if state.mode is None:
            print("No mode selected. Exiting...")
            break

        # Initialize or reset the system after mode selection
        initialize_system()

        print(f"[{time.strftime('%H:%M:%S')}] Starting in {state.mode} mode...")

        while state.system_running and state.running:
            if state.mode == "gesture" and cap is not None:  # Process frames in Sign Mode
                start_time = time.time()

                data_aux = []
                x_ = []
                y_ = []

                ret, frame = cap.read()
                if not ret:
                    print("Error: Cannot access webcam.")
                    break

                H, W, _ = frame.shape
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Background segmentation
                if segmentation:
                    seg_results = segmentation.process(frame_rgb)
                    condition = np.stack((seg_results.segmentation_mask,) * 3, axis=-1) > 0.5
                    bg_image = np.zeros(frame.shape, dtype=np.uint8)
                    frame_rgb = np.where(condition, frame_rgb, bg_image)

                results = hands.process(frame_rgb)
                predicted_class = None
                confidence = 0.0
                x1, y1, x2, y2 = 0, 0, 0, 0  # Initialize bounding box coordinates

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp.solutions.hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            x_.append(x)
                            y_.append(y)

                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            data_aux.append(x - min(x_))
                            data_aux.append(y - min(y_))

                        x1 = int(min(x_) * W) - 10
                        y1 = int(min(y_) * H) - 10
                        x2 = int(max(x_) * W) - 10
                        y2 = int(max(y_) * H) - 10

                    if len(data_aux) == 42:
                        prediction = model.predict([np.asarray(data_aux)])
                        predicted_idx = int(prediction[0])
                        predicted_class = gestures[predicted_idx]
                        confidence = model.predict_proba([np.asarray(data_aux)]).max()

                        if confidence > 0.95:
                            current_time = time.time()
                            # Only process if the gesture is different or enough time has passed and it's a new detection
                            if (predicted_class != state.last_detected_gesture or 
                                current_time - state.last_gesture_time >= state.cooldown):
                                state.last_gesture_time = current_time
                                state.last_detected_gesture = predicted_class
                                # Draw bounding box and label in green for better visibility
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
                                cv2.putText(frame, f"{predicted_class}", (x1, y1 - 10), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
                                cv2.imshow('Presentation Controller - Sign Mode', frame)
                                cv2.waitKey(1)  # Ensure the frame updates

                                print(f"[{time.strftime('%H:%M:%S')}] Predicted: {predicted_class} ({confidence:.2f})")
                                print(f"[{time.strftime('%H:%M:%S')}] System Active: {state.system_active}")

                                # Wait for 1.2 seconds before executing the action
                                time.sleep(state.action_delay)

                                if predicted_class == 'thumbs_up':
                                    state.system_active = True
                                    state.system_running = True  # Ensure system is running
                                    state.last_detected_action = "Thumbs Up (System On)"
                                elif predicted_class == 'thumbs_down':
                                    if state.system_active:
                                        state.system_active = False
                                        state.system_running = False  # Fully stop the system
                                        state.last_detected_action = "Thumbs Down (System Off)"
                                        print(f"[{time.strftime('%H:%M:%S')}] System stopped. Returning to mode selection...")
                                elif state.system_active and state.mode == "gesture":
                                    action = gesture_action_map.get(predicted_class)
                                    if action:
                                        slide_controller.perform_action(action)
                                        state.last_detected_action = f"{predicted_class.replace('_', ' ').title()}"
                                    else:
                                        print(f"[{time.strftime('%H:%M:%S')}] No action mapped for {predicted_class}")
                                else:
                                    print(f"[{time.strftime('%H:%M:%S')}] System Inactive: No action taken")
                else:
                    # No hand detected; reset the last detected gesture
                    state.last_detected_gesture = None

                # Draw status bar at the bottom of the frame
                status_text = "System: ON" if state.system_active else "System: OFF"
                status_color = (0, 255, 0) if state.system_active else (0, 0, 255)  # Green for ON, Red for OFF
                status_bar_height = 40
                cv2.rectangle(frame, (0, H - status_bar_height), (W, H), status_color, -1)  # Filled rectangle
                cv2.putText(frame, status_text, (10, H - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.imshow('Presentation Controller - Sign Mode', frame)
                end_time = time.time()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    state.running = False
                    break
            else:  # Voice Mode
                time.sleep(0.1)  # Small delay to prevent CPU overload
                # Check for 'q' keypress using msvcrt for Windows (non-blocking)
                try:
                    import msvcrt
                    if msvcrt.kbhit():
                        if msvcrt.getch().decode('utf-8').lower() == 'q':
                            state.running = False
                            break
                except ImportError:
                    pass  # If msvcrt is not available, rely on Ctrl+C

except KeyboardInterrupt:
    print("\n[{time.strftime('%H:%M:%S')}] Program interrupted by user. Exiting...")
    if 'cap' in globals() and cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    print("Thanks for using the Presentation Controller! Come back soon!")
    exit(0)

# Ensure resources are cleaned up if the loop exits normally
if 'cap' in globals() and cap is not None:
    cap.release()
cv2.destroyAllWindows()
print("Thanks for using the Presentation Controller! Come back soon!")