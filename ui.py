import event_factory as events
import pygame
import threading
import time
import speech_recognition as sr


window_dimensions = (500, 500)
     
class PygameWindow:
    def __init__(self) -> None:
        pygame.init()
        self.animation_in_progress = threading.RLock()
        self.seconds_between_frames = 0.2
        pygame.fastevent.init()
        threading.Thread(target=self.animate).start()
        self.listening_for_keystrokes = threading.Event()
        self.animation_in_progress = threading.RLock()

    def get_keyboard_events(self, keyboard_commands: list):
        self.listening_for_keystrokes.wait()
        while self.listening_for_keystrokes.is_set():
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        keyboard_commands.append(events.Up()) 
                    if event.key == pygame.K_DOWN:
                        keyboard_commands.append(events.Down()) 
                    if event.key == pygame.K_LEFT:
                        keyboard_commands.append(events.Left())
                    if event.key == pygame.K_RIGHT:
                        keyboard_commands.append(events.Right())

    def listen_for_keystrokes(self, duration):
        result = []
        self.listening_for_keystrokes.set()
        threading.Thread(target=self.get_keyboard_events, args=(result,)).start()
        time.sleep(duration)
        self.listening_for_keystrokes.clear()
        return result

    def show_prompts(self, voice_command, hardware_command):
        print(f"Say: {voice_command}")
        print(f"Do: {hardware_command}")

    def animate(self):
        window = pygame.display.set_mode(window_dimensions)
        pygame.display.set_caption("Do as I say not as I do")
        running = True
        with self.animation_in_progress:
            starting_time = time.process_time()
            with self.animation_in_progress:
                window.fill((0,200,0))
                pygame.fastevent.pump()
                elapsed_time = time.process_time() - starting_time
                if elapsed_time < self.seconds_between_frames:
                    pygame.time.wait(round((self.seconds_between_frames - elapsed_time) * 1000))
                pygame.display.flip()

class SpeechRecognizer(sr.Recognizer):
    # TODO: we going to have to not use the default google api key for production
    def __init__(self) -> None:
        super().__init__()
        self.mic = sr.Microphone()
        self.energy_threshold = 4000
        self.audio_data = None
    
    def listen_for_audio(self, seconds):
        with self.mic as source:
            audio_data = self.record(source, duration=seconds)
        self.audio_data = audio_data
        return audio_data

    def process_audio_data(self, audio_data: sr.AudioData):
        words_detected = self.recognize_google(audio_data)
        result = self.create_events(words_detected)
        return result

    def create_events(self, words_detected: str):
        word_list = words_detected.split()
        output_commands = []
        for word in word_list:
            if word == "up":
                output_commands.append(events.Up())
            elif word == "down":
                output_commands.append(events.Down())
            elif word == "left":
                output_commands.append(events.Left())
            elif word == "right":
                output_commands.append(events.Right())
        return output_commands

    def get_voice_responses(self, duration):
        voice_response = self.process_audio_data(self.listen_for_audio(duration))
        return voice_response


pygame_window = PygameWindow()
speech_rec = SpeechRecognizer()

def start_game(duration):

    threading.Thread(target=pygame_window.listen_for_keystrokes, args=(duration,)).start()
    threading.Thread(target=speech_rec.get_voice_responses, args=(duration,))
    print("break")

start_game(5)
