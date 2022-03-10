
#import nltk
#nltk.data.path.append("S:\ICLMScProject - Imperial MSc project/nltk_data")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

######################################################
class VaderSentimentAnalyzer:
    
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
        Build sentiment table sorted by UserId with cap specifying number of users. User must have a minimum of 
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
    

    
    def BuildSentimentHistory(self, inputData, userId, minN = 3):
        """
        Build sentiment history of one user. 
        Parameters:
            -inputData  --  pd.DataFrame: UserId and Value (string) 
                            required.
            -userId     --  self explanatory.
            -minN       --  minimum number of data points to be considered.
        Returns:
            -pd.DataFrame with structure:
             ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
             sorted by UserId
        """
        dataPts = inputData.loc[inputData["UserId"] == userId]
        if len(dataPts) < minN:
            print("No match found!")
            return

        col = ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
        sentiments = pd.DataFrame(columns = col)
        idx = 0
        for index, row in dataPts.iterrows():
            s = self.calculateSentiment(str(row['Value']))
            #process date format. some are just strings.
            date = str(row["CompletedDate"])            
            dateProcessed = datetime.strptime(date , "%d/%m/%Y")
            content = [userId, dateProcessed, s["neg"], s["neu"], s["pos"], s["compound"]]
            sentiments.loc[idx] = content
            idx += 1
        
        return sentiments
    
    
        
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
    
    def calcSentiments(self, inputData, numPts = 0) :
        """
        Build sentiment history of one user. 
        Parameters:
            -inputData  --  pd.DataFrame: UserId and Value (string) 
                            required.
            -numPts     --  Number of data pts to be calculated.
                            if 0, will calculate all pts in set.
        Returns:
            -np.array with structure: ["compound", "neg", "neu", "pos"]
        """
        #calc sentiments   
        data = inputData.filter(["Value"])
        sens = np.zeros((numPts, 4))

        count = 0
        for idx, row in data.iterrows():
            if idx % int(numPts/10) == 0:
                print(f"Processing sentiments {idx/numPts * 100}% ...")
            if numPts != 0 and count == numPts:
                break
            res = self.calculateSentiment(str(row['Value']));
            sens[idx] = res["compound"], res["neg"] , res["neu"] , res["pos"]
            count+=1
            
            
    def _collapseSameDateEntries(userId, dataPts) :
        """ Checks if there are several entries for the same date. If there are,
            entries will be collapsed into one with mean taken for the sentiments.

        Args:
            userId (int): Unique user ID belonging to the data points.
            dataPts (pd.DataFrame): 
                ["UserId", "CompletedDate", 
                "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
        """
        uniqueDates = pd.unique(dataPts.loc[:, "CompletedDate"])
        for date in range(len(uniqueDates)):
            sameDate = dataPts.loc[dataPts["CompletedDate"] == uniqueDates[date]]
            if len(sameDate) > 1:
                avgScore = [userId, uniqueDates[date], 
                            sameDate["Sent_Neg"].mean(), sameDate["Sent_Neu"].mean(),
                            sameDate["Sent_Pos"].mean(), sameDate["Sent_Comp"].mean()]
                dataPts = dataPts.loc[dataPts["CompletedDate"] != uniqueDates[date]]
                dataPts.loc[len(dataPts)] = avgScore
        return