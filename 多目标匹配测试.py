import time

import cv2
import numpy as np

from Adbutils import adb_connect, get_screenshot, click

template = cv2.imread("static/novaimgs/acquisition/elite_wreckage.png")
# device = adb_connect(0)
# get_screenshot(device)


def non_max_suppression(boxes, scores, overlap_thresh=0.3):
    if len(boxes) == 0:
        return []

    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float32")

    idx_ls = np.argsort(scores)[::-1]

    pick = []

    while len(idx_ls) > 0:
        i = idx_ls[0]
        pick.append(i)

        suppress = [i]
        for pos in range(1, len(idx_ls)):
            j = idx_ls[pos]
            xx1 = max(boxes[i][0], boxes[j][0])
            yy1 = max(boxes[i][1], boxes[j][1])
            xx2 = min(boxes[i][0] + boxes[i][2], boxes[j][0] + boxes[j][2])
            yy2 = min(boxes[i][1] + boxes[i][3], boxes[j][1] + boxes[j][3])

            w = max(0, xx2 - xx1)
            h = max(0, yy2 - yy1)
            inter_area = w * h

            box_area = (boxes[i][2] * boxes[i][3])
            box_area2 = (boxes[j][2] * boxes[j][3])

            # 计算重叠比率
            overlap = inter_area / float(box_area + box_area2 - inter_area)

            # 如果重叠度大于阈值, 进行抑制
            if overlap > overlap_thresh:
                suppress.append(j)

        # 删除已经抑制的框 移除 suppress 中的索引
        idx_ls = [idx for idx in idx_ls if idx not in suppress]

    return pick


def get_coordinate(template, believe):
    original = cv2.imread("screenshot.png")
    img = cv2.imread("screenshot.png")
    h, w = template.shape[:2]
    ret = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # 筛选出匹配程度大于 believe 的坐标
    threshold = believe
    locations = np.where(ret >= threshold)
    boxes = []

    # 构建候选框，记录每个框的位置和分数
    for pt in zip(*locations[::-1]):
        boxes.append([pt[0], pt[1], w, h])

    result = []

    # 使用 NMS 进行重叠去除
    if len(boxes) > 0:
        boxes = np.array(boxes)
        scores = ret[locations]
        picks = non_max_suppression(boxes, scores)

        # 绘制矩形框
        for pick in picks:
            pt = boxes[pick]
            result.append([pt[0], pt[1]])
            cv2.rectangle(original, (pt[0], pt[1]), (pt[0] + pt[2], pt[1] + pt[3]), (0, 0, 255), 1)

    print(result)
    # 显示结果图像
    cv2.imshow('rect', original)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return result


def move_coordinates(results):
    new_coordinates = [results[0]]
    target = [960, 540]
    # 计算第一个坐标移动到目标点的偏移
    offset = [target[0] - results[0][0], target[1] - results[0][1]]

    for res in range(1, len(results)):
        new_x = results[res][0] + offset[0]
        new_y = results[res][1] + offset[1]
        if new_x <= 1920 and new_y <= 1080:
            new_coordinates.append([new_x, new_y])
        offset = [target[0] - result[res][0], target[1] - result[res][1]]
    print(new_coordinates)
    return new_coordinates


result = get_coordinate(template, 0.73)
res2 = move_coordinates(result)

# for i in res2:
#     get_screenshot(device)
#     original = cv2.imread("screenshot.png")
#     cv2.rectangle(original, (i[0]-8, i[1]-9), (i[0] + 10, i[1] + 10), (0, 0, 255), 1)
#     cv2.imshow('rect', original)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     click(device, i)
#     time.sleep(2)
