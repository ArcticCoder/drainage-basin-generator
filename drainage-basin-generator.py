import tkinter as tk

from PIL import Image
import random

inputPath = "test.png"
pathCount = 10**4
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
    while True:
        visited.add(pixelpos)
        outputGreyscale[pixelpos] = min((outputGreyscale[pixelpos] + 16), 256)

        if(inputGreyscale[pixelpos] == 0):
            break

        neighbours = []
        for dx in range(-1,2):
            for dy in range(-1,2):
                neighbourPos = pixelpos+dy+dx*width
                neighbours.append((inputGreyscale[neighbourPos], neighbourPos))

        neighbours.sort()
        validNeighbour = False
        for i in range(len(neighbours)):
            value, pos = neighbours[i]
            if pos not in visited:
                pixelpos = pos
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
