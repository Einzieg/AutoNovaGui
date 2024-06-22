"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
# from tkinter import *
from ttkbootstrap import *


class WinGUI(Window):
    def __init__(self):
        super().__init__()
        self.__win()
        self.iconbitmap("static/ico/auto.ico")
        self.tk_button_start_btn = self.__tk_button_start_btn(self)
        self.tk_button_stop_btn = self.__tk_button_stop_btn(self)
        self.tk_text_window_log = self.__tk_text_window_log(self)
        self.tk_label_frame_lxq1wys2 = self.__tk_label_frame_lxq1wys2(self)
        self.tk_label_setting_window_name = self.__tk_label_setting_windie_name(self.tk_label_frame_lxq1wys2)
        self.tk_label_setting_confidence = self.__tk_label_setting_confidence(self.tk_label_frame_lxq1wys2)
        self.tk_label_setting_monster_confidence = self.__tk_label_setting_monster_confidence(
            self.tk_label_frame_lxq1wys2)
        self.tk_label_setting_corpse_confidence = self.__tk_label_setting_corpse_confidence(
            self.tk_label_frame_lxq1wys2)
        self.tk_label_setting_offset = self.__tk_label_setting_offset(self.tk_label_frame_lxq1wys2)
        self.tk_input_get_setting_window_name = self.__tk_input_get_setting_windie_name(self.tk_label_frame_lxq1wys2)
        self.tk_input_get_setting_confidence = self.__tk_input_get_setting_confidence(self.tk_label_frame_lxq1wys2)
        self.tk_input_get_setting_monster_confidence = self.__tk_input_get_setting_monster_confidence(
            self.tk_label_frame_lxq1wys2)
        self.tk_input_get_setting_corpse_confidence = self.__tk_input_get_setting_corpse_confidence(
            self.tk_label_frame_lxq1wys2)
        self.tk_input_get_setting_offset = self.__tk_input_get_setting_offset(self.tk_label_frame_lxq1wys2)
        self.tk_label_frame_lxq2hcjy = self.__tk_label_frame_lxq2hcjy(self)
        self.tk_check_button_if_elite_monsters = self.__tk_check_button_if_elite_monsters(self.tk_label_frame_lxq2hcjy)
        self.tk_check_button_if_normal_monster = self.__tk_check_button_if_normal_monster(self.tk_label_frame_lxq2hcjy)
        self.tk_check_button_if_apocalypse = self.__tk_check_button_if_apocalypse(self.tk_label_frame_lxq2hcjy)
        self.tk_check_button_if_wreckage = self.__tk_check_button_if_wreckage(self.tk_label_frame_lxq2hcjy)

    def __win(self):
        self.title("AutoNova")
        # 设置窗口大小、居中
        width = 500
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""

        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)

        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)

        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_button_start_btn(self, parent):
        btn = Button(parent, text="开始", takefocus=False, bootstyle=(SUCCESS, OUTLINE))
        btn.place(x=50, y=50, width=150, height=50)
        return btn

    def __tk_button_stop_btn(self, parent):
        btn = Button(parent, text="停止", takefocus=False, bootstyle=(DANGER, OUTLINE))
        btn.place(x=50, y=150, width=150, height=50)
        return btn

    def __tk_text_window_log(self, parent):
        text = Text(parent)
        text.place(x=0, y=300, width=500, height=201)
        return text

    def __tk_label_frame_lxq1wys2(self, parent):
        frame = LabelFrame(parent, text="启动参数", )
        frame.place(x=290, y=10, width=200, height=170)
        return frame

    def __tk_label_setting_windie_name(self, parent):
        label = Label(parent, text="窗口名称", anchor="center", )
        label.place(x=2, y=2, width=60, height=26)
        return label

    def __tk_label_setting_confidence(self, parent):
        label = Label(parent, text="通用置信", anchor="center", )
        label.place(x=2, y=32, width=60, height=26)
        return label

    def __tk_label_setting_monster_confidence(self, parent):
        label = Label(parent, text="野怪置信", anchor="center", )
        label.place(x=2, y=62, width=60, height=26)
        return label

    def __tk_label_setting_corpse_confidence(self, parent):
        label = Label(parent, text="残骸置信", anchor="center", )
        label.place(x=2, y=92, width=60, height=26)
        return label

    def __tk_label_setting_offset(self, parent):
        label = Label(parent, text="偏移量", anchor="center", )
        label.place(x=2, y=122, width=60, height=26)
        return label

    def __tk_input_get_setting_windie_name(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=65, y=2, width=120, height=26)
        # ipt.insert(0, "Space Armada")
        return ipt

    def __tk_input_get_setting_confidence(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=65, y=32, width=120, height=26)
        ipt.insert(0, "0.7")
        return ipt

    def __tk_input_get_setting_monster_confidence(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=65, y=62, width=120, height=26)
        ipt.insert(0, "0.65")
        return ipt

    def __tk_input_get_setting_corpse_confidence(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=65, y=92, width=120, height=26)
        ipt.insert(0, "0.65")
        return ipt

    def __tk_input_get_setting_offset(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=65, y=122, width=120, height=26)
        ipt.insert(0, "3")
        return ipt

    def __tk_label_frame_lxq2hcjy(self, parent):
        frame = LabelFrame(parent, text="运行选择", )
        frame.place(x=290, y=190, width=200, height=100)
        return frame

    def __tk_check_button_if_elite_monsters(self, parent):
        cb = Checkbutton(parent, text="精英怪", )
        cb.place(x=5, y=2, width=80, height=30)
        return cb

    def __tk_check_button_if_normal_monster(self, parent):
        cb = Checkbutton(parent, text="普通怪", )
        cb.place(x=110, y=2, width=80, height=30)
        return cb

    def __tk_check_button_if_apocalypse(self, parent):
        cb = Checkbutton(parent, text="天启", )
        cb.place(x=5, y=50, width=80, height=30)
        return cb

    def __tk_check_button_if_wreckage(self, parent):
        cb = Checkbutton(parent, text="残骸", )
        cb.place(x=110, y=50, width=80, height=30)
        return cb


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)

    def __event_bind(self):
        self.tk_button_start_btn.bind('<Button>', self.ctl.start)
        self.tk_button_stop_btn.bind('<Button>', self.ctl.stop)
        pass

    def __style_config(self):
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
