import logging
import os
import random
import sys
import time

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw


def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 加载怪物模板图像
monster_templates = [cv2.imread(resource_path('static/novaimgs/monsters/lv4_boss.png'), cv2.IMREAD_GRAYSCALE),
                     cv2.imread(resource_path('static/novaimgs/monsters/lv6_monster.png'), cv2.IMREAD_GRAYSCALE),
                     cv2.imread(resource_path('static/novaimgs/monsters/lv5_monster.png'), cv2.IMREAD_GRAYSCALE)]
# 加载普通怪物模板图像
normal_monster_templates = [cv2.imread(resource_path('static/novaimgs/monsters/lv2_normal_monster.png'), cv2.IMREAD_GRAYSCALE),
                            cv2.imread(resource_path('static/novaimgs/monsters/lv3_normal_monster.png'), cv2.IMREAD_GRAYSCALE),
                            cv2.imread(resource_path('static/novaimgs/monsters/lv4_normal_monster.png'), cv2.IMREAD_GRAYSCALE)]
# 加载深红怪物模板图像
red_monster_templates = [cv2.imread(resource_path('static/novaimgs/crimson_invades/red_wandering.png'), cv2.IMREAD_GRAYSCALE),
                         cv2.imread(resource_path('static/novaimgs/crimson_invades/red_wandering (2).png'), cv2.IMREAD_GRAYSCALE),
                         cv2.imread(resource_path('static/novaimgs/crimson_invades/lv4_red_transport.png'), cv2.IMREAD_GRAYSCALE),
                         cv2.imread(resource_path('static/novaimgs/crimson_invades/lv6_red_monster.png'), cv2.IMREAD_GRAYSCALE)]
# 加载残骸图标
debris_templates = [cv2.imread(resource_path('static/novaimgs/wreckage/gather_wreckage.png'), cv2.IMREAD_GRAYSCALE),
                    cv2.imread(resource_path('static/novaimgs/wreckage/gather_mineral.png'), cv2.IMREAD_GRAYSCALE)]
# 加载采集图标
collect_icon = cv2.imread(resource_path('static/novaimgs/game_button/button_collect.png'), cv2.IMREAD_GRAYSCALE)
# 加载攻击图标
attack_icon = cv2.imread(resource_path('static/novaimgs/game_button/button_attack.png'), cv2.IMREAD_GRAYSCALE)
# 加载选择全部图标
select_all_icon = cv2.imread(resource_path('static/novaimgs/game_button/button_selectall.png'), cv2.IMREAD_GRAYSCALE)
# 加载确定图标
confirm_icon = cv2.imread(resource_path('static/novaimgs/game_button/button_confirm.png'), cv2.IMREAD_GRAYSCALE)
# 加载空间站图标
space_station_icon = cv2.imread(resource_path('static/novaimgs/game_button/to_station.png'), cv2.IMREAD_GRAYSCALE)
# 加载星系图标
star_system_icon = cv2.imread(resource_path('static/novaimgs/game_button/to_galaxy.png'), cv2.IMREAD_GRAYSCALE)
# 加载关闭图标
close_icon = [cv2.imread(resource_path('static/novaimgs/game_button/button_close.png'), cv2.IMREAD_GRAYSCALE),
              cv2.imread(resource_path('static/novaimgs/game_button/button_close2.png'), cv2.IMREAD_GRAYSCALE),
              cv2.imread(resource_path('static/novaimgs/game_button/button_close3.png'), cv2.IMREAD_GRAYSCALE)]
# 加载主页图标
home_icon = cv2.imread(resource_path('static/novaimgs/game_button/button_home.png'), cv2.IMREAD_GRAYSCALE)
# 加载返回图标
return_icon = cv2.imread(resource_path('static/novaimgs/game_button/button_return.png'), cv2.IMREAD_GRAYSCALE)
# 加载坐标管理图标
coordinate_icon = cv2.imread(resource_path('static/novaimgs/game_button/button_coordinate.png'), cv2.IMREAD_GRAYSCALE)

# 禁止点击区
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

window_left, window_top, window_width, window_height = None, None, None, None
window_name = None
offset = None
confidence = None
monster_confidence = None
corpse_confidence = None
if_reset = True
if_normal_monster = False
if_elite_monster = False
if_apocalypse = False
if_wreckage = False
if_hidden = False
if_orders = False


def initialize(game_window_name, game_offset, game_confidence, game_monster_confidence, game_corpse_confidence,
               game_if_elite_monster, game_if_normal_monster, game_if_wreckage, game_if_apocalypse,
               game_if_hidden, game_if_orders):
    logging.info("正在初始化...")
    window = gw.getWindowsWithTitle(game_window_name)
    if window:
        window = window[0]
        window.maximize()  # 最大化窗口
        window.activate()  # 将窗口置顶
        if game_window_name == 'Space Armada':
            pyautogui.hotkey('alt', 'enter')
            print("")
        else:
            pyautogui.hotkey('F11')
    else:
        logging.error('未找到窗口，请检查是否已打开游戏窗口。')
        return False

    global if_reset
    global window_left, window_top, window_width, window_height
    global window_name, offset, confidence, monster_confidence, corpse_confidence
    global if_normal_monster, if_elite_monster, if_apocalypse, if_wreckage
    global if_hidden, if_orders
    window_left, window_top, window_width, window_height = window.left, window.top, window.width, window.height
    window_name = game_window_name
    offset = game_offset
    confidence = game_confidence
    monster_confidence = game_monster_confidence
    corpse_confidence = game_corpse_confidence
    if_normal_monster = game_if_normal_monster
    if_elite_monster = game_if_elite_monster
    if_apocalypse = game_if_apocalypse
    if_wreckage = game_if_wreckage
    if_hidden = game_if_hidden
    if_orders = game_if_orders

    logging.info(f"窗口名称：{window_name}")
    logging.info(f"窗口位置：{window_left}, {window_top}, {window_width}, {window_height}")
    logging.info(f"偏移量：{offset}")
    logging.info(f"通用识别置信度：{confidence}")
    logging.info(f"怪物识别置信度：{monster_confidence}")
    logging.info(f"残骸识别置信度：{corpse_confidence}")
    if if_hidden:
        logging.info("开启刷隐秘,其它功能将被关闭")
        if_reset, if_normal_monster, if_elite_monster, if_apocalypse, if_wreckage, if_orders = False, False, False, False, False, False
    if if_orders:
        logging.info("开启刷订单,其它功能将被关闭")
        if_reset, if_normal_monster, if_elite_monster, if_apocalypse, if_wreckage, if_hidden = False, False, False, False, False, False
    if if_elite_monster:
        logging.info("开启刷精英怪")
    if if_normal_monster:
        logging.info("开启刷普通怪")
    if if_wreckage:
        logging.info("开启拾取残骸")
    if if_apocalypse:
        logging.info("开启刷深红")
    logging.info("初始化完成...")


# 根据图片返回屏幕坐标
def get_coordinate(img, believe, forbidden_zones=None):
    screenshot = pyautogui.screenshot(region=(window_left, window_top, window_width, window_height))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

    if forbidden_zones is not None:
        for zone in no_click_zones:
            left, top, right, bottom = zone
            width = right - left
            height = bottom - top
            screenshot[top:top + height, left:left + width] = 0

    result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    logging.info(f"匹配置信度：{max_val}")
    if max_val >= believe:
        icon_w, icon_h = img.shape[::-1]
        icon_center_x = max_loc[0] + icon_w // 2
        icon_center_y = max_loc[1] + icon_h // 2
        # 加入随机偏移
        random_offset_x = random.randint(-offset, offset)
        random_offset_y = random.randint(-offset, offset)
        screen_x = window_left + icon_center_x + random_offset_x
        screen_y = window_top + icon_center_y + random_offset_y
        logging.info(f"匹配成功，坐标 [{screen_x}, {screen_y}]")
        return screen_x, screen_y
    return None


# ------------------------------------------------------------------------
# 依次匹配精英怪物模板
def find_monster_coordinates(believe):
    for template in monster_templates:
        coords = get_coordinate(template, believe, no_click_zones)
        if coords is not None:
            return coords
    logging.info("未找到精英怪<<<")
    return None


# 点击精英怪
def find_monsters():
    logging.info("正在寻找精英怪>>>")
    coordinates = find_monster_coordinates(monster_confidence)
    # if coordinates:
    x, y = coordinates
    # for zone in no_click_zones:
    #     if zone[0] <= x <= zone[2] and zone[1] <= y <= zone[3]:
    #         logging.info(f"坐标 [{x}, {y}] 在禁止点击区")
    #         return None
    pyautogui.mouseDown(x, y)
    time.sleep(0.3)
    pyautogui.mouseUp(x, y)
    time.sleep(3)


# ------------------------------------------------------------------------
# 依次匹配普通怪模板
def find_normal_monster_coordinates(believe):
    for template in normal_monster_templates:
        coords = get_coordinate(template, believe, no_click_zones)
        if coords is not None:
            return coords
    logging.info("未找到普通怪<<<")
    return None


# 依次匹配深红怪模板
def find_red_monster_coordinates(believe):
    for template in red_monster_templates:
        coords = get_coordinate(template, believe, no_click_zones)
        if coords is not None:
            return coords
    logging.info("未找到深红怪<<<")
    return None


# 点击普通怪
def find_normal_monsters():
    logging.info("正在寻找普通怪>>>")
    coordinates = find_normal_monster_coordinates(monster_confidence)
    # if coordinates:
    x, y = coordinates
    #     for zone in no_click_zones:
    #         if zone[0] <= x <= zone[2] and zone[1] <= y <= zone[3]:
    #             logging.info(f"坐标 [{x}, {y}] 在禁止点击区")
    #             return None
    pyautogui.mouseDown(x, y)
    time.sleep(0.3)
    pyautogui.mouseUp(x, y)
    time.sleep(3)


# 点击深红怪
def find_red_monsters():
    logging.info("正在寻找深红怪>>>")
    coordinates = find_red_monster_coordinates(monster_confidence)
    # if coordinates:
    x, y = coordinates
    # for zone in no_click_zones:
    #     if zone[0] <= x <= zone[2] and zone[1] <= y <= zone[3]:
    #         logging.info(f"坐标 [{x}, {y}] 在禁止点击区")
    #         return None
    pyautogui.mouseDown(x, y)
    time.sleep(0.3)
    pyautogui.mouseUp(x, y)
    time.sleep(3)


# ------------------------------------------------------------------------

# 点击攻击
def attack_monsters():
    logging.info("正在匹配攻击图标>>>")
    x, y = get_coordinate(attack_icon, confidence)
    pyautogui.mouseDown(x, y)
    time.sleep(0.3)
    pyautogui.mouseUp(x, y)
    time.sleep(3)


# 选择全部
def select_all():
    logging.info("正在匹配选择全部图标>>>")
    x, y = get_coordinate(select_all_icon, confidence)
    pyautogui.mouseDown(x, y)
    time.sleep(0.3)
    pyautogui.mouseUp(x, y)
    time.sleep(3)


# 确定
def confirm():
    logging.info("正在匹配确定图标>>>")
    x, y = get_coordinate(confirm_icon, confidence)
    pyautogui.mouseDown(x, y)
    time.sleep(0.3)
    pyautogui.mouseUp(x, y)
    time.sleep(3)

    # global ATTACKS_NO
    # ATTACKS_NO += 1


# 刷精英怪流程
def attack_process():
    logging.info("开始刷怪流程>>>")
    try:
        find_monsters()
        attack_monsters()
        select_all()
        confirm()
        logging.info("刷怪流程结束<<<")
        time.sleep(120)
        attack_process()
    except TypeError:
        logging.info("未匹配,流程结束<<<")


# 刷普通怪流程
def attack_normal_process():
    logging.info("开始刷普通怪流程>>>")
    try:
        find_normal_monsters()
        attack_monsters()
        select_all()
        confirm()
        logging.info("刷怪流程结束<<<")
        time.sleep(120)
    except TypeError:
        logging.info("未匹配,流程结束<<<")


def attack_apocalypse_process():
    logging.info("开始刷深红流程>>>")
    try:
        find_red_monsters()
        attack_monsters()
        select_all()
        confirm()
        logging.info("刷深红流程结束<<<")
        time.sleep(60)

        attack_apocalypse_process()
    except TypeError:
        logging.info("未匹配,流程结束<<<")


# ------------------------------------------------------------------------
# 依次匹配残骸图标
def find_debris_coordinates(believe):
    for template in debris_templates:
        coords = get_coordinate(template, believe, no_click_zones)
        if coords is not None:
            return coords
    logging.info("未找到残骸<<<")
    return None


def find_debris():
    logging.info("正在寻找残骸>>>")
    coordinates = find_debris_coordinates(corpse_confidence)
    # if coordinates:
    x, y = coordinates
    # for zone in no_click_zones:
    #     if zone[0] <= x <= zone[2] and zone[1] <= y <= zone[3]:
    #         logging.info(f"坐标 [{x}, {y}] 在禁止点击区")
    #         return None
    pyautogui.mouseDown(x, y)
    time.sleep(0.3)
    pyautogui.mouseUp(x, y)
    time.sleep(3)


def collect():
    logging.info("正在匹配采集图标>>>")
    screen_x, screen_y = get_coordinate(collect_icon, confidence)
    pyautogui.mouseDown(screen_x, screen_y)
    time.sleep(0.3)
    pyautogui.mouseUp(screen_x, screen_y)
    time.sleep(3)

    # global WRECKAGE_NO
    # WRECKAGE_NO += 1


def debris_process():
    logging.info("开始采集残骸流程>>>")
    for i in range(5):
        try:
            find_debris()
            collect()
            logging.info("采集残骸<<<")
            time.sleep(60)
        except TypeError:
            logging.info("未匹配<<<")


# ------------------------------------------------------------------------


# 空间站
def space_station():
    logging.info("正在匹配空间站图标>>>")
    try:
        screen_x, screen_y = get_coordinate(space_station_icon, confidence)
        pyautogui.click(screen_x, screen_y)
        time.sleep(10)
    except TypeError:
        logging.info("未匹配空间站图标<<<")


# 星系
def star_system():
    logging.info("正在匹配星系图标>>>")
    try:
        screen_x, screen_y = get_coordinate(star_system_icon, confidence)
        pyautogui.click(screen_x, screen_y)
        time.sleep(10)
    except TypeError:
        logging.info("未匹配星系图标<<<")


def find_close_icons(believe):
    for template in close_icon:
        coords = get_coordinate(template, believe)
        if coords is not None:
            return coords
    logging.info("未找到关闭图标<<<")
    return None


def find_close():
    logging.info("正在寻找关闭图标>>>")
    coordinates = find_close_icons(confidence)
    if coordinates:
        x, y = coordinates
        pyautogui.mouseDown(x, y)
        time.sleep(0.3)
        pyautogui.mouseUp(x, y)


def home():
    logging.info("正在匹配主页图标>>>")
    try:
        screen_x, screen_y = get_coordinate(home_icon, confidence)
        pyautogui.click(screen_x, screen_y)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配主页图标<<<")


# 返回按钮检查
def examine_return():
    logging.info("正在匹配返回图标>>>")
    try:
        if get_coordinate(return_icon, confidence):
            screen_x, screen_y = get_coordinate(coordinate_icon, confidence)
            pyautogui.click(screen_x, screen_y)
            time.sleep(3)
            find_close()
            time.sleep(3)
    except TypeError:
        logging.info("未匹配返回图标<<<")


# 缩小窗口
def zoom_out():
    logging.info("正在缩小窗口>>>")
    window_center_x = window_left + window_width // 2
    window_center_y = window_top + window_height // 2
    pyautogui.moveTo(window_center_x, window_center_y)
    scroll_amount = -1000
    for i in range(30):
        pyautogui.keyDown("ctrl")
        pyautogui.scroll(scroll_amount)
        pyautogui.keyUp("ctrl")


# 放大窗口
def zoom_in():
    window_center_x = window_left + window_width // 2
    window_center_y = window_top + window_height // 2
    pyautogui.moveTo(window_center_x, window_center_y)
    scroll_amount = 1000
    if window_name == 'Space Armada':
        for i in range(30):
            pyautogui.scroll(scroll_amount)
    else:
        pyautogui.keyDown("ctrl")
        pyautogui.scroll(scroll_amount)
        pyautogui.keyUp("ctrl")


# 重置视角流程
def reset_process():
    logging.info("正在重置视角>>>")
    find_close()
    home()
    examine_return()
    space_station()
    star_system()
    zoom_out()
    time.sleep(3)


def close_game():
    logging.info("正在关闭游戏>>>")
    os.system("taskkill /f /im SpaceArmada.exe")
    os.system("D:\Software\MuMuPlayer-12.0\shell\MuMuManager.exe api -v 5 shutdown_player")


# 主循环
def main_loop():
    time.sleep(3)
    if if_reset:
        reset_process()
    if if_apocalypse:
        attack_apocalypse_process()
    if if_elite_monster:
        attack_process()
    if if_normal_monster:
        attack_normal_process()
    if if_wreckage:
        debris_process()
    time.sleep(60)
