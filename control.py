import logging
import os
import random
import sys
import time

import cv2

from Adbutils import adb_connect, get_screenshot, zoom_out, click, back, send_scripts


def cv_imread(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except AttributeError:
        base_path = os.path.abspath(".")
    file_path = os.path.join(base_path, relative_path)
    return cv2.imread(file_path.__str__())


# 加载怪物模板图像
monster_templates = [cv_imread('static/novaimgs/monsters/leader_lv6.png'),
                     cv_imread('static/novaimgs/monsters/leader_lv5.png'),
                     cv_imread('static/novaimgs/monsters/elite_lv6.png'),
                     cv_imread('static/novaimgs/monsters/elite_lv5.png')
                     ]
# 加载普通怪物模板图像
normal_monster_templates = [cv_imread('static/novaimgs/monsters/normal_lv2.png'),
                            cv_imread('static/novaimgs/monsters/normal_lv3.png'),
                            cv_imread('static/novaimgs/monsters/normal_lv4.png')]
# 加载深红怪物模板图像
red_monster_templates = [cv_imread('static/novaimgs/red_invade/wandering.png'),
                         cv_imread('static/novaimgs/red_invade/wandering_s.png'),
                         cv_imread('static/novaimgs/red_invade/lv4_red_transport.png'),
                         cv_imread('static/novaimgs/red_invade/lv6_node.png')]
# 加载残骸图标
debris_templates = [cv_imread('static/novaimgs/acquisition/elite_wreckage.png'),
                    cv_imread('static/novaimgs/acquisition/alloy_wreckage.png'),
                    cv_imread('static/novaimgs/acquisition/crystal_wreckage.png')]
# 加载采集图标
collect_icon = cv_imread('static/novaimgs/button/button_acquisition.png')
# 加载攻击图标
attack_icon = cv_imread('static/novaimgs/attack/attack.png')
# 加载选择全部图标
select_all_icon = cv_imread('static/novaimgs/attack/select_all.png')
# 加载确定图标
confirm_icon = cv_imread('static/novaimgs/attack/confirm_attack.png')
# 加载空间站图标
space_station_icon = cv_imread('static/novaimgs/button/to_station.png')
# 加载星系图标
star_system_icon = cv_imread('static/novaimgs/button/to_galaxy.png')
# 加载关闭图标
close_icon = [cv_imread('static/novaimgs/button/button_close.png'),
              cv_imread('static/novaimgs/button/button_close2.png'),
              cv_imread('static/novaimgs/button/button_close3.png')]
# 加载主页图标
home_icon = cv_imread('static/novaimgs/button/to_home.png')
# 加载返回图标
return_icon = cv_imread('static/novaimgs/button/recall.png')
# 加载坐标管理图标
coordinate_icon = cv_imread('static/novaimgs/button/button_coordinate.png')
# 加载雷达图标
radar_icon = cv_imread('static/novaimgs/hidden/radar.png')
# 加载搜索图标
search_icon = cv_imread('static/novaimgs/hidden/search.png')
# 加载维修图标
repair_icon = cv_imread('static/novaimgs/button/repair.png')
# 加载使用图标
button_use_props = cv_imread('static/novaimgs/hidden/button_use_prop.png')
# 加载max图标
button_max = cv_imread('static/novaimgs/hidden/MAX.png')
# 加载使用能量图标
button_use_energy = cv_imread('static/novaimgs/hidden/energy.png')
# 加载购买图标
button_buy = cv_imread('static/novaimgs/hidden/button_buy.png')
# 加载使用GEC购买能量图标
button_use_gec_buy_energy = cv_imread('static/novaimgs/hidden/GEC.png')
# 加载确认重登按钮
button_relogin = cv_imread('static/novaimgs/button/button_confirm_relogin.png')
# 加载快捷菜单识别图标
in_shortcut = cv_imread('static/novaimgs/identify_in/in_menu.png')
# 识别选择舰队界面
in_select_fleet = cv_imread('static/novaimgs/identify_in/in_fleet.png')
# 加载处于星云界面
in_galaxy = cv_imread('static/novaimgs/identify_in/in_xingyun.png')
# 加载系统菜单
button_system = cv_imread('static/novaimgs/button/button_system.png')
# 加载天赋图标
button_talent = cv_imread('static/novaimgs/talent/to_talent.png')
# 加载切换天赋图标
button_change_talent = cv_imread('static/novaimgs/talent/special_talent.png')
# 加载天赋-获得RC增加
button_talent_increase_rc = cv_imread('static/novaimgs/talent/increase_rc.png')
# 加载天赋-订单数量增加
button_talent_increase_orders = cv_imread('static/novaimgs/talent/increase_orders.png')
# 加载确认更改天赋图标
button_confirm_change_talent = cv_imread('static/novaimgs/talent/confirm_replacement_talent.png')
# 加载订单图标
button_orders = cv_imread('static/novaimgs/order/to_order.png')
# 加载一键交付
button_deliver_all = cv_imread('static/novaimgs/order/delivery.png')
# 加载确认交付
button_confirm_deliver = cv_imread('static/novaimgs/order/confirm_delivery.png')
# 加载离港图标
button_depart = cv_imread('static/novaimgs/order/departures.png')
# 加载关闭订单图标
button_close_orders = cv_imread('static/novaimgs/order/close_order.png')
# 加载更多订单
button_more_orders = cv_imread('static/novaimgs/order/more_order.png')
# 加载快进下一批
button_next_orders = cv_imread('static/novaimgs/order/fast_forward.png')
# 检查抢登
in_relogin_icon = cv_imread('static/novaimgs/identify_in/in_relogin.png')
# 战斗检查
in_battle = cv_imread('static/novaimgs/identify_in/in_battle.png')

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

offset = 3
confidence = None
monster_confidence = None
corpse_confidence = None
if_reset = True
if_relogin = True
if_normal_monster = False
if_elite_monster = False
if_apocalypse = False
if_wreckage = False
if_hidden = False
if_hidden_gec = False
if_orders = False
device = None
hidden_interval = 60
relogin_time = 60


def initialize(game_virtual_num, game_offset, game_confidence, game_monster_confidence, game_corpse_confidence, game_relogin_time,
               game_if_elite_monster, game_if_normal_monster, game_if_wreckage, game_if_apocalypse, game_if_hidden, game_if_hidden_gec, game_if_orders, game_if_relogin):
    logging.info("正在初始化...")

    global device
    device = adb_connect(game_virtual_num)
    send_scripts(device)

    global if_reset, if_relogin
    global offset, confidence, monster_confidence, corpse_confidence, hidden_interval, relogin_time
    global if_normal_monster, if_elite_monster, if_apocalypse, if_wreckage, if_hidden, if_hidden_gec, if_orders

    offset = game_offset
    if_relogin = game_if_relogin
    confidence = game_confidence
    monster_confidence = game_monster_confidence
    corpse_confidence = game_corpse_confidence
    relogin_time = game_relogin_time

    if_normal_monster = game_if_normal_monster
    if_elite_monster = game_if_elite_monster
    if_apocalypse = game_if_apocalypse
    if_wreckage = game_if_wreckage
    if_hidden = game_if_hidden
    if_hidden_gec = game_if_hidden_gec
    if_orders = game_if_orders

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
        if_reset = True
    if if_normal_monster:
        logging.info("开启刷普通怪")
        if_reset = True
    if if_wreckage:
        logging.info("开启拾取残骸")
        if_reset = True
    if if_apocalypse:
        logging.info("开启刷深红")
        if_reset = True
    logging.info("初始化完成...")


# 根据图片返回屏幕坐标
def get_coordinate(img, believe, forbidden_zones=None):
    screenshot = cv2.imread('screenshot.png')

    if forbidden_zones is not None:
        for zone in no_click_zones:
            left, top, right, bottom = zone
            width = right - left
            height = bottom - top
            screenshot[top:top + height, left:left + width] = 0

    result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    logging.debug(f"匹配置信度：{max_val:.2%}")
    if max_val >= believe:
        icon_w, icon_h = img.shape[1], img.shape[0]
        # ===============
        # top_left = max_loc
        # bottom_right = (top_left[0] + icon_w, top_left[1] + icon_h)
        # cv2.rectangle(screenshot, top_left, bottom_right, (0, 0, 255), 10)
        # cv2.imshow('result', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
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
        logging.debug(f"匹配成功，坐标 [{screen_x}, {screen_y}]")
        return screen_x, screen_y
    return None


# ------------------------------------------------------------------------
# 依次匹配精英怪物模板
def find_monster_coordinates(believe):
    get_screenshot(device)
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
    click(device, coordinates)
    time.sleep(3)


# ------------------------------------------------------------------------
# 依次匹配普通怪模板
def find_normal_monster_coordinates(believe):
    get_screenshot(device)
    for template in normal_monster_templates:
        coords = get_coordinate(template, believe, no_click_zones)
        if coords is not None:
            return coords
    logging.info("未找到普通怪<<<")
    return None


# 依次匹配深红怪模板
def find_red_monster_coordinates(believe):
    get_screenshot(device)
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
    click(device, coordinates)
    time.sleep(3)


# 点击深红怪
def find_red_monsters():
    logging.info("正在寻找深红怪>>>")
    coordinates = find_red_monster_coordinates(monster_confidence)
    click(device, coordinates)
    time.sleep(3)


# ------------------------------------------------------------------------

# 点击攻击
def attack_monsters():
    logging.info("正在匹配攻击图标>>>")
    get_screenshot(device)
    coordinates = get_coordinate(attack_icon, confidence)
    click(device, coordinates)
    time.sleep(3)


# 选择全部
def select_all():
    logging.info("正在匹配选择全部图标>>>")
    get_screenshot(device)
    coordinates = get_coordinate(select_all_icon, confidence)
    click(device, coordinates)
    time.sleep(1)


# 确定
def confirm():
    logging.info("正在匹配确定图标>>>")
    get_screenshot(device)
    coordinates = get_coordinate(confirm_icon, confidence)
    click(device, coordinates)
    time.sleep(1)

    # global ATTACKS_NO
    # ATTACKS_NO += 1


# 刷精英怪流程
def attack_process():
    logging.info("开始刷精英流程>>>")
    try:
        find_monsters()
        attack_monsters()
        find_repair()
        select_all()
        confirm()
        combat_checks(attack_process)
        logging.info("刷精英流程结束<<<")
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
        combat_checks(attack_normal_process)
        logging.info("刷怪流程结束<<<")
    except TypeError:
        logging.info("未匹配,流程结束<<<")


def attack_apocalypse_process():
    logging.info("开始刷深红流程>>>")
    try:
        find_red_monsters()
        attack_monsters()
        find_repair()
        select_all()
        confirm()
        combat_checks(attack_apocalypse_process)
        logging.info("刷深红流程结束<<<")
    except TypeError:
        logging.info("未匹配,流程结束<<<")


# ------------------------------------------------------------------------
# 依次匹配残骸图标
def find_debris_coordinates(believe):
    get_screenshot(device)
    for template in debris_templates:
        coords = get_coordinate(template, believe, no_click_zones)
        if coords is not None:
            return coords
    logging.info("未找到残骸<<<")
    return None


def find_debris():
    logging.info("正在寻找残骸>>>")
    coordinates = find_debris_coordinates(corpse_confidence)
    click(device, coordinates)
    time.sleep(3)


def collect():
    logging.info("正在匹配采集图标>>>")
    get_screenshot(device)
    coordinates = get_coordinate(collect_icon, confidence)
    click(device, coordinates)
    time.sleep(3)


def debris_process():
    logging.info("开始采集残骸流程>>>")
    for i in range(5):
        try:
            find_debris()
            collect()
            time.sleep(60)
        except TypeError:
            logging.info("未匹配<<<")


# ------------------------------------------------------------------------


# 点击雷达
def find_radar():
    logging.info("正在匹配雷达图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(radar_icon, confidence)
        click(device, coordinates)
        time.sleep(2)
    except TypeError:
        logging.info("未匹配雷达图标<<<")


# 点击搜索
def find_search():
    logging.info("正在匹配搜索图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(search_icon, confidence)
        click(device, coordinates)
        time.sleep(2)
    except TypeError:
        logging.info("未匹配搜索图标<<<")


# 点击维修
def find_repair():
    logging.info("正在匹配维修图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(repair_icon, confidence)
        click(device, coordinates)
        time.sleep(1)
    except TypeError:
        logging.info("未匹配维修图标<<<")


# 点击使用
def find_use():
    logging.info("正在匹配使用图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_use_props, confidence)
        click(device, coordinates)
        time.sleep(1)
        return True
    except TypeError:
        return False


def find_buy():
    logging.info("正在匹配购买图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_buy, confidence)
        click(device, coordinates)
        time.sleep(1)
        return True
    except TypeError:
        return False


# 点击max
def find_max():
    try:
        logging.info("正在匹配max图标>>>")
        get_screenshot(device)
        coordinates = get_coordinate(button_max, confidence)
        click(device, coordinates)
        time.sleep(1)
    except TypeError:
        logging.info("未匹配max图标<<<")


# 点击使用道具
def find_use_props():
    logging.info("正在匹配使用道具图标>>>")
    get_screenshot(device)
    coordinates = get_coordinate(button_use_energy, confidence)
    click(device, coordinates)
    time.sleep(1)


# 使用GEC购买能量
def find_use_gec_buy_energy():
    logging.info("正在匹配购买能量图标>>>")
    get_screenshot(device)
    coordinates = get_coordinate(button_use_gec_buy_energy, confidence)
    click(device, coordinates)
    time.sleep(1)


# 刷隐秘流程
def hide_process():
    logging.info("开始刷隐秘流程>>>")
    relogin_check()
    find_close()
    home()
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
    try:
        attack_monsters()
        find_repair()
        select_all()
        confirm()
        combat_checks(hide_process)
    except TypeError:
        return


# order ------------------------------------------------------------------------

def open_system():
    logging.info("正在匹配系统图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_system, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配系统图标<<<")


def open_talent():
    logging.info("正在匹配天赋图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_talent, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配天赋图标<<<")


def change_talent():
    logging.info("正在匹配修改天赋图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_change_talent, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配修改天赋图标<<<")


def change_talent_rc():
    logging.info("正在匹配获得RC增加图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_talent_increase_rc, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配获得RC增加图标<<<")


def change_talent_order():
    logging.info("正在匹配订单数量增加图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_talent_increase_orders, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配订单数量增加图标<<<")


def confirm_change_talent():
    logging.info("正在匹配确认修改天赋图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_confirm_change_talent, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配确认修改天赋图标<<<")


def change_talent_process(talent: bool):
    logging.info("开始修改天赋流程>>>")
    home()
    open_system()
    open_talent()
    change_talent()
    if talent:
        change_talent_rc()
    else:
        change_talent_order()
    confirm_change_talent()
    home()


def open_orders():
    logging.info("正在匹配订单图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_orders, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配订单图标<<<")


def deliver_all():
    logging.info("正在匹配一键交付图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_deliver_all, 0.48)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配一键交付图标<<<")


def confirm_deliver():
    logging.info("正在匹配确认交付图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_confirm_deliver, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配确认交付图标<<<")


def depart():
    logging.info("正在匹配离港图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_depart, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配离港图标<<<")


def close_orders():
    logging.info("正在匹配关闭订单图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_close_orders, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配关闭订单图标<<<")


def more_order():
    logging.info("正在匹配更多订单图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_more_orders, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配更多订单图标<<<")


def next_order():
    logging.info("正在匹配下一批图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(button_next_orders, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配下一批图标<<<")


# order
def orders_process():
    relogin_check()
    find_close()
    home()
    change_talent_process(True)
    open_system()
    open_orders()
    deliver_all()
    confirm_deliver()
    change_talent_process(False)
    open_system()
    open_orders()
    depart()
    close_orders()
    more_order()
    next_order()
    confirm_deliver()
    home()


# --------------------------------------------------------------------------------

# 空间站
def space_station():
    logging.info("正在匹配空间站图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(space_station_icon, confidence)
        click(device, coordinates)
        time.sleep(10)
    except TypeError:
        logging.info("未匹配空间站图标<<<")


# 星系
def star_system():
    logging.info("正在匹配星系图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(star_system_icon, confidence)
        click(device, coordinates)
        time.sleep(10)
    except TypeError:
        logging.info("未匹配星系图标<<<")


def find_close_icons(believe):
    get_screenshot(device)
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
        click(device, coordinates)


def home():
    logging.info("正在匹配主页图标>>>")
    try:
        get_screenshot(device)
        coordinates = get_coordinate(home_icon, confidence)
        click(device, coordinates)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配主页图标<<<")


def relogin():
    try:
        logging.info(f"{relogin_time} 秒后重新登录...")
        time.sleep(relogin_time)
        get_screenshot(device)
        coordinates = get_coordinate(button_relogin, confidence)
        if coordinates:
            click(device, coordinates)
            time.sleep(10)
    except TypeError:
        return


def in_shortcut_examine():
    try:
        get_screenshot(device)
        if get_coordinate(in_shortcut, confidence) is not None:
            back(device)
            time.sleep(3)
    except TypeError:
        return


# 选择舰队检查
def in_select_fleet_fun():
    try:
        get_screenshot(device)
        if get_coordinate(in_select_fleet, confidence) is not None:
            back(device)
            time.sleep(3)
    except TypeError:
        return


# 战斗检查
def in_battle_check():
    try:
        get_screenshot(device)
        if get_coordinate(in_battle, confidence) is not None:
            return True
    except TypeError:
        return False


# 星云界面检查
def in_galaxy_fun():
    try:
        get_screenshot(device)
        if get_coordinate(in_galaxy, confidence) is not None:
            back(device)
            time.sleep(3)
    except TypeError:
        return


# 返回按钮检查
def examine_return():
    logging.info("正在匹配返回图标>>>")
    try:
        get_screenshot(device)
        if get_coordinate(return_icon, confidence):
            back(device)
            time.sleep(3)
    except TypeError:
        logging.info("未匹配返回图标<<<")


# 抢登检查
def relogin_check():
    logging.info("正在检查是否被抢登>>>")
    get_screenshot(device)
    if get_coordinate(in_relogin_icon, confidence):
        if if_relogin:
            logging.info("被抢登,正在重新登录")
            relogin()
        else:
            raise RuntimeError("被抢登,执行结束")


def combat_checks(callback):
    logging.info("正在检查战斗状态>>>")
    to_battle = True
    fighting = False
    check_time = 0

    while to_battle and check_time < 120:
        logging.debug("检查是否进入战斗")
        check_time += 1
        if in_battle_check():
            logging.info("进入战斗")
            to_battle = False
            fighting = True

    while fighting:
        logging.debug("检查战斗是否结束")
        if not in_battle_check():
            logging.info("战斗结束")
            fighting = False
            callback()


# 重置视角流程
def reset_process():
    logging.info("正在重置视角>>>")
    relogin_check()
    examine_return()
    in_shortcut_examine()
    in_select_fleet_fun()
    in_galaxy_fun()
    find_close()
    home()
    space_station()
    star_system()
    zoom_out(device)
    time.sleep(3)


# 主循环
def main_loop():
    time.sleep(3)
    if if_reset:
        reset_process()
    if if_hidden:
        hide_process()
    if if_orders:
        orders_process()
    if if_apocalypse:
        attack_apocalypse_process()
    if if_elite_monster:
        attack_process()
    if if_normal_monster:
        attack_normal_process()
    if if_wreckage:
        debris_process()
    else:
        time.sleep(60)
