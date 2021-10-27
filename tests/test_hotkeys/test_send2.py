import time

import pyautogui

start = time.time()
pyautogui.hotkey(['control', 'v'])
print(f'pyautogui took {time.time() - start} secs.')

