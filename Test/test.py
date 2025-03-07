import tkinter as tk

class DraggableRectangle:
    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.item = canvas.create_rectangle(x, y, x+width, y+height, fill=color)
        self.canvas.tag_bind(self.item, '<Button-1>', self.on_press)
        self.canvas.tag_bind(self.item, '<B1-Motion>', self.on_drag)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.item, dx, dy)
        self.start_x = event.x
        self.start_y = event.y

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

rectangle = DraggableRectangle(canvas, 50, 50, 100, 80, 'red')

root.mainloop()
