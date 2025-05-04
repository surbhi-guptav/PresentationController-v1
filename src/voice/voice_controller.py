import speech_recognition as sr
import pyautogui 
import threading
import winsound
import time
import re
import pyaudio

class VoiceController:
    def __init__(self, slide_controller, state):
        self.slide_controller = slide_controller
        self.state = state
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.running = True
        self.pyaudio_instance = None  # To manage PyAudio instance
        self.stream = None  # To manage the audio stream

        # Optimized for accuracy
        self.recognizer.energy_threshold = 350
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.9

        self.commands = {
            "next": ["next slide", "next", "go next", "slide forward", "next one", "next sl", "forward", "forward one"],
            "previous": ["previous slide", "previous", "go back", "back one", "prev", "prev slide", "back", "backward", "pre"],
            "on": ["on", "start", "enable", "begin", "activate", "initiate", "launch", "turn on", "open"],
            "off": ["off", "stop", "disable", "end", "deactivate", "quit", "close", "terminate"],
            "zoom_in": ["zoom in", "increase zoom", "zoomin", "zoom bigger"],
            "zoom_out": ["zoom out", "decrease zoom", "zoomout", "zoom smaller"],
            "go_to": ["go to slide", "jump to slide", "open slide", "to slide"],
            "switch_to_sign": ["switch to sign", "sign mode", "gesture mode", "switch to gesture", "gesture", "sign"],
            "exit": ["exit system"]
        }

        self.number_words = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
        }

    def word_to_number(self, word):
        return self.number_words.get(word.lower(), None)

    def match_command(self, command, group):
        matched = any(re.search(rf"\b{kw}\b", command, re.IGNORECASE) for kw in self.commands[group])
        if matched:
            pass
        return matched

    def _open_stream(self):
        """Open a new PyAudio stream."""
        try:
            if self.pyaudio_instance is None:
                self.pyaudio_instance = pyaudio.PyAudio()
            self.stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024
            )
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Failed to open audio stream: {e}")
            self._close_stream()

    def _close_stream(self):
        """Close the PyAudio stream and terminate the PyAudio instance."""
        try:
            if self.stream is not None:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            if self.pyaudio_instance is not None:
                self.pyaudio_instance.terminate()
                self.pyaudio_instance = None
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Error closing audio stream: {e}")

    def listen(self):
        print(f"[{time.strftime('%H:%M:%S')}] Voice control initializing...")
        try:
            with self.mic as source:
                print(f"[{time.strftime('%H:%M:%S')}] Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print(f"[{time.strftime('%H:%M:%S')}] Microphone calibrated. Say 'On' to activate commands.")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Microphone error: {e}. Ensure mic is connected.")
            return

        retry_delay = 2
        while self.running and self.state.system_running:
            timestamp = time.strftime("%H:%M:%S")
            try:
                print(f"[{timestamp}] Listening for audio input...")
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = self.recognizer.listen(source, phrase_time_limit=6)
                print(f"[{timestamp}] Processing audio...")
                command = self.recognizer.recognize_google(audio).lower()
                print(f"\n[{timestamp}] Heard: '{command}'")

                if self.match_command(command, "on") and not self.state.system_active:
                    self.state.system_active = True
                    self.state.system_running = True
                    winsound.Beep(1000, 200)
                    print(f"[{timestamp}] System: ON")
                elif self.match_command(command, "off") and self.state.system_active:
                    self.state.system_active = False
                    winsound.Beep(500, 200)
                    print(f"[{timestamp}] System: OFF")
                elif self.match_command(command, "exit") and self.state.system_active:
                    self.state.system_active = False
                    self.state.system_running = False
                    winsound.Beep(500, 200)
                    print(f"[{timestamp}] System: OFF (via Exit System command)")
                    print(f"[{timestamp}] System stopped. Returning to mode selection...")
                elif self.state.system_active:
                    if self.state.action_delay > 0:
                        print(f"[{timestamp}] Waiting {self.state.action_delay} seconds before executing action...")
                        time.sleep(self.state.action_delay)

                    if self.match_command(command, "next"):
                        count = 1
                        match = re.search(r'next\s+(\d+)(?:\s+slide)?', command, re.IGNORECASE)
                        if match:
                            count = int(match.group(1))
                        else:
                            match = re.search(r'next\s+(\w+)(?:\s+slide)?', command, re.IGNORECASE)
                            if match:
                                number_word = match.group(1)
                                count = self.word_to_number(number_word)
                                if count is not None:
                                    pass
                                else:
                                    if (command == "next slide" or command == "next") and number_word == "slide":
                                        count = 1
                                    else:
                                        print(f"[{timestamp}] Unrecognized number word: {number_word}")
                                        count = None
                            else:
                                for word in command.split():
                                    num = self.word_to_number(word)
                                    if num:
                                        count = num
                                        print(f"[{timestamp}] Parsed count from split: {word} -> {count}")
                                        break
                        if count is None:
                            count = 1
                            print(f"[{timestamp}] Defaulting count to 1 due to parsing failure")
                        self.slide_controller.perform_action(f"fist_right_{count}")
                    elif self.match_command(command, "previous"):
                        count = 1
                        match = re.search(r'previous\s+(\d+)(?:\s+slide)?', command, re.IGNORECASE)
                        if match:
                            count = int(match.group(1))
                        else:
                            match = re.search(r'previous\s+(\w+)(?:\s+slide)?', command, re.IGNORECASE)
                            if match:
                                number_word = match.group(1)
                                count = self.word_to_number(number_word)
                                if count is not None:
                                    pass
                                else:
                                    if (command == "previous slide" or command == "previous") and number_word == "slide":
                                        count = 1
                                    else:
                                        print(f"[{timestamp}] Unrecognized number word: {number_word}")
                                        count = None
                            else:
                                for word in command.split():
                                    num = self.word_to_number(word)
                                    if num:
                                        count = num
                                        print(f"[{timestamp}] Parsed count from split: {word} -> {count}")
                                        break
                        if count is None:
                            count = 1
                            print(f"[{timestamp}] Defaulting count to 1 due to parsing failure")
                        print(f"[{timestamp}] Executing previous slide with count: {count}")
                        self.slide_controller.perform_action(f"fist_left_{count}")
                    elif self.match_command(command, "zoom_out"):
                        print(f"[{timestamp}] Executing zoom out")
                        self.slide_controller.perform_action("zoom_out")
                    elif self.match_command(command, "zoom_in"):
                        print(f"[{timestamp}] Executing zoom in")
                        self.slide_controller.perform_action("zoom_in")
                    elif self.match_command(command, "go_to"):
                        match = re.search(r'slide\s+(\d+|\w+)', command, re.IGNORECASE)
                        if match:
                            slide_num_str = match.group(1)
                            slide_num = self.word_to_number(slide_num_str) or int(slide_num_str) if slide_num_str.isdigit() else None
                            if slide_num:
                                print(f"[{timestamp}] Executing go to slide: {slide_num}")
                                self.slide_controller.go_to_slide(slide_num)
                            else:
                                print(f"[{timestamp}] Invalid slide number")
                        else:
                            print(f"[{timestamp}] Please specify a slide number")
                    elif self.match_command(command, "switch_to_sign"):
                        self.state.mode = "gesture"
                        print(f"[{timestamp}] Switched to gesture mode")
                    else:
                        print(f"[{timestamp}] Unrecognized command")

            except sr.UnknownValueError:
                print(".", end="", flush=True)
            except sr.RequestError as e:
                print(f"\n[{timestamp}] Network error: {e}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 10)
            except Exception as e:
                print(f"\n[{timestamp}] Error: {e}")
            finally:
                # Ensure the stream is closed after each listen attempt
                self._close_stream()
                self._open_stream()  # Reopen for the next iteration

    def start(self):
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self._close_stream()