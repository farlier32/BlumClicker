import pygetwindow as gw
import cv2
import numpy as np
from PIL import ImageGrab
import keyboard
import time
import ctypes
from threading import Thread

# Определения для ctypes
user32 = ctypes.windll.user32
mouse_event = user32.mouse_event
SW_RESTORE = 9
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

def restore_window(hwnd):
    user32.ShowWindow(hwnd, SW_RESTORE)

# Найти окно приложения по его заголовку (пример: "Untitled - Notepad")
window_title = "TelegramDesktop"  # Замените на заголовок вашего окна
windows = gw.getWindowsWithTitle(window_title)

if not windows:
    print("Окно не найдено")
else:
    window = windows[0]
    
    # Определение цвета, который мы ищем
    target_color = np.array([0, 234, 197])  # BGR формат
    
    # Переменная для включения/выключения скрипта
    running = False

    def toggle_running():
        global running
        running = not running
        if running:
            print("Скрипт включен")
        else:
            print("Скрипт выключен")

    # Привязка клавиш к функциям включения и выключения скрипта
    keyboard.add_hotkey('p', toggle_running)
    
    print("Нажмите 'p' для включения/выключения скрипта")

    def click(x, y):
        # Переместить курсор мыши
        ctypes.windll.user32.SetCursorPos(x, y)
        # Симулировать нажатие и отпускание левой кнопки мыши
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def main_loop():
        global running
        while True:
            if running:
                try:
                    # Активировать окно
                    window.activate()

                    # Получить координаты окна
                    left, top, right, bottom = window.left, window.top, window.right, window.bottom

                    # Сделать скриншот области окна
                    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

                    # Преобразование скриншота в формат, понятный OpenCV
                    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                    # Создание маски для выделения нужного цвета
                    mask = cv2.inRange(image, target_color, target_color)

                    # Поиск контуров в маске
                    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    # Кликать по каждому найденному контуру
                    for contour in contours:
                        # Получение координат центра контура
                        x, y, w, h = cv2.boundingRect(contour)
                        center_x = left + x + w // 2
                        center_y = top + y + h // 2

                        # Перемещение курсора и клик
                        click(center_x, center_y)

                except Exception as e:
                    print(f"Произошла ошибка: {e}")
                    running = False
            else:
                # Если скрипт не запущен, небольшая пауза перед проверкой состояния
                time.sleep(0.01)

    # Запуск основного цикла в отдельном потоке
    main_thread = Thread(target=main_loop)
    main_thread.start()
