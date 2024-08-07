import threading
import time

from adb_shell.adb_device import AdbDeviceTcp

n = 6  # n为模拟器编号，初始为0

device = AdbDeviceTcp('127.0.0.1', 16384 + 32 * n)
device.connect()


def get_screenshot():
    device.shell("screencap -p /sdcard/screenshot.png")
    device.pull('/sdcard/screenshot.png', 'screenshot.png')
    time.sleep(1)  # 图片传输可能会有延迟


# 缩小屏幕(半有效，但有多线程超时问题)
def shrink_screen():
    for i in range(0, 3):
        threads = []
        script_thread_up = threading.Thread(target=up)
        script_thread_down = threading.Thread(target=down)
        threads.append(script_thread_up)
        threads.append(script_thread_down)

        for t in threads:
            t.start()

        time.sleep(3)

        for t in threads:
            t.join()

        time.sleep(3)


def up():
    device.shell("input swipe {} {} {} {}".format(1000, 200, 1000, 500))


def down():
    device.shell("input swipe {} {} {} {}".format(1000, 800, 1000, 500))


def click(x, y):
    device.shell("input tap {} {}".format(x, y))


# 缩小屏幕，无效果，可能哪里写错了
def send_event():
    device.shell("sendevent /dev/input/event4 3 57 0")
    device.shell("sendevent /dev/input/event4 3 53 300")
    device.shell("sendevent /dev/input/event4 3 54 800")
    device.shell("sendevent /dev/input/event4 0 0 0")

    device.shell("sendevent /dev/input/event4 3 57 1")
    device.shell("sendevent /dev/input/event4 3 53 800")
    device.shell("sendevent /dev/input/event4 3 54 800")
    device.shell("sendevent /dev/input/event4 0 0 0")

    device.shell("sendevent /dev/input/event4 3 53 350")
    device.shell("sendevent /dev/input/event4 3 54 800")

    device.shell("sendevent /dev/input/event4 3 57 0")
    device.shell("sendevent /dev/input/event4 3 53 750")
    device.shell("sendevent /dev/input/event4 3 54 800")
    device.shell("sendevent /dev/input/event4 3 57 1")
    device.shell("sendevent /dev/input/event4 0 0 0")

    device.shell("sendevent /dev/input/event4 3 53 400")
    device.shell("sendevent /dev/input/event4 3 54 800")
    device.shell("sendevent /dev/input/event4 3 57 0")
    device.shell("sendevent /dev/input/event4 3 53 700")
    device.shell("sendevent /dev/input/event4 3 54 800")
    device.shell("sendevent /dev/input/event4 3 57 1")
    device.shell("sendevent /dev/input/event4 0 0 0")

    device.shell("sendevent /dev/input/event4 3 57 4294967295")
    device.shell("sendevent /dev/input/event4 0 0 0")

    device.shell("sendevent /dev/input/event4 3 57 4294967295")
    device.shell("sendevent /dev/input/event4 0 0 0")


# 缩小屏幕，无效果，阻塞执行
def move_screen():
    device.shell("input touchscreen swipe 1000 200 1000 500")
    device.shell("input touchscreen swipe 1000 800 1000 500")


# get_screenshot(device)
# shrink_screen()
# send_event()
move_screen()
# click(1510, 955, 1)

device.close()
