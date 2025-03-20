import tkinter as tk
import threading
import time
import win32process
import win32gui
import wmi
from collections import defaultdict
from item import Item
from category import Category

class Watcher:
    def __init__(self):
        self.c = wmi.WMI()        
        self.categories = []
        self.listbox_dict = {}
        
        self.categories.append(Category(name="未分類"))

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

    def item_exists(self, previous_window, elapsed_time):
        for category in self.categories:
            for item in category.items:
                if previous_window == item.name:
                    item.active_time += elapsed_time
                    return
        self.categories[0].add_item(Item(name=previous_window, active_time=elapsed_time))
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

    def update_window_name(self):
        previous_time = time.time()
        previous_window = None
        while True:
            hwnd = win32gui.GetForegroundWindow()
            current_time = time.time()
            elapsed_time = current_time - previous_time
            window_name = self.get_app_name(hwnd)
            if window_name:
                if previous_window:
                    self.item_exists(previous_window, elapsed_time)
                previous_window = window_name
                previous_time = current_time
            for category in self.categories:
                print(f"Category: {category.name}")
                for item in category.items:
                    print(f"Item: {item.name}, Active Time: {item.active_time}")
            time.sleep(1)
            
    def openGUI(self):
        root = tk.Tk()
        root.title("Window Management")

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
            listbox = tk.Listbox(frame)
            listbox.pack(fill=tk.BOTH, expand=True)
            self.listbox_dict[category_index] = listbox
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

def main():
    watcher = Watcher()
    threading.Thread(target=watcher.openGUI, daemon=True).start()
    watcher.update_window_name()

if __name__ == "__main__":
    main()