import ctypes
from PIL import Image
import random
import tkinter as tk
import sys

def data_from_image(img, width, height, mode):
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


def image_from_output(img, outputGreyscale, width, height, mode):
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

def run_simulation():
    try:
        inputPath = i_filepath_ent.get()
    except:
        i_filepath_ent.delete(0,tk.END)
        return

    try:
        pathCount = int(path_count_ent.get())
    except:
        path_count_ent.delete(0,tk.END)
        return

    try:
        outputPath = inputPath.split(".")
        outputPath = f"{outputPath[0]}-{pathCount}.{outputPath[-1]}"
    except:
        i_filepath_ent.delete(0,tk.END)
        return

    try:
        perPath = int(per_path_ent.get())
    except:
        per_path_ent.delete(0,tk.END)
        return
    pixelMax = 255
    pixelMaxI = (2**16)-1
    perPathI = perPath * (pixelMaxI // pixelMax)

    #LOADING
    if sys.platform.startswith("linux"):
        libcpp = ctypes.CDLL("./terraingen.so")
    elif sys.platform.startswith("win32"):
        libcpp = ctypes.CDLL(".\\terraingen.dll")
    else:
        raise RuntimeError("Unknow platform (should be windows or linux)")

    try:
        img = Image.open(inputPath)
    except:
        i_filepath_ent.delete(0,tk.END)
        return
    width, height = img.size
    mode = img.mode
    inputGreyscale = data_from_image(img, width, height, mode)
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
    image_from_output(img, outputGreyscale, width, height, mode)
    img.save(outputPath)

#Window definition
window = tk.Tk()
window.minsize(250,160)

#Input filepath
i_filepath_frm = tk.Frame()
i_filepath_lbl = tk.Label(i_filepath_frm, text="Input image filepath:", anchor="w")
i_filepath_ent = tk.Entry(i_filepath_frm)
i_filepath_ent.insert(0,"input.png")
i_filepath_frm.pack(fill=tk.X)
i_filepath_lbl.pack(fill=tk.X)
i_filepath_ent.pack(fill=tk.X)

#Path count
path_count_frm = tk.Frame()
path_count_lbl = tk.Label(path_count_frm, text="Path count:", anchor="w")
path_count_ent = tk.Entry(path_count_frm, width=30)
path_count_ent.insert(0,"10000")
path_count_frm.pack(fill=tk.X)
path_count_lbl.pack(fill=tk.X)
path_count_ent.pack(side=tk.LEFT)

#Per path
per_path_frm = tk.Frame()
per_path_lbl = tk.Label(per_path_frm, text="Pixel value increase per path (0-255):", anchor="w")
per_path_ent = tk.Entry(per_path_frm, width=30)
per_path_ent.insert(0,"8")
per_path_frm.pack(fill=tk.X)
per_path_lbl.pack(fill=tk.X)
per_path_ent.pack(side=tk.LEFT)

#RUN-button
run_btn = tk.Button(text="Run", command=run_simulation)
run_btn.pack(fill=tk.BOTH)

window.mainloop()
