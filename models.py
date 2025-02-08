from typing import List, Optional
from dataclasses import dataclass
import json
import random
from enum import Enum
from datetime import datetime

class QuestionType(Enum):
    SCIENCE = "วิทยาศาสตร์"
    GENERAL = "ความรู้ทั่วไป"
    EMOTIONAL = "คำถามเชิงอารมณ์"

@dataclass
class Question:
    id: str
    type: QuestionType
    text: str
    answer: str

@dataclass
class ResponseLog:
    question_id: str
    question_type: QuestionType
    answer: str
    emotion_level: float
    timestamp: datetime

class EmotionCalculator:
    def __init__(self):
        self.previous_emotion: float = 100.0
        self.previous_type: Optional[QuestionType] = None
        self.emotional_streak: int = 0
    
    def calculate_science_emotion(self) -> float:
        if (self.previous_type == QuestionType.EMOTIONAL and 
            self.previous_emotion is not None and 
            self.previous_emotion < 30):
            return random.uniform(10, 40)
        return random.uniform(50, 80)
    
    def calculate_general_emotion(self) -> float:
        if (self.previous_type == QuestionType.SCIENCE and 
            self.previous_emotion is not None and 
            self.previous_emotion < 60):
            return random.uniform(30, 60)
        return random.uniform(70, 100)
    
    def calculate_emotional_emotion(self) -> float:
        if self.emotional_streak >= 3:
            return random.uniform(20, 50)
        
        if self.previous_emotion is None:
            return 100.0
            
        change = random.uniform(-10, 10)
        return max(0, min(100, self.previous_emotion + change))
    
    def get_emotion(self, question_type: QuestionType) -> float:
        if question_type == QuestionType.EMOTIONAL:
            self.emotional_streak += 1
        else:
            self.emotional_streak = 0
            
        emotion = {
            QuestionType.SCIENCE: self.calculate_science_emotion,
            QuestionType.GENERAL: self.calculate_general_emotion,
            QuestionType.EMOTIONAL: self.calculate_emotional_emotion
        }[question_type]()
        
        self.previous_emotion = emotion
        self.previous_type = question_type
        return round(emotion, 2)

class ChatbotDatabase:
    def __init__(self, filename: str = "questions.json"):
        self.filename = filename
        self.questions: List[Question] = []
        self.logs: List[ResponseLog] = []
        self.load_data()
        
    def load_data(self) -> None:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.questions = [
                    Question(
                        id=q['id'],
                        type=QuestionType(q['type']),
                        text=q['text'],
                        answer=q['answer']
                    ) for q in data['questions']
                ]
        except FileNotFoundError:
            self._create_sample_data()
            self.save_data()
    
    def save_data(self) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump({
                'questions': [
                    {
                        'id': q.id,
                        'type': q.type.value,
                        'text': q.text,
                        'answer': q.answer
                    }
                    for q in self.questions
                ]
            }, f, ensure_ascii=False, indent=2)
    
    def get_random_question(self, type: QuestionType) -> Question:
        questions_of_type = [q for q in self.questions if q.type == type]
        return random.choice(questions_of_type)
    
    def log_response(self, response: ResponseLog) -> None:
        self.logs.append(response)
        ChatLogger.log_chat(response)
    
    def get_average_emotions(self) -> dict:
        if not self.logs:
            return {
                'overall': 0,
                QuestionType.SCIENCE.value: 0,
                QuestionType.GENERAL.value: 0,
                QuestionType.EMOTIONAL.value: 0
            }
        
        emotions = {type: [] for type in QuestionType}
        for log in self.logs:
            emotions[log.question_type].append(log.emotion_level)
        
        all_emotions = [log.emotion_level for log in self.logs]
        
        return {
            'overall': sum(all_emotions) / len(all_emotions),
            **{
                type.value: (sum(vals) / len(vals) if vals else 0)
                for type, vals in emotions.items()
            }
        }

class ChatLogger:
    @staticmethod
    def log_chat(response: ResponseLog):
        with open("chat_log.txt", "a", encoding="utf-8") as f:
            f.write(
                f"{response.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"ประเภท: {response.question_type.value} | "
                f"คำถาม ID: {response.question_id} | "
                f"อารมณ์: {response.emotion_level:.2f}%\n"
            )
