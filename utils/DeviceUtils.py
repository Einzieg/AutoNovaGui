import logging

from msc.minicap import MiniCap
from msc.mumu import MuMuScreenCap, get_mumu_path
from mtc.mumu import MuMuTouch
from path_util import resource_path
from AdbClient import AdbClient


class DeviceUtils:
    def __init__(self, ip="127.0.0.1", port=5555, instance_index=None, mumu_path=None):
        """
        初始化DeviceUtils实例。
        :param ip: 设备IP地址，默认为"127.0.0.1"。
        :param port: 设备端口号，默认为5555。
        :param instance_index: 实例索引，用于计算多开设备的端口号，默认为None。
        """
        self.ip = ip
        self.port = port
        self.instance_index = instance_index

        if instance_index is not None:
            self.port = 16384 + 32 * instance_index
            logging.info(f"计算端口号为 {self.port}")

        if mumu_path:
            self.mumu_path = mumu_path
            logging.info(f"使用 mumu_path: {self.mumu_path}")
        else:
            self.mumu_path = None
            logging.info(f"未设置 mumu_path,获取路径: {get_mumu_path()}")

        # 初始化 ADB 客户端并保持连接
        self.adb = AdbClient(ip=self.ip, port=self.port)

    def adb_shell(self, command):
        """执行ADB shell命令"""
        try:
            return self.adb.shell(command)
        except Exception as e:
            logging.error(f"执行命令 {command} 时出错: {str(e)}")
            raise

    def push_scripts(self):
        """推送脚本文件到设备"""
        try:
            self.adb.push(resource_path("static/zoom_in.sh"), "/sdcard/zoom_in.sh")
            self.adb.push(resource_path("static/zoom_out.sh"), "/sdcard/zoom_out.sh")
            logging.debug("脚本文件推送成功")
        except Exception as e:
            logging.error(f"推送脚本文件时出错: {str(e)}")
            raise

    def click_back(self):
        """模拟点击返回键"""
        try:
            self.adb.shell("input keyevent 4")
            logging.debug("已点击返回键")
        except Exception as e:
            logging.error(f"点击返回键时出错: {str(e)}")
            raise

    def zoom_out(self):
        """执行缩放操作"""
        try:
            self.adb.shell("sh /sdcard/zoom_out.sh")
            logging.debug("已执行缩放操作")
        except Exception as e:
            logging.error(f"执行缩放操作时出错: {str(e)}")
            raise

    def mumu_screencap(self, file_name: str = "screenshot.png"):
        """使用MuMu进行屏幕截图"""
        try:
            if self.mumu_path:
                mumu = MuMuScreenCap(instance_index=self.instance_index, emulator_install_path=self.mumu_path)
            else:
                mumu = MuMuScreenCap(self.instance_index)
            mumu.save_screencap(file_name)
            logging.debug(f"屏幕截图保存为 {file_name}")
        except Exception as e:
            logging.error(f"使用MuMu进行屏幕截图时出错: {str(e)}")
            raise

    def minicap_screencap(self, file_name: str = "screenshot.png"):
        """
        使用Minicap进行屏幕截图（较慢，非必要不用）
        :param file_name: 保存的文件名，默认为"screenshot.png"
        """
        try:
            minicap = MiniCap(f"{self.ip}:{self.port}")
            minicap.save_screencap(file_name)
            logging.debug(f"屏幕截图保存为 {file_name}")
        except Exception as e:
            logging.error(f"使用Minicap进行屏幕截图时出错: {str(e)}")
            raise

    def mumu_click(self, coordinates):
        """使用MuMu进行点击操作"""
        x, y = coordinates
        try:
            if self.mumu_path:
                mumu = MuMuTouch(instance_index=self.instance_index, emulator_install_path=self.mumu_path)
            else:
                mumu = MuMuTouch(self.instance_index)
            mumu.click(x, y)
            logging.debug(f"已点击坐标 ({x}, {y})")
        except Exception as e:
            logging.error(f"点击坐标 ({x}, {y}) 时出错: {str(e)}")
            raise

# if __name__ == "__main__":
#     try:
#         device = DeviceUtils(instance_index=0)
#         device.mumu_screencap("screenshot.png")
#     except Exception as e:
#         logging.error(f"操作失败: {str(e)}")
