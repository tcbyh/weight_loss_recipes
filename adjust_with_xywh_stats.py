import json
from collections import defaultdict, Counter
from pprint import pprint

import cv2
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # 设置后端为 Agg
import matplotlib.pyplot as plt


def cluster_ys(y_counter_items_sorted, delta_y_thr):

    clusters = []
    current_cluster = [y_counter_items_sorted[0]]

    for i in range(1, len(y_counter_items_sorted)):
        # 计算当前元素与前一个元素的差值
        assert y_counter_items_sorted[i][0] > y_counter_items_sorted[i-1][0], f'{y_counter_items_sorted[i][0] = }, {y_counter_items_sorted[i-1][0] = }'
        delta_y = y_counter_items_sorted[i][0] - y_counter_items_sorted[i-1][0]

        if delta_y <= delta_y_thr:
            current_cluster.append(y_counter_items_sorted[i])
        else:
            clusters.append(current_cluster)
            current_cluster = [y_counter_items_sorted[i]]

    clusters.append(current_cluster)  # 添加最后一个聚类
    return clusters


def main(capture_dir, vis_capture=False, vis_thumbnail=False):
    csv_res_file = Path(capture_dir) / 'recipe_thumbnails.csv'
    with open(csv_res_file, 'w') as f:
        f.write('capture,x,y,w,h\n')

    captures = sorted(Path(capture_dir).glob('*.jpg'))

    for capture in captures:
        print(capture.name)
        y_counter_in_capture = Counter()

        json_path = capture.with_suffix('.json')
        if not json_path.exists():
            continue

        if vis_capture or vis_thumbnail:
            img = cv2.imread(str(capture))
            print(img.shape)

        with open(json_path, 'r') as f:
            data = json.load(f)

        shapes = data['shapes']

        # cluster ys
        for shape in shapes:
            if shape['shape_type'] != 'rectangle':
                continue
            bbox = shape['points']
            y = bbox[0][1]
            y_counter_in_capture[y] += 1

        y_counter_in_capture = sorted(y_counter_in_capture.items(), key=lambda item: item[0])
        y_clusters = cluster_ys(y_counter_in_capture, 530)
        for cluster in y_clusters:
            if len(cluster) > 1:
                max_y = int(max(cluster, key=lambda item: item[0])[0])
                y_mapping = {y[0]: max_y for y in cluster}

        # mapping x, y, w, h
        for shape in shapes:
            if shape['shape_type'] != 'rectangle':
                continue

            bbox = shape['points']
            bbox = np.array(bbox, dtype=np.int32).flatten().tolist()
            x, y, x2, y2 = bbox
            w, h = x2 - x, y2 - y

            # set x, y, w, h according to stats -------------------------------
            w = h = 528
            x = 66 if x < 600 else 626
            y = y_mapping.get(y, y)
            x2 = x + w
            y2 = y + h
            # --------------------------------------------------------------

            if vis_thumbnail:
                recipe_thumbnail_img = img[y:y2, x:x2]
                cv2.imshow('recipe_thumbnail_img', recipe_thumbnail_img)
                cv2.waitKey(0)

            with open(csv_res_file, 'a') as f:
                f.write(f'{capture.name},{x},{y},{w},{h}\n')

        if vis_capture:
            for i in range(len(y_counter_in_capture) - 1):
                y0 = y_counter_in_capture[i][0]
                y1 = y_counter_in_capture[i+1][0]
                crop_img = img[y0-5:y1+5, :]
                cv2.imshow('img', crop_img)
                cv2.waitKey(0)

    if vis_capture or vis_thumbnail:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main('captures')
