import abc

class ISentimentAnalyzer(abc.ABC) :
    @abc.abstractclassmethod
    def calculateSentiment(self) :
        pass

    @abc.abstractclassmethod
    def buildSentimentHistory(self) :
        pass

    @abc.abstractclassmethod
    def buildEDSSHistory(self) :
        pass

    


