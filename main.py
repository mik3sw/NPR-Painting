#from tkinter import W
import random
import time
import imgtools as imt
import cv2
import numpy as np
from rich.progress import Progress
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)

LIVE = False

bar = Progress(
        SpinnerColumn("dots"),
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    )


def step(task):
    bar.update(task, advance=1)


def iter(out, img, cells, task):
    global LIVE
    cells_c = cells.copy()
    while len(cells_c) != 0:
        x = random.choice(cells_c)
        color = imt.get_mean_color(img,x)
        out = imt.put_stroke(out, x, color)

        if LIVE:
            cv2.imshow("out", out)
            cv2.waitKey(1)

        cells_c.remove(x)
        step(task)
    return out


def get_new_cells(cells):
    ncells = []
    for x in cells:
        tmp = imt.get_4cell(x)
        ncells = ncells + tmp
    return ncells


def crop(im, px, w, h):
    y = px
    x = px
    crop_img = im[y:y+h, x:x+w]
    #cv2.imshow("cropped", crop_img)
    #cv2.waitKey(0)
    return crop_img


def main(image, outname="out.jpg" ,iterations=5, live = False):
    
    global LIVE
    LIVE = live
    if live:
        print("Live process: True")
        print("Computational time will increase")
    count = 0
    if iterations < 2:
        print("Setting iterations = 2")
        iterations = 2
    if iterations == 2:
        count = 85
    if iterations == 3:
        count = 277
    if iterations == 4:
        count = 1045
    if iterations == 5:
        count = 5460 
    if iterations == 6:
        count = 21844
    if iterations == 7:
        count = 87360
    if iterations > 7:
        iterations = 7
        count = 87360
        print("Iterations can't be > 7")
    
    with bar as progress:
        task = progress.add_task("[bold green]Processing...", total=count)
        img = imt.readimg(image)
        img = imt.imborder(img, 50)
        
        height, width, _ = img.shape
        cells = []

        height -= 100
        width -= 100
        x1 = int(height/2) + 50
        y1 = int(width/2) + 50

        cells.append([50,x1,50,y1])
        cells.append([50, x1, y1, width-1])
        cells.append([x1, height-1, 50,y1])
        cells.append([x1, height-1, y1, width-1])

        out = np.zeros_like(img, np.uint8)
        color = imt.get_mean_color(img,[0,height-1,0,width-1])
        out = imt.put_stroke(out, [0,height-1,0,width-1], color)

        out = iter(out, img, cells, task)

        for x in range(iterations):
            ncells = get_new_cells(cells)
            cells = ncells
            out=iter(out,img, cells, task)
            ncells = []
            
        out = crop(out, 50, width-50, height-50)    
        cv2.imshow("test", out)
        cv2.waitKey(0)

        cv2.imwrite(outname, out)



if __name__ == "__main__":
    main("input/im2.jpg", "output/out2.jpg", iterations=6, live=False)
