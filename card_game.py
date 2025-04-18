import logging
import time

import cv2
from path_util import cv_imread

class AutoFlipMemoryGameSolver:

    def __init__(self, device):
        self.device = device
        self.x_start = 670
        self.y_start = 130
        self.card_width = 170
        self.card_height = 200
        self.x_gap = 15
        self.y_gap = 20

        self.card_templates = {}

        for name, path in [
            ("HERO", "static/novaimgs/CARD_GAME/v1/HERO.png"),
            ("PLANET", "static/novaimgs/CARD_GAME/v1/PLANET.png"),
            ("SHIP", "static/novaimgs/CARD_GAME/v1/SHIP.png"),
            ("SPACE_STATION", "static/novaimgs/CARD_GAME/v1/SPACE_STATION.png"),
            ("UNIT", "static/novaimgs/CARD_GAME/v1/UNIT.png")
        ]:
            try:
                img = cv_imread(path)
                if img is None:
                    raise FileNotFoundError(f"未能读取文件 {path}")
                self.card_templates[name] = img
                logging.info(f"加载模板图片 {name}: {path}")
            except Exception as e:
                logging.error(f"加载模板图片失败: {e}")

    def get_card_position(self, row, col):
        x = self.x_start + col * (self.card_width + self.x_gap) + self.card_width // 2
        y = self.y_start + row * (self.card_height + self.y_gap) + self.card_height // 2
        return x, y

    def click_card(self, row, col):
        center = self.get_card_position(row, col)
        self.device.click(center)
        logging.info(f"点击卡牌 ({row}, {col})")

    def recognize_card(self, img, card_templates):
        best_match, best_score = None, 0.0
        for name, template in card_templates.items():
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > best_score:
                best_match, best_score = name, max_val
        return best_match if best_score > 0.7 else None

    def play_game(self):
        opened_cards = []
        flipped_cards = set()
        total_cards = 4 * 5
        opened = 0

        while len(flipped_cards) < total_cards:
            for i in range(4):
                for j in range(5):
                    if (i, j) not in flipped_cards:
                        self.click_card(i, j)

                        time.sleep(0.4)
                        self.device.screencap()
                        screenshot_img = cv2.imread("./screenshot.png")

                        x_start_card = self.x_start + j * (self.card_width + self.x_gap)
                        y_start_card = self.y_start + i * (self.card_height + self.y_gap)
                        x_end_card = x_start_card + self.card_width
                        y_end_card = y_start_card + self.card_height
                        card_region = screenshot_img[y_start_card:y_end_card, x_start_card:x_end_card]

                        card_name = self.recognize_card(card_region, self.card_templates)
                        logging.info(f"识别到卡牌 {card_name} ({i}, {j})")

                        if card_name:
                            found_entry = None
                            opened += 1
                            for entry in opened_cards:
                                if entry[0] == card_name and (entry[1], entry[2]) != (i, j):
                                    found_entry = entry
                                    break
                            if found_entry:
                                prev_row, prev_col = found_entry[1], found_entry[2]
                                flipped_cards.add((i, j))
                                flipped_cards.add((prev_row, prev_col))
                                opened_cards.remove(found_entry)
                                if opened == 2:
                                    time.sleep(1.5)
                                    self.click_card(i, j)
                                    time.sleep(0.4)
                                    self.click_card(prev_row, prev_col)
                                    time.sleep(1.5)
                                    opened = 0
                                else:
                                    self.click_card(prev_row, prev_col)
                                    time.sleep(1.5)
                                    opened = 0
                            else:
                                opened_cards.append((card_name, i, j))
                                flipped_cards.add((i, j))
                                time.sleep(1.2)
                        else:
                            flipped_cards.add((i, j))
                            time.sleep(1)
