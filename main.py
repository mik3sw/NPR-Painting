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

import pixel_art as px

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
    cont = 0
    while len(cells_c) != 0:
        x = random.choice(cells_c)
        color = imt.get_mean_color(img,x)
        out = imt.put_stroke(out, x, color)
        #cv2.imshow("iter", out)
        #cv2.waitKey(0)
        cont += 1

        if LIVE:
            cv2.imshow("out", out)
            cv2.waitKey(1)

        cells_c.remove(x)
        step(task)
    print("cont: {}".format(cont))
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
    '''if iterations == 2:
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
        count = 87360'''
    

    if iterations > 7:
        iterations = 7
        print("Iterations can't be > 7")
    
    count = pow(4, iterations+1) #+ 4

    
    with bar as progress:
        start = time.time()
        task = progress.add_task("[bold green]Processing...", total=count)
        img = imt.readimg(image)
        img = imt.imborder(img, 100)
        #cv2.imshow("image", img)
        #cv2.waitKey(0)
        
        height, width, _ = img.shape
        cells = []

        height -= 100
        width -= 100
        x1 = int(height/2) + 100
        y1 = int(width/2) + 100

        cells.append([100,x1,100,y1])
        cells.append([100, x1, y1, width-1])
        cells.append([x1, height-1, 100,y1])
        cells.append([x1, height-1, y1, width-1])

        if LIVE:
            out = np.zeros_like(img, np.uint8)
        else:
            out = img
        #print(cells)
        #color = imt.get_mean_color(img,[0,height-1,0,width-1])
        #out = imt.put_stroke(out, [0,height-1,0,width-1], color)

        #out = iter(out, img, cells, task)

        if LIVE:
            for x in range(iterations):
                ncells = get_new_cells(cells)
                cells = ncells
                out = iter(out,img, cells, task)
                ncells = []
        else:
            for x in range(iterations):
                ncells = get_new_cells(cells)
                cells = ncells
                if (iterations < 6):
                    if (x<4):
                        out = iter(out,img, cells, task)
                if (x == iterations-1):
                    out = iter(out,img, cells, task)
                ncells = []
            
        out = crop(out, 100, width-100, height-100)    
        #cv2.imshow("test", out)
        #cv2.waitKey(0)

        cv2.imwrite(outname, out)
        end = time.time()
        print(f"Total time: {end - start}")



if __name__ == "__main__":
    #main("input/im1.jpg", "output/out1.jpg", iterations=6, live=False)
    #main("input/im2.jpg", "output/out2.jpg", iterations=4, live=False)
    #main("input/im3.jpg", "output/out3.jpg", iterations=6, live=False)
    #main("input/im4.jpg", "output/out4.jpg", iterations=6, live=False)
    #main("input/im5.jpg", "output/out5.jpg", iterations=6, live=False)
    #main("input/im6.jpg", "output/out6.jpg", iterations=6, live=False)
    #main("input/im7.jpg", "output/out7.jpg", iterations=6, live=False)
    #main("input/im8.jpg", "output/out8.jpg", iterations=6, live=False)
    #main("input/im9.jpg", "output/out9.jpg", iterations=6, live=False)
    main("input/im12.jpg", "output/out12.jpg", iterations=6, live=False)
    #main("input/time1.jpg", "output/time1out.jpg", iterations=6, live=False)
    #main("input/time2.png", "output/time2out.jpg", iterations=5, live=False)
    #px.run("input/im11.jpg", "output/px11.jpg", 32)
