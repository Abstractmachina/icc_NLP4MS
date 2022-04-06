from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter import filedialog
from AppClass import App

""" This Code is purely Aesthetic - creates a Splash Screen with a Loading Bar, deletes itself and then runs AppClass"""

w=Tk()

width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))


w.overrideredirect(1)


s = ttk.Style()
s.theme_use('classic')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
progress=Progressbar(w,style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=500,mode='determinate',)

""" Responsible for creating an instance of the app and running the app """

def load_app_class():
    root = Tk()
    App(root)
    root.mainloop()

""" LOADING BAR, once complete, it deletes the Splash Window and calls load_app_class above"""

def bar():

    l4=Label(w,text='Loading...',fg='white',bg=a)
    lst4=('Calibri (Body)',10)
    l4.config(font=lst4)
    l4.place(x=18,y=210)
    import time
    r=0
    for i in range(100):
        progress['value']=r
        w.update_idletasks()
        time.sleep(0.03)
        r=r+1
    
    w.destroy()

    load_app_class()

""" GET STARTED BUTTON """
    
progress.place(x=-10,y=235)
a='#249794'
Frame(w,width=427,height=241,bg=a).place(x=0,y=0)  #249794
b1=Button(w,width=10,height=1,text='Get Started',command=bar,border=0,fg=a,bg='white')
b1.place(x=170,y=200)


""" LABELS """

l1=Label(w,text='PATIENT FREE TEXT EXPLORER',fg='white',bg=a)
lst1=('Calibri (Body)',18,'bold')
l1.config(font=lst1)
l1.place(x=50,y=80)


l3=Label(w,text='Applying NLP to better understand MS',fg='white',bg=a)
lst3=('Calibri (Body)',13)
l3.config(font=lst3)
l3.place(x=50,y=110)


w.mainloop()


