import os
import random
import sys

import cv2
import numpy as np
from matplotlib import pyplot as plt


def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def cv_imread(file_path):
    # cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8),-1)
    # cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    cv_img = cv2.imread(file_path)
    # plt.imshow(cv_img)
    # plt.show()
    return cv_img


icon = cv2.imread("../static/novaimgs/attack/confirm_attack.png")

offset = 3


def get_coordinate(img, believe, no_click_zone=None):
    screenshot = cv2.imread("../screenshot.png")

    # 遍历需要屏蔽的区域并填充为黑色
    if no_click_zone is not None:
        for zone in no_click_zone:
            left, top, right, bottom = zone
            width = right - left
            height = bottom - top
            screenshot[top:top + height, left:left + width] = 0

        plt.imshow(screenshot)
        plt.title('Modified Screenshot')
        plt.show()

    result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print("匹配置信度:", max_val)  # 1.0
    if max_val >= believe:
        print(f"模板尺寸: {img.shape[:2]}")  # (height, width)
        icon_w, icon_h = img.shape[1], img.shape[0]

        top_left = max_loc
        bottom_right = (top_left[0] + icon_w, top_left[1] + icon_h)
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 0, 255), 2)
        cv2.imshow('result', screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        plt.imshow(screenshot)
        plt.show()

        # 计算模板图像的中心坐标
        icon_center_x = max_loc[0] + icon_w // 2
        icon_center_y = max_loc[1] + icon_h // 2

        # 去掉不必要的随机偏移，直接返回坐标
        screen_x = max(0, min(icon_center_x, screenshot.shape[1] - 1))
        screen_y = max(0, min(icon_center_y, screenshot.shape[0] - 1))

        print(f"匹配成功，坐标 [{screen_x}, {screen_y}]")
        return screen_x, screen_y
    print("匹配失败")
    return None


no_click_zones = [
    (0, 0, 500, 260),  # 左上角人物
    (490, 0, 680, 140),  # 3D
    # (946, 524, 974, 552),  # 中央
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
print(x, y) # 匹配成功，坐标 [1372, 1110]
