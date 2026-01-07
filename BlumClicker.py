import pygetwindow as gw
import cv2
import numpy as np
from PIL import ImageGrab
import keyboard
import time
import ctypes
from threading import Thread

user32 = ctypes.windll.user32
mouse_event = user32.mouse_event
SW_RESTORE = 9
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

def restore_window(hwnd):
    user32.ShowWindow(hwnd, SW_RESTORE)


window_title = "TelegramDesktop"
windows = gw.getWindowsWithTitle(window_title)

if not windows:
    print("Окно не найдено")
else:
    window = windows[0]
    
    # Определение цвета, который мы ищем
    target_color = np.array([0, 234, 197])  # BGR формат
    
    running = False

    def toggle_running():
        global running
        running = not running
        if running:
            print("Скрипт включен")
        else:
            print("Скрипт выключен")

    keyboard.add_hotkey('p', toggle_running)
    
    print("Нажмите 'p' для включения/выключения скрипта")

    def click(x, y):
        ctypes.windll.user32.SetCursorPos(x, y)

        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def main_loop():
        global running
        while True:
            if running:
                try:

                    window.activate()

                    left, top, right, bottom = window.left, window.top, window.right, window.bottom

                    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
                    
                    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                    mask = cv2.inRange(image, target_color, target_color)

                    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    for contour in contours:
                        x, y, w, h = cv2.boundingRect(contour)
                        center_x = left + x + w // 2
                        center_y = top + y + h // 2

                        click(center_x, center_y)

                except Exception as e:
                    print(f"Произошла ошибка: {e}")
                    running = False
            else:
                time.sleep(0.01)

    main_thread = Thread(target=main_loop)
    main_thread.start()

