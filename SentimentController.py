from SentimentModel import SentimentModel
from SentimentGrapher import SentimentGrapher as sg

class SentimentController:
    def __init__(self) :
        self.model = SentimentModel()
        
    def setUserView(self, view):
        self.userview = view
        
    def setTrendview(self, view) :
        self.trendview = view
    
    
    def loadCSV(self, filepath):
        #"C:\\Users\\taole\\Imperial_local\\2_NLP4MS\\nlp-ui-project\\dummy_free2.csv"
        self.model.importFile(filepath)
    
    def buildUserInfo(self, userId) -> str:
        #TODO: diagnosis date not imported correctly
        return self.model.getUserInfo(userId)
    
    def buildUserGraphs(self, tk_frame, userId, sent_on, disabl_on,
                                        anx_on, combine_on):
        if sent_on:
            #generate sentiment history
            sentimentHistory = self.model.buildSentimentHistory_single(userId = userId)
            print(sentimentHistory)
            sg.plotSentimentHistory_single(sentimentHistory, tk_frame)
        
        # if self.disabl_on:
        #     edssHistory = analyzer.buildEDSSHistory_single(userId)
        #     sg.plotEDSSHistory()