#!/usr/bin/env python3.7
# -*-coding: utf8-*-

#KÜTÜPHANE
from tkinter import *
import serial
import time
import math
import queue
from random import seed
from random import randint
from threading import Thread

arduinoData = serial.Serial('/dev/ttyS0',4800,timeout=1) #SERIAL PORT TANIMLAMA
	
# PROGRAMIN TAM EKRAN KODU      
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
      
root = Tk() #TKINTER ARAYÜZ OLUŞTURMA
var = StringVar() #SÜRE STRING TANIMLAMA
puan = StringVar() #PUAN STRING TANIMLAMA
score = 0 #DEFAULT SÜRE
seconds = 60 #MAX. SÜRE
var.set(seconds) #VAR DEĞİŞKENİNE SÜREYİ ATAMA
puan.set(score)  #PUAN DEĞİŞKENİNE SKORU ATAMA
after = None

 #BAŞLAT FONKSİYONU
def baslat():
    arduinoData.write("RUN".encode())
    baslatbutton.configure(state=DISABLED)
    bitirbutton.configure(state=NORMAL)
    ledbutton.configure(state=DISABLED)
    time.sleep(2)
    countdown(seconds)
	
#PUAN FONKSİYONU
def puan_1():
    time.sleep(1)
    i=0
    arduinoData.flushInput()
    while True:
        s = arduinoData.readline()
        s = s.strip()
        arduinoData.write('PUAN"\n"'.encode("utf-8"))
        puan.set(s.decode("utf-8"))
        print(s.decode("utf-8"))
        i += 1
        if i == 2:
            break
  #SAYAÇ FONKSİYONU                
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
#BİTİRME FONKSİYONU
def bitir():
    arduinoData.write("STOP".encode())
    baslatbutton.configure(state=NORMAL)
    ledbutton.configure(state=NORMAL)
    root.after_cancel(after)
    var.set(seconds)
    puan.set(score)

 #SIRALI LED FONKSİYONU   
def led():
    arduinoData.write("LED".encode())
    puan.set(score)
    i = 0
    while True:
        s = arduinoData.readline()
        s = s.strip()
        i += 1
        if i == 40:
            break

#PROGRAM BUTON,YAZI VE BOUTLANDIRMA AYARLARI
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

puanLabel = Label(root,text="Puan: ", font=("Helvetica", 50))
puanLabel.place(relx=0.46,rely=0.3,anchor=CENTER)
puanLabel.configure(bg=color_text)

puanSayi = Label(root,textvariable=puan,font=("Helvetica", 50))
puanSayi.place(relx=0.55,rely=0.3,anchor=CENTER)
puanSayi.configure(bg=color_text)

sureLabel = Label(root, text="Süre: ", font=("Helvetica", 50))
sureLabel.place(relx=0.46,rely=0.45,anchor=CENTER)
sureLabel.configure(bg=color_text)

sureSayi = Label(root, textvariable=var, font=("Helvetica", 50))
sureSayi.place(relx=0.55,rely=0.45,anchor=CENTER)
sureSayi.configure(bg=color_text)


baslatbutton = Button(root, text="Game Start",fg="green", font=("Helvetica", 25),height=1, width=15, command=baslat)
baslatbutton.place(relx=0.4, rely=0.65, anchor=CENTER)


bitirbutton = Button(root, text="Game Stop",fg="red", font=("Helvetica", 25),height=1, width=15, command=bitir)
bitirbutton.place(relx=0.4,rely=0.75,anchor=CENTER)


ledbutton = Button(root, text="Panel Led",fg="black", font=("Helvetica", 25),height=1, width=10, command=led)
ledbutton.place(relx=0.6,rely=0.75,anchor=CENTER)

Stopbutton = Button(root,text="Quit",fg="red",font=("Helvetica",25),height=1,width=10,command=root.destroy)
Stopbutton.pack()
Stopbutton.place(relx=0.6,rely=0.65,anchor=CENTER)
app=FullScreenApp(root)
root.mainloop()
