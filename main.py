import game_model
import ui
import event_factory as events


class Controller:
    def __init__(self) -> None:
        self.window = ui.PygameWindow()
        self.speech = ui.SpeechRecognizer()
        self.game_model = game_model.GameModel()

    def game_loop(self):
        self.window.show_prompts(self.game_model.current_prompt)
        # wait for one keyboard and one voice command(?)
        self.game_model.next_prompt()
