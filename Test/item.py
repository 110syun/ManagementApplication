class Item:
    def __init__(self, name, category="未分類", active_time=0):
        self.name = name
        self.category = category
        self.active_time = active_time

    def __str__(self):
        return self.name