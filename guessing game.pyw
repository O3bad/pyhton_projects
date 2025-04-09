import tkinter as tk
from tkinter import messagebox

# Quiz data
sequences = [
    ("1 | ? | 2 | 3 | 5", 1),
    ("2 | 4 | ? | 16 | 32", 8),
    ("7 | 20 | 47 | 97 | ?", 167),
    ("205 | 163 | 121 | ? | 37", 79),
    ("2 | 3 | 5 | ? | 17", 11),
    ("1 | 4 | 9 | ? | 25", 16),
    ("2 | 6 | 12 | 20 | ?", 30),
    ("81 | 27 | 9 | ? | 1", 3),
    ("1 | 2 | 6 | 24 | ?", 120),
    ("3 | 5 | 9 | 17 | ?", 33)
]

class MathQuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Missing Number Quiz - Kids Edition! | ❤️ Lives: 5")
        self.root.geometry("800x600")
        self.root.configure(bg="#a8d8ea")
        
        # Game state
        self.current = 0
        self.points = 0
        self.lives = 5
        self.user_answers = []
        self.wrong_answers = []  # Store wrong answers with question info
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg="#a8d8ea", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Draw background
        self.draw_background()
        
        # Create UI elements
        self.create_widgets()
        
        # Start first question
        self.show_question(0)
    
    def draw_background(self):
        # Main game area
        self.canvas.create_rectangle(100, 80, 700, 520, fill="white", outline="#2b5f75", width=3)
        
        # Draw a robot mascot
        self.draw_robot(650, 50)
        
        # Decorative elements
        for i in range(0, 800, 50):
            self.canvas.create_line(i, 0, i, 600, fill="#d4f1f9", width=1)
        for i in range(0, 600, 50):
            self.canvas.create_line(0, i, 800, i, fill="#d4f1f9", width=1)
    
    def draw_robot(self, x, y):
        # Robot head
        self.canvas.create_rectangle(x, y, x+100, y+120, fill="#4CAF50", outline="#2b5f75", width=2)
        
        # Eyes
        self.canvas.create_oval(x+20, y+20, x+40, y+40, fill="white", outline="#2b5f75", width=2)
        self.canvas.create_oval(x+60, y+20, x+80, y+40, fill="white", outline="#2b5f75", width=2)
        
        # Mouth
        for i in range(3):
            self.canvas.create_rectangle(x+25+(i*15), y+70, x+35+(i*15), y+80, fill="#f44336", outline="")
        
        # Antenna
        self.canvas.create_line(x+50, y, x+50, y-20, fill="#FFC107", width=3)
        self.canvas.create_oval(x+40, y-30, x+60, y-10, fill="#FFC107", outline="")
    
    def create_widgets(self):
        # Main frame
        self.content_frame = tk.Frame(self.canvas, bg="white")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center", width=550, height=400)
        
        # Title
        self.title_label = tk.Label(
            self.content_frame,
            text="Can You Find the\nMissing Number?",
            font=("Comic Sans MS", 28, "bold"),
            bg="white", fg="#2b5f75",
            justify="center"
        )
        self.title_label.pack(pady=20)
        
        # Question
        self.question_label = tk.Label(
            self.content_frame,
            text="",
            font=("Comic Sans MS", 24),
            bg="white", fg="#3a3a3a"
        )
        self.question_label.pack(pady=10)
        
        # Answer entry
        self.entry = tk.Entry(
            self.content_frame,
            font=("Comic Sans MS", 20),
            justify="center",
            bg="white",
            width=15,
            bd=3,
            relief="ridge"
        )
        self.entry.pack(pady=15)
        self.entry.bind('<Return>', lambda e: self.check_answer())
        
        # Submit button
        self.submit_button = tk.Button(
            self.content_frame,
            text="Submit ➤",
            font=("Comic Sans MS", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=30,
            pady=10,
            command=self.check_answer
        )
        self.submit_button.pack(pady=10)
    
    def show_question(self, index):
        self.question_label.config(text=f"Sequence {index + 1}:\n{sequences[index][0]}")
        self.entry.focus()
    
    def check_answer(self):
        user_input = self.entry.get()
        
        if not user_input.isdigit():
            messagebox.showwarning("Oops!", "Please enter a number!")
            return
        
        user_input = int(user_input)
        question_text = sequences[self.current][0]
        correct_answer = sequences[self.current][1]
        
        if user_input == correct_answer:
            self.points += 1
            self.current += 1
            self.entry.delete(0, tk.END)
            
            if self.current >= len(sequences):
                self.show_result()
            else:
                self.show_question(self.current)
        else:
            self.lives -= 1
            # Store wrong answer details
            self.wrong_answers.append({
                "question": question_text,
                "user_answer": user_input,
                "correct_answer": correct_answer,
                "question_num": self.current + 1
            })
            
            self.root.title(f"Missing Number Quiz - Kids Edition! | ❤️ Lives: {self.lives}")
            if self.lives <= 0:
                messagebox.showerror("Game Over!", "💔 You ran out of lives!")
                self.show_result()
            else:
                messagebox.showerror("Wrong!", f"Try again! ❤️ Lives left: {self.lives}")
                self.entry.delete(0, tk.END)
                self.entry.focus()
    
    def show_result(self):
        result_msg = f"Your score: {self.points}/{len(sequences)}\n"
        if self.points >= 8:
            result_msg += "🎉 You're a math genius!"
        elif self.points >= 5:
            result_msg += "👍 Good job! Keep practicing!"
        else:
            result_msg += "💡 Don't worry! Math gets easier with practice!"
        
        # Add wrong answers details
        if self.wrong_answers:
            result_msg += "\n\nHere's what you missed:\n"
            for wrong in self.wrong_answers:
                result_msg += (f"\n❌ Question {wrong['question_num']}: {wrong['question']}\n"
                             f"   Your answer: {wrong['user_answer']}\n"
                             f"   Correct answer: {wrong['correct_answer']}\n")
        
        messagebox.showinfo("Game Over!", result_msg)
        self.root.destroy()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = MathQuizGame(root)
    root.mainloop()