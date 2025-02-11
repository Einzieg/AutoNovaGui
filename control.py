import logging
import os
import random
import sys
import time

import cv2

from DeviceUtils import DeviceUtils
from utils.MultiTargeting import move_coordinates


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
                    cv_imread('static/novaimgs/acquisition/elite_wreckage.png'),
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
# 无可用工程船
none_available = cv_imread('static/novaimgs/acquisition/none_available.png')
# 加速
button_speedup = cv_imread('static/novaimgs/button/speed_up.png')

# 禁止点击区
no_click_zones = [
    (0, 0, 500, 260),  # 左上角人物
    (490, 0, 680, 130),  # 3D
    (800, 0, 1920, 100),  # 上方资源栏
    (1300, 100, 1920, 270),  # 右上角活动*3
    # (910, 0, 1920, 250),  # 右上角活动*5
    (1700, 270, 1920, 400),  # 极乐入口
    (0, 950, 1300, 1080),  # 下方聊天栏
    (1350, 870, 1920, 1080),  # 星云按钮
    (1680, 250, 1920, 750)  # 右侧活动及快捷菜单
]


# offset = 3
# self.confidence = None
# self.monster_self.confidence = None
# corpse_self.confidence = None
# if_reset = True
# if_relogin = True
# if_normal_monster = False
# if_elite_monster = False
# if_apocalypse = False
# if_wreckage = False
# if_hidden = False
# if_hidden_gec = False
# if_orders = False
# device = None
# hidden_interval = 60
# relogin_time = 60
# device_utils = None


class Control:
    def __init__(self,
                 game_virtual_num,  # 模拟器编号
                 game_offset,  # 点击偏移量
                 game_confidence,  # 置信度
                 game_monster_confidence,  # 怪物置信度
                 game_corpse_confidence,  # 残骸置信度
                 game_relogin_time,  # 重登时间
                 game_if_elite_monster,  # 是否开启精英怪
                 game_if_normal_monster,  # 是否开启普通怪
                 game_if_wreckage,  # 是否开启残骸
                 game_if_apocalypse,  # 是否开启红色
                 game_if_hidden,  # 是否开启隐秘
                 game_if_hidden_gec,  # 是否开启GEC隐秘
                 game_if_orders,  # 是否开启订单
                 game_if_relogin,  # 是否开启重登
                 ):
        self.device = DeviceUtils(instance_index=game_virtual_num)
        self.offset = game_offset
        self.confidence = game_confidence
        self.monster_confidence = game_monster_confidence
        self.corpse_confidence = game_corpse_confidence
        self.relogin_time = game_relogin_time
        self.if_elite_monster = game_if_elite_monster
        self.if_normal_monster = game_if_normal_monster
        self.if_wreckage = game_if_wreckage
        self.if_apocalypse = game_if_apocalypse
        self.if_hidden = game_if_hidden
        self.if_hidden_gec = game_if_hidden_gec
        self.if_orders = game_if_orders
        self.if_relogin = game_if_relogin
        if self.if_hidden:
            logging.info("开启刷隐秘,其它功能将被关闭")
            self.if_reset, self.if_normal_monster, self.if_elite_monster, self.if_apocalypse, self.if_wreckage, self.if_orders = False, False, False, False, False, False
        if self.if_orders:
            logging.info("开启刷订单,其它功能将被关闭")
            self.if_reset, self.if_normal_monster, self.if_elite_monster, self.if_apocalypse, self.if_wreckage, self.if_hidden = False, False, False, False, False, False
        if self.if_elite_monster:
            logging.info("开启刷精英怪")
            self.if_reset = True
        if self.if_normal_monster:
            logging.info("开启刷普通怪")
            self.if_reset = True
        if self.if_wreckage:
            logging.info("开启拾取残骸")
            self.if_reset = True
        if self.if_apocalypse:
            logging.info("开启刷深红")
            self.if_reset = True
        logging.info("初始化完成...")

    def get_coordinate(self, img, believe, forbidden_zones=None):
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
            # ===============
            icon_center_x = max_loc[0] + icon_w // 2
            icon_center_y = max_loc[1] + icon_h // 2
            # 加入随机偏移
            random_offset_x = random.randint(-self.offset, self.offset)
            random_offset_y = random.randint(-self.offset, self.offset)
            screen_x = icon_center_x + random_offset_x
            screen_y = icon_center_y + random_offset_y
            logging.debug(f"匹配成功，坐标 [{screen_x}, {screen_y}]")
            return screen_x, screen_y
        return None

    # ------------------------------------------------------------------------
    # 依次匹配精英怪物模板
    def find_monster_coordinates(self, believe):
        self.device.mumu_screencap()
        self.device.mumu_screencap()
        for template in monster_templates:
            coords = self.get_coordinate(template, believe, no_click_zones)
            if coords is not None:
                return coords
        logging.info("未找到精英怪<<<")
        return None

    # 点击精英怪
    def find_monsters(self):
        logging.info("正在寻找精英怪>>>")
        coordinates = self.find_monster_coordinates(self.monster_confidence)
        self.device.mumu_click(coordinates)

        time.sleep(3)

    # ------------------------------------------------------------------------
    # 依次匹配普通怪模板
    def find_normal_monster_coordinates(self, believe):
        self.device.mumu_screencap()
        for template in normal_monster_templates:
            coords = self.get_coordinate(template, believe, no_click_zones)
            if coords is not None:
                return coords
        logging.info("未找到普通怪<<<")
        return None

    # 依次匹配深红怪模板
    def find_red_monster_coordinates(self, believe):
        self.device.mumu_screencap()
        for template in red_monster_templates:
            coords = self.get_coordinate(template, believe, no_click_zones)
            if coords is not None:
                return coords
        logging.info("未找到深红怪<<<")
        return None

    # 点击普通怪
    def find_normal_monsters(self):
        logging.info("正在寻找普通怪>>>")
        coordinates = self.find_normal_monster_coordinates(self.monster_confidence)
        self.device.mumu_click(coordinates)
        time.sleep(3)

    # 点击深红怪
    def find_red_monsters(self):
        logging.info("正在寻找深红怪>>>")
        coordinates = self.find_red_monster_coordinates(self.monster_confidence)
        self.device.mumu_click(coordinates)
        time.sleep(3)

    # ------------------------------------------------------------------------

    # 点击攻击
    def attack_monsters(self):
        logging.info("正在匹配攻击图标>>>")
        self.device.mumu_screencap()
        coordinates = self.get_coordinate(attack_icon, self.confidence)
        self.device.mumu_click(coordinates)
        time.sleep(3)

    # 选择全部
    def select_all(self):
        logging.info("正在匹配选择全部图标>>>")
        self.device.mumu_screencap()
        coordinates = self.get_coordinate(select_all_icon, self.confidence)
        self.device.mumu_click(coordinates)
        time.sleep(1)

    # 确定
    def confirm(self):
        logging.info("正在匹配确定图标>>>")
        self.device.mumu_screencap()
        coordinates = self.get_coordinate(confirm_icon, self.confidence)
        self.device.mumu_click(coordinates)
        time.sleep(1)

        # global ATTACKS_NO
        # ATTACKS_NO += 1

    # 刷精英怪流程
    def attack_process(self):
        logging.info("开始刷精英流程>>>")
        try:
            self.find_monsters()
            self.attack_monsters()
            self.find_repair()
            self.select_all()
            self.confirm()
            self.combat_checks(self.attack_process)
            logging.info("刷精英流程结束<<<")
        except TypeError:
            logging.info("未匹配,流程结束<<<")

    # 刷普通怪流程
    def attack_normal_process(self):
        logging.info("开始刷普通怪流程>>>")
        try:
            self.find_normal_monsters()
            self.attack_monsters()
            self.select_all()
            self.confirm()
            self.combat_checks(self.attack_normal_process)
            logging.info("刷怪流程结束<<<")
        except TypeError:
            logging.info("未匹配,流程结束<<<")

    def attack_apocalypse_process(self):
        logging.info("开始刷深红流程>>>")
        try:
            self.find_red_monsters()
            self.attack_monsters()
            self.find_repair()
            self.select_all()
            self.confirm()
            self.combat_checks(self.attack_apocalypse_process)
            logging.info("刷深红流程结束<<<")
        except TypeError:
            logging.info("未匹配,流程结束<<<")

    # ------------------------------------------------------------------------
    # 依次匹配残骸图标
    def find_debris_coordinates(self, believe):
        self.device.mumu_screencap()
        for template in debris_templates:
            coords = self.get_coordinate(template, believe, no_click_zones)
            if coords is not None:
                return coords
        logging.info("未找到残骸<<<")
        return None

    def find_debris(self):
        logging.info("正在寻找残骸>>>")
        coordinates = self.find_debris_coordinates(self.corpse_confidence)
        self.device.mumu_click(coordinates)
        time.sleep(3)

    def collect(self):
        logging.info("正在匹配采集图标>>>")
        self.device.mumu_screencap()
        try:
            coordinates = self.get_coordinate(collect_icon, self.confidence)
            self.device.mumu_click(coordinates)
        except TypeError:
            if self.get_coordinate(return_icon, self.confidence):
                self.device.click_back()
                time.sleep(2)
        time.sleep(3)

    def check_none_available(self):
        """
        检查是否弹出 无可用工程船
        :return:
        """
        self.device.mumu_screencap()
        coordinates = self.get_coordinate(none_available, self.confidence)
        if coordinates:
            self.device.click_back()
            logging.info("无可用工程船")
            raise TypeError
        return False

    def debris_process(self):
        logging.info("开始采集残骸流程>>>")
        try:
            for template in debris_templates:
                self.device.mumu_screencap()
                debris = move_coordinates(template, no_click_zones)
                if debris:
                    for i in debris:
                        # if ships > 6:
                        #     return
                        # ========== DEBUG =========
                        # self.device.mumu_screencap()
                        # original = cv2.imread("screenshot.png")
                        # cv2.rectangle(original, (i[0] - 8, i[1] - 9), (i[0] + 10, i[1] + 10), (0, 0, 255), 1)
                        # cv2.imshow('rect', original)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()
                        # ==========================
                        self.device.mumu_click(i)
                        time.sleep(2)
                        self.collect()
                        self.check_none_available()

                        check = 0
                        while check < 60:
                            time.sleep(1)
                            check += 1
                            self.device.mumu_screencap()
                            if self.get_coordinate(button_speedup, self.confidence):
                                pass
                            else:
                                break
        except TypeError:
            logging.info("采集结束<<<")

    # ------------------------------------------------------------------------

    # 点击雷达
    def find_radar(self):
        logging.info("正在匹配雷达图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(radar_icon, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(2)
        except TypeError:
            logging.info("未匹配雷达图标<<<")

    # 点击搜索
    def find_search(self):
        logging.info("正在匹配搜索图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(search_icon, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(2)
        except TypeError:
            logging.info("未匹配搜索图标<<<")

    # 点击维修
    def find_repair(self):
        logging.info("正在匹配维修图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(repair_icon, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(1)
        except TypeError:
            logging.info("未匹配维修图标<<<")

    # 点击使用
    def find_use(self):
        logging.info("正在匹配使用图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_use_props, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(1)
            return True
        except TypeError:
            return False

    def find_buy(self):
        logging.info("正在匹配购买图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_buy, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(1)
            return True
        except TypeError:
            return False

    # 点击max
    def find_max(self):
        try:
            logging.info("正在匹配max图标>>>")
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_max, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(1)
        except TypeError:
            logging.info("未匹配max图标<<<")

    # 点击使用道具
    def find_use_props(self):
        logging.info("正在匹配使用道具图标>>>")
        self.device.mumu_screencap()
        coordinates = self.get_coordinate(button_use_energy, self.confidence)
        self.device.mumu_click(coordinates)
        time.sleep(1)

    # 使用GEC购买能量
    def find_use_gec_buy_energy(self):
        logging.info("正在匹配购买能量图标>>>")
        self.device.mumu_screencap()
        coordinates = self.get_coordinate(button_use_gec_buy_energy, self.confidence)
        self.device.mumu_click(coordinates)
        time.sleep(1)

    # 刷隐秘流程
    def hide_process(self):
        logging.info("开始刷隐秘流程>>>")
        self.relogin_check()
        self.find_close()
        self.home()
        self.find_radar()
        self.find_search()
        if self.find_use() | self.find_buy():
            self.find_max()
            try:
                self.find_use_props()
            except TypeError:
                if self.if_hidden_gec:
                    self.find_use_gec_buy_energy()
            self.find_search()
        try:
            self.attack_monsters()
            self.find_repair()
            self.select_all()
            self.confirm()
            self.combat_checks(self.hide_process)
        except TypeError:
            return

    # order ------------------------------------------------------------------------

    def open_system(self):
        logging.info("正在匹配系统图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_system, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配系统图标<<<")

    def open_talent(self):
        logging.info("正在匹配天赋图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_talent, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配天赋图标<<<")

    def change_talent(self):
        logging.info("正在匹配修改天赋图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_change_talent, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配修改天赋图标<<<")

    def change_talent_rc(self):
        logging.info("正在匹配获得RC增加图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_talent_increase_rc, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配获得RC增加图标<<<")

    def change_talent_order(self):
        logging.info("正在匹配订单数量增加图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_talent_increase_orders, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配订单数量增加图标<<<")

    def confirm_change_talent(self):
        logging.info("正在匹配确认修改天赋图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_confirm_change_talent, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配确认修改天赋图标<<<")

    def change_talent_process(self, talent: bool):
        logging.info("开始修改天赋流程>>>")
        self.home()
        self.open_system()
        self.open_talent()
        self.change_talent()
        if talent:
            self.change_talent_rc()
        else:
            self.change_talent_order()
        self.confirm_change_talent()
        self.home()

    def open_orders(self):
        logging.info("正在匹配订单图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_orders, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配订单图标<<<")

    def deliver_all(self):
        logging.info("正在匹配一键交付图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_deliver_all, 0.48)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配一键交付图标<<<")

    def confirm_deliver(self):
        logging.info("正在匹配确认交付图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_confirm_deliver, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配确认交付图标<<<")

    def depart(self):
        logging.info("正在匹配离港图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_depart, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配离港图标<<<")

    def close_orders(self):
        logging.info("正在匹配关闭订单图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_close_orders, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配关闭订单图标<<<")

    def more_order(self):
        logging.info("正在匹配更多订单图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_more_orders, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配更多订单图标<<<")

    def next_order(self):
        logging.info("正在匹配下一批图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_next_orders, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配下一批图标<<<")

    # order
    def orders_process(self):
        self.relogin_check()
        self.find_close()
        self.home()
        self.change_talent_process(True)
        self.open_system()
        self.open_orders()
        self.deliver_all()
        self.confirm_deliver()
        self.change_talent_process(False)
        self.open_system()
        self.open_orders()
        self.depart()
        self.close_orders()
        self.more_order()
        self.next_order()
        self.confirm_deliver()
        self.home()

    # --------------------------------------------------------------------------------

    # 空间站
    def space_station(self):
        logging.info("正在匹配空间站图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(space_station_icon, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(10)
        except TypeError:
            logging.info("未匹配空间站图标<<<")

    # 星系
    def star_system(self):
        logging.info("正在匹配星系图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(star_system_icon, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(10)
            return True
        except TypeError:
            logging.info("未匹配星系图标<<<")
            return False

    def find_close_icons(self, believe):
        self.device.mumu_screencap()
        for template in close_icon:
            coords = self.get_coordinate(template, believe)
            if coords is not None:
                return coords
        logging.info("未找到关闭图标<<<")
        return None

    def find_close(self):
        logging.info("正在寻找关闭图标>>>")
        coordinates = self.find_close_icons(self.confidence)
        if coordinates:
            self.device.mumu_click(coordinates)

    def home(self):
        logging.info("正在匹配主页图标>>>")
        try:
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(home_icon, self.confidence)
            self.device.mumu_click(coordinates)
            time.sleep(3)
        except TypeError:
            logging.info("未匹配主页图标<<<")

    def relogin(self):
        try:
            logging.info(f"{self.relogin_time} 秒后重新登录...")
            time.sleep(self.relogin_time)
            self.device.mumu_screencap()
            coordinates = self.get_coordinate(button_relogin, self.confidence)
            if coordinates:
                self.device.mumu_click(coordinates)
                time.sleep(10)
        except TypeError:
            return

    def in_shortcut_examine(self):
        try:
            self.device.mumu_screencap()
            if self.get_coordinate(in_shortcut, self.confidence) is not None:
                self.device.click_back()
                time.sleep(3)
        except TypeError:
            return

    # 选择舰队检查
    def in_select_fleet_fun(self):
        try:
            self.device.mumu_screencap()
            if self.get_coordinate(in_select_fleet, self.confidence) is not None:
                self.device.click_back()
                time.sleep(3)
        except TypeError:
            return

    # 战斗检查
    def in_battle_check(self):
        try:
            self.device.mumu_screencap()
            if self.get_coordinate(in_battle, self.confidence) is not None:
                return True
        except TypeError:
            return False

    # 星云界面检查
    def in_galaxy_fun(self):
        try:
            self.device.mumu_screencap()
            if self.get_coordinate(in_galaxy, self.confidence) is not None:
                self.device.click_back()
                time.sleep(3)
        except TypeError:
            return

    # 返回按钮检查
    def examine_return(self):
        logging.info("正在匹配返回图标>>>")
        try:
            self.device.mumu_screencap()
            if self.get_coordinate(return_icon, self.confidence):
                self.device.click_back()
                time.sleep(1)
        except TypeError:
            logging.info("未匹配返回图标<<<")

    # 抢登检查
    def relogin_check(self):
        logging.info("正在检查是否被抢登>>>")
        self.device.mumu_screencap()
        if self.get_coordinate(in_relogin_icon, self.confidence):
            if self.if_relogin:
                logging.info("被抢登,正在重新登录")
                self.relogin()
            else:
                raise RuntimeError("被抢登,执行结束")

    def combat_checks(self, callback):
        logging.info("正在检查战斗状态>>>")
        to_battle = True
        fighting = False
        check_time = 0

        while to_battle and check_time < 180:
            time.sleep(1)
            logging.debug("检查是否进入战斗")
            check_time += 1
            if self.in_battle_check():
                logging.info("进入战斗")
                to_battle = False
                fighting = True

        while fighting:
            time.sleep(1)
            logging.debug("检查战斗是否结束")
            if not self.in_battle_check():
                logging.info("战斗结束")
                fighting = False
                callback()

    # 重置视角流程
    def reset_process(self):
        logging.info("正在重置视角>>>")
        self.relogin_check()
        self.examine_return()
        self.in_shortcut_examine()
        self.in_select_fleet_fun()
        self.in_galaxy_fun()
        self.find_close()
        self.home()
        self.space_station()
        if self.star_system():
            self.device.zoom_out()
        time.sleep(3)

    # 主循环
    def main_loop(self):
        time.sleep(3)
        if self.if_reset:
            self.reset_process()
        if self.if_hidden:
            self.hide_process()
        if self.if_orders:
            self.orders_process()
        if self.if_apocalypse:
            self.attack_apocalypse_process()
        if self.if_elite_monster:
            self.attack_process()
        if self.if_normal_monster:
            self.attack_normal_process()
        if self.if_wreckage:
            self.debris_process()
        else:
            time.sleep(60)
