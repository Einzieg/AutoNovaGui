import time

from adb_shell.adb_device import AdbDeviceTcp


# n = 6  # n为模拟器编号，初始为0


# device = AdbDeviceTcp('127.0.0.1', 16384 + 32 * n)

def adb_connect(n):
    device = AdbDeviceTcp('127.0.0.1', 16384 + 32 * n)
    device.connect()
    return device


def get_screenshot(device):
    device.shell("screencap -p /sdcard/screenshot.png")
    device.pull('/sdcard/screenshot.png', 'screenshot.png')
    time.sleep(1)  # 图片传输可能会有延迟


def swipe(device, start_x, start_y, end_x, end_y, duration):
    device.shell(f"input touchscreen swipe {start_x} {start_y} {end_x} {end_y} 200")


def zoom_out(device):
    device.shell("sh /sdcard/zoom_out.sh")  # try running the script to pinchout
    time.sleep(6)


def zoom_in(device):
    device.shell("sh /sdcard/zoom_in.sh")  # try running the script to zoomin
    time.sleep(6)


def up(device):
    device.shell("input swipe {} {} {} {}".format(1000, 200, 1000, 500))


def down(device):
    device.shell("input swipe {} {} {} {}".format(1000, 800, 1000, 500))


def click(device, x, y):
    device.shell("input tap {} {}".format(x, y))


# 把缩小和放大的脚本放到模拟器上
def send_scripts(device):
    device.push("zoom_in.sh", "/sdcard/zoom_in.sh")
    device.push("zoom_out.sh", "/sdcard/zoom_out.sh")


# device = adb_connect(0)
# send_scripts()
# get_screenshot(device)
# move_screen()
# zoom_in(device)
# zoom_out()
# click(1510, 955, 1)
# device.close()
