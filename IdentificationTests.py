import logging
import os
import random
import sys

import cv2
from matplotlib import pyplot as plt


def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


icon = cv2.imread(resource_path('../AutoNovaGui/static/novaimgs/game_button/button_close2.png'), cv2.IMREAD_GRAYSCALE)

# logging.info("正在初始化...")
# window = gw.getWindowsWithTitle('Space Armada')
# window = window[0]
# window.maximize()  # 最大化窗口
# window.activate()  # 将窗口置顶
# pyautogui.hotkey('alt', 'enter')
# window_left, window_top, window_width, window_height = window.left, window.top, window.width, window.height
# time.sleep(5)
offset = 3


def get_coordinate(img, believe, no_click_zones=[]):
    # screenshot = pyautogui.screenshot(region=(window_left, window_top, window_width, window_height))
    # screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    screenshot = cv2.imread(resource_path("../AutoNovaGui/screenshot.png"), cv2.IMREAD_GRAYSCALE)
    # 遍历需要屏蔽的区域并填充为黑色
    if no_click_zones is not None:
        for zone in no_click_zones:
            left, top, right, bottom = zone
            width = right - left
            height = bottom - top
            screenshot[top:top + height, left:left + width] = 0

        plt.imshow(screenshot, cmap='gray')
        plt.title('Modified Screenshot')
        plt.show()

    result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print("匹配置信度:", max_val)
    if max_val >= believe:
        icon_w, icon_h = img.shape[::-1]

        top_left = max_loc
        bottom_right = (top_left[0] + icon_w, top_left[1] + icon_h)
        cv2.rectangle(screenshot, top_left, bottom_right, (139, 0, 0), 15)
        plt.imshow(screenshot, cmap='gray')
        plt.show()

        icon_center_x = max_loc[0] + icon_w // 2
        icon_center_y = max_loc[1] + icon_h // 2
        random_offset_x = random.randint(-offset, offset)
        random_offset_y = random.randint(-offset, offset)
        screen_x = icon_center_x + random_offset_x
        screen_y = icon_center_y + random_offset_y
        print(f"匹配成功，坐标 [{screen_x}, {screen_y}]")
        return screen_x, screen_y
    print("匹配失败")
    return None


no_click_zones = [
    (0, 0, 500, 260),  # 左上角人物
    (490, 0, 680, 140),  # 3D
    (946, 524, 974, 552),  # 中央
    (800, 0, 1920, 100),  # 上方资源栏
    (1300, 100, 1920, 270),  # 右上角活动*2
    # (910, 0, 1920, 250),  # 右上角活动*5
    (0, 950, 1920, 1080),  # 下方聊天栏
    (1600, 888, 1920, 1080),  # 星系按钮
    (5, 0, 5, 1080),  # 左侧屏幕边缘
    (1680, 250, 1920, 750)  # 右侧活动及快捷菜单
]

x, y = get_coordinate(icon, 0.75)
# pyautogui.click(x, y)
print(x, y)


def close_game():
    logging.info("正在关闭游戏>>>")
    # os.system("taskkill /f /im SpaceArmada.exe")
    os.system("D:\Software\MuMuPlayer-12.0\shell\MuMuManager.exe api -v 5 shutdown_player")