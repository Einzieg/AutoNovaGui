import logging
import os
import sys
import time

from AdbClient import AdbClient


def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def adb_connect(n):
    device = AdbClient(ip='127.0.0.1', port=16384 + 32 * n)
    return device


def get_screenshot(device):
    device.shell("screencap -p /sdcard/screenshot.png")
    device.pull('/sdcard/screenshot.png', 'screenshot.png')


def swipe(device, start_x, start_y, end_x, end_y):
    device.shell(f"input touchscreen swipe {start_x} {start_y} {end_x} {end_y} 200")


def zoom_out(device):
    logging.debug("zoom out")
    device.shell("sh /sdcard/zoom_out.sh")  # try running the script to pinchout


def zoom_in(device):
    device.shell("sh /sdcard/zoom_in.sh")  # try running the script to zoomin
    time.sleep(3)


def up(device):
    device.shell("input swipe {} {} {} {}".format(1000, 200, 1000, 500))


def down(device):
    device.shell("input swipe {} {} {} {}".format(1000, 800, 1000, 500))


def click(device, x, y):
    device.shell("input tap {} {}".format(x, y))


def back(device):
    device.shell("input keyevent 4")


# 把缩小和放大的脚本放到模拟器上
def send_scripts(device):
    logging.debug("send scripts")
    device.push(resource_path("static/zoom_in.sh"), "/sdcard/zoom_in.sh")
    device.push(resource_path("static/zoom_out.sh"), "/sdcard/zoom_out.sh")

# devic = adb_connect(0)
# get_screenshot(devic)
# click(devic, 761, 644)
# send_scripts(devic)
# zoom_out(devic)
# devic.disconnect()
