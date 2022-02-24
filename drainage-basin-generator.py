#import tkinter as tk

from PIL import Image
import random
import ctypes

def data_from_image():
    inputGreyscale = [0]*width*height

    if(mode == "L" or mode == "P" or mode == "I"):
        inputGreyscale = list(img.getdata())
    elif(mode == "RGB"):
        rawRGB = list(img.getdata())
        for i in range(width*height):
            R,G,B = rawRGB[i]
            inputGreyscale[i] = (R+G+B)//3
    elif(mode == "RGBA"):
        rawRGB = list(img.getdata())
        for i in range(width*height):
            R,G,B,A = rawRGB[i]
            inputGreyscale[i] = (R+G+B)//3

    for i in range(width):
        inputGreyscale[i] = 0
    for i in range(width):
        inputGreyscale[i+(height-1)*width] = 0
    for i in range(height):
        inputGreyscale[i*width] = 0
    for i in range(height):
        inputGreyscale[i*width+width-1] = 0

    return inputGreyscale


def image_from_output(outputGreyscale):
    if(mode == "RGB"):
        RGB = [(0,0,0)]*width*height
        for i in range(width*height):
            x = outputGreyscale[i]
            RGB[i]= (x,x,x)
        outputGreyscale = RGB
    elif(mode == "RGBA"):
        RGBA = [(0,0,0,0)]*width*height
        for i in range(width*height):
            x = outputGreyscale[i]
            RGBA[i]= (x,x,x,255)
        outputGreyscale = RGBA

    img.putdata(outputGreyscale)


def drainage_iteration():
    pixelpos = 0
    while True:
        pixelpos = random.randrange(width*height)
        if inputGreyscale[pixelpos] > 0:
            break

    visited = set()
    prevDx = 0
    prevDy = 0
    while True:
        visited.add(pixelpos)
        if mode == "I":
            outputGreyscale[pixelpos] = min((outputGreyscale[pixelpos] + perPathI), pixelMaxI)
        else:
            outputGreyscale[pixelpos] = min((outputGreyscale[pixelpos] + perPath), pixelMax)

        if(inputGreyscale[pixelpos] == 0):
            break

        neighbours = []
        for dx in range(-1,2):
            for dy in range(-1,2):
                neighbourPos = pixelpos+dy+dx*width
                if neighbourPos not in visited:
                    neighbours.append((inputGreyscale[neighbourPos], neighbourPos, dx, dy))

        neighbours.sort()

        if len(neighbours) == 0:
            break
        minElev,_,_,_ = neighbours[0]
        neighbours = [(e,p,dx,dy) for e,p,dx,dy in neighbours if e == minElev]
        angles = []
        for i in range(len(neighbours)):
            value, pos, dx, dy = neighbours[i]
            angle = abs(prevDx-dx) + abs(prevDy-dy)
            angles.append((angle, pos, dx, dy))

        angles.sort()
        validNeighbour = False
        for i in range(len(angles)):
            angle, pos, dx, dy = angles[i]
            if pos not in visited:
                pixelpos = pos
                prevDx = dx
                prevDy = dy
                validNeighbour = True
                break
        if not validNeighbour:
            break

#SETTINGS
inputPath = "test.png"
pathCount = int(1.0*10**5)
perPath = 8
pixelMax = 255
pixelMaxI = (2**16)-1
perPathI = perPath * (pixelMaxI // pixelMax)
outputPath = f"test-{pathCount}.png"

#LOADING
libcpp = ctypes.CDLL("./terraingen.so")
img = Image.open(inputPath)
width, height = img.size
mode = img.mode
inputGreyscale = data_from_image()
outputGreyscale = [0]*width*height

c_inputGreyscale = (ctypes.c_int * len(inputGreyscale))(*inputGreyscale)
c_outputGreyscale = (ctypes.c_int * len(outputGreyscale))(*outputGreyscale)

#ITERATIONS
#for i in range(pathCount):
    #if i % 1000 == 0:
    #    print(f"{i//1000}K")
#    drainage_iteration()
#CALL C++-lib for actual processing
if mode == "I":
    libcpp.drainage_simulation(c_inputGreyscale, c_outputGreyscale, width, height, pathCount, perPathI, pixelMaxI)
else:
    libcpp.drainage_simulation(c_inputGreyscale, c_outputGreyscale, width, height, pathCount, perPath, pixelMax)
outputGreyscale = list(c_outputGreyscale)

#OUTPUT
image_from_output(outputGreyscale)
img.save(outputPath)


#Window definition
#window = tk.Tk()

#Input filepath

#Output filepath

#Path count

#RNG seed (opt)

#Live preview?

#window.mainloop()
