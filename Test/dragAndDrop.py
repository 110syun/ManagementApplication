import tkinter as tk
from tkinter import ttk
from Item import Item

class DragAndDropApp:
    def __init__(self, root, items):
        self.root = root
        self.root.title("ドラッグ＆ドロップでジャンル分け")

        self.items = items
        self.categories = ["仕事,勉強", "休憩", "趣味A", "趣味B", "その他"]

        self.create_widgets()

    def create_widgets(self):
        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        for item in self.items:
            self.listbox.insert(tk.END, item.name)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.category_frames = {}
        for category in self.categories:
            frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            label = tk.Label(frame, text=category)
            label.pack()
            listbox = tk.Listbox(frame)
            listbox.pack(fill=tk.BOTH, expand=True)
            self.category_frames[category] = listbox

        self.listbox.bind("<B1-Motion>", self.on_drag)
        self.listbox.bind("<ButtonRelease-1>", self.on_drop)

    def on_drag(self, event):
        widget = event.widget
        index = widget.nearest(event.y)
        self.drag_data = self.items[index]

    def on_drop(self, event):
        widget = event.widget
        if widget != self.listbox:
            category = widget.master.winfo_children()[0].cget("text")
            self.category_frames[category].insert(tk.END, self.drag_data.name)
            self.items.remove(self.drag_data)
            self.drag_data.category = category
            self.listbox.delete(self.listbox.nearest(event.y))

    def update_items(self):
        self.listbox.delete(0, tk.END)
        for item in self.items:
            self.listbox.insert(tk.END, item.name)

if __name__ == "__main__":
    root = tk.Tk()
    items = [Item("test1"), Item("test2"), Item("test3"), Item("test4"), Item("test5")]
    app = DragAndDropApp(root, items)
    root.mainloop()