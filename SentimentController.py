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
        #TODO: need to check that all dates follow "%d/%m/%Y" format
        self.model.importFile(filepath)
    
    
    #   USER PAGE
    def buildUserInfo(self, userId) -> str:
        #TODO: diagnosis date not imported correctly
        return self.model.getUserInfo(userId)
    
    
    def buildUserGraphs(self, userId, tk_frame, sent_on, 
                        disabl_on, combine_on):
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
    
    #TREND PAGE
    def calcSentiments(self):
        self.model.calcSentiments()
        return
    
    def calcEDSS(self):
        self.model.processEDSS()
        
        return
    
    
    def buildTrendGraphs(self, num, displayFrame,
                         sa_on, disabl_on):
        if sa_on.get():
            self.model.buildSentimentHistory(cap = num)
        if disabl_on.get():
            self.model.buildEDSSHistory(cap = num)
            
        sg.plotTrendGraphs(displayFrame, sa_on.get(), disabl_on.get(),
                           self.model.sentimentHistory,
                           self.model.EDSS_history)
        return
    
    
    def buildSentDistribution(self, num, displayFrame,
                              distroNeg_on, distroNeu_on,
                              distroPos_on, distroComp_on,
                              scatter_on):
        sg.plotSentimentDistribution(num, displayFrame, self.model.sentimentSet,
                              distroNeg_on.get(), distroNeu_on.get(),
                              distroPos_on.get(), distroComp_on.get(),
                              scatter_on.get())
        return