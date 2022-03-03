
#from sentimentAnalysis import getPolarityScore
#import nltk
#nltk.data.path.append("S:\ICLMScProject - Imperial MSc project/nltk_data")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

######################################################
class SentimentAnalyzer:
    
    def __init__(self):
        #self.sentiments
        pass
        
    def calculateSentiment(self, text):
        '''
        Arguments:
            -text -- string
        Return: 
            dictionary with keys ["neg", "neu", "pos", "compound"]
        '''
        result = pd.DataFrame()
        
        result = SentimentIntensityAnalyzer().polarity_scores(text)
        return result
        

    def buildSentimentHistory(self, inputData, minN = 3, cap = 0):
        '''
        Build sentiment table sorted by UserId. User must have a minimum of 
        minN data points to be added to the table.
        
        Parameters:
            -inputData  --  pd.DataFrame: UserId and Value (string) 
                            required.
            -minN       --  minimum number of data points to be considered.
            -cap        --  function is stopped when number of found users reaches cap.
        Returns:
            -pd.DataFrame with structure:
             ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
             sorted by UserId
        '''
        
        uniqueUserId = pd.unique(inputData.loc[:,"UserId"])

        
        col = ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
        sentiments = pd.DataFrame(columns = col)
        userCount = 0
        idx = 0
        for i in range(len(uniqueUserId)):
            dataPts = inputData.loc[inputData["UserId"] == uniqueUserId[i]]
            if len(dataPts) < minN:
                continue
            if cap != 0 and userCount > cap:
                break
            if cap !=0 and userCount % int(cap/20) == 0:
                    print(f"Calculating Sentiments {int((userCount/cap) * 100)}%")
            for index, row in dataPts.iterrows():
                
                s = self.calculateSentiment(str(row['Value']))
                #process date format. some are just strings.
                date = str(row["CompletedDate"])            
                dateProcessed = datetime.strptime(date , "%d/%m/%Y")
                content = [uniqueUserId[i], dateProcessed, s["neg"], s["neu"], s["pos"], s["compound"]]
                sentiments.loc[idx] = content
                idx += 1
            userCount += 1
        print("Finished Calculating Sentiments")
        return sentiments
    
    
    def plotSentimentHistory(self, sentimentHistory):
        """
        Parameters:
            -sentimentHistory --pd.DataFrame with structure:
                ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
                
        """
        print("Building sentiment history plot...")
        uniqueId = pd.unique(sentimentHistory.loc[:,"UserId"])
        fig, ax = plt.subplots(2,1, figsize=(13,10))
        for user in range(len(uniqueId)):
            
            
            dataPts = sentimentHistory.loc[sentimentHistory["UserId"] == uniqueId[user]]
            
            #check if there are multiple entries for same date.
            #if so, collapse into averaged score
            uniqueDates = pd.unique(dataPts.loc[:, "CompletedDate"])
            for date in range(len(uniqueDates)):
                sameDate = dataPts.loc[dataPts["CompletedDate"] == uniqueDates[date]]
                if len(sameDate) > 1:
                    avgScore = [uniqueId[user], uniqueDates[date], 
                                sameDate["Sent_Neg"].mean(), sameDate["Sent_Neu"].mean(),
                                sameDate["Sent_Pos"].mean(), sameDate["Sent_Comp"].mean()]
                    dataPts = dataPts.loc[dataPts["CompletedDate"] != uniqueDates[date]]
                    dataPts.loc[len(dataPts)] = avgScore
                
            sortedPts = dataPts.sort_values(by="CompletedDate")

            
            if sortedPts.iloc[0]["Sent_Comp"] < sortedPts.iloc[-1]["Sent_Comp"]:
                ax[0].plot(sortedPts["CompletedDate"], sortedPts["Sent_Comp"])
            else:
                ax[1].plot(sortedPts["CompletedDate"], sortedPts["Sent_Comp"])
                
        ax[0].set_title("Improved Outcome")
        ax[1].set_title("Deteriorated Outcome")
        plt.show()
            
        return
        
    def buildEDSSHistory(self, inputData, minN = 3, cap = 0):
        uniqueUserId = pd.unique(inputData.loc[:,"UserId"])

        col = ["UserId", "CompletedDate", "EDSS"]
        EDSS = pd.DataFrame(columns = col)
        userCount = 0
        idx = 0
        for i in range(len(uniqueUserId)):
            dataPts = inputData.loc[inputData["UserId"] == uniqueUserId[i]]
            
            if len(dataPts) < minN:
                continue
            if cap != 0 and userCount > cap:
                break
            
            
            if cap !=0 and userCount % int(cap/20) == 0:
                    print(f"Calculating EDSS {int((userCount/cap) * 100)}%")
                    
            for index, row in dataPts.iterrows():
                date = str(row["CompletedDate_webEDSS"])            
                dateProcessed = datetime.strptime(date , "%Y-%m-%d")
                
                content = [uniqueUserId[i], dateProcessed, row["webEDSS"]]
                #temp = pd.DataFrame(content, columns = col)
                EDSS.loc[idx] = content
                idx+=1
            userCount += 1
            
        print("Finished building EDSS")
        return EDSS


    def plot_EDSS_sentiment(self, userId, edss_history, sentiment_history):
        
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
            
            
        
        
    def min_max_scaling(self, data):
        minV = np.min(data)
        maxV = np.max(data)
        return (data - minV) / (maxV - minV)
    
    