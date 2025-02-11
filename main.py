import configparser
import ctypes
import inspect
import logging
import os
import sys
import threading
import time

from ttkbootstrap import *

from control import Control


# from control import main_loop


class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.yview(tk.END)

        self.text_widget.after(0, append)


def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class GuiApp:
    def __init__(self, root_app, level=logging.DEBUG):
        self.level = level
        self.log_text_handler = None
        self.root = root_app
        self.root.title("NovaAH")
        self.root.iconbitmap(resource_path("static/ico/auto.ico"))
        self.root.geometry("850x800")
        self.root.resizable(False, False)
        self.config_file = 'config.ini'
        self.setup_ui()
        self.running = False
        self.script_thread = None
        self.setup_logging()
        self.load_config()

    def setup_ui(self):
        self.start_image = tk.PhotoImage(file=resource_path("static/ico/start.png"))
        self.stop_image = tk.PhotoImage(file=resource_path("static/ico/stop.png"))

        self.start_button = self.__tk_button_start_btn(self.root)
        self.stop_button = self.__tk_button_stop_btn(self.root)
        self.stop_button.place_forget()  # 隐藏停止按钮
        self.__tk_button_toggle_log()

        self.log_text = self.__tk_text_window_log(self.root)
        self.config_frame = self.__tk_label_frame_lxq1wys2(self.root)

        # 配置
        self.virtual_num = tk.IntVar(value=0)
        self.offset = tk.IntVar(value=3)
        self.confidence = tk.DoubleVar(value=0.75)
        self.monster_confidence = tk.DoubleVar(value=0.65)
        self.corpse_confidence = tk.DoubleVar(value=0.65)
        self.hidden_interval = tk.IntVar(value=60)
        self.relogin_time = tk.IntVar(value=60)

        self.__tk_label_setting_virtual_num(self.config_frame)
        self.__tk_label_setting_confidence(self.config_frame)
        self.__tk_label_setting_monster_confidence(self.config_frame)
        self.__tk_label_setting_corpse_confidence(self.config_frame)
        self.__tk_label_setting_offset(self.config_frame)
        # self.__tk_label_hidden_interval(self.config_frame)
        self.__tk_label_setting_relogin_time(self.config_frame)
        self.__tk_input_get_setting_virtual_num(self.config_frame).config(textvariable=self.virtual_num)
        self.__tk_input_get_setting_confidence(self.config_frame).config(textvariable=self.confidence)
        self.__tk_input_get_setting_monster_confidence(self.config_frame).config(textvariable=self.monster_confidence)
        self.__tk_input_get_setting_corpse_confidence(self.config_frame).config(textvariable=self.corpse_confidence)
        self.__tk_input_get_setting_offset(self.config_frame).config(textvariable=self.offset)
        # self.__tk_label_get_setting_hidden_interval(self.config_frame).config(textvariable=self.hidden_interval)
        self.__tk_input_get_setting_relogin_time(self.config_frame).config(textvariable=self.relogin_time)

        self.run_options_frame = self.__tk_label_frame_run_choose(self.root)
        self.if_elite_monsters = tk.BooleanVar(value=True)
        self.if_normal_monster = tk.BooleanVar(value=False)
        self.if_wreckage = tk.BooleanVar(value=True)
        self.if_apocalypse = tk.BooleanVar(value=False)
        self.if_hidden = tk.BooleanVar(value=False)
        self.if_hidden_gec = tk.BooleanVar(value=False)
        self.if_order = tk.BooleanVar(value=False)
        self.if_relogin = tk.BooleanVar(value=True)

        self.__tk_check_button_if_elite_monsters(self.run_options_frame).config(variable=self.if_elite_monsters)
        self.__tk_check_button_if_normal_monster(self.run_options_frame).config(variable=self.if_normal_monster)
        self.__tk_check_button_if_wreckage(self.run_options_frame).config(variable=self.if_wreckage)
        self.__tk_check_button_if_apocalypse(self.run_options_frame).config(variable=self.if_apocalypse)
        self.__tk_check_button_if_hidden(self.run_options_frame).config(variable=self.if_hidden)
        self.__tk_check_button_if_hidden_gec(self.run_options_frame).config(variable=self.if_hidden_gec)
        self.__tk_check_button_if_orders(self.run_options_frame).config(variable=self.if_order)
        self.__tk_check_button_if_relogin(self.run_options_frame).config(variable=self.if_relogin)

    def toggle_log(self):
        if self.log_text.winfo_ismapped():
            self.log_text.place_forget()
            self.root.geometry("850x400")

        else:
            self.log_text.place(x=10, y=400, width=830, height=390)
            self.root.geometry("850x800")

    def __tk_button_toggle_log(self):
        btn = Button(self.root, text="显示/隐藏日志框", bootstyle="success-outline-toolbutton", command=self.toggle_log)
        btn.place(x=50, y=350, width=200, height=30)

    def __tk_button_start_btn(self, parent):
        # noinspection PyArgumentList
        btn = Button(parent, image=self.start_image, takefocus=False, bootstyle=(SUCCESS, OUTLINE), command=self.toggle_script)
        btn.place(x=50, y=150, width=200, height=100)  # Left side position
        return btn

    def __tk_button_stop_btn(self, parent):
        # noinspection PyArgumentList
        btn = Button(parent, image=self.stop_image, takefocus=False, bootstyle=(DANGER, OUTLINE), command=self.toggle_script)
        btn.place(x=50, y=150, width=200, height=100)  # Left side position
        return btn

    def __tk_text_window_log(self, parent):
        text = ScrolledText(parent, wrap=tk.WORD)
        text.place(x=10, y=400, width=830, height=390)
        return text

    def __tk_label_frame_lxq1wys2(self, parent):
        frame = LabelFrame(parent, text="启动参数")
        frame.place(x=300, y=10, width=300, height=380)
        return frame

    def __tk_label_setting_virtual_num(self, parent):
        label = Label(parent, text="模拟器编号", anchor="center")
        label.place(x=2, y=2, width=100, height=35)
        return label

    def __tk_label_setting_confidence(self, parent):
        label = Label(parent, text="通用置信度", anchor="center")
        label.place(x=2, y=40, width=100, height=35)
        return label

    def __tk_label_setting_monster_confidence(self, parent):
        label = Label(parent, text="野怪置信度", anchor="center")
        label.place(x=2, y=78, width=100, height=35)
        return label

    def __tk_label_setting_corpse_confidence(self, parent):
        label = Label(parent, text="残骸置信度", anchor="center")
        label.place(x=2, y=116, width=100, height=35)
        return label

    def __tk_label_setting_offset(self, parent):
        label = Label(parent, text="点击偏移量", anchor="center")
        label.place(x=2, y=154, width=100, height=35)
        return label

    def __tk_label_hidden_interval(self, parent):
        label = Label(parent, text="隐秘攻击间隔", anchor="center")
        label.place(x=2, y=192, width=100, height=35)
        return label

    def __tk_label_setting_relogin_time(self, parent):
        label = Label(parent, text="重登等待时长", anchor="center")
        label.place(x=2, y=192, width=100, height=35)
        return label

    def __tk_input_get_setting_virtual_num(self, parent):
        ipt = Entry(parent)
        ipt.place(x=110, y=2, width=180, height=35)
        return ipt

    def __tk_input_get_setting_confidence(self, parent):
        ipt = Entry(parent)
        ipt.place(x=110, y=40, width=180, height=35)
        return ipt

    def __tk_input_get_setting_monster_confidence(self, parent):
        ipt = Entry(parent)
        ipt.place(x=110, y=78, width=180, height=35)
        return ipt

    def __tk_input_get_setting_corpse_confidence(self, parent):
        ipt = Entry(parent)
        ipt.place(x=110, y=116, width=180, height=35)
        return ipt

    def __tk_input_get_setting_offset(self, parent):
        ipt = Entry(parent)
        ipt.place(x=110, y=154, width=180, height=35)
        return ipt

    def __tk_label_get_setting_hidden_interval(self, parent):
        label = Entry(parent)
        label.place(x=110, y=192, width=180, height=35)
        return label

    def __tk_input_get_setting_relogin_time(self, parent):
        ipt = Entry(parent)
        ipt.place(x=110, y=192, width=180, height=35)
        return ipt

    def __tk_label_frame_run_choose(self, parent):
        frame = LabelFrame(parent, text="运行选择")
        frame.place(x=610, y=10, width=230, height=380)
        return frame

    def __tk_check_button_if_elite_monsters(self, parent):
        cb = Checkbutton(parent, bootstyle="round-toggle", text="精英怪")
        cb.place(x=10, y=2, width=80, height=30)
        return cb

    def __tk_check_button_if_normal_monster(self, parent):
        cb = Checkbutton(parent, bootstyle="round-toggle", text="普通怪")
        cb.place(x=10, y=42, width=80, height=30)
        return cb

    def __tk_check_button_if_wreckage(self, parent):
        cb = Checkbutton(parent, bootstyle="round-toggle", text="残骸")
        cb.place(x=10, y=82, width=80, height=30)
        return cb

    def __tk_check_button_if_apocalypse(self, parent):
        cb = Checkbutton(parent, bootstyle="round-toggle", text="深红")
        cb.place(x=10, y=122, width=80, height=30)
        return cb

    def __tk_check_button_if_hidden(self, parent):
        cb = Checkbutton(parent, bootstyle="round-toggle", text="隐秘")
        cb.place(x=10, y=162, width=80, height=30)
        return cb

    def __tk_check_button_if_hidden_gec(self, parent):
        cb = Checkbutton(parent, bootstyle="round-toggle", text="使用GEC")
        cb.place(x=120, y=162, width=100, height=30)
        return cb

    def __tk_check_button_if_orders(self, parent):
        cb = Checkbutton(parent, bootstyle="round-toggle", text="订单")
        cb.place(x=10, y=202, width=80, height=30)
        return cb

    def __tk_check_button_if_relogin(self, parent):
        cb = Checkbutton(parent, bootstyle="round-toggle", text="重新登录")
        cb.place(x=10, y=242, width=100, height=30)
        return cb

    def setup_logging(self):
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        root_logger = logging.getLogger()
        root_logger.setLevel(self.level)

        log_file_handler = logging.FileHandler(filename=os.path.join(log_dir, f"AutoNova_{datetime.now().strftime('%Y-%m-%d')}.log"), mode='a', encoding='utf-8')
        log_file_handler.setFormatter(log_formatter)
        root_logger.addHandler(log_file_handler)

        self.log_text_handler = TextHandler(self.log_text)
        self.log_text_handler.setFormatter(log_formatter)
        root_logger.addHandler(self.log_text_handler)

    def toggle_script(self):
        if not self.running:
            self.start_script()
        else:
            self.stop_script()

    @staticmethod
    def _async_raise(tid, extype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(extype):
            extype = type(extype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(extype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def start_script(self):
        if not self.running:
            self.running = True
            self.save_config()
            self.script_thread = threading.Thread(target=self.run_script)
            self.script_thread.start()
            self.start_button.place_forget()
            self.stop_button.place(x=50, y=150, width=200, height=100)
            logging.info("开始执行>>>")

    def stop_script(self):
        if self.running:
            self.running = False
            self._async_raise(self.script_thread.ident, SystemExit)
            self.stop_button.place_forget()
            self.start_button.place(x=50, y=150, width=200, height=100)
            logging.info("执行结束<<<")
            self.save_config()

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            self.virtual_num.set(config.get('Settings', 'virtual_num', fallback=0))
            self.offset.set(config.getint('Settings', 'offset', fallback=3))
            self.confidence.set(config.getfloat('Settings', 'confidence', fallback=0.75))
            self.monster_confidence.set(config.getfloat('Settings', 'monster_confidence', fallback=0.65))
            self.corpse_confidence.set(config.getfloat('Settings', 'corpse_confidence', fallback=0.65))
            self.hidden_interval.set(config.getint('Settings', 'hidden_interval', fallback=90))
            self.relogin_time.set(config.getint('Settings', 'relogin_time', fallback=60))
            self.if_elite_monsters.set(config.getboolean('Settings', 'if_elite_monsters', fallback=True))
            self.if_normal_monster.set(config.getboolean('Settings', 'if_normal_monster', fallback=False))
            self.if_wreckage.set(config.getboolean('Settings', 'if_wreckage', fallback=True))
            self.if_apocalypse.set(config.getboolean('Settings', 'if_apocalypse', fallback=False))
            self.if_hidden.set(config.getboolean('Settings', 'if_hidden', fallback=False))
            self.if_hidden_gec.set(config.getboolean('Settings', 'if_hidden_gec', fallback=False))
            self.if_order.set(config.getboolean('Settings', 'if_order', fallback=False))
            self.if_relogin.set(config.getboolean('Settings', 'if_relogin', fallback=True))

    def save_config(self):
        config = configparser.ConfigParser()
        config['Settings'] = {
            'virtual_num': self.virtual_num.get(),
            'offset': self.offset.get(),
            'confidence': self.confidence.get(),
            'monster_confidence': self.monster_confidence.get(),
            'corpse_confidence': self.corpse_confidence.get(),
            'hidden_interval': self.hidden_interval.get(),
            'relogin_time': self.relogin_time.get(),
            'if_elite_monsters': self.if_elite_monsters.get(),
            'if_normal_monster': self.if_normal_monster.get(),
            'if_wreckage': self.if_wreckage.get(),
            'if_apocalypse': self.if_apocalypse.get(),
            'if_hidden': self.if_hidden.get(),
            'if_hidden_gec': self.if_hidden_gec.get(),
            'if_order': self.if_order.get(),
            'if_relogin': self.if_relogin.get()
        }
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def on_closing(self):
        self.save_config()
        self.root.destroy()  # 确保关闭窗口

    # 主函数
    def run_script(self):
        try:
            control = Control(game_virtual_num=self.virtual_num.get(),
                              game_offset=self.offset.get(),
                              game_confidence=self.confidence.get(),
                              game_monster_confidence=self.monster_confidence.get(),
                              game_corpse_confidence=self.corpse_confidence.get(),
                              game_relogin_time=self.relogin_time.get(),
                              game_if_elite_monster=self.if_elite_monsters.get(),
                              game_if_normal_monster=self.if_normal_monster.get(),
                              game_if_wreckage=self.if_wreckage.get(),
                              game_if_apocalypse=self.if_apocalypse.get(),
                              game_if_hidden=self.if_hidden.get(),
                              game_if_hidden_gec=self.if_hidden_gec.get(),
                              game_if_orders=self.if_order.get(),
                              game_if_relogin=self.if_relogin.get(),
                              )
            while self.running:
                control.main_loop()
                time.sleep(3)
        except ConnectionError as e:
            logging.error(f"连接模拟器失败: {e}")
            self.stop_button.place_forget()
            self.start_button.place(x=50, y=150, width=200, height=100)
        except Exception as e:
            logging.error(f"主函数异常: {e}")
            self.stop_button.place_forget()
            self.start_button.place(x=50, y=150, width=200, height=100)


if __name__ == "__main__":
    root = Window(themename='darkly')
    app = GuiApp(root, level=logging.DEBUG)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # 在窗口关闭时保存配置并关闭窗口
    root.mainloop()
