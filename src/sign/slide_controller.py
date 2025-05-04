import pyautogui # type: ignore
import win32gui
import time

class SlideController:
    def __init__(self):
        # Generic PowerPoint-related titles
        self.powerpoint_titles = ["PowerPoint", "Microsoft PowerPoint", "Slide Show"]

    def focus_powerpoint(self):
        for attempt in range(2):
            hwnd = win32gui.FindWindow(None, None)
            while hwnd:
                title = win32gui.GetWindowText(hwnd)
                if any(ptitle in title for ptitle in self.powerpoint_titles):
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                        # print(f"[{time.strftime('%H:%M:%S')}] PowerPoint focused: {title}")
                        time.sleep(0.5)  # Give time for focus to settle
                        return True
                    except Exception as e:
                        print(f"[{time.strftime('%H:%M:%S')}] Focus failed: {e}")
                hwnd = win32gui.GetWindow(hwnd, 2)
            # print(f"[{time.strftime('%H:%M:%S')}] Attempt {attempt + 1}/2: PowerPoint window not found. Trying to switch...")
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.5)
        # print(f"[{time.strftime('%H:%M:%S')}] Failed to focus PowerPoint after 2 attempts.")
        return False

    def perform_action(self, gesture):
        if gesture:
            if self.focus_powerpoint():
                print(f"[{time.strftime('%H:%M:%S')}] Executing action: {gesture}")
                if "fist_right" in gesture:
                    count = int(gesture.split('_')[-1])
                    # print(f"[{time.strftime('%H:%M:%S')}] Next {count} Slide")
                    for _ in range(count):
                        pyautogui.press('right')
                        time.sleep(0.1)  # Small delay between key presses
                elif "fist_left" in gesture:
                    count = int(gesture.split('_')[-1])
                    #print(f"[{time.strftime('%H:%M:%S')}] Previous {count} Slide")
                    for _ in range(count):
                        pyautogui.press('left')
                        time.sleep(0.1)  # Small delay between key presses
                elif gesture == "zoom_in":
                    pyautogui.hotkey('ctrl', '+')
                   # print(f"[{time.strftime('%H:%M:%S')}] Zooming In")
                elif gesture == "zoom_out":
                    pyautogui.hotkey('ctrl', '-')
                   # print(f"[{time.strftime('%H:%M:%S')}] Zooming Out")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Action skipped: PowerPoint not focused")

    def go_to_slide(self, slide_number):
        if self.focus_powerpoint():
            pyautogui.hotkey('ctrl', 'g')
            time.sleep(0.2)
            pyautogui.write(str(slide_number))
            pyautogui.press('enter')
            print(f"[{time.strftime('%H:%M:%S')}] Navigating to slide {slide_number}")