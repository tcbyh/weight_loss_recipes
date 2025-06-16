import json
from pathlib import Path

import cv2
from tqdm import tqdm


recipes_crop_recog_dir = 'recipes_crop_recog'
recipes_dir = 'recipes'
recipes_csv_file = 'recipes/recipe.csv'

with open(recipes_csv_file, 'w') as f:
    f.write('name,stuff,bv,difficulty,tags,methods,tools\n')

recipe_img_paths = list(Path(recipes_crop_recog_dir).glob('*.png'))
for recipe_img_path in tqdm(recipe_img_paths):
    recipe_img_path2 = Path(recipes_dir) / recipe_img_path.name
    recipe_json_path = recipe_img_path.with_suffix('.json')
    with open(recipe_json_path, 'r') as f:
        recipe_json_data = json.load(f)
        recipe_name = ''.join(recipe_json_data['rec_texts'])

    recipe_img = cv2.imread(str(recipe_img_path))
    h, w, _ = recipe_img.shape
    recipe_img = cv2.resize(recipe_img, (w//2, h//2))
    cv2.imwrite(str(recipe_img_path2), recipe_img)
    with open(recipes_csv_file, 'a') as f:
        f.write(f'{recipe_name},,{recipe_img_path2.name},,,,\n')
