import matplotlib.pyplot as plt
import enum
import pandas as pd

class SentimentScoreType(enum.Enum) :
    COMPOUND = 0
    NEGATIVE = 1
    NEUTRAL = 2
    POSITIVE = 3

class SentimentGrapher:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def plotScoreDistribution(sentimentScores, type, numSlices = 100, ) :
        """_summary_
            Plots a histogram showing the distribution of one sentiment score type.
        Args:
            sentimentScores ( ndarray ( ,4) ): 0 = compound, 1 = neg, 2 = neu, 3 = pos.
            type (int): select which type to plot.
            numSlices (int, optional): Define resolution of histogram. Defaults to 100.
        """
        if type < 0 or type > 3:
            raise ValueError("Sentiment Type must be value 0-3.")
#
        numSlices = 100
        #filter out 0
        sc = sentimentScores[sentimentScores[:, type] != 0]
        
        plt.hist(sc[:,0], numSlices)
        plt.title("Compound Sentiment Distribution")
        plt.ylabel("count")
        plt.xlabel("score")
        plt.show()
        
        
    @staticmethod
    def plotNegPosScatter(sentimentScores) : 
        """_summary_
            Plots a scatter graph. x-axis for negative sentiment, y-axis for 
            positive sentiment
        Args:
            sentimentScores (ndarray ( , 4 )): 0 = compound, 1 = neg, 2 = neu, 3 = pos.
        """
        #scatter positive to negative sentiment
        plt.figure()
        plt.scatter(sentimentScores[:, 1], sentimentScores[:, 3])
        plt.title("Positive to Negative Sentiment")
        plt.xlabel("negative sentiment")
        plt.ylabel("positive sentiment")
        plt.show()
        
        
    @staticmethod
    def plotSentimentHistory(sentimentHistory):
        """Plot sentiment history of a collection of users. 
        Args:
            sentimentHistory (pd.DataFrame): 
                ["UserId", "CompletedDate", 
                "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
                
        """
        print("Building sentiment history plot...")
        uniqueId = pd.unique(sentimentHistory.loc[:,"UserId"])
        fig, ax = plt.subplots(2,1, figsize=(13,10))
        for user in range(len(uniqueId)):
            dataPts = sentimentHistory.loc[sentimentHistory["UserId"] == uniqueId[user]]
            
            sortedPts = dataPts.sort_values(by="CompletedDate")
            
            if sortedPts.iloc[0]["Sent_Comp"] < sortedPts.iloc[-1]["Sent_Comp"]:
                ax[0].plot(sortedPts["CompletedDate"], sortedPts["Sent_Comp"])
            else:
                ax[1].plot(sortedPts["CompletedDate"], sortedPts["Sent_Comp"])
                
        ax[0].set_title("Improved Outcome")
        ax[1].set_title("Deteriorated Outcome")
        plt.show()
        return
    
    @staticmethod
    def plot_EDSS_sentiment(userId, edss_history, sentiment_history):
        
        data_edss = edss_history.loc[edss_history["UserId"] == userId]
        data_sent = sentiment_history.loc[sentiment_history["UserId"] == userId]
        
        #if no matching user, ignore
        if len(data_sent) == 0 or len(data_edss) == 0:
            print("No matches found.")
            return
        
        sorted_edss = data_edss.sort_values(by="CompletedDate")
        sorted_sent = data_sent.sort_values(by="CompletedDate")
        plt.figure()
        
        plt.plot(sorted_edss["CompletedDate"], sorted_edss["EDSS"])
        plt.plot(sorted_sent["CompletedDate"], sorted_sent["Sent_Comp"])
        
        plt.show()
        return
            