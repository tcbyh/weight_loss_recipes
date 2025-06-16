import json
from pathlib import Path

import cv2
import numpy as np


class LabelmeJsonData:
    def __init__(self):
        self.data = {
            "version": "5.8.1",
            "flags": {},
            "shapes": [],
            "imagePath": "",
            "imageData": None,
            "imageHeight": 40941,
            "imageWidth": 1220
        }

    def add_image_meta(self, image_path, image_height, image_width):
        self.data["imagePath"] = image_path
        self.data["imageHeight"] = image_height
        self.data["imageWidth"] = image_width

    def add_rectangle(self, rectangle, label="1"):
        self.data["shapes"].append({
            "label": label,
            "points": rectangle,
            "group_id": None,
            "description": "",
            "shape_type": "rectangle",
            "flags": {},
            "mask": None
        })

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.data, f)


def detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 应用二值化
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # 进行形态学操作，去除噪声
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    # 检测轮廓
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历轮廓，绘制矩形框
    bboxes = []
    for contour in contours:
        # 计算轮廓的边界框
        x, y, w, h = cv2.boundingRect(contour)
        x = x * 2.0
        y = y * 2.0
        w = w * 2.0
        h = h * 2.0

        # 过滤掉可能是文字的小轮廓
        # if 259 < w < 270 and 259 < h < 270:  # 根据实际情况调整大小阈值
        if w > 200 and h > 200 and 0.8 < w/h < 1.2:
            bboxes.append([[x, y], [x+w, y+h]])

    bboxes.sort(key=lambda bbox: bbox[0][1]*10000 + bbox[0][0])

    return image, bboxes


def main(captures_dir):
    captures = sorted(Path(captures_dir).glob('*.jpg'))

    all_bboxes = []

    for capture in captures:
        print(capture)
        capture_img = cv2.imread(str(capture))

        h, w, _ = capture_img.shape

        labelme_json_data = LabelmeJsonData()
        labelme_json_data.add_image_meta(capture.name, h, w)

        capture_img_resized = cv2.resize(capture_img, (w//2, h//2))

        gray_image = cv2.cvtColor(capture_img_resized, cv2.COLOR_BGR2GRAY)

        # 应用 Canny 边缘检测
        edges = cv2.Canny(gray_image, threshold1=100, threshold2=200)

        detected_image, bboxes = detect(capture_img_resized)

        for bbox in bboxes:
            labelme_json_data.add_rectangle(bbox)

        labelme_json_data.save(f'{captures_dir}/{capture.stem}.json')


if __name__ == '__main__':
    main('capture')
