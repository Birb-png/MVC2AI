# view.py
import tkinter as tk
from tkinter import ttk
from typing import Callable
from models import QuestionType
from PIL import Image, ImageTk
import io
from datetime import datetime

class ModernChatbotView:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AI Chatbot Birb-png")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f2f5')
        
        self.setup_ui()
    def setup_ui(self):
        # main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # chat area (left side)
        self.chat_frame = ttk.Frame(self.main_container)
        self.chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # msg area
        self.messages_frame = ttk.Frame(self.chat_frame)
        self.messages_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollable message area
        self.canvas = tk.Canvas(self.messages_frame, bg='#f0f2f5')
        self.scrollbar = ttk.Scrollbar(self.messages_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=580)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Question type and button frame
        input_frame = ttk.Frame(self.chat_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Question Type Selection
        self.question_type = tk.StringVar(value=QuestionType.SCIENCE.value)
        type_frame = ttk.LabelFrame(input_frame, text="ประเภทคำถาม", padding=5)
        type_frame.pack(fill=tk.X, pady=(0, 5))
        
        for qt in QuestionType:
            ttk.Radiobutton(
                type_frame,
                text=qt.value,
                value=qt.value,
                variable=self.question_type
            ).pack(side=tk.LEFT, padx=5)
        
        # generate button styled as modern button
        style = ttk.Style()
        style.configure("Modern.TButton", 
                       padding=10, 
                       font=('TkDefaultFont', 10, 'bold'))
        
        self.generate_button = ttk.Button(
            input_frame,
            text="สุ่มคำถาม",
            style="Modern.TButton",
            command=lambda: self.on_generate_click()
        )
        self.generate_button.pack(fill=tk.X, pady=5)
        
        # stats panel (right side)
        stats_panel = ttk.LabelFrame(self.main_container, text="สถิติและอารมณ์", padding=10)
        stats_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # current emotion display
        self.emotion_var = tk.StringVar(value="อารมณ์ปัจจุบัน: 100%")
        emotion_label = ttk.Label(
            stats_panel,
            textvariable=self.emotion_var,
            font=("TkDefaultFont", 12, "bold")
        )
        emotion_label.pack(pady=(0, 10))
        
        # STATISTICS!
        self.stats_vars = {
            'overall': tk.StringVar(value="เฉลี่ยรวม: 0%"),
            QuestionType.SCIENCE.value: tk.StringVar(value=f"{QuestionType.SCIENCE.value}: 0%"),
            QuestionType.GENERAL.value: tk.StringVar(value=f"{QuestionType.GENERAL.value}: 0%"),
            QuestionType.EMOTIONAL.value: tk.StringVar(value=f"{QuestionType.EMOTIONAL.value}: 0%")
        }
        
        for var in self.stats_vars.values():
            ttk.Label(
                stats_panel,
                textvariable=var,
                font=("TkDefaultFont", 10)
            ).pack(pady=2)
            
    def create_message_bubble(self, message: str, is_bot: bool = True):
        # Message frame
        message_frame = ttk.Frame(self.scrollable_frame)
        message_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Profile picture (placeholder)
        profile_frame = ttk.Frame(message_frame)
        profile_frame.pack(side=tk.LEFT if is_bot else tk.RIGHT, padx=5)
        
        profile_label = ttk.Label(
            profile_frame,
            text="🤖" if is_bot else "👤",
            font=("TkDefaultFont", 20)
        )
        profile_label.pack()
        
        # Msg bubble
        bubble_style = {
            'bg': '#e4e6eb' if is_bot else '#0084ff',
            'fg': 'black' if is_bot else 'white'
        }
        
        bubble = tk.Label(
            message_frame,
            text=message,
            wraplength=400,
            justify=tk.LEFT,
            padx=10,
            pady=8,
            **bubble_style
        )
        bubble.pack(side=tk.LEFT if is_bot else tk.RIGHT)
        
        # Timestamp
        time_label = ttk.Label(
            message_frame,
            text=datetime.now().strftime("%H:%M"),
            font=("TkDefaultFont", 8)
        )
        time_label.pack(side=tk.LEFT if is_bot else tk.RIGHT, padx=5)
        
        # scroll to bottom
        self.canvas.yview_moveto(1)
        
    def set_generate_callback(self, callback: Callable[[], None]):
        self.generate_callback = callback
    
    def on_generate_click(self):
        if hasattr(self, 'generate_callback'):
            self.generate_callback()
    
    def update_response(self, question: str, answer: str, emotion: float):
        # user "question" (random generation)
        self.create_message_bubble(f": สุ่มคำถาม{self.question_type.get()} :", is_bot=False)
        # question
        self.create_message_bubble(question, is_bot=False)
        # bot response
        self.create_message_bubble(answer, is_bot=True)
        self.create_message_bubble(f"ระดับอารมณ์ที่ได้: {emotion:.1f}%", is_bot=True)
        # update emotion
        self.emotion_var.set(f"อารมณ์ปัจจุบัน: {emotion:.1f}%")
        # **Scrollbar ให้เลื่อนลงอัตโนมัติ** หลังจาก gen chat เสร็จอีกที
        self.root.update_idletasks()  # อัปเดต UI
        self.canvas.yview_moveto(1)   # เลื่อน Scrollbar ไปด้านล่างสุด
    
    def update_stats(self, stats: dict):
        """Update ค่าเฉลี่ยนรวมจากทั้ง 3 genre"""
        self.stats_vars['overall'].set(
            f"เฉลี่ยรวม: {stats['overall']:.1f}%"
        )
        for qt in QuestionType:
            self.stats_vars[qt.value].set(
                f"{qt.value}: {stats[qt.value]:.1f}%"
            )
    
    def get_selected_type(self) -> QuestionType:
        return QuestionType(self.question_type.get())
