import tkinter as tk
import threading
import time
import win32process
import win32gui
import wmi
from collections import defaultdict
from Item import Item
from dragAndDrop import DragAndDropApp

c = wmi.WMI()

active_window_times = defaultdict(float)
items = {}
previous_window = None
previous_time = time.time()
app = None

def get_app_name(hwnd):
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in c.query(f'SELECT Name FROM Win32_Process WHERE ProcessId = {str(pid)}'):
            exe = p.Name
            break
    except Exception as e:
        print(f"Exception: {e}")
        return None
    else:
        return exe

def update_window_name():
    global previous_window, previous_time
    while True:
        hwnd = win32gui.GetForegroundWindow()
        current_time = time.time()
        window_name = get_app_name(hwnd)
        if window_name:
            if previous_window:
                active_window_times[previous_window] += current_time - previous_time
                if previous_window in items:
                    items[previous_window].active_time += current_time - previous_time
                else:
                    items[previous_window] = Item(name=previous_window, active_time=current_time - previous_time)
            previous_window = window_name
            previous_time = current_time
        time.sleep(1)

def update_label(label):
    while True:
        if previous_window:
            label.config(text=f"アクティブウィンドウのアプリケーション名: {previous_window}")
        else:
            label.config(text="アクティブウィンドウが見つかりませんでした。")
        time.sleep(1)

def show_window_times():
    window_times = "\n".join([f"{item.name}: {item.active_time:.2f}秒" for item in items.values()])
    popup = tk.Toplevel()
    popup.title("ウィンドウアクティブ時間")
    tk.Label(popup, text=window_times, padx=20, pady=20).pack()

def create_window():
    root = tk.Tk()
    root.title("アクティブウィンドウ表示")
    label = tk.Label(root, text="アクティブウィンドウのアプリケーション名を取得中...", padx=20, pady=20)
    label.pack()
    button = tk.Button(root, text="ウィンドウアクティブ時間を表示", command=show_window_times)
    button.pack()
    threading.Thread(target=update_label, args=(label,), daemon=True).start()
    root.mainloop()

def open_drag_and_drop_app():
    root = tk.Tk()
    app_items = list(items.values())
    app = DragAndDropApp(root, app_items)
    root.mainloop()

if __name__ == "__main__":
    threading.Thread(target=create_window, daemon=True).start()
    threading.Thread(target=open_drag_and_drop_app, daemon=True).start()
    update_window_name()