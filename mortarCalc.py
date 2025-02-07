import tkinter as tk
from tkinter import Button, PhotoImage
import math
from tkinter.ttk import Label
from PIL import ImageGrab, Image

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
            text2.config(text=f"Dist:   {round(dist_m,2)}m\nAzy:    {round(degree,2)}{a}\nMortar: {round(mortar_milirad(round(dist_m,2)),2)}{a}",font=('Helvetica 15 bold italic'))
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

def setFocus():
    root.focus_set()

def on_press(key):
    print(key)
    if key == "/":
        setFocus()
def endPro():
    root.destroy()

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
