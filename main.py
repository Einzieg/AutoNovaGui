from control import Controller as MainUIController
from ui import Win as MainWin

running = False

app = MainWin(MainUIController())
if __name__ == "__main__":
    # 启动
    app.mainloop()


