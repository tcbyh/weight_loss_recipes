# Weight Loss Recipes

## Intermittent Fasting (5+2) diet reference

![](assets/5+2_diet_reference.jpg)

## Data generation steps

**The annotations in the current captures directory have been manually adjusted, so remember to back them up before overwriting.**

| Step | Script | Status | Output Files | Remarks |
|------|--------|--------|-------|---------|
| 1 | detect_recipe_thumbnail.py | Done | captures/*.json | detect coarse bbox using cv2.findContours |
| 2 | [Manual] | Done | captures/*.json | adjust using labelme |
| 3 | adjust_with_xywh_stats.py | Done | captures/recipe_thumbnails.csv | adjust according to xywh stats |
| 4 | recognize_recipe_name.py | Done | recipes_crop_recog/*.png(json) | using paddleocr |
| 5 | resize_and_extract.py | Half-Done | recipes/recipe.csv | [cook/app/data/recipe.csv](https://github.com/YunYouJun/cook/blob/dev/app/data/recipe.csv?plain=1)


## Acknowledgement

- https://github.com/YunYouJun/cook
- https://github.com/Anduin2017/HowToCook
