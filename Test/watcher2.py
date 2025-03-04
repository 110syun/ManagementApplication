import win32process
import win32gui
import wmi
from time import sleep

c = wmi.WMI()

def get_app_path(hwnd):
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in c.query(f'SELECT ExecutablePath FROM Win32_Process WHERE ProcessId = {str(pid)}'):
            exe = p.ExecutablePath
            break
    except:
        return None
    else:
        return exe


def get_app_name(hwnd):
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in c.query(f'SELECT Name FROM Win32_Process WHERE ProcessId = {str(pid)}'):
            exe = p.Name
            break
    except:
        return None
    else:
        return exe
    
    
print("\n1秒ごとにアクティブなアプリケーションのパスと名前を表示します。\n")
while(True):
    hwnd = win32gui.GetForegroundWindow()
    print(get_app_path(hwnd))
    print(get_app_name(hwnd))
    sleep(1)