import cv2

with open('recipes/recipe.csv', 'r') as f:
    for i, line in enumerate(f):
        if i == 0:
            continue
        name, stuff, bv, difficulty, tags, methods, tools = line.strip().split(',')
        img_path = f'recipes/{bv}'
        img = cv2.imread(img_path)
        print(name)
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()