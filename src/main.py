import threading
import atexit
import json
from watcher import Watcher

def cleanup(watcher):
    data = [category.to_dict() for category in watcher.categories]
    with open("categories.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    try:
        with open("categories.json", "r", encoding="utf-8") as f:
            categories_data = json.load(f)
    except FileNotFoundError:
        categories_data = None

    watcher = Watcher(categories_data)
    atexit.register(cleanup, watcher)
    threading.Thread(target=watcher.openGUI, daemon=True).start()
    watcher.update_window_name()

if __name__ == "__main__":
    main()