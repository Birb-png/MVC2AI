import tkinter as tk
from datetime import datetime
from models import ChatbotDatabase, EmotionCalculator, ResponseLog
from views import ModernChatbotView  # import UI view

class ChatbotController:
    def __init__(self):
        """ Initialize database, emotion calculator, and UI setup. """
        self.db = ChatbotDatabase()  # question storage and logging
        self.emotion_calc = EmotionCalculator()  # cal emotion levels

        self.root = tk.Tk()
        self.view = ModernChatbotView(self.root)  # init bot UI

        self.view.set_generate_callback(self.generate_response)  # connect button to function
    
    def generate_response(self) -> None:
        """ Generate a question, process emotion, and update UI. """
        question_type = self.view.get_selected_type()  # get selected category
        question = self.db.get_random_question(question_type)  # fetch question
        emotion = self.emotion_calc.get_emotion(question_type)  # get emotion score
        
        # log response details in database
        self.db.log_response(ResponseLog(
            question_id=question.id,
            question_type=question_type,
            answer=question.answer,
            emotion_level=emotion,
            timestamp=datetime.now()
        ))

        # update chatbot UI with question .. answer and emotion level
        self.view.update_response(question.text, question.answer, emotion)
        self.view.update_stats(self.db.get_average_emotions())  # refresh stats

    def run(self) -> None:
        """ Start the chatbot UI event loop. """
        self.root.mainloop()

if __name__ == "__main__":
    app = ChatbotController()
    app.run()
