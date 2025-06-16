import os
from pathlib import Path

import cv2

from paddleocr import PaddleOCR
# 初始化 PaddleOCR 实例
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False)

capture_dir = 'captures'
recipe_thumbnails_csv_file = Path(capture_dir) / 'recipe_thumbnails.csv'
outptu_dir = 'recipes_crop_recog'

with open(recipe_thumbnails_csv_file, 'r') as f:
    for i, line in enumerate(f):
        if i == 0:
            continue
        capture, x, y, w, h = line.strip().split(',')
        file_name = '_'.join([capture.split('.')[0], 'x', x, 'y', y, 'w', w, 'h', h])
        x, y, w, h = int(x), int(y), int(w), int(h)
        img = cv2.imread(os.path.join(capture_dir, capture))
        recipe_thumbnail_img = img[y:y+h, x:x+w]
        recipe_name_img = img[y+h: y+h+180, x:x+w]
        cv2.imwrite(f'{outptu_dir}/{file_name}.png', recipe_thumbnail_img)

        result = ocr.predict(input=recipe_name_img)
        for res in result:
            res.save_to_json(f'{outptu_dir}/{file_name}.json')
        print(f'{file_name} done')