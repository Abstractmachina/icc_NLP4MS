from math import comb
from SentimentModel import SentimentModel
from SentimentGrapher import SentimentGrapher_tk as sg

class SentimentController:
    def __init__(self) :
        self.model = SentimentModel()
        
        
    def setUserView(self, view):
        self.userview = view
        
        
    def setTrendview(self, view) :
        self.trendview = view
    
    
    def loadCSV(self, filepath):
        self.model.importFile(filepath)
    
    
    def buildUserInfo(self, userId) -> str:
        #TODO: diagnosis date not imported correctly
        return self.model.getUserInfo(userId)
    
    
    def buildUserGraphs(self, userId, tk_frame, sent_on, disabl_on, combine_on):
        sHist = None
        dHist = None
        if sent_on.get() or combine_on.get():
            sHist = self.model.buildSentimentHistory_single(userId)
        if disabl_on.get() or combine_on.get():
            dHist = self.model.buildEDSSHistory_single(userId)
        
        sg.plotUserGraphs(  tk_frame, sent_on.get(), 
                            disabl_on.get(), combine_on.get(), 
                            sentimentHistory=sHist, edssHistory=dHist)
        return
    
    
    def getFreeTxt(self, userId) -> list:
        result = "\n\n\n"
        txt = self.model.getUserFreetxt(userId)
        for entry in txt:
            result += entry
            result += "\n\n"
        return result