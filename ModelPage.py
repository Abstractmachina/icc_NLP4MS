from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from predict_adapter import predict

class ModelPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app

        self.configureModelPage()

    def configureModelPage(self):
        """
        Configures the model page, when the model prediction is clicked. 
        Here, the model is easily replacable (we use an adapter)
        """
        
        
        l = Label(self.frame, text="Please enter the text you wish to predict: ")
        l.pack(side=TOP)
        # Configure large text box
        self.text_entry = Text(self.frame, undo = True)
        self.text_entry.pack(side=TOP)

        # Configure back button
        back_b = ttk.Button(self.frame, text="Back", command= lambda: self.app.displayFrame("home frame"))
        back_b.pack(padx=5, pady=15, side=RIGHT)

        # Configure predict button
        predict_b = ttk.Button(self.frame, text="Predict", command=self.predictModelPopUp)
        predict_b.pack(padx=5, pady=20, side=RIGHT)
    
    def predictModelPopUp(self):
        # get main window position
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()

        # add offset
        win_x = root_x + 300
        win_y = root_y + 100

        # Popup window
        modelPopupWindow = Toplevel()
        modelPopupWindow.geometry(f'+{win_x}+{win_y}')
        modelPopupWindow.wm_title("Prediction")
        l = Label(modelPopupWindow, text="The MS type predicted from the given text is:")
        l.grid(row=0, column=0)

        predict_text = self.text_entry.get("1.0", 'end-1c')
        prediction = predict(predict_text)
        ans = Label(modelPopupWindow, text=prediction)
        ans.grid(row=1, column=0)

        b = ttk.Button(modelPopupWindow, text="Okay", command=modelPopupWindow.destroy)
        b.grid(row=3, column=0)