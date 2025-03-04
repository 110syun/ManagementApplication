import pygetwindow as gw

win = gw.getActiveWindow()
if win:
    print(win.title)
else:
    print("No active window")