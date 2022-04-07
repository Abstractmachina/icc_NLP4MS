import pandas as pd
from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

import csv
import random
import time
# import lipsum # for testing purposes only!

#================================================================
class DataQuery:
    """Generic data extractor for csv file. any header name 
    can be added to query, will return empty if name doesnt match."""


    #headers legend for MS specific table
    #DOB	Gender	OnsetDate	DiagnosisDate	MSAtDiagnosis	MSTypeNow	QuestionnaireKey	
    #QuestionnaireId	CompletedDate	Value	GroupId	QueryDate
    def __init__(self, path, filterVals):
        self.path = path;
        self.filterValues = filterVals
    
    def execute(self) -> pd.DataFrame:
        """Execute query and return a pd.DataFrame;
        # """
        dat_raw = pd.read_csv(self.path)
        dat = dat_raw.filter(self.filterValues)
        return dat
    
#================================================================
class DataQueryBuilder:

    """
    syntax: query(path).withAttr1().withAttr2().build().execute()
    will return a pd.DataFrame. Without execute() will return 
    a DataQuery object.
    """
    
    def __init__(self):
        self.filterValues = list()
        self.path = None
        
    @staticmethod
    def query(path):
        qb = DataQueryBuilder()
        qb.path = path
        return qb
        
    def build(self):
        return DataQuery(self.path, self.filterValues)
        
    def add(self, customHeader) :
        """Append a custom header to the query string.
        Args:
            customHeader (string): Match with header in CSV file.

        """
        self.filterValues.append(customHeader)
        return self
    
    def withUserId(self):
        self.filterValues.append("UserId")
        return self
    
    def withBirthDate(self):
        self.filterValues.append("DOB")
        return self    
    
    def withOnsetDate(self):
        self.filterValues.append("OnsetDate")
        return self
    
    def withValue(self):
        self.filterValues.append("Value")
        return self
    
    def withDiagnosisDate(self):
        self.filterValues.append("DiagnosisDate")
        return self
    
    def withQuestionnaireId(self):
        self.filterValues.append("QuestionnaireId")
        return self
    
    def withCompletedDate(self):
        self.filterValues.append("CompletedDate")
        return self
    
    def withGroupdD(self):
        self.filterValues.append("GroupId")
        return self
    
    def withGender(self):
        self.filterValues.append("Gender")
        return self
    
    def withMSAtDiagnosis(self):
        self.filterValues.append("MSAtDiagnosis")
        return self
    
    def withMSTypeNow(self):
        self.filterValues.append("MSTypeNow")
        return self
    
    def withQuestionnaireKey(self):
        self.filterValues.append("QuestionnaireKey")
        return self
    
    def withWebEDSS(self):
        self.filterValues.append("webEDSS")
        return self
    
    def withCompletedDate_webEDSS(self):
        self.filterValues.append("CompletedDate_webEDSS")
        return self

#================================================================

class DataDisplayer:
 
    """
    Display/Download Graphs in App Feature
    """
 
    #Embeds MatplotLib Chart into a Window.
    def display(plot, title, window):
        fig = Figure(figsize = (5,5), dpi = 100)
        canvas = FigureCanvasTkAgg(fig, master = window)
        canvas.draw()
        canvas.get_tik_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
        canvas.get_tik_widget().pack()
 
        window.title(title)
        window.geometry("750x750")
        plot_button = Button(master = window, 
                     command = plot,
                     height = 2, 
                     width = 10,
                     text = "Plot")
        plot_button.pack()
 

 #===============================================================
 #Utility functions
def min_max_scaling(self, data, minV, maxV):
    return (data - minV) / (maxV - minV)

#===============================================================
#                   RANDOM CSV GENERATOR
#===============================================================
"""
For testing purposes only.

def generateFreeText(filename, N):
    headers = ["UserId","Value","CompletedDate", "webEDSS", "Anxiety", "Depression", "DOB", "Gender", "MS_Type", "OnsetDate", "DiagnosisDate"]
    
    with open(filename, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        
        csvwriter.writerow(headers)
        
        for i in range(N):
            row = []
            row.append(random.randrange(0,N/4)) #userid
            txt = lipsum.generate_words(random.randrange(50, 500))
            row.append(txt) #value
            date = str_time_prop("1/1/2000", "25/3/2021", "%d/%m/%Y", random.random())
            row.append(date)
            row.append(random.randrange(0,10)) #EDSS disability
            row.append(random.randrange(0, 21)) #anxiety
            row.append(random.randrange(0,21)) #depression
            row.append(str_time_prop("1/1/1970", "1/1/1990", "%d/%m/%Y", random.random())) # dob
            r = random.random()
            row.append("M" if r > 0.5 else "F") #Gender
            row.append(str_time_prop("1/1/1990", "1/1/2005", "%d/%m/%Y", random.random())) #onset date
            row.append(str_time_prop("1/1/2000", "1/1/2020", "%d/%m/%Y", random.random())) #diagnosis date
            
            csvwriter.writerow(row)
    return

def generateScores(filename, N):
    headers = ["UserId","CompletedDate", "webEDSS"]
    
    with open(filename, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        
        csvwriter.writerow(headers)
        
        for i in range(N):
            row = []
            row.append(random.randrange(0,N/4)) #userid
            date = str_time_prop("1/1/2000", "25/3/2021", "%d/%m/%Y", random.random())
            row.append(date)
            row.append(random.randrange(0,10)) #EDSS disability
            row.append(random.randrange(0, 21)) #anxiety
            row.append(random.randrange(0,21)) #depression
            csvwriter.writerow(row)
    return

def str_time_prop(start, end, time_format, prop):
    '''Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    '''

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y', prop)

if __name__ == "__main__":
    generateFreeText("dummy_free2.csv", 100)
    
"""