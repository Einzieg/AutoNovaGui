import ctypes
import inspect
import logging
import os
import threading
import time
from tkinter import scrolledtext

from ttkbootstrap import *

from control import initialize
from control import main_loop
from control import resource_path


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


class GuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoNovaGui")
        self.root.iconbitmap(resource_path("static/ico/auto.ico"))
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        self.setup_ui()
        self.running = False
        self.script_thread = None
        self.setup_logging()

    def setup_ui(self):
        self.start_image = tk.PhotoImage(file=resource_path("static/ico/start.png"))
        self.stop_image = tk.PhotoImage(file=resource_path("static/ico/stop.png"))

        self.start_button = self.__tk_button_start_btn(self.root)
        self.stop_button = self.__tk_button_stop_btn(self.root)
        self.stop_button.place_forget()  # 隐藏停止按钮

        self.log_text = self.__tk_text_window_log(self.root)
        self.config_frame = self.__tk_label_frame_lxq1wys2(self.root)

        # 配置
        self.window_name = tk.StringVar(value='Space Armada')
        self.offset = tk.DoubleVar(value=3)
        self.confidence = tk.DoubleVar(value=0.75)
        self.monster_confidence = tk.DoubleVar(value=0.65)
        self.corpse_confidence = tk.DoubleVar(value=0.65)

        self.__tk_label_setting_window_name(self.config_frame)
        self.__tk_label_setting_confidence(self.config_frame)
        self.__tk_label_setting_monster_confidence(self.config_frame)
        self.__tk_label_setting_corpse_confidence(self.config_frame)
        self.__tk_label_setting_offset(self.config_frame)
        self.__tk_input_get_setting_window_name(self.config_frame).config(textvariable=self.window_name)
        self.__tk_input_get_setting_confidence(self.config_frame).config(textvariable=self.confidence)
        self.__tk_input_get_setting_monster_confidence(self.config_frame).config(textvariable=self.monster_confidence)
        self.__tk_input_get_setting_corpse_confidence(self.config_frame).config(textvariable=self.corpse_confidence)
        self.__tk_input_get_setting_offset(self.config_frame).config(textvariable=self.offset)

        self.run_options_frame = self.__tk_label_frame_run_choose(self.root)
        self.if_elite_monsters = tk.BooleanVar(value=True)
        self.if_normal_monster = tk.BooleanVar(value=False)
        self.if_wreckage = tk.BooleanVar(value=True)
        self.if_apocalypse = tk.BooleanVar(value=False)
        self.if_hidden = tk.BooleanVar(value=False)
        self.if_order = tk.BooleanVar(value=False)

        self.__tk_check_button_if_elite_monsters(self.run_options_frame).config(variable=self.if_elite_monsters)
        self.__tk_check_button_if_normal_monster(self.run_options_frame).config(variable=self.if_normal_monster)
        self.__tk_check_button_if_wreckage(self.run_options_frame).config(variable=self.if_wreckage)
        self.__tk_check_button_if_apocalypse(self.run_options_frame).config(variable=self.if_apocalypse)
        self.__tk_check_button_if_hidden(self.run_options_frame).config(variable=self.if_hidden)
        self.__tk_check_button_if_orders(self.run_options_frame).config(variable=self.if_order)

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
        text = scrolledtext.ScrolledText(parent, wrap=tk.WORD)
        text.place(x=10, y=400, width=780, height=390)
        return text

    def __tk_label_frame_lxq1wys2(self, parent):
        frame = LabelFrame(parent, text="启动参数")
        frame.place(x=300, y=3, width=490, height=221)
        return frame

    def __tk_label_setting_window_name(self, parent):
        label = Label(parent, text="窗口名称", anchor="center")
        label.place(x=2, y=2, width=80, height=35)
        return label

    def __tk_label_setting_confidence(self, parent):
        label = Label(parent, text="通用置信", anchor="center")
        label.place(x=2, y=40, width=80, height=35)
        return label

    def __tk_label_setting_monster_confidence(self, parent):
        label = Label(parent, text="野怪置信", anchor="center")
        label.place(x=2, y=78, width=80, height=35)
        return label

    def __tk_label_setting_corpse_confidence(self, parent):
        label = Label(parent, text="残骸置信", anchor="center")
        label.place(x=2, y=116, width=80, height=35)
        return label

    def __tk_label_setting_offset(self, parent):
        label = Label(parent, text="偏移量", anchor="center")
        label.place(x=2, y=154, width=80, height=35)
        return label

    def __tk_input_get_setting_window_name(self, parent):
        ipt = Entry(parent)
        ipt.place(x=90, y=2, width=200, height=35)
        return ipt

    def __tk_input_get_setting_confidence(self, parent):
        ipt = Entry(parent)
        ipt.place(x=90, y=40, width=200, height=35)
        return ipt

    def __tk_input_get_setting_monster_confidence(self, parent):
        ipt = Entry(parent)
        ipt.place(x=90, y=78, width=200, height=35)
        return ipt

    def __tk_input_get_setting_corpse_confidence(self, parent):
        ipt = Entry(parent)
        ipt.place(x=90, y=116, width=200, height=35)
        return ipt

    def __tk_input_get_setting_offset(self, parent):
        ipt = Entry(parent)
        ipt.place(x=90, y=154, width=200, height=35)
        return ipt

    def __tk_label_frame_run_choose(self, parent):
        frame = LabelFrame(parent, text="运行选择")
        frame.place(x=300, y=236, width=490, height=150)
        return frame

    def __tk_check_button_if_elite_monsters(self, parent):
        cb = Checkbutton(parent, text="精英怪")
        cb.place(x=10, y=2, width=80, height=30)
        return cb

    def __tk_check_button_if_normal_monster(self, parent):
        cb = Checkbutton(parent, text="普通怪")
        cb.place(x=110, y=2, width=80, height=30)
        return cb

    def __tk_check_button_if_wreckage(self, parent):
        cb = Checkbutton(parent, text="残骸")
        cb.place(x=210, y=2, width=80, height=30)
        return cb

    def __tk_check_button_if_apocalypse(self, parent):
        cb = Checkbutton(parent, text="深红")
        cb.place(x=310, y=2, width=80, height=30)
        return cb

    def __tk_check_button_if_hidden(self, parent):
        cb = Checkbutton(parent, text="隐秘")
        cb.place(x=10, y=32, width=80, height=30)
        return cb

    def __tk_check_button_if_orders(self, parent):
        cb = Checkbutton(parent, text="订单")
        cb.place(x=110, y=32, width=80, height=30)
        return cb

    def setup_logging(self):
        log_dir = 'AutoNova-log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

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

    # 主函数
    def run_script(self):
        try:
            initialize(self.window_name.get(),
                       self.offset.get(),
                       self.confidence.get(),
                       self.monster_confidence.get(),
                       self.corpse_confidence.get(),
                       self.if_elite_monsters.get(),
                       self.if_normal_monster.get(),
                       self.if_wreckage.get(),
                       self.if_apocalypse.get(),
                       self.if_hidden.get(),
                       self.if_order.get()
                       )
            time.sleep(6)
            while self.running:
                main_loop()
                time.sleep(3)
        except Exception as e:
            logging.error(f"主函数异常: {e}")


if __name__ == "__main__":
    root = Window(themename='darkly')
    app = GuiApp(root)
    root.mainloop()
