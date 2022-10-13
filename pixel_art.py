from collections import defaultdict
from scipy import stats
import numpy as np
import cv2


def get_mean_color(x, y, img, px1, px2):
    r = 0
    g = 0
    b = 0
    for i in range(px1):
        for j in range(px2):
            r += img[x:x+px1, y:y+px2][i][j][0]
            g += img[x:x+px1, y:y+px2][i][j][1]
            b += img[x:x+px1, y:y+px2][i][j][2]
    if px2 == 0:
        px2 = 1
    r = int(r/(px1*px2))
    g = int(g/(px1*px2))
    b = int(b/(px1*px2))
    return (r,g,b)


def pixelize_color(image, px=32):
    try:
        img = cv2.imread(image)
    except:
        img = image
    #xborder = int(img.shape[0]%px)
    #yborder = int(img.shape[1]%px)
    yb = image.shape[0] - (int(image.shape[0]/px)*px)
    xb = image.shape[1] - (int(image.shape[1]/px)*px)
    print(xb)
    print(yb)
    y = 0 
    while y < img.shape[1]:
        x = 0
        while x < img.shape[0]:
            try:
                img[x:x+px, y:y+px] = get_mean_color(x, y, img, px, px)
                #cv2.imshow("test", img)
                #cv2.waitKey(0)
            except:
                try:
                    img[x:x+yb, y:y+px] = get_mean_color(x, y, img, yb, px)
                except:
                    try:
                        img[x:x+px, y:y+xb] = get_mean_color(x, y, img, px, xb)
                    except:
                        try:
                            img[x:x+yb, y:y+xb] = get_mean_color(x, y, img, yb, xb)
                        except:
                            pass
            x += px
        y += px

    return img

    

def run(img, out, pixels):
    #img = "donut.jpg"
    image = cv2.imread(img)
    pxc = pixelize_color(image, pixels)
    cv2.imwrite(out, pxc)
    print("Pixel Art filter completed")
    