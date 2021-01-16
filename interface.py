#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import tkinter as tk
from PIL import ImageTk,Image
from threading import Timer
from pynput import mouse
from sms import SepcapMessagingSystem as SMS


IMG_X = 80
IMG_Y = 200
IMG_DIMX = 355
IMG_DIMY = 240
IMG_SEP = "sep.png"
IMG_LOGO = "logo.png"
IMG_OFF = "off.png"
IMG_CAPS = "caps.PNG"
IMG_EMER = "emergencyStop.png"


class interface(tk.Tk):
    
    def __init__(self,*args,**kwargs):
        
        tk.Tk.__init__(self,*args,**kwargs)
        self.title("SEPCAP")
        self.geometry("800x480")
        self.attributes("-zoomed", True)
        self.overrideredirect(1)
        container = tk.Frame(self,width = 800, height = 480)
        container.pack(side="top",fill="both",expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        
        self.frames = {}
        
        self.sms = SMS(open(sys.argv[1], "rb"), open(sys.argv[2], "wb"))

        lg = Image.open(IMG_LOGO)
        lg = lg.resize((70,70),Image.ANTIALIAS)
        logo= ImageTk.PhotoImage(lg, Image.ANTIALIAS)
        
        pageId = (iniPage,menuSep,menuCont,separacao1,separacao2,separacao3,contagem1,contagem2,calib1,calib2,calib3,emergencyStop)

        pageName = ("","MENU INICIAL","MENU INICIAL","SEPARAÇÃO","SEPARAÇÃO","SEPARAÇÃO","CONTAGEM","CONTAGEM","CALIBRAÇÃO","CALIBRAÇÃO","CALIBRAÇÃO","")


        for F,pName in zip(pageId,pageName):
            frame = F(container,self)
            frame.config(cursor='none')
            if ((F!=iniPage)and(F!=emergencyStop)):
                canvas = tk.Canvas(frame, width=300, height=80,bg="black",highlightthickness=3)
                canvas.place(x=-5,y=30)
                logoTop = tk.Label(frame, image=logo, bg='black')
                logoTop.image = logo
                logoTop.place(x=5,y=35)
                w = tk.Label(frame, text=pName,font=("Paytone One", 20),fg='white',bg='black').place(x=75,y=48)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        global X,Y
        X=0
        Y=0
        self.frames[calib2].imgSep.bind('<Button-1>',calculate_coordinates)
        self.showFrame(iniPage)
        self.update()

    def showFrame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
            
    def update(self):
        self.frames[calib2].sep = Image.open(IMG_SEP)
        self.frames[calib2].sep = self.frames[calib2].sep.resize((IMG_DIMX,IMG_DIMY),Image.ANTIALIAS)
        self.frames[calib2].sep= ImageTk.PhotoImage(self.frames[calib2].sep, Image.ANTIALIAS)
        self.frames[calib2].imgSep.configure(image=self.frames[calib2].sep)
        self.frames[calib2].imgSep.image = self.frames[calib2].sep
        global nCaps
        
        if self.sms.isData():
            address, mtype, data = self.sms.readPacket()
            print(f'Int: {address}, {mtype}, {data}')
            if ((address==SMS.Address.Broadcast)or(address==SMS.Address.Interface)):
                if (mtype==SMS.Message.EmergencyStop.type):
                    if(data==SMS.Message.EmergencyStop.Emergency):
                        self.showFrame(emergencyStop)
                    elif(data==SMS.Message.EmergencyStop.Resume):
                        self.showFrame(menuSep)
                elif (mtype==SMS.Message.NewCapsule.type):
                    i = int(data) 
                    n = int(nCaps[i].get())+1
                    nCaps[i].set(str(n)) 
                    total = int(nCaps[8].get()) + 1
                    nCaps[8].set(total)
            
        #for i in range(0,8,1):
        #        n = int(nCaps[i].get())+1
        #        nCaps[i].set(str(n)) 
        #        total = total + n
        #nCaps[8].set(total)
        self.frames[calib2].updateRGB()
        self.after(100,self.update)


class iniPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black")
        lg = Image.open(IMG_LOGO)
        logo= ImageTk.PhotoImage(lg, Image.ANTIALIAS)
        logoIni = tk.Label(self, image=logo, bg='black')
        logoIni.image = logo
        logoIni.place(x=120,y=105)
        w = tk.Label(self, text="SEPCAP",font=("Paytone One", 40),fg='white',bg='black').place(x=320,y=180)
        ld = tk.Label(self, text="A INICIALIZAR O SISTEMA...",font=("Paytone One", 15),fg='grey',bg='black').place(x=320,y=245)
        t = Timer(interval=5,function=lambda:controller.showFrame(menuSep))
        t.start()
        

class menuSep(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black")
        buttonMode = tk.Button(self, text = "MODO: SEPARAÇÃO",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=2,width=15,command=lambda:controller.showFrame(menuCont)).place(x=42,y=160)
        buttonCalib = tk.Button(self, text = "CALIBRAR CORES",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=2,width=15,command=lambda:controller.showFrame(calib1)).place(x=42,y=312)
        buttonStart = tk.Button(self, text = "INICIAR",font=("Paytone One", 33),bd=10,bg='#00B050',activebackground='#00B050',fg="black",height=4,width=8,command=lambda:controller.showFrame(separacao1)).place(x=462,y=160)
        off = Image.open(IMG_OFF)
        off = off.resize((90,90),Image.ANTIALIAS)
        offImg= ImageTk.PhotoImage(off, Image.ANTIALIAS)
        buttonOff = tk.Button(self, image = offImg,command=lambda:controller.destroy())
        buttonOff.image = offImg
        buttonOff.place(x=660,y=30)


class menuCont(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black")
        buttonMode = tk.Button(self, text = "MODO: CONTAGEM",font=("Paytone One", 25),bd=10,bg='grey',fg="black",activebackground='grey',height=2,width=15,command=lambda:controller.showFrame(menuSep)).place(x=42,y=160)
        buttonCalib = tk.Button(self, text = "CALIBRAR CORES",font=("Paytone One", 25),bd=10,bg='grey',fg="black",activebackground='grey',height=2,width=15,command=lambda:controller.showFrame(calib1)).place(x=42,y=312)
        buttonStart = tk.Button(self, text = "INICIAR",font=("Paytone One", 33),bd=10,bg='#00B050',activebackground='#00B050',fg="black",height=4,width=8,command=lambda:self.contIni(controller)).place(x=462,y=160)
        off = Image.open(IMG_OFF)
        off = off.resize((90,90),Image.ANTIALIAS)
        offImg= ImageTk.PhotoImage(off, Image.ANTIALIAS)
        buttonOff = tk.Button(self, image = offImg,command=lambda:controller.destroy())
        buttonOff.image = offImg
        buttonOff.place(x=660,y=30)
        
    def contIni(self,ctrl):
        ctrl.sms.sendPacket(
            SMS.Address.Broadcast,
            SMS.Message.StartStop.type,
            SMS.Message.StartStop.Start
        )
        global nCaps
        nCaps[8].set(0)
        ctrl.showFrame(contagem1)
        

class separacao1(tk.Frame):
   
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black")
        l = tk.Label(self, text="Nº DE \nCÁPSULAS:",font=("Paytone One", 22),fg='white',bg='black',justify='left').place(x=40,y=142)
        canvas = tk.Canvas(self, width=140, height=77,bg="black",highlightthickness=3)
        canvas.place(x=225,y=148)
        global nCap
        nCap = tk.StringVar(self)
        nCap.set("")
        w = tk.Label(self, textvar=nCap,font=("Paytone One", 36),fg='#db9d00',bg='black').place(x=247,y=151)
        button3 = tk.Button(self, text = "3",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=1,command=lambda:self.add(3)).place(x=590,y=150)   
        button6 = tk.Button(self, text = "6",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=1,command=lambda:self.add(6)).place(x=590,y=250)
        button9 = tk.Button(self, text = "9",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=1,command=lambda:self.add(9)).place(x=590,y=350)
        button2 = tk.Button(self, text = "2",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=1,command=lambda:self.add(2)).place(x=500,y=150)
        button5 = tk.Button(self, text = "5",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=1,command=lambda:self.add(5)).place(x=500,y=250)
        button8 = tk.Button(self, text = "8",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=1,command=lambda:self.add(8)).place(x=500,y=350)
        button1 = tk.Button(self, text = "1",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=1,command=lambda:self.add(1)).place(x=410,y=150)
        button4 = tk.Button(self, text = "4",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=1,command=lambda:self.add(4)).place(x=410,y=250)
        button7 = tk.Button(self, text = "7",font=("Paytone One", 25),bd=10,bg='grey',fg="black",height=1,width=1,command=lambda:self.add(7)).place(x=410,y=350)
        buttonDel = tk.Button(self, text = "<",font=("Paytone One", 26),bd=10,bg='#383838',fg="black",height=3,width=1,command=lambda:self.delete()).place(x=680,y=150)
        button0 = tk.Button(self, text = "0",font=("Paytone One", 25),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=1,command=lambda:self.add(0)).place(x=680,y=350)
        buttonBack = tk.Button(self, text = "VOLTAR",font=("Paytone One", 20),bd=10,bg='#c20000',activebackground='#c20000',fg="black",height=1,width=6,command=lambda:controller.showFrame(menuSep)).place(x=596,y=40)
        buttonGo = tk.Button(self, text = "AVANÇAR",font=("Paytone One", 25),bd=10,bg='#00B050',activebackground='#00B050',fg="black",height=1,width=12,command=lambda:self.sepIni(controller)).place(x=45,y=350)
    
    def add(self,num):
        global nCap
        n = nCap.get()
        if (len(n)<3):
                nCap.set(str(n)+str(num))
        
    def delete(self):    
        global nCap
        n = nCap.get()
        if (len(n)>0):
                nCap.set(str(n[:-1]))
                
    def sepIni(self,ctrl):
        ctrl.sms.sendPacket(
            SMS.Address.Broadcast,
            SMS.Message.StartStop.type,
            SMS.Message.StartStop.Start
        )
        global nCaps
        for i in range(0,9,1):
                nCaps[i].set(0)
        
        ctrl.showFrame(separacao2)
        
                
class separacao2(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black") 
        canvas = tk.Canvas(self,bg="black",highlightthickness=0)
        canvas.pack(fill='both',expand=1) 
        canvas.create_rectangle(450,30,805,110,width=3,outline='red')
        l1 = tk.Label(self, text="EM OPERAÇÃO...",font=("Paytone One", 20),fg='red',bg='black').place(x=517,y=48)
        global nCaps
        nCaps = []
        for i in range(0,9,1):
                var = tk.StringVar(self)
                var.set("0")
                nCaps.append(var)
        nCaps[8].set(0)
        y = 160
        n=0
        for x in range(45,750,90):
                canvas.create_oval(x,y,x+70,y+70,width=3,outline='grey')
                l = tk.Label(self, text=n,font=("Paytone One", 28),fg='grey',bg='black').place(x=x+22,y=y+5)
                nc = tk.Label(self, textvar=nCaps[n],font=("Paytone One", 40),width=2,justify='center',fg='white',bg='black').place(x=x,y=y+78)
                n = n+1
        l2 = tk.Label(self, text="TOTAL:",font=("Paytone One", 30),fg='white',bg='black').place(x=45,y=355)
        l3 = tk.Label(self, textvar=nCaps[8],font=("Paytone One", 40),fg='#db9d00',bg='black').place(x=205,y=345)
        buttonGo = tk.Button(self, text = "PARAR",font=("Paytone One", 25),bd=12,bg='red',activebackground='red',fg="black",height=1,width=10,command=lambda:self.sepStop(controller)).place(x=470,y=350)
    
    def sepStop(self,ctrl):
        ctrl.sms.sendPacket(
            SMS.Address.Broadcast,
            SMS.Message.StartStop.type,
            SMS.Message.StartStop.Stop
        )
        ctrl.showFrame(separacao3)


class separacao3(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black") 
        canvas = tk.Canvas(self,bg="black",highlightthickness=0)
        canvas.pack(fill='both',expand=1) 
        canvas.create_rectangle(450,30,805,110,width=3,outline='#00B050')
        l1 = tk.Label(self, text="OPERAÇÃO CONCLUÍDA",font=("Paytone One", 20),fg='#00B050',bg='black').place(x=465,y=48)
        global nCaps
        y = 160
        n=0
        for x in range(45,750,90):
                canvas.create_oval(x,y,x+70,y+70,width=3,outline='grey')
                l = tk.Label(self, text=n,font=("Paytone One", 28),fg='grey',bg='black').place(x=x+22,y=y+5)
                nc = tk.Label(self, textvar=nCaps[n],font=("Paytone One", 40),width=2,justify='center',fg='white',bg='black').place(x=x,y=y+78)
                n = n+1
        l2 = tk.Label(self, text="TOTAL:",font=("Paytone One", 30),fg='white',bg='black').place(x=45,y=355)
        l3 = tk.Label(self, textvar=nCaps[8],font=("Paytone One", 40),fg='#db9d00',bg='black').place(x=205,y=345)
        buttonGo = tk.Button(self, text = "AVANÇAR",font=("Paytone One", 25),bd=12,bg='#00B050',activebackground='#00B050',fg="black",height=1,width=10,command=lambda:controller.showFrame(menuSep)).place(x=470,y=350)


class contagem1(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black") 
        global nCaps 
        canvas = tk.Canvas(self,bg="black",highlightthickness=0)
        canvas.pack(fill='both',expand=1) 
        canvas.create_rectangle(450,30,805,110,width=3,outline='red')
        l1 = tk.Label(self, text="EM OPERAÇÃO...",font=("Paytone One", 20),fg='red',bg='black').place(x=517,y=48)
        l2 = tk.Label(self, text="Nº DE CÁPSULAS:",font=("Paytone One", 30),fg='white',bg='black').place(x=230,y=155)
        l3 = tk.Label(self, textvar=nCaps[8],font=("Paytone One", 50),width=5,justify='center',fg='#db9d00',bg='black').place(x=280,y=205)
        buttonGo = tk.Button(self, text = "PARAR",font=("Paytone One", 30),bd=12,bg='red',activebackground='red',fg="black",height=1,width=10,command=lambda:self.exitCont1(controller)).place(x=233,y=340)
 
    def exitCont1(self,ctrl):
        ctrl.sms.sendPacket(
            SMS.Address.Broadcast,
            SMS.Message.StartStop.type,
            SMS.Message.StartStop.Stop
        )
        ctrl.showFrame(contagem2)
        

class contagem2(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black")  
        global nCaps
        canvas = tk.Canvas(self,bg="black",highlightthickness=0)
        canvas.pack(fill='both',expand=1) 
        canvas.create_rectangle(450,30,805,110,width=3,outline='#00B050')
        l1 = tk.Label(self, text="OPERAÇÃO CONCLUÍDA",font=("Paytone One", 20),fg='#00B050',bg='black').place(x=465,y=48)
        l2 = tk.Label(self, text="Nº DE CÁPSULAS:",font=("Paytone One", 30),fg='white',bg='black').place(x=230,y=155)
        l3 = tk.Label(self, textvar=nCaps[8],font=("Paytone One", 50),width=5,justify='center',fg='#db9d00',bg='black').place(x=280,y=205)
        buttonGo = tk.Button(self, text = "AVANÇAR",font=("Paytone One", 30),bd=12,bg='#00B050',activebackground='#00B050',fg="black",height=1,width=10,command=lambda:controller.showFrame(menuSep)).place(x=233,y=340)


class calib1(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black")   
        l1 = tk.Label(self, text="Selecione a cor a calibrar:",font=("Paytone One", 20),fg='white',bg='black').place(x=50,y=124)
        caps = Image.open(IMG_CAPS)
        caps = caps.resize((700,130),Image.ANTIALIAS)
        caps= ImageTk.PhotoImage(caps, Image.ANTIALIAS)
        capsImg = tk.Label(self, image=caps, bg='black')
        capsImg.image = caps
        capsImg.place(x=45,y=160)
        buttonBack = tk.Button(self, text = "VOLTAR",font=("Paytone One", 20),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=7,command=lambda:controller.showFrame(menuSep)).place(x=570,y=40)
        button1 = tk.Button(self, text = "",font=("Paytone One", 10),bd=0,bg='#D8CF3B',activebackground='#D8CF3B',fg="black",height=3,width=3,command=lambda:self.exitCalib1(controller,0)).place(x=65,y=300)
        button2 = tk.Button(self, text = "",font=("Paytone One", 10),bd=0,bg='#F9EA0B',activebackground='#F9EA0B',fg="black",height=3,width=3,command=lambda:self.exitCalib1(controller,1)).place(x=139,y=300)
        button4 = tk.Button(self, text = "",font=("Paytone One", 10),bd=0,bg='#075730',activebackground='#075730',fg="black",height=3,width=3,command=lambda:self.exitCalib1(controller,2)).place(x=213,y=300)
        button5 = tk.Button(self, text = "",font=("Paytone One", 10),bd=0,bg='#D8CF3B',activebackground='#D8CF3B',fg="black",height=3,width=3,command=lambda:self.exitCalib1(controller,3)).place(x=213,y=380)
        button6 = tk.Button(self, text = "",font=("Paytone One", 10),bd=0,bg='#91AE8D',activebackground='#91AE8D',fg="black",height=3,width=3,command=lambda:self.exitCalib1(controller,4)).place(x=287,y=300)
        button7 = tk.Button(self, text = "",font=("Paytone One", 10),bd=0,bg='#075730',activebackground='#075730',fg="black",height=3,width=3,command=lambda:self.exitCalib1(controller,5)).place(x=287,y=380)
        button8 = tk.Button(self, text = "",font=("Paytone One", 10),bd=0,bg='#075730',activebackground='#075730',fg="black",height=3,width=3,command=lambda:self.exitCalib1(controller,6)).place(x=360,y=300)
        button9 = tk.Button(self, text = "",font=("Paytone One", 10),bd=0,bg='#007CCB',activebackground='#007CCB',fg="black",height=3,width=3,command=lambda:self.exitCalib1(controller,7)).place(x=437,y=300)
        button10 = tk.Button(self, text = "",font=("Paytone One", 10),bd=0,bg='#EA2322',activebackground='#EA2322',fg="black",height=3,width=3,command=lambda:self.exitCalib1(controller,8)).place(x=513,y=300)
        button11 = tk.Button(self, text = "",font=("Paytone One", 10),bd=0,bg='#EA2322',activebackground='#EA2322',fg="black",height=3,width=3,command=lambda:self.exitCalib1(controller,9)).place(x=589,y=300)

    def exitCalib1(self,ctrl,color):
        ctrl.sms.sendPacket(
            SMS.Address.Classification,
            SMS.Message.CalibrationColor.type,
            color
        )
        ctrl.showFrame(calib2)
        

class calib2(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black")   
        global nPoints,meanR,meanG,meanB,r,g,b
        nPoints = 0
        meanR = 0
        meanG = 0
        meanB = 0
        r = 0
        g = 0
        b = 0
        rec = tk.Canvas(self,bg='black',highlightthickness=2,width=268,height=76)
        rec.place(x=470,y=200)
        l1 = tk.Label(self, text="Selecione a cor pretendida:",font=("Paytone One", 20),fg='white',bg='black').place(x=50,y=140)
        self.rgbCode = tk.StringVar(self)
        self.rgbCode.set("")
        l3 = tk.Label(self, textvar=self.rgbCode,font=("Paytone One", 14),fg='white',bg='black').place(x=550,y=225)
        self.canvas = tk.Canvas(self,bg=from_rgb((0,0,0)),highlightthickness=0,width=60,height=60)
        self.canvas.place(x=480,y=210)
        self.sep = Image.open(IMG_SEP)
        self.sep = self.sep.resize((IMG_DIMX,IMG_DIMY),Image.ANTIALIAS)
        self.sep= ImageTk.PhotoImage(self.sep, Image.ANTIALIAS)
        self.imgSep = tk.Label(self, image=self.sep, bg='black')
        self.imgSep.image = self.sep
        self.imgSep.place(x=IMG_X,y=IMG_Y)
        buttonBack = tk.Button(self, text = "VOLTAR",font=("Paytone One", 20),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=7,command=lambda:self.exitCalib2(controller,"back")).place(x=570,y=40)
        buttonNext = tk.Button(self, text = "SEGUINTE",font=("Paytone One", 20),bd=10,bg='#00B050',activebackground='#00B050',fg="black",height=1,width=10,command=lambda:self.exitCalib2(controller,"next")).place(x=516,y=370)
        buttonAdd = tk.Button(self, text = "ADICIONAR PONTO",font=("Paytone One", 14),bd=10,bg='grey',activebackground='grey',fg="black",height=1,width=14,command=lambda:self.updateMean()).place(x=515,y=296)

    def updateMean(self):
        global meanR,meanG,meanB,r,g,b,nPoints
        nPoints = nPoints + 1
        if (nPoints==1):
                meanR = r
                meanG = g
                meanB = b
        else:
                meanR = int((meanR*(nPoints-1)+r)/nPoints)
                meanG = int((meanG*(nPoints-1)+g)/nPoints)
                meanB = int((meanB*(nPoints-1)+b)/nPoints)
    
    def updateRGB(self):
        global X,Y,meanR,meanG,meanB,nPoints,r,g,b
        if ((X<IMG_DIMX)and(Y<IMG_DIMY)):
                #print("X: "+str(X)+"   Y: "+str(Y)+"  MeanR: "+str(meanR)+"  MeanG: "+str(meanG)+"  MeanB: "+str(meanB)+"  nPoints: "+str(nPoints))
                #print("R: "+str(r)+"   G: "+str(g)+"   B: "+str(b))
                im = Image.open(IMG_SEP)
                im = im.resize((IMG_DIMX,IMG_DIMY),Image.ANTIALIAS)
                im = im.convert('RGB')
                r, g, b = im.getpixel((X, Y))
                self.canvas.config(bg=from_rgb((r,g,b)))
                self.rgbCode.set("R:"+str(r)+" G:"+str(g)+" B:"+str(b))
                
    def exitCalib2(self,ctrl,dest):
        global meanR,meanG,meanB,nPoints
        if ((dest=="next")and(nPoints>0)):
                ctrl.frames[calib3].calibColor.config(bg=from_rgb((meanR,meanG,meanB)))
                ctrl.frames[calib3].rgbCode.set("R: "+str(meanR)+"\nG: "+str(meanG)+"\nB: "+str(meanB))
                nPoints = 0
                ctrl.sms.sendPacket(
                    SMS.Address.Classification,
                    SMS.Message.CalibrationRComponent.type,
                    meanR
                )
                ctrl.sms.sendPacket(
                    SMS.Address.Classification,
                    SMS.Message.CalibrationGComponent.type,
                    meanG
                )
                ctrl.sms.sendPacket(
                    SMS.Address.Classification,
                    SMS.Message.CalibrationBComponent.type,
                    meanB
                )
                ctrl.showFrame(calib3)
        elif (dest=="back"):
                nPoints = 0
                ctrl.showFrame(calib1)
                
                

class calib3(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black")  
        self.rgbCode = tk.StringVar(self)
        self.rgbCode.set("")
        canvas = tk.Canvas(self,bg="black",highlightthickness=0)
        canvas.pack(fill='both',expand=1) 
        canvas.create_rectangle(430,30,805,110,width=3,outline='#00B050')
        canvas.create_rectangle(200,160,600,300,width=2,outline='white')
        l1 = tk.Label(self, text="CALIBRAÇÃO CONCLUÍDA",font=("Paytone One", 20),fg='#00B050',bg='black').place(x=448,y=48)
        l2 = tk.Label(self, text="COR SELECIONADA:",font=("Paytone One", 15),fg='white',bg='black').place(x=220,y=168)
        l3 = tk.Label(self, textvar=self.rgbCode,font=("Paytone One", 14),fg='white',bg='black').place(x=240,y=202)
        self.calibColor = tk.Canvas(self,bg=from_rgb((0,0,0)),highlightthickness=0,width=80,height=80)
        self.calibColor.place(x=490,y=190)
        buttonGo = tk.Button(self, text = "AVANÇAR",font=("Paytone One", 30),bd=12,bg='#00B050',activebackground='#00B050',fg="black",height=1,width=10,command=lambda:controller.showFrame(menuSep)).place(x=233,y=340)
     

class emergencyStop(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="black")   
        imgEme = Image.open(IMG_EMER)
        imgEme = imgEme.resize((800,480),Image.ANTIALIAS)
        imgEme= ImageTk.PhotoImage(imgEme, Image.ANTIALIAS)
        emeMsg = tk.Label(self, image=imgEme, bg='black')
        emeMsg.image = imgEme
        emeMsg.place(x=0,y=0)


def from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

def calculate_coordinates(event):
    global X,Y
    X = event.x
    Y = event.y

app = interface()
app.mainloop()
