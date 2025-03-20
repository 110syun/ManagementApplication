import tkinter as tk
from tkinter import ttk

class DragDropListbox(tk.Listbox):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app  # アプリケーションの参照
        self.bind("<ButtonPress-1>", self.prepare_drag)
        self.bind("<B1-Motion>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag, add=True)
        self.bind("<ButtonRelease-1>", self.drop_item)
        self.drag_data = {"index": None, "text": None, "started": False}
        self.drag_label = None  # ドラッグ中のラベル用
    
    def prepare_drag(self, event):
        """ドラッグ準備（クリック時）"""
        index = self.nearest(event.y)
        if index >= 0:
            self.drag_data["index"] = index
            self.drag_data["text"] = self.get(index)
            self.drag_data["started"] = False  # まだドラッグ開始していない
            self.app.drag_source = self  # ドラッグ元を記録
    
    def start_drag(self, event):
        """ドラッグ開始（マウスを動かした瞬間）"""
        if not self.drag_data["started"] and self.drag_data["text"]:
            self.delete(self.drag_data["index"])
            self.drag_data["started"] = True
            
            # ドラッグ用ラベル作成
            self.drag_label = tk.Toplevel(self)
            self.drag_label.overrideredirect(True)
            self.drag_label.attributes("-alpha", 0.7)  # 半透明
            label = tk.Label(self.drag_label, text=self.drag_data["text"], bg="lightgray", relief=tk.SOLID)
            label.pack()
            self.update_drag_label(event)
    
    def do_drag(self, event):
        """ドラッグ中の処理（マウス追従）"""
        if self.drag_label:
            self.update_drag_label(event)
        self.event_generate("<<ListboxSelect>>")  # 選択状態を更新

    def update_drag_label(self, event):
        """ドラッグ中のラベルの位置を更新"""
        x = self.winfo_rootx() + event.x + 10
        y = self.winfo_rooty() + event.y + 10
        self.drag_label.geometry(f"+{x}+{y}")

    def drop_item(self, event):
        """ドロップ処理"""
        if self.drag_data["started"]:
            target_listbox = self.app.get_listbox_at(event)
            if target_listbox:
                target_listbox.insert(tk.END, self.drag_data["text"])  # 他のリストボックスに挿入
            else:
                self.insert(tk.END, self.drag_data["text"])  # 元のリストに戻す
            self.drag_data = {"index": None, "text": None, "started": False}  # リセット

            # ドラッグ用ラベルを削除
            if self.drag_label:
                self.drag_label.destroy()
                self.drag_label = None

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("動的フレーム作成とドラッグ＆ドロップ")
        self.geometry("400x500")
        
        self.frame_container = tk.Frame(self)
        self.frame_container.pack(fill=tk.BOTH, expand=True)

        self.add_frame_button = ttk.Button(self, text="フレーム追加", command=self.add_frame)
        self.add_frame_button.pack(pady=10)
        
        self.listboxes = []  # すべてのListboxを格納
        self.drag_source = None  # ドラッグ元のListbox

    def add_frame(self):
        """新しいフレームを作成"""
        frame = tk.Frame(self.frame_container, relief=tk.RAISED, borderwidth=2)
        frame.pack(pady=5, fill=tk.X)

        listbox = DragDropListbox(frame, self, selectmode=tk.SINGLE, height=5)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)

        self.listboxes.append(listbox)

        # ダミーアイテムを追加
        for i in range(5):
            listbox.insert(tk.END, f"Item {i+1}")
    
    def get_listbox_at(self, event):
        """マウス位置にあるListboxを取得"""
        for listbox in self.listboxes:
            x1, y1, x2, y2 = listbox.winfo_rootx(), listbox.winfo_rooty(), listbox.winfo_rootx() + listbox.winfo_width(), listbox.winfo_rooty() + listbox.winfo_height()
            if x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2:
                return listbox
        return None

if __name__ == "__main__":
    app = App()
    app.mainloop()
