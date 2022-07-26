import cv2
import numpy as np
from random import randint
import random

def readimg(img):
    return cv2.imread(img)

def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

def gbr2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def get_mean_color(img, cell):
    r = 0
    g = 0
    b = 0
    for x in range(cell[1]-cell[0]):
        for y in range(cell[3]-cell[2]):
            r += img[cell[0]:cell[1], cell[2]:cell[3]][x][y][0]
            g += img[cell[0]:cell[1], cell[2]:cell[3]][x][y][1]
            b += img[cell[0]:cell[1], cell[2]:cell[3]][x][y][2]
    
    r = int(r/((cell[1]-cell[0])*(cell[3]-cell[2])))
    g = int(g/((cell[1]-cell[0])*(cell[3]-cell[2])))
    b = int(b/((cell[1]-cell[0])*(cell[3]-cell[2])))
    return (r,g,b)

def put_stroke(img, position, color):
    xs = position[0]
    xf = position[1]
    ys = position[2]
    yf = position[3]

    percent1 = 3
    percent2 = 5
    
    if position[0] - int((position[0]/100)*percent1) > 0:
        xs = position[0] - int((position[0]/100)*percent1)
    else:
        if position[0] - int((position[0]/100)*percent2) > 0:
            xs = position[0] - int((position[0]/100)*percent2)

    if position[1] + int((position[1]/100)*percent1) < img.shape[0]:
        xf = position[1] + int((position[1]/100)*percent1)
    else:
        if position[1] + int((position[1]/100)*percent2) < img.shape[0]:
            xf = position[1] + int((position[1]/100)*percent2)

    if position[2] - int((position[2]/100)*percent1) > 0:
        ys = position[2] - int((position[2]/100)*percent1)
    else:
        if position[2] - int((position[2]/100)*percent2) > 0:
            ys = position[2] - int((position[2]/100)*percent2)

    if position[3] + int((position[3]/100)*percent1) < img.shape[1]:
        yf = position[3] + int((position[3]/100)*percent1)
    else:
        if position[3] + int((position[3]/100)*percent2) < img.shape[1]:
            yf = position[3] + int((position[3]/100)*percent2)


    position = [xs, xf, ys, yf]
    x = (position[1]-position[0])
    y = (position[3]-position[2])
    brush = readimg(get_random_brush())

    (h, w) = brush.shape[:2]
    center = (w / 2, h / 2)
    angles = [30, 60, 90, 120, 150, 180]
    angle = random.choice(angles)
    scale = 1
    M = cv2.getRotationMatrix2D(center, angle, scale)
    brush = cv2.warpAffine(brush, M, (w, h))

    # resize brush
    brush = cv2.resize(brush, (y, x))
    brush_g = cv2.cvtColor(brush, cv2.COLOR_BGR2GRAY)
    brush2 = np.zeros_like(brush, np.uint8)
    mask = cv2.inRange(brush_g, 0, 100)
    brush2[mask == 0] = color
    shapes = np.zeros_like(img, np.uint8)

    # Overlay
    shapes[position[0]:position[1], position[2]:position[3]] = brush2
    mask = shapes.astype(bool)
    bg_img = img.copy()
    bg_img[mask] = cv2.addWeighted(bg_img, 0 , shapes, 1, 0)[mask]

    return bg_img


def get_4cell(cell):
    sx = cell[0]
    fx = cell[1]
    sy = cell[2] 
    fy = cell[3]
    y = fy - sy
    x = fx - sx
    cells = [
        [sx, sx+int(x/2), sy, sy+int(y/2)],
        [sx, sx+int(x/2), sy+int(y/2), fy],
        [sx+int(x/2), fx, sy, sy+int(y/2)],
        [sx+int(x/2), fx, sy+int(y/2), fy],
    ]
    return cells


def get_random_brush():
    brushes = [ "brushes/brush2.png", "brushes/brush3.png", "brushes/brush4.png", "brushes/brush6.png", "brushes/brush7.png"]
    #brushes = ["brushes/brush4.png", "brushes/brush6.png", "brushes/brush7.png"]
    #brushes = ["brushes/brush2.png"]
    return random.choice(brushes)
    

def imborder(im, bordersize=50):
    row, col = im.shape[:2]
    bottom = im[row-2:row, 0:col]
    mean = cv2.mean(bottom)[0]

    border = cv2.copyMakeBorder(
        im,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[mean, mean, mean]
    )

    return border