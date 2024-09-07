import asyncio
import cv2
import pyautogui
import numpy as np
import time
import os

# 設定檢查的間隔時間（秒）
CHECK_INTERVAL = 2

# 加載待匹配的按鈕圖片
toss_btn_path = './imgs/toss.png'
toss_btn = cv2.imread(toss_btn_path, cv2.IMREAD_GRAYSCALE)

quit_btn_path = './imgs/quit.png'
quit_btn = cv2.imread(quit_btn_path, cv2.IMREAD_GRAYSCALE)

option_btn_path = './imgs/option.png'
option_btn = cv2.imread(option_btn_path, cv2.IMREAD_GRAYSCALE)

enemy_btn_path = './imgs/enemy.png'
enemy_btn = cv2.imread(enemy_btn_path, cv2.IMREAD_GRAYSCALE)

self_btn_path = './imgs/self.png'
self_btn = cv2.imread(self_btn_path, cv2.IMREAD_GRAYSCALE)

use_btn_path = './imgs/use.png'
exec_card_btn = cv2.imread(use_btn_path, cv2.IMREAD_GRAYSCALE)

skip_btn_path = './imgs/skip.png'
skip_btn = cv2.imread(skip_btn_path, cv2.IMREAD_GRAYSCALE)

skip_confirm_btn_path = './imgs/skip_confirm.png'
skip_confirm_btn = cv2.imread(skip_confirm_btn_path, cv2.IMREAD_GRAYSCALE)

ready_battle_btn_path = './imgs/ready_battle.png'
ready_battle_btn = cv2.imread(ready_battle_btn_path, cv2.IMREAD_GRAYSCALE)

button_priority = [ready_battle_btn, option_btn, quit_btn, toss_btn, skip_confirm_btn, skip_btn]

def initCards(folder):
    cards = []
    for filename in os.listdir(folder):
      if filename.endswith('.png'):
          img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)
          if img is not None:
              cards.append(img)
    return cards

positive_effect_card = initCards('./imgs/positiveEffect');
positive_dice = initCards('./imgs/positiveDice');

negative_effect_card = initCards('./imgs/negativeEffect');
negative_dice_card = initCards('./imgs/negativeDice');

def click_enemy():
   click_button(*find_button(enemy_btn))

def click_self():
    click_button(*find_button(self_btn))

def click_use():
    x, y = find_button(exec_card_btn,  0.6)
    click_button(x, y)
    if (x is not None and y is not None):
        print(f"[use] clicked ")
        click_button(x, y)
        time.sleep(1)
    else:
        print(f"[use] not found ")


def exec_positive_effect():
    if (positive_effect_card is None):
        return
    for card in positive_effect_card:
        x, y = find_button(card, 0.8)
        if x is not None and y is not None:
            print(f"[positive effect] found ")
            click_button(x, y)
            # time.sleep(1)
            click_use();
            break

def exec_positive_dice():
    if (positive_dice is None):
        return
    for card in positive_dice:
        x, y = find_button(card)
        if x is not None and y is not None:
            print(f"[positive dice] found ")
            click_button(x, y)
            # time.sleep(1)
            click_self();

            break

def exec_negative_effect():
    if (negative_effect_card is None):
        return
    for card in negative_effect_card:
        x, y = find_button(card, 0.8)
        if x is not None and y is not None:
            print(f"[negative effect] found ")
            click_button(x, y)
            # time.sleep(1)
            click_enemy();
            break

def exec_negative_dice():
    if (negative_dice_card is None):
        return
    for card in negative_dice_card:
        x, y = find_button(card)
        if x is not None and y is not None:
            print(f"[negative dice] found ")
            click_button(x, y)
            # time.sleep(1)
            click_enemy();
            break

def find_button(button, threshold=0.6):
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, button, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        button_x = pt[0] + button.shape[1] // 2
        button_y = pt[1] + button.shape[0] // 2
        return button_x, button_y
    # current_time = time.strftime("%H:%M:%S", time.localtime())
    # print(f"{current_time}: Button not found.")
    return None, None

def click_button(button_x, button_y):
    pyautogui.click(button_x, button_y)
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"{current_time}: Clicked.")

if __name__ == '__main__':
  while True:
    os.system('cls')

    for cards in [exec_positive_effect, exec_positive_dice, exec_negative_dice, exec_negative_effect]:
        cards()
        time.sleep(1)
  
    for button in button_priority:
      button_x, button_y = find_button(button)
      if button_x is not None and button_y is not None:
        click_button(button_x, button_y)
        break

    

    time.sleep(CHECK_INTERVAL)