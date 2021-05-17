import easyocr
import cv2
import numpy as np
import torch
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import dataSavers as SQL
import random
import time

if __name__=="__main__":
#if __main__: sentens

    lGray ='gray60'
    dGray ='gray'
    tFrStic = "NEW"

    #This is the tkinter window setup
    window = tk.Tk()
    window.wm_title("Magic Card Scanner") 
    window.geometry('{}x{}'.format(1200,600)) #This is the size of the window

    #These are the frames inside the window, collours must be change
    topFrame = tk.Frame(window,bg=lGray,width=700,height=10,pady=2)
    imageFrame = tk.Frame(window,bg='black', width=700, height=200,padx=5,pady=2)
    SkideFrame = tk.Frame(window,bg=lGray,width=300,height=400,pady=2)
    topRightFrame = tk.Frame(window,bg=lGray,width=300,height=10,pady=2)
     

    #This is the grid setup for the frames
    topFrame.grid(row=0,column=0,padx=5,pady=2,sticky=tFrStic)
    imageFrame.grid(row=1, column=0, padx=5, pady=2)

    SkideFrame.grid(row=1,column=1,padx=2, pady=2,sticky="news")
    topRightFrame.grid(row=0,column=1,padx=2, pady=2,sticky=tFrStic)     

    #This is a item inside a frame, it's bg is black becouse the frame is black
    lmain = tk.Label(imageFrame,bg="black")
    lmain.grid(row=0, column=0)# It's possion in the grid

    cap = cv2.cv2.VideoCapture(0,cv2.cv2.CAP_DSHOW)# this is for taking the webcam feed

    var1= tk.IntVar() #this is for the checkbox so it is posible to check if it has been checked
    var2 = tk.IntVar()
    var3 = tk.StringVar()
    ResizeX0 = 200
    ResizeY0 = 150
    ResizeX = 1000
    ResizeY = 1300

    if torch.cuda.is_available():
        reader = easyocr.Reader(['en'],gpu=True,model_storage_directory="tessdata")
    else:
        reader = easyocr.Reader(['en'],gpu=False,model_storage_directory="tessdata")
    #This is the reader function, I chose to load it early so that the largest part of lagines is at the start 


    def show_frame():# This functiom shows either the test frame or the webcam feed
        showButton.config(state=tk.DISABLED) #this is mainly so the program dosn't crash
        if var1.get()==1: # this checks if the checkbox has benn checked or not
            _, frame = cap.read()
            croPD=cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
            croPD= croPD[ResizeX0:ResizeX,ResizeY0:ResizeY]
            img = Image.fromarray(croPD)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)
        elif var1.get()==0:
            frame=cv2.imread(r"image000R.jpg")
            croPD=cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
            croPD= croPD
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
                croPD=frame[ResizeX0:ResizeX,ResizeY0:ResizeY]
                result = reader.readtext(croPD,workers=2,detail=0,paragraph=True,slope_ths=0.1)
                listOfCards.insert(tk.END,str(result[0]))
            except Exception():
                print("test")
        elif var1.get()==0:
            try:
                frame=cv2.cv2.imread(r'image000R.jpg')
                frame=cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
                croPD=frame
                result=reader.readtext(croPD,workers=2,detail=0,paragraph=True,slope_ths=0.1)
                listOfCards.insert(tk.END,str(result[0]))
            except Exception():
                print("test")
    
    def deleteSelectedItem():
        sel = listOfCards.curselection()
        for index in sel[::-1]:
            listOfCards.delete(index)

    def checkSelItem():
        sel= listOfCards.curselection()
        for i in sel[::-1]:
            time.sleep(0.1)
            try:
                ser =SQL.Scryfall(listOfCards.get(i))
                checkdText = ser.realName
                if checkdText != listOfCards.get(i):
                    listOfCards.delete(i)
                    listOfCards.insert(i,checkdText)
                listOfCards.selection_clear(i)
            except:
                print("name to wrong, fix whit entryBox")


    def addCardToDB():
        
        sel= listOfCards.curselection()
        for value,i in enumerate( sel[::-1]):
            if var2.get() ==1:
                db= SQL.SQL()
                db.sendCard(str(listOfCards.get(i)))
                listOfCards.selection_clear(i)
            elif var2.get()==0:
                db = SQL.Xcel()
                db.InPutData(value, str(listOfCards.get(i)))
                listOfCards.selection_clear(i)

    #this is a function for adding a card to the listbox so that i check if the checkSelIttem fuction works
    def addCardToBox():

        listOfRCards=["Domri's Ambush","Viviens Grizzly","Skywhalers Shot","Teferi's Ageless Insight"]
        listOfCards.insert(tk.END,listOfRCards[random.randint(0, 3)])
    def editTextBox():
        sel = listOfCards.curselection()
        for i in sel[::-1]:
            nav= listOfCards.get(i)
            userInp = simpledialog.askstring(title="test", prompt="Current name: \n"+ str(nav)+"\n Press ok to change to what you have typed")
            if userInp !="" :
                listOfCards.delete(i)
                listOfCards.insert(i,userInp)

    ScanButton=tk.Button(master=topFrame,text="Scan Frame",command=rLine)
    ScanButton.grid(row=0,column=0,padx=5,pady=2)
    
    showButton=tk.Button(master=topFrame,text="Show Frame",command=show_frame)
    showButton.grid(row=0,column=1,padx=5,pady=2)
    
    checkBox2=tk.Checkbutton(master=topFrame,text="Use database",variable=var2,bg=dGray)
    checkBox2.grid(row=1,column=0,sticky="nwes")
    
    sendToFiOrDb=tk.Button(master=topFrame,text="send to db\n or file",command=addCardToDB)
    sendToFiOrDb.grid(row=1,column=1,padx=5,pady=2)   
    
    editSelect=tk.Button(master=topFrame,text="Edit Sellected",command=editTextBox)
    editSelect.grid(row=0,column=2,padx=5,pady=2)   
 

    checkBox1=tk.Checkbutton(master=SkideFrame,text="use webcam",variable=var1,bg=dGray)
    checkBox1.grid(row=0,column=0,sticky="nwes")
    scrollBar = tk.Scrollbar(master=SkideFrame)
    listOfCards= tk.Listbox(master=SkideFrame,yscrollcommand=scrollBar.set,selectmode=tk.MULTIPLE,width=70,height=27)
    listOfCards.grid(row=1,column=0,sticky="news")
    scrollBar.config(command=listOfCards.yview)
    scrollBar.grid(row=1,column=1,sticky="news")

    deleteSelectedbot=tk.Button(master=topRightFrame,text="Delete\nSellected",command=deleteSelectedItem)
    deleteSelectedbot.grid(row=0,column=0,sticky="news")     

    checkSelBot=tk.Button(master=topRightFrame,text="Check\nSellected",command=checkSelItem)
    checkSelBot.grid(row=0,column=1,sticky="news") 

    addRandom=tk.Button(master=topRightFrame,text="Add\ncard",command=addCardToBox)
    addRandom.grid(row=1,column=0,sticky="news") 

    window.mainloop()


