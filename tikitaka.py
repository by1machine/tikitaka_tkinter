#!/usr/bin/env python3
# -*-coding: utf8-*-

from tkinter import *
import serial
import time
import math
import queue


arduinoData = serial.Serial('COM19',4800,timeout=1)

# Full Screen Code      
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='800x300+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom=geom
      
root = Tk()
var = StringVar()
puan = StringVar()
atis = StringVar()
score = 0
seconds = 60
atis_sayi = 0
var.set(seconds)
puan.set(score)
atis.set(atis_sayi)
after = None
p=False

def baslat():
    arduinoData.write("RUN".encode())
    baslatbutton.configure(state=DISABLED)
    bitirbutton.configure(state=NORMAL)
    ledbutton.configure(state=DISABLED)
    puan.set(score)
    time.sleep(2)
    countdown(seconds)
    
def puan_1():
    i = 0
    arduinoData.flushInput()
    while True:
        s = arduinoData.readline()
        s = s.strip()
        print(s.decode("utf-8"))
        i += 1
        if i == 3:
            puan.set(s.decode("utf-8"))
        if i == 4:
            atis.set(s.decode("utf-8"))
            break
                  
def countdown(count):
    var.set(float("%.2f" % count))
    global after
    after = root.after(100, countdown, count - 0.1)
    if count < 0.1:
        arduinoData.write("STOP".encode())
        puan_1()
        root.after_cancel(after)
        var.set(seconds)
        baslatbutton.configure(state=NORMAL)
        ledbutton.configure(state=NORMAL)
    if count > 0.1:
        after

def bitir():
    arduinoData.write("STOP".encode())
    puan_1()
    baslatbutton.configure(state=NORMAL)
    ledbutton.configure(state=NORMAL)
    root.after_cancel(after)
    var.set(seconds)

    
def led():
    arduinoData.write("LED".encode())
    puan.set(score)
    i = 0
    while True:
        s = arduinoData.readline()
        s = s.strip()
        print(s.decode("utf-8"))
        i += 1
        if i == 40:
            break

root.title("TikiTaka")
root.overrideredirect(1)    
root.attributes("-topmost",1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.resizable(width=False, height=False)
root.configure(background='white')
color_text = "white"

resim = PhotoImage(file="tikitaka.png")
yazi = Label(image = resim,compound="left")
yazi.place(relx=0.49,rely=0.1,anchor=CENTER)

puanLabel = Label(root,text="Puan: ", font=("Helvetica", 40))
puanLabel.place(relx=0.46,rely=0.3,anchor=CENTER)
puanLabel.configure(bg=color_text)

puanSayi = Label(root,textvariable=puan,font=("Helvetica", 40))
puanSayi.place(relx=0.55,rely=0.3,anchor=CENTER)
puanSayi.configure(bg=color_text)

sureLabel = Label(root, text="Süre: ", font=("Helvetica", 40))
sureLabel.place(relx=0.46,rely=0.4,anchor=CENTER)
sureLabel.configure(bg=color_text)

sureSayi = Label(root, textvariable=var, font=("Helvetica", 40))
sureSayi.place(relx=0.55,rely=0.4,anchor=CENTER)
sureSayi.configure(bg=color_text)

atisLabel = Label(root, text="Atış: ", font=("Helvetica", 40))
atisLabel.place(relx=0.46,rely=0.5,anchor=CENTER)
atisLabel.configure(bg=color_text)

atisSayi = Label(root, textvariable=atis, font=("Helvetica", 32))
atisSayi.place(relx=0.55,rely=0.5,anchor=CENTER)
atisSayi.configure(bg=color_text)

baslatbutton = Button(root, text="Game Start",fg="white", font=("Helvetica", 25),height=1, width=15, command=baslat)
baslatbutton.place(relx=0.4, rely=0.65, anchor=CENTER)
baslatbutton.configure(bg="green",fg="white")

bitirbutton = Button(root, text="Game Stop",fg="red", font=("Helvetica", 25),height=1, width=15, command=bitir)
bitirbutton.place(relx=0.4,rely=0.75,anchor=CENTER)


ledbutton = Button(root, text="Panel Led",fg="black", font=("Helvetica", 25),height=1, width=10, command=led)
ledbutton.place(relx=0.6,rely=0.75,anchor=CENTER)

Stopbutton = Button(root,text="Quit",fg="red",font=("Helvetica",25),height=1,width=10,command=root.destroy)
Stopbutton.pack()
Stopbutton.place(relx=0.6,rely=0.65,anchor=CENTER)
app=FullScreenApp(root)
root.mainloop()
