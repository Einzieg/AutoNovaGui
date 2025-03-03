import matplotlib.patches as patches
import matplotlib.pyplot as plt

# 屏幕尺寸
screen_width = 1920
screen_height = 1080

# 禁止点击区域的坐标
no_click_zones = [
    (0, 0, 500, 260),  # 左上角人物
    (1, 260, 140, 450),  # 任务
    (500, 0, 680, 130),  # 3D
    (800, 0, 1920, 100),  # 上方资源栏
    (1300, 100, 1920, 270),  # 右上角活动*3
    # (910, 0, 1920, 250),  # 右上角活动*5
    (1700, 270, 1920, 400),  # 极乐入口
    (0, 950, 1350, 1080),  # 下方聊天栏
    (1350, 870, 1920, 1080),  # 星云按钮
    (1450, 400, 1920, 580),  # 右侧活动及快捷菜单
    (1700, 580, 1920, 740),  # 右侧活动及快捷菜单
]

# 创建绘图
fig, ax = plt.subplots(figsize=(12, 7))

# 绘制禁止点击区域
for zone in no_click_zones:
    x1, y1, x2, y2 = zone
    width = x2 - x1
    height = y2 - y1
    rect = patches.Rectangle((x1, y1), width, height, linewidth=1, edgecolor='r', facecolor='r', alpha=0.5)
    ax.add_patch(rect)

# 设置坐标轴
ax.set_xlim([0, screen_width])
ax.set_ylim([0, screen_height])
# ax.set_title("No Click Zones on Screen")
# ax.set_xlabel("Width")
# ax.set_ylabel("Height")

# 反转Y轴
plt.gca().invert_yaxis()
plt.show()
