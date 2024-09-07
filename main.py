import cv2
import pyautogui
import numpy as np
import time

# 設定檢查的間隔時間（秒）
CHECK_INTERVAL = 5

# 加載待匹配的按鈕圖片
toss_btn_path = './imgs/toss.png'
toss_btn = cv2.imread(toss_btn_path, cv2.IMREAD_GRAYSCALE)

quit_btn_path = './imgs/quit.png'
quit_btn = cv2.imread(quit_btn_path, cv2.IMREAD_GRAYSCALE)

button_priority = [quit_btn, toss_btn]

def find_button(screen, button):
    result = cv2.matchTemplate(screen, button, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        button_x = pt[0] + button.shape[1] // 2
        button_y = pt[1] + button.shape[0] // 2
        return button_x, button_y
    print(f"{time.time()}: Button not found.")
    return None, None

def click_button(button_x, button_y):
    pyautogui.click(button_x, button_y)
    print(f"{time.time()}: Clicked.")

if __name__ == '__main__':
  while True:
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
  
    for button in button_priority:
      button_x, button_y = find_button(screenshot_gray, button)
      if button_x is not None and button_y is not None:
        click_button(button_x, button_y)
        continue

    time.sleep(CHECK_INTERVAL)