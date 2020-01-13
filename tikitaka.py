#!/usr/bin/env python3
# -*-coding: utf8-*-

from tkinter import *
import serial
import time
import math
import queue


arduinoData = serial.Serial('COM5',4800,timeout=1)
#arduinoData.flushInput()

      
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
   # arduinoData.flushInput()
    
def puan_1():
    i = 0
    arduinoData.flushInput()
    while True:
        s = arduinoData.readline()
        s = s.strip()
        print(s.decode("utf-8"))
        puan.set(s.decode("utf-8"))
        i += 1
        if i == 3:
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
    atis.set(atis_sayi)
'''
def reset():
    baslatbutton.configure(state=NORMAL)
    bitirbutton.configure(state=NORMAL)
    arduinoData.write("RESET".encode())
    #root.after_cancel(after)
    var.set(seconds)
    puan.set(score)
    atis.set(atis_sayi)
'''

    
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
#Button(root,text="Kapat",command=root.destroy).pack()
resim = PhotoImage(file="tikitaka.png")
yazi = Label(image = resim,compound="left")
yazi.pack()

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.resizable(width=False, height=False)
root.configure(background='antiquewhite')
color_text = "antiquewhite"

puanLabel = Label(root,text="Puan: ", font=("Helvetica", 40))
#puanLabel.grid(row=0, column=0, padx=(320, 0), pady=10, sticky=W)
puanLabel.place(relx=0.4,rely=0.3,anchor=CENTER)
puanLabel.configure(bg=color_text)

puanSayi = Label(root,textvariable=puan,font=("Helvetica", 40))
#puanSayi.grid(row=0, column=1, padx=(0, 320), pady=10, sticky=W)
puanSayi.place(relx=0.5,rely=0.3,anchor=CENTER)
puanSayi.configure(bg=color_text)

sureLabel = Label(root, text="Süre: ", font=("Helvetica", 40))
#sureLabel.grid(row=1, column=0, padx=(320, 0), pady=10, sticky=W)
sureLabel.place(relx=0.4,rely=0.4,anchor=CENTER)
sureLabel.configure(bg=color_text)

sureSayi = Label(root, textvariable=var, font=("Helvetica", 40))
#sureSayi.grid(row=1, column=1, padx=(0, 320), pady=10, sticky=W)
sureSayi.place(relx=0.5,rely=0.4,anchor=CENTER)
sureSayi.configure(bg=color_text)
'''
atisSayi = Label(root, textvariable=atis, font=("Helvetica", 32))
atisSayi.place(relx=0.6,rely=0.4,anchor=CENTER)
'''

baslatbutton = Button(root, text="Game Start",fg="white", font=("Helvetica", 25),height=1, width=15, command=baslat)
baslatbutton.place(relx=0.33, rely=0.6, anchor=CENTER)
#baslatbutton.grid(row=2, column=0, sticky=S, pady=10)
baslatbutton.configure(bg="green",fg="white")

bitirbutton = Button(root, text="Game Stop",fg="red", font=("Helvetica", 25),height=1, width=15, command=bitir)
#bitirbutton.grid(row=3, column=0, sticky=S, pady=10)
bitirbutton.place(relx=0.33,rely=0.7,anchor=CENTER)

'''
resetbutton = Button(root, text="Reset",fg="black", font=("Helvetica", 25),height=1, width=10, command=reset)
#resetbutton.grid(row=2, column=1, sticky=S, pady=10)
resetbutton.place(relx=0.6,rely=0.6,anchor=CENTER)
'''

ledbutton = Button(root, text="Panel Led",fg="black", font=("Helvetica", 25),height=1, width=10, command=led)
#ledbutton.grid(row=3, column=1, sticky=S, pady=10)
ledbutton.place(relx=0.6,rely=0.7,anchor=CENTER)

Stopbutton = Button(root,text="Quit",fg="red",font=("Helvetica",25),height=1,width=10,command=root.destroy)
Stopbutton.pack()
Stopbutton.place(relx=0.6,rely=0.6,anchor=CENTER) 
app=FullScreenApp(root)
root.mainloop()
