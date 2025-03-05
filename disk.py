import tkinter as tk
from tkinter import ttk, messagebox
import time

class NeonTypingChallenge:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Typing Challenge")
        self.root.configure(bg='#0a0812')
        
        self.levels = [
            {"text": "Hello world! Start your typing journey here.", "time": 30},
            {"text": "Practice makes perfect! Keep going!", "time": 25},
            {"text": "Focus on accuracy and speed together!", "time": 20},
            {"text": "Final challenge! Show your true skills!", "time": 15}
        ]
        
        self.current_level = 0
        self.start_time = 0
        self.correct_chars = 0
        self.total_chars = 0
        self.timer_id = None
        
        self.create_password_screen()
        
    def create_password_screen(self):
        self.password_frame = tk.Frame(self.root, bg='#0a0812')
        self.password_frame.pack(pady=50)
        
        try:
            logo_img = tk.PhotoImage(file='logo.png')
            logo_label = tk.Label(self.password_frame, image=logo_img, bg='#0a0812')
            logo_label.image = logo_img
            logo_label.pack()
        except Exception as e:
            print(f"Error loading image: {e}")

        tk.Label(self.password_frame, text="🔒 Unlock the Challenge", 
                font=('Courier New', 16), fg='#bc13fe', bg='#0a0812').pack(pady=10)
        
        self.password_entry = ttk.Entry(self.password_frame, width=20, show='*', 
                                      font=('Courier New', 12))
        self.password_entry.pack(pady=5)
        
        ttk.Button(self.password_frame, text="Unlock", command=self.check_password).pack(pady=10)
        self.password_error = tk.Label(self.password_frame, text="", fg='#ff4444', bg='#0a0812')
        self.password_error.pack()

    def create_main_interface(self):
        self.password_frame.destroy()
        
        main_frame = tk.Frame(self.root, bg='#0a0812')
        main_frame.pack(pady=20, padx=20)
        
        stats_frame = tk.Frame(main_frame, bg='#0a0812')
        stats_frame.pack()
        
        self.time_label = self.create_stat_box(stats_frame, "⏳ Time", "0")
        self.accuracy_label = self.create_stat_box(stats_frame, "🎯 Accuracy", "100%")
        self.wpm_label = self.create_stat_box(stats_frame, "⚡ WPM", "0")
        
        self.text_display = tk.Text(main_frame, height=6, width=50, wrap='word',
                                   font=('Courier New', 12), bg='#1a0d2e', fg='white',
                                   borderwidth=2, relief='solid')
        self.text_display.pack(pady=10)
        
        self.input_entry = ttk.Entry(main_frame, width=50, font=('Courier New', 12))
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<KeyRelease>', self.update_display)
        
        button_frame = tk.Frame(main_frame, bg='#0a0812')
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="🚀 Start", command=self.start_challenge).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔄 Restart", command=self.restart_challenge).pack(side='left', padx=5)
        
    def create_stat_box(self, parent, title, value):
        frame = tk.Frame(parent, bg='#1a0d2e', padx=10, pady=5, relief='solid', borderwidth=1)
        frame.pack(side='left', padx=10)
        
        tk.Label(frame, text=title, bg='#1a0d2e', fg='#bc13fe', 
                font=('Courier New', 10)).pack()
        label = tk.Label(frame, text=value, bg='#1a0d2e', fg='white',
                        font=('Courier New', 12, 'bold'))
        label.pack()
        return label

    def check_password(self):
        if self.password_entry.get() == "root@123":
            self.create_main_interface()
        else:
            self.password_error.config(text="Incorrect password! Try again.")

    def start_challenge(self):
        self.init_level()
        self.input_entry.focus()

    def init_level(self):
        self.start_time = time.time()
        level = self.levels[self.current_level]
        self.text_display.delete('1.0', 'end')
        self.text_display.insert('end', level['text'])
        self.start_timer(level['time'])

    def start_timer(self, seconds):
        self.time_left = seconds
        self.update_timer()

    def update_timer(self):
        if self.time_left >= 0:
            self.time_label.config(text=str(self.time_left))
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.check_result()

    def update_display(self, event):
        user_input = self.input_entry.get()
        target_text = self.levels[self.current_level]['text']
        
        self.text_display.tag_configure('correct', foreground='#bc13fe')
        self.text_display.tag_configure('wrong', foreground='#ff4444')
        
        self.text_display.delete('1.0', 'end')
        for i, char in enumerate(target_text):
            if i < len(user_input):
                tag = 'correct' if user_input[i] == char else 'wrong'
                self.text_display.insert('end', char, tag)
            else:
                self.text_display.insert('end', char)
        
        self.update_stats(user_input, target_text)

    def update_stats(self, input_text, target_text):
        self.total_chars = len(input_text)
        self.correct_chars = sum(
            1 for i, c in enumerate(input_text) 
            if i < len(target_text) and c == target_text[i]
        )
        
        time_elapsed = (time.time() - self.start_time) / 60
        if time_elapsed == 0:
            wpm = 0
        else:
            wpm = int((self.correct_chars / 5) / time_elapsed)
        self.wpm_label.config(text=str(wpm))
        
        if self.total_chars > 0:
            accuracy = int((self.correct_chars / self.total_chars) * 100)
        else:
            accuracy = 100
        self.accuracy_label.config(text=f"{accuracy}%")

    def check_result(self):
        user_input = self.input_entry.get()
        target_text = self.levels[self.current_level]['text']
        
        if user_input == target_text:
            if self.current_level < len(self.levels) - 1:
                self.current_level += 1
                self.start_challenge()
            else:
                messagebox.showinfo("Congratulations!", "🎉 You completed all levels!")
        else:
            messagebox.showwarning("Time's Up!", "❌ Try again! Better luck next time!")

    def restart_challenge(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.current_level = 0
        self.input_entry.delete(0, 'end')
        self.start_challenge()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeonTypingChallenge(root)
    root.mainloop()