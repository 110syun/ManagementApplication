import tkinter as tk
import threading
import time
import win32process
import win32gui
import wmi
import os
from item import Item
from category import Category
from dnd_listbox import DragDropListbox

class Watcher:
    def __init__(self, categories_data=None, timestamps=None):
        self.c = wmi.WMI()        
        self.categories = []
        self.listbox_dict = {}
        self.previous_window = None
        self.previous_category = None
        self.lock = threading.Lock()  # ロックを追加
        self.running = True
        self.timestamps = timestamps if timestamps else []  # タイムスタンプのリストを追加

        if categories_data:
            for category_data in categories_data:
                category = Category(name=category_data["name"])
                for item_data in category_data["items"]:
                    item = Item(name=item_data["name"], active_time=item_data["active_time"])
                    category.add_item(item)
                self.categories.append(category)
        else:
            self.categories.append(Category(name="未分類"))

    def get_app_name(self, hwnd):
        exe = None  # ここで初期化
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            for p in self.c.query(f'SELECT Name FROM Win32_Process WHERE ProcessId = {str(pid)}'):
                exe = p.Name
                break
        except Exception as e:
            print(f"Exception: {e}")
        return exe

    def item_exists(self, elapsed_time):
        with self.lock:  # ロックを取得
            for category in self.categories:
                for item in category.items:
                    if self.previous_window == item.name:
                        item.active_time += elapsed_time
                        return
            self.categories[0].add_item(Item(name=self.previous_window, active_time=elapsed_time))
            self.update_listbox(False)
            return

    def update_listbox(self, all):
        if all:
            for category_index, listbox in self.listbox_dict.items():
                listbox.delete(0, tk.END)
                for item in self.categories[category_index].items:
                    listbox.insert(tk.END, f"{item.name}")
        else:
            listbox = self.listbox_dict[0]
            listbox.delete(0, tk.END)
            for item in self.categories[0].items:
                listbox.insert(tk.END, f"{item.name}")

    def get_listbox_at(self, event):
        for listbox in self.listbox_dict.values():
            x1, y1, x2, y2 = listbox.winfo_rootx(), listbox.winfo_rooty(), listbox.winfo_rootx() + listbox.winfo_width(), listbox.winfo_rooty() + listbox.winfo_height()
            if x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2:
                return listbox
        return None

    def update_window_name(self):
        previous_time = time.time()
        while self.running:
            hwnd = win32gui.GetForegroundWindow()
            current_time = time.time()
            elapsed_time = current_time - previous_time
            window_name = self.get_app_name(hwnd)
            if window_name:
                if self.previous_window:
                    self.item_exists(elapsed_time)
                    if self.previous_window == window_name:
                        # 最後のタイムスタンプのendの値を更新
                        if self.timestamps:
                            self.timestamps[-1]["end"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                    else:
                        # 新しいタイムスタンプを追加
                        self.previous_window = window_name
                        for category in self.categories:
                            for item in category.items:
                                if item.name == self.previous_window:
                                    self.previous_category = category
                        self.timestamps.append({
                            "app": self.previous_window,
                            "category": self.previous_category.name if self.previous_category else "未分類",
                            "start": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(previous_time)),
                            "end": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                        })
                else:
                    # 初回のタイムスタンプを追加
                    self.previous_window = window_name
                    for category in self.categories:
                        for item in category.items:
                            if item.name == self.previous_window:
                                self.previous_category = category
                    self.timestamps.append({
                        "app": self.previous_window,
                        "category": self.previous_category.name if self.previous_category else "未分類",
                        "start": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(previous_time)),
                        "end": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                    })
                previous_time = current_time
            time.sleep(1)

    def openGUI(self):
        root = tk.Tk()
        root.title("Window Management")

        def on_closing():
            self.running = False
            root.quit()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        def rename_category(label, category_index):
            entry = tk.Entry(root)
            entry.insert(0, label.cget("text"))
            entry.pack()
            entry.focus_set()

            def save_name(event):
                new_name = entry.get()
                label.config(text=new_name)
                self.categories[category_index].name = new_name
                entry.destroy()

            entry.bind("<Return>", save_name)

        def create_category_frame(category_index, category):
            frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            label = tk.Label(frame, text=category.name)
            label.pack()
            label.bind("<Double-Button-1>", lambda event, lbl=label: rename_category(lbl, category_index))
            listbox = DragDropListbox(frame, self, category)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.listbox_dict[category_index] = listbox
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)
            self.update_listbox(all)

        def create_category():
            new_category = "名前の無いカテゴリ"
            self.categories.append(Category(name=new_category))
            create_category_frame(len(self.categories) - 1, self.categories[-1])

        def create_widgets():
            for index, category in enumerate(self.categories):
                create_category_frame(index, category)

            create_category_button = tk.Button(root, text="カテゴリ作成", command=create_category)
            create_category_button.pack(side=tk.BOTTOM)

        create_widgets()
        root.mainloop()