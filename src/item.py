class Item:
    def __init__(self, name, active_time=0):
        self.name = name
        self.active_time = active_time

    def to_dict(self):
        return {
            "name": self.name,
            "active_time": self.active_time
        }