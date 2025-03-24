from item import Item

class Category:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item):
        if isinstance(item, Item):
            self.items.append(item)

    def total_active_time(self):
        return sum(item.active_time for item in self.items)

    def change_name(self, new_name):
        self.name = new_name