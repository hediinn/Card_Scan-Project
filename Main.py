import easyocr
import cv2
import numpy as np
import torch
import tkinter as tk
from PIL import Image, ImageTk
import DbSFCVS as SQL
import random
import time
#from mtgsdk import Card
#these are the imports i will use


if __name__=="__main__":
#if __main__: sentens



    #This is the tkinter window setup
    window = tk.Tk()
    window.wm_title("test") #title of the window is test, needs to be changed
    window.geometry('{}x{}'.format(1200,300)) #This is the size of the window

    #These are the frames inside the window, collours must be change
    topFrame = tk.Frame(window,bg='gray60',width=520,height=10,pady=2)
    imageFrame = tk.Frame(window,bg='black', width=520, height=200,padx=5,pady=5)
    SkideFrame = tk.Frame(window,bg='gray60',width=300,height=200,pady=4)
    topLeftFrame = tk.Frame(window,bg='gray60',width=300,height=10,pady=2)

    
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(501, weight=1)


    #This is the grid setup for the frames
    topFrame.grid(row=0,column=0,padx=5,pady=2,sticky="news")
    imageFrame.grid(row=1, column=0, padx=5, pady=2,sticky="news")
    SkideFrame.grid(row=1,column=1,padx=0, pady=0,sticky="news")
    topLeftFrame.grid(row=0,column=1,padx=2, pady=2,sticky="news")     

    #This is a item inside a frame, it's bg is black becouse the frame is black
    lmain = tk.Label(imageFrame,bg="black")
    lmain.grid(row=1, column=0)# It's possion in the grid

    cap = cv2.cv2.VideoCapture(0,cv2.cv2.CAP_DSHOW)# this is for taking the webcam feed

    var1= tk.IntVar() #this is for the checkbox so it is posible to check if it has been checked
    var2 = tk.IntVar()
    global VaribleX = 0
    reader = easyocr.Reader(['en'],gpu=True,model_storage_directory="tessdata")
    #This is the reader function, I chose to load it early so that the largest part of lagines is at the start 



    def show_frame():# This functiom shows either the test frame or the webcam feed
        showButton.config(state=tk.DISABLED) #this is mainly so the program dosn't crash
        if var1.get()==1: # this checks if the checkbox has benn checked or not
            _, frame = cap.read()
            croPD=cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
            croPD= croPD[320:520,0:1300]
            img = Image.fromarray(croPD)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)
        elif var1.get()==0:
            frame=cv2.imread(r"image000R.jpg")
            croPD=cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
            img = Image.fromarray(croPD)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10,show_frame)
        
    
    def rLine(): #this is a fuction that scans whats intfron of the webcam or scans the test image
        if var1.get()==1:
            try:
                _, frame = cap.read()
                frame= cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
                croPD=frame
                croPD= croPD[320:520,0:1300]
                result = reader.readtext(croPD,workers=2,detail=0,paragraph=True,slope_ths=0.1)
                listOfCards.insert(tk.END,str(result[0]))
            except:
                print("test")
        elif var1.get()==0:
            try:
                frame=cv2.cv2.imread(r'image000R.jpg')
                frame=cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
                croPD=frame
                result=reader.readtext(croPD,workers=2,detail=0,paragraph=True,slope_ths=0.1)
                listOfCards.insert(tk.END,str(result[0]))
            except:
                print("test")
    
    def deleteSelectedItem():
        sel = listOfCards.curselection()
        for index in sel[::-1]:
            listOfCards.delete(index)

    def checkSelItem():
        sel= listOfCards.curselection()
        for i in sel[::-1]:
            time.sleep(0.1)
            ser =SQL.Scryfall(listOfCards.get(i))
            checkdText = ser.realName
            if checkdText != listOfCards.get(i):
                listOfCards.delete(i)
                listOfCards.insert(i,checkdText)
                
    
    def addCardToDB():
        
        if var2.get() ==1:
            sel= listOfCards.curselection()
            for i in sel[::-1]:
                db= SQL.SQL(db="cards")
                db.sendCard(str(listOfCards.get(i)))
        elif var2.get()==0:
            global VaribleX =global VaribleX+1
            sel= listOfCards.curselection()
            for i in sel[::-1]:
                db = SQL.CSV()
                db.InPutData(VaribleX, str(listOfCards.get(i)))

    #this is a function for adding a card to the listbox so that i check if the checkSelIttem fuction works
    def addCardToBox():

        listOfRCards=["Domri's Ambush","Viviens Grizzly","Skywhalers Shot"]
        listOfCards.insert(tk.END,listOfRCards[random.randint(0, 2)])



    ScanButton=tk.Button(master=topFrame,text="Scan Frame",command=rLine)
    ScanButton.grid(row=0,column=0,padx=5,pady=2)
    
    showButton=tk.Button(master=topFrame,text="Show Frame",command=show_frame)
    showButton.grid(row=0,column=1,padx=5,pady=2)
    checkBox2=tk.Checkbutton(master=topFrame,text="Use database",variable=var2,bg="gray")
    checkBox2.grid(row=1,column=0,sticky="nwes")
    sendToFiOrDb=tk.Button(master=topFrame,text="send to db\n or file",command=addCardToDB)
    sendToFiOrDb.grid(row=1,column=1,padx=5,pady=2)   

    checkBox1=tk.Checkbutton(master=SkideFrame,text="use webcam",variable=var1,bg="gray")
    checkBox1.grid(row=0,column=0,sticky="nwes")


    scrollBar = tk.Scrollbar(master=SkideFrame)
    listOfCards= tk.Listbox(master=SkideFrame,yscrollcommand=scrollBar.set,selectmode=tk.MULTIPLE,width=70)
    listOfCards.grid(row=1,column=0,sticky="news")
    scrollBar.config(command=listOfCards.yview)
    scrollBar.grid(row=1,column=1,sticky="news")

    deleteSelectedbot=tk.Button(master=topLeftFrame,text="Delete\nSellected",command=deleteSelectedItem)
    deleteSelectedbot.grid(row=0,column=0,sticky="news")     

    checkSelBot=tk.Button(master=topLeftFrame,text="Check\nSellected",command=checkSelItem)
    checkSelBot.grid(row=0,column=1,sticky="news") 

    addRandom=tk.Button(master=topLeftFrame,text="Add\ncard",command=addCardToBox)
    addRandom.grid(row=1,column=0,sticky="news") 

    window.mainloop()


