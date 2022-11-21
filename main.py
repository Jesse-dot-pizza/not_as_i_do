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

        
        # result = self.game_model.evaluate_responses(self.game_model.current_prompt)
        # self.ui.play_feedback(result)
        

