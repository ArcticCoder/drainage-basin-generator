import tkinter as tk

from PIL import Image
import random

inputPath = "test.png"
pathCount = 10**6
outputPath = f"test-{pathCount}.png"

inputImage = Image.open(inputPath)
inputGreyscale = list(inputImage.getdata())
width, height = inputImage.size

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
                if (neighbourPos < 0):
                    print(pixelpos, dx, dy, width, height)
                    exit()
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
