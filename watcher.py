import tkinter as tk
import threading
import time
import pygetwindow as gw
from collections import defaultdict

active_window_times = defaultdict(float)
previous_window = None
previous_time = time.time()

def get_active_window_name():
    try:
        result = gw.getActiveWindow()
        title = result.title
        if title:
            return title
        else:
            return None
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

def update_window_name(label):
    global previous_window, previous_time
    while True:
        current_time = time.time()
        window_name = get_active_window_name()
        if window_name:
            if previous_window:
                active_window_times[previous_window] += current_time - previous_time
            previous_window = window_name
            previous_time = current_time
            label.config(text=f"アクティブウィンドウのアプリケーション名: {window_name}")
        else:
            label.config(text="アクティブウィンドウが見つかりませんでした。")
        time.sleep(1)

def show_window_times():
    window_times = "\n".join([f"{window}: {time:.2f}秒" for window, time in active_window_times.items()])
    popup = tk.Toplevel()
    popup.title("ウィンドウアクティブ時間")
    tk.Label(popup, text=window_times, padx=20, pady=20).pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("アクティブウィンドウ表示")
    label = tk.Label(root, text="アクティブウィンドウのアプリケーション名を取得中...", padx=20, pady=20)
    label.pack()

    thread = threading.Thread(target=update_window_name, args=(label,))
    thread.daemon = True
    thread.start()

    button = tk.Button(root, text="ウィンドウアクティブ時間を表示", command=show_window_times)
    button.pack()

    root.mainloop()