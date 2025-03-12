import tkinter as tk
import threading
import time
import win32process
import win32gui
import wmi
from collections import defaultdict
from item import Item

class Watcher:
    def __init__(self):
        self.active_window_times = defaultdict(float)
        self.items = {}
        self.previous_window = None
        self.previous_time = time.time()
        self.c = wmi.WMI()
        
        self.categories = {"未分類": []}
        self.category_frames = {}

    def get_app_name(self, hwnd):
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            for p in self.c.query(f'SELECT Name FROM Win32_Process WHERE ProcessId = {str(pid)}'):
                exe = p.Name
                break
        except Exception as e:
            print(f"Exception: {e}")
            return None
        else:
            return exe

    def update_window_name(self):
        while True:
            hwnd = win32gui.GetForegroundWindow()
            current_time = time.time()
            window_name = self.get_app_name(hwnd)
            if window_name:
                if self.previous_window:
                    self.active_window_times[self.previous_window] += current_time - self.previous_time
                    if self.previous_window in self.items:
                        self.items[self.previous_window].active_time += current_time - self.previous_time
                    else:
                        self.items[self.previous_window] = Item(name=self.previous_window, active_time=current_time - self.previous_time)
                self.previous_window = window_name
                self.previous_time = current_time
            time.sleep(1)
            
    def openGUI(self):
        root = tk.Tk()
        root.title("Window Management")

        def create_category():
            new_category = "名前の無いカテゴリ"
            self.categories[new_category] = []
            update_categories()

        def update_categories():
            for frame in self.category_frames.values():
                frame.destroy()
            self.category_frames.clear()

            for category, items in self.categories.items():
                frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
                frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                label = tk.Label(frame, text=category)
                label.pack()
                label.bind("<Double-1>", lambda e, cat=category: edit_category_name(e, cat))
                self.category_frames[category] = frame

                for item in items:
                    item_label = tk.Label(frame, text=item.name)
                    item_label.pack()
                    item_label.bind("<Button-1>", lambda e, itm=item: start_drag(e, itm))
                    item_label.bind("<ButtonRelease-1>", lambda e, itm=item: stop_drag(e, itm))

        def edit_category_name(event, category):
            label = event.widget
            entry = tk.Entry(root)
            entry.insert(0, category)
            entry.pack()
            entry.focus_set()

            def save_name(event):
                new_name = entry.get()
                if new_name:
                    self.categories[new_name] = self.categories.pop(category)
                    update_categories()
                entry.destroy()

            entry.bind("<Return>", save_name)

        def start_drag(event, item):
            event.widget.startX = event.x
            event.widget.startY = event.y

        def stop_drag(event, item):
            for category, frame in self.category_frames.items():
                if frame.winfo_containing(event.x_root, event.y_root):
                    self.categories[category].append(item)
                    for cat, items in self.categories.items():
                        if item in items and cat != category:
                            items.remove(item)
                    update_categories()
                    break

        create_category_button = tk.Button(root, text="カテゴリ作成ボタン", command=create_category)
        create_category_button.pack()

        update_categories()
        root.mainloop()

def main():
    watcher = Watcher()
    threading.Thread(target=watcher.openGUI, daemon=True).start()
    watcher.update_window_name()

if __name__ == "__main__":
    main()