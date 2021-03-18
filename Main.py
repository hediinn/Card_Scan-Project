import easyocr
import cv2
import numpy as np
import torch
import tkinter as tk
from PIL import Image, ImageTk
#these are the imports i will use


if __name__=="__main__":
#if __main__: sentens



    #This is the tkinter window setup
    window = tk.Tk()
    window.wm_title("test") #title of the window is test, needs to be changed
    window.geometry('{}x{}'.format(600,300)) #This is the size of the window

    #These are the frames inside the window, collours must be change
    topFrame = tk.Frame(window,bg='cyan',width=500,height=20,pady=2)
    imageFrame = tk.Frame(window,bg='black', width=500, height=200,padx=5,pady=5)
    SkideFrame = tk.Frame(window,bg='green',width=200,height=200,pady=4)
    
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(501, weight=1)


    #This is the grid setup for the frames
    topFrame.grid(row=0,column=0,padx=5,pady=2,sticky="news")
    imageFrame.grid(row=1, column=0, padx=5, pady=2,sticky="news")
    SkideFrame.grid(row=1,column=1,padx=0, pady=0,sticky="news")     

    #This is a item inside a frame, it's bg is black becouse the frame is black
    lmain = tk.Label(imageFrame,bg="black")
    lmain.grid(row=1, column=0)# It's possion in the grid

    cap = cv2.cv2.VideoCapture(0,cv2.cv2.CAP_DSHOW)# this is for taking the webcam feed

    var1= tk.IntVar() #this is for the checkbox so it is posible to check if it has been checked

    reader = easyocr.Reader(['en'],gpu=True,model_storage_directory="tessdata")
    #This is the reader function, I chose to load it early so that the largest part of lagines is at the start 


    def show_frame():# This functiom shows either the test frame or the webcam feed
        testButton.config(state=tk.DISABLED) #this is mainly so the program dosn't crash
        if var1.get()==1: # this checks if the checkbox has benn checked or not
            _, frame = cap.read()
            croPD=cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
            croPD= croPD[320:520,0:500]
            img = Image.fromarray(croPD)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)
        elif var1.get()==0:
            frame=cv2.cv2.imread("image000R.jpg")
            croPD=cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
            img = Image.fromarray(croPD)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10,show_frame)
        
    
    def rLine():
        if var1.get()==1:
            _, frame = cap.read()
            frame= cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
            croPD=frame
            croPD= croPD[320:520,0:750]
            result = reader.readtext(croPD,workers=2,detail=0,paragraph=True,slope_ths=0.1)
            print(result[0])
            test.config(text=test.cget("text")+"\n"+result[0])
        elif var1.get()==0:
            frame=cv2.cv2.imread("image000R.jpg")
            frame=cv2.cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2GRAY)
            croPD=frame
            result=reader.readtext(croPD,workers=2,detail=0,paragraph=True,slope_ths=0.1)
            
            test.config(text=test.cget("text")+"\n"+result[0])
            print(result)


    textButton=tk.Button(master=topFrame,text="Scan Frame",command=rLine)
    textButton.grid(row=0,column=0)
    
    testButton=tk.Button(master=topFrame,text="Show Frame",command=show_frame)
    testButton.grid(row=0,column=2)
    checkBox1=tk.Checkbutton(master=SkideFrame,text="use webcam",variable=var1,bg="green")
    checkBox1.grid(row=1,column=1,sticky="nwes")

    test= tk.Label(SkideFrame,text="cards \n that have\n been scanned\n----------",bg="green")

    test.grid(row=2,column=1,sticky="news")
     


    window.mainloop()


