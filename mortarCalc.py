import tkinter as tk
from tkinter import Button, PhotoImage
import math
from tkinter.ttk import Label
from PIL import ImageGrab, Image
import os.path


metry = 100
pixele = 519
dystans = 0
azymut = 0

def setDyst(dys):
    global dystans
    dystans = dys

def setAzy(azy):
    global azymut
    azymut = azy

def dist_a(y,y1):
    return -(y - y1)

def dist_c(x,x1,y,y1):
    return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

def azi(pixel_dist_a,pixel_dist_c,x,x1,y,y1):
    degree = math.degrees(math.asin(pixel_dist_a / pixel_dist_c))
    if (x - x1 > 0 and -(y - y1) > 0) or (x - x1 > 0 and -(y - y1) < 0):
        degree = 90 - degree
    else:
        degree = 270 + degree
    return degree

def zdj():
    img = Image.open(f"screenshot.png")
    img= img.convert("L")
    d = img.getdata()
    new_image = []
    for item in d:
        if item == 0:
            new_image.append(item)
        else:
            new_image.append(240)

    img.putdata(new_image)
    width, height = img.size
    left = width * 5 / 8
    top = 58.5 * height / 64
    right = width
    bottom = 59.5 * height / 64
    img = img.crop((left, top, right, bottom))
    return img.convert("L")

def naj_2(lista: list):
    for i in range(len(lista) - 3):
        if lista[i] == lista[i + 1] and lista[i + 2] < lista[i]:
            return lista[i]

def licz_czarne(img):
    lista = []
    for j in range(img.height):
        czarne = 0
        for i in range(img.width):
            x = img.getpixel((i,j))
            if x == 0:
                czarne+=1
        lista.append(czarne)
    return naj_2(lista)

def mortar_milirad(dist):
    tab1 = [0,1579,1558,1538,1517,1496,1475,1453,1431,1409,1387,1364,1341,1317,1292,1267,1240,1212,1183,1152,1118,1081,1039,988,918,800]
    tab2=[0,0.42,0.4,0.42,0.42,0.42,0.44,0.44,0.44,0.44,0.46,0.46,0.48,0.5,0.5,0.54,0.56,0.58,0.62,0.68,0.74,0.84,1.02,1.4,2.36]
    if dist>=0 and dist<=1250:
        if dist%50==0:
            return tab1[int(dist/50)]
        else:
            prze = math.floor(dist/50)
            dist = dist - (prze*50)
            return tab1[prze]-(dist*tab2[prze])
    else:
        return 0

def hellcanon_degree(dist):
    tab1 = [ 90,89.2,88.5,87.7,86.9,86.1,85.3,84.5,83.7,82.9,82.1,81.3,80.5,79.7,78.9,78,77.1,76.2,75.4,74.5,73.6,72.6,71.7,70.7,69.7,68.6,67.5,66.4,65.3,64.1,62.7,61.4,59.8,58.2,56.3,54.1,51.2,45.4]
    tab2= [0.02,0.032,0.028,0.032,0.032,0.032,0.032,0.032,0.032,0.032,0.032,0.032,0.032,0.032,0.032,0.036,0.036,0.036,0.032,0.036,0.036,0.04,0.036,0.04,0.04,0.044,0.044,0.044,0.044,0.048,0.056,0.052,0.064,0.064,0.076,0.088,0.116,0.232]

    if dist>=0 and dist<=925:
        if dist%25==0:
            return tab1[int(dist/25)],90-tab1[int(dist/25)]
        else:
            prze = math.floor(dist/25)
            dist = dist - (prze*25)
            x=tab1[prze]-(dist*round(tab2[prze],2))
            return x,90-x
    else:
        return 0,0

def windo():
    win = tk.Toplevel(root)
    makeScreenShot()
    width_screen = win.winfo_screenwidth()
    height_screen = win.winfo_screenheight()
    win.attributes('-fullscreen', True)
    win.geometry(f"{width_screen}x{height_screen}")

    def endCal():
        win.destroy()

    def draw_line(e):
        x, y = e.x, e.y
        if canvas.old_coords:
            x1, y1 = canvas.old_coords
            setPixel()
            pixel_dist_c = dist_c(x, x1, y, y1)
            pixel_dist_a = dist_a(y, y1)
            dist_m = (pixel_dist_c / pixele) * metry
            degree = azi(pixel_dist_a,pixel_dist_c, x, x1, y, y1)
            a = '\u00b0'
            hell,canon= hellcanon_degree(dist_m)
            tekst = f"Dist:   {round(dist_m,2)}m\nAzy:    {round(degree,2)}{a}\nMortar: {round(mortar_milirad(round(dist_m,2)),2)}{a}\nHell Canon: {round(hell,2)}{a}/{round(canon,2)}{a}"
            text2.config(text=tekst,font=('Helvetica 15 bold italic'))
            endCal()
        else:
            canvas.old_coords = x, y


    canvas = tk.Canvas(win, width=width_screen, height=height_screen)
    canvas.pack()
    updateBackground()
    canvas.create_image(0, 0, anchor="nw", image=background_img)
    canvas.old_coords = None
    exit_button = Button(win, text="Exit", command=endCal)
    exit_button.place(x=1880, y=10)
    win.bind('<ButtonPress-1>', draw_line)

def updateBackground():
    global background_img
    background_img = PhotoImage(file="screenshot.png")

def set900():
    global metry
    metry = 900
    windo()

def set300():
    global metry
    metry = 300
    windo()

def set100():
    global metry
    metry = 100
    windo()

def setPixel():
    global pixele
    pixele = licz_czarne(zdj())

def makeScreenShot():
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    screenshot.close()

def makeFile():
    if not os.path.isfile("screenshot.png"):
        new = Image.new(mode="RGBA", size=(1920, 1080))
        new.save("screenshot.png")
        new.close()

def setFocus():
    root.focus_set()

def on_press(key):
    print(key)
    if key == "/":
        setFocus()
def endPro():
    root.destroy()

makeFile()
root = tk.Tk()
root.geometry("400x200")
root.title("MAIN")


text2 = Label(root,font=('Helvetica 15 bold italic'), text=f"Dist: {round(dystans,2)}\nAzy: {round(azymut,2)}", )
text2.place(x=10, y=10)
button900 = Button(root, text="900m",font=('Helvetica 15 bold italic'), command=set900)
button900.place(x=320, y=10)
button300 = Button(root, text="300m",font=('Helvetica 15 bold italic'), command=set300)
button300.place(x=250, y=10)
button100 = Button(root, text="100m",font=('Helvetica 15 bold italic'), command=set100)
button100.place(x=180, y=10)
background_img = PhotoImage(file="screenshot.png")
exit_button1 = Button(root, text="____Exit program____",font=('Helvetica 15 bold italic'), command=endPro)
exit_button1.place(x=100, y=150)

root.wm_attributes("-topmost", 1)


root.mainloop()
