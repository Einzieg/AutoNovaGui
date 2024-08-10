import logging
import os
import sys
import time

from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.exceptions import TcpTimeoutException

logging.basicConfig(level=logging.INFO)


# n = 6  # n为模拟器编号，初始为0


# device = AdbDeviceTcp('127.0.0.1', 16384 + 32 * n)

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def adb_connect(n):
    device = AdbDeviceTcp('127.0.0.1', 16384 + 32 * n)
    device.connect(read_timeout_s=30)
    return device


def get_screenshot(device):
    device.shell("screencap -p /sdcard/screenshot.png")
    device.pull('/sdcard/screenshot.png', 'screenshot.png')
    # time.sleep(1)  # 图片传输可能会有延迟


def swipe(device, start_x, start_y, end_x, end_y, duration):
    device.shell(f"input touchscreen swipe {start_x} {start_y} {end_x} {end_y} 200")


def zoom_out(device):
    logging.debug("zoom out")
    try:
        device.shell("sh /sdcard/zoom_out.sh", read_timeout_s=30)  # try running the script to pinchout
        # time.sleep(10)
        # device.shell("sh /sdcard/zoom_out.sh")
        # # time.sleep(10)
        # device.shell("sh /sdcard/zoom_out.sh")
    except TcpTimeoutException as e:
        logging.error(e)
        zoom_out(device)


def zoom_in(device):
    device.shell("sh /sdcard/zoom_in.sh")  # try running the script to zoomin
    time.sleep(3)


def up(device):
    device.shell("input swipe {} {} {} {}".format(1000, 200, 1000, 500))


def down(device):
    device.shell("input swipe {} {} {} {}".format(1000, 800, 1000, 500))


def click(device, x, y):
    device.shell("input tap {} {}".format(x, y))


# 把缩小和放大的脚本放到模拟器上
def send_scripts(device):
    logging.debug("send scripts")
    device.push(resource_path("static/zoom_in.sh"), "/sdcard/zoom_in.sh")
    device.push(resource_path("static/zoom_out.sh"), "/sdcard/zoom_out.sh")


devic = adb_connect(0)
# get_screenshot(device)
send_scripts(devic)
zoom_out(devic)
devic.close()
