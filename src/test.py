import tkinter as tk
from tkinter import messagebox
import re

class Scheduler:
    def __init__(self, app):
        if (app):
            self.homescreen = app
            self.watcher = self.homescreen.app

    def openGUI(self):
        root = tk.Tk()
        root.title("Time Scheduler")
        
        # ウィンドウ全体を管理するメインフレーム
        main_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ウィンドウを横に三分割するフレームを作成
        frame1 = tk.Frame(main_frame, bd=2, relief=tk.SUNKEN)
        frame2 = tk.Frame(main_frame, bd=2, relief=tk.SUNKEN)
        frame3 = tk.Frame(main_frame, bd=2, relief=tk.SUNKEN)

        # フレームをウィンドウに横に配置
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=(25, 5))
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=(25, 5))
        frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=(25, 5))

        # 各フレームの境目にEntryを配置
        entry1 = tk.Entry(main_frame)
        entry1.place(relx=0.33, y=2.5, anchor="n", width=60, height=20)  # frame1とframe2の境目

        entry2 = tk.Entry(main_frame)
        entry2.place(relx=0.66, y=2.5, anchor="n", width=60, height=20)  # frame2とframe3の境目

        root.mainloop()

if __name__ == "__main__":
    scheduler = Scheduler(None)
    scheduler.openGUI()