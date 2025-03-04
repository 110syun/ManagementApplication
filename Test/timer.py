import tkinter as tk
from tkinter import messagebox
import threading
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer Application")

        self.timer_a_duration = tk.IntVar(value=5)
        self.timer_b_duration = tk.IntVar(value=5)
        self.timer_a_count = tk.IntVar(value=0)
        self.timer_b_count = tk.IntVar(value=0)

        self.create_widgets()
        self.running = False

    def create_widgets(self):
        tk.Label(self.root, text="Timer A Duration (seconds):").pack()
        tk.Entry(self.root, textvariable=self.timer_a_duration).pack()

        tk.Label(self.root, text="Timer B Duration (seconds):").pack()
        tk.Entry(self.root, textvariable=self.timer_b_duration).pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_timers)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_timers)
        self.stop_button.pack()

        tk.Label(self.root, text="Timer A Count:").pack()
        tk.Label(self.root, textvariable=self.timer_a_count).pack()

        tk.Label(self.root, text="Timer B Count:").pack()
        tk.Label(self.root, textvariable=self.timer_b_count).pack()

    def start_timers(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            threading.Thread(target=self.run_timer_a).start()

    def stop_timers(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def run_timer_a(self):
        while self.running:
            time.sleep(self.timer_a_duration.get())
            self.timer_a_count.set(self.timer_a_count.get() + 1)
            messagebox.showinfo("Timer A", "Timer A has finished!")
            if self.running:
                threading.Thread(target=self.run_timer_b).start()
                break

    def run_timer_b(self):
        while self.running:
            time.sleep(self.timer_b_duration.get())
            self.timer_b_count.set(self.timer_b_count.get() + 1)
            messagebox.showinfo("Timer B", "Timer B has finished!")
            if self.running:
                threading.Thread(target=self.run_timer_a).start()
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()