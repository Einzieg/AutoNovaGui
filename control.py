import logging
import os
import random
import sys
import time

import cv2

import adbutils


# import pyautogui
# import pygetwindow as gw


# from adbutils import click, get_screenshot


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
# 加载雷达图标
radar_icon = cv2.imread(resource_path('static/novaimgs/game_button/button_radar.png'), cv2.IMREAD_GRAYSCALE)
# 加载搜索图标
search_icon = cv2.imread(resource_path('static/novaimgs/game_button/button_search.png'), cv2.IMREAD_GRAYSCALE)
# 加载维修图标
repair_icon = cv2.imread(resource_path('static/novaimgs/game_button/button_repair.png'), cv2.IMREAD_GRAYSCALE)
# 加载使用图标
button_use_props = cv2.imread(resource_path('static/novaimgs/game_button/button_use_props.png'), cv2.IMREAD_GRAYSCALE)
# 加载max图标
button_max = cv2.imread(resource_path('static/novaimgs/game_button/button_max.png'), cv2.IMREAD_GRAYSCALE)
# 加载使用能量图标
button_use_energy = cv2.imread(resource_path('static/novaimgs/game_button/energy.png'), cv2.IMREAD_GRAYSCALE)
# 加载购买图标
button_buy = cv2.imread(resource_path('static/novaimgs/game_button/button_buy.png'), cv2.IMREAD_GRAYSCALE)
# 加载使用GEC购买能量图标
button_use_gec_buy_energy = cv2.imread(resource_path('static/novaimgs/game_button/gec_buy_energy.png'), cv2.IMREAD_GRAYSCALE)
# 加载确认重登按钮
button_relogin = cv2.imread(resource_path('static/novaimgs/game_button/button_confirm_relogin.png'), cv2.IMREAD_GRAYSCALE)

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

# window_left, window_top, window_width, window_height = None, None, None, None
# virtual_num = None
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
if_hidden_gec = False
if_orders = False
device = None


def initialize(game_virtual_num, game_offset, game_confidence, game_monster_confidence, game_corpse_confidence,
               game_if_elite_monster, game_if_normal_monster, game_if_wreckage, game_if_apocalypse,
               game_if_hidden, game_if_hidden_gec, game_if_orders):
    logging.info("正在初始化...")
    global device
    # try:
    device = adbutils.adb_connect(game_virtual_num)
    adbutils.send_scripts(device)
    # except Exception as e:
    #     logging.error(e)
    # window = gw.getWindowsWithTitle(game_window_name)
    # if window:
    #     window = window[0]
    #     window.maximize()  # 最大化窗口
    #     window.activate()  # 将窗口置顶
    #     if game_window_name == 'Space Armada':
    #         pyautogui.hotkey('alt', 'enter')
    #         print("")
    #     else:
    #         pyautogui.hotkey('F11')
    # else:
    #     logging.error('未找到窗口，请检查是否已打开游戏窗口。')
    #     return False

    global if_reset
    # global window_left, window_top, window_width, window_height
    global offset, confidence, monster_confidence, corpse_confidence
    global if_normal_monster, if_elite_monster, if_apocalypse, if_wreckage
    global if_hidden, if_hidden_gec, if_orders
    # window_left, window_top, window_width, window_height = window.left, window.top, window.width, window.height

    # virtual_num = game_window_name
    offset = game_offset
    confidence = game_confidence
    monster_confidence = game_monster_confidence
    corpse_confidence = game_corpse_confidence
    if_normal_monster = game_if_normal_monster
    if_elite_monster = game_if_elite_monster
    if_apocalypse = game_if_apocalypse
    if_wreckage = game_if_wreckage
    if_hidden = game_if_hidden
    if_hidden_gec = game_if_hidden_gec
    if_orders = game_if_orders

    # logging.info(f"窗口名称：{window_name}")
    # logging.info(f"窗口位置：{window_left}, {window_top}, {window_width}, {window_height}")
    logging.info(f"偏移量：{offset}")
    logging.info(f"通用识别置信度：{confidence:.2%}")
    logging.info(f"怪物识别置信度：{monster_confidence:.2%}")
    logging.info(f"残骸识别置信度：{corpse_confidence:.2%}")
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
    # adbutils.get_screenshot(device)
    screenshot = cv2.imread('screenshot.png', cv2.IMREAD_GRAYSCALE)

    if forbidden_zones is not None:
        for zone in no_click_zones:
            left, top, right, bottom = zone
            width = right - left
            height = bottom - top
            screenshot[top:top + height, left:left + width] = 0

    result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    logging.info(f"匹配置信度：{max_val:.2%}")
    if max_val >= believe:
        icon_w, icon_h = img.shape[::-1]
        # ===============
        # top_left = max_loc
        # bottom_right = (top_left[0] + icon_w, top_left[1] + icon_h)
        # cv2.rectangle(screenshot, top_left, bottom_right, (139, 0, 0), 15)
        # plt.imshow(screenshot, cmap='gray')
        # plt.show()
        # ===============
        icon_center_x = max_loc[0] + icon_w // 2
        icon_center_y = max_loc[1] + icon_h // 2
        # 加入随机偏移
        random_offset_x = random.randint(-offset, offset)
        random_offset_y = random.randint(-offset, offset)
        screen_x = icon_center_x + random_offset_x
        screen_y = icon_center_y + random_offset_y
        logging.info(f"匹配成功，坐标 [{screen_x}, {screen_y}]")
        return screen_x, screen_y
    return None


# def click(x, y, sleep):
#     pyautogui.mouseDown(x, y)
#     time.sleep(sleep)
#     pyautogui.mouseUp(x, y)


# ------------------------------------------------------------------------
# 依次匹配精英怪物模板
def find_monster_coordinates(believe):
    adbutils.get_screenshot(device)
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
    x, y = coordinates
    adbutils.click(device, x, y)
    time.sleep(3)


# ------------------------------------------------------------------------
# 依次匹配普通怪模板
def find_normal_monster_coordinates(believe):
    adbutils.get_screenshot(device)
    for template in normal_monster_templates:
        coords = get_coordinate(template, believe, no_click_zones)
        if coords is not None:
            return coords
    logging.info("未找到普通怪<<<")
    return None


# 依次匹配深红怪模板
def find_red_monster_coordinates(believe):
    logging.info("正在寻找深红怪>>>")
    adbutils.get_screenshot(device)
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
    x, y = coordinates
    adbutils.click(device, x, y)
    time.sleep(3)


# 点击深红怪
def find_red_monsters():
    logging.info("正在寻找深红怪>>>")
    coordinates = find_red_monster_coordinates(monster_confidence)
    x, y = coordinates
    adbutils.click(device, x, y)
    time.sleep(3)


# ------------------------------------------------------------------------

# 点击攻击
def attack_monsters():
    logging.info("正在匹配攻击图标>>>")
    adbutils.get_screenshot(device)
    x, y = get_coordinate(attack_icon, confidence)
    adbutils.click(device, x, y)
    time.sleep(3)


# 选择全部
def select_all():
    logging.info("正在匹配选择全部图标>>>")
    adbutils.get_screenshot(device)
    x, y = get_coordinate(select_all_icon, confidence)
    adbutils.click(device, x, y)
    time.sleep(3)


# 确定
def confirm():
    logging.info("正在匹配确定图标>>>")
    adbutils.get_screenshot(device)
    x, y = get_coordinate(confirm_icon, confidence)
    adbutils.click(device, x, y)
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
        time.sleep(90)

        attack_apocalypse_process()
    except TypeError:
        logging.info("未匹配,流程结束<<<")


# ------------------------------------------------------------------------
# 依次匹配残骸图标
def find_debris_coordinates(believe):
    adbutils.get_screenshot(device)
    for template in debris_templates:
        coords = get_coordinate(template, believe, no_click_zones)
        if coords is not None:
            return coords
    logging.info("未找到残骸<<<")
    return None


def find_debris():
    logging.info("正在寻找残骸>>>")
    coordinates = find_debris_coordinates(corpse_confidence)
    x, y = coordinates
    adbutils.click(device, x, y)
    time.sleep(3)


def collect():
    logging.info("正在匹配采集图标>>>")
    adbutils.get_screenshot(device)
    x, y = get_coordinate(collect_icon, confidence)
    adbutils.click(device, x, y)
    time.sleep(3)


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


# 点击雷达
def find_radar():
    logging.info("正在匹配雷达图标>>>")
    adbutils.get_screenshot(device)
    x, y = get_coordinate(radar_icon, confidence)
    adbutils.click(device, x, y)
    time.sleep(3)


# 点击搜索
def find_search():
    logging.info("正在匹配搜索图标>>>")
    adbutils.get_screenshot(device)
    x, y = get_coordinate(search_icon, confidence)
    adbutils.click(device, x, y)
    time.sleep(3)


# 点击维修
def find_repair():
    logging.info("正在匹配维修图标>>>")
    try:
        adbutils.get_screenshot(device)
        x, y = get_coordinate(repair_icon, confidence)
        adbutils.click(device, x, y)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配维修图标<<<")


# 点击使用
def find_use():
    logging.info("正在匹配使用图标>>>")
    try:
        adbutils.get_screenshot(device)
        x, y = get_coordinate(button_use_props, confidence)
        adbutils.click(device, x, y)
        time.sleep(3)
        return True
    except TypeError:
        return False


def find_buy():
    logging.info("正在匹配购买图标>>>")
    try:
        adbutils.get_screenshot(device)
        x, y = get_coordinate(button_buy, confidence)
        adbutils.click(device, x, y)
        time.sleep(3)
        return True
    except TypeError:
        return False


# 点击max
def find_max():
    logging.info("正在匹配max图标>>>")
    adbutils.get_screenshot(device)
    x, y = get_coordinate(button_max, confidence)
    adbutils.click(device, x, y)
    time.sleep(3)


# 点击使用道具
def find_use_props():
    logging.info("正在匹配使用道具图标>>>")
    adbutils.get_screenshot(device)
    x, y = get_coordinate(button_use_energy, confidence)
    adbutils.click(device, x, y)
    time.sleep(3)


# 使用GEC购买能量
def find_use_gec_buy_energy():
    logging.info("正在匹配购买能量图标>>>")
    adbutils.get_screenshot(device)
    x, y = get_coordinate(button_use_gec_buy_energy, confidence)
    adbutils.click(device, x, y)
    time.sleep(3)


# 刷隐秘流程
def hide_process():
    logging.info("开始刷隐秘流程>>>")
    try:
        find_radar()
        find_search()
        if find_use() | find_buy():
            find_max()
            try:
                find_use_props()
            except TypeError:
                if if_hidden_gec:
                    find_use_gec_buy_energy()
            find_search()
        attack_monsters()
        find_repair()
        select_all()
        confirm()

    except TypeError:
        logging.info("未匹配<<<")


# ------------------------------------------------------------------------

# 空间站
def space_station():
    logging.info("正在匹配空间站图标>>>")
    try:
        adbutils.get_screenshot(device)
        x, y = get_coordinate(space_station_icon, confidence)
        adbutils.click(device, x, y)
        time.sleep(10)
    except TypeError:
        logging.info("未匹配空间站图标<<<")


# 星系
def star_system():
    logging.info("正在匹配星系图标>>>")
    try:
        adbutils.get_screenshot(device)
        x, y = get_coordinate(star_system_icon, confidence)
        adbutils.click(device, x, y)
        time.sleep(10)
    except TypeError:
        logging.info("未匹配星系图标<<<")


def find_close_icons(believe):
    adbutils.get_screenshot(device)
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
        adbutils.click(device, x, y)


def home():
    logging.info("正在匹配主页图标>>>")
    try:
        adbutils.get_screenshot(device)
        x, y = get_coordinate(home_icon, confidence)
        adbutils.click(device, x, y)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配主页图标<<<")


def relogin():
    try:
        adbutils.get_screenshot(device)
        x, y = get_coordinate(button_relogin, confidence)
        adbutils.click(device, x, y)
        time.sleep(3)
    except TypeError:
        return


# 返回按钮检查
def examine_return():
    logging.info("正在匹配返回图标>>>")
    try:
        adbutils.get_screenshot(device)
        if get_coordinate(return_icon, confidence):
            x, y = get_coordinate(coordinate_icon, confidence)
            adbutils.click(device, x, y)
            time.sleep(3)
            find_close()
            time.sleep(3)
    except TypeError:
        logging.info("未匹配返回图标<<<")


# 缩小窗口
def zoom_out():
    adbutils.zoom_out(device)


# 放大窗口
def zoom_in():
    adbutils.zoom_in(device)


# 重置视角流程
def reset_process():
    logging.info("正在重置视角>>>")
    relogin()
    find_close()
    home()
    examine_return()
    space_station()
    star_system()
    zoom_out()
    find_close()
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
    if if_hidden:
        hide_process()
    if if_apocalypse:
        attack_apocalypse_process()
    if if_elite_monster:
        attack_process()
    if if_normal_monster:
        attack_normal_process()
    if if_wreckage:
        debris_process()
    time.sleep(60)
