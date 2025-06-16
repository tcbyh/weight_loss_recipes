import cv2
import os

capture_dir = 'capture_recipe_thumbnail'

with open('recipe_thumbnails.csv', 'r') as f:
    for i, line in enumerate(f):
        if i == 0:
            continue
        capture, x, y, w, h = line.strip().split(',')
        x, y, w, h = int(x), int(y), int(w), int(h)
        img = cv2.imread(os.path.join(capture_dir, capture))

        recipe_thumbnail_img = img[y:y+h+180, x:x+w]
        cv2.imshow('recipe_thumbnail_img', recipe_thumbnail_img)
        cv2.waitKey(0)

cv2.destroyAllWindows()