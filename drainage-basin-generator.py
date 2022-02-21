import tkinter as tk

from PIL import Image
import random

inputPath = "test.png"
pathCount = 10**5
perPath = 8
outputPath = f"test-{pathCount}.png"

inputImage = Image.open(inputPath)
width, height = inputImage.size

inputGreyscale = [0]*width*height

mode = inputImage.mode
if(mode == "L" or mode == "P"):
    inputGreyscale = list(inputImage.getdata())
elif(mode == "RGB"):
    rawRGB = list(inputImage.getdata())
    for i in range(width*height):
        R,G,B = rawRGB[i]
        inputGreyscale[i] = (R+G+B)//3
elif(mode == "RGBA"):
    rawRGB = list(inputImage.getdata())
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

outputGreyscale = [0]*width*height

for i in range(pathCount):
    if i % 1000 == 0:
        print(i)

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
        outputGreyscale[pixelpos] = min((outputGreyscale[pixelpos] + perPath), 256)

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

inputImage.putdata(outputGreyscale)
inputImage.save(outputPath)


#Window definition
#window = tk.Tk()

#Input filepath

#Output filepath

#Path count

#RNG seed (opt)

#Live preview?

#window.mainloop()
