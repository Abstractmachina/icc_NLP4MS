
#import nltk
#nltk.data.path.append("S:\ICLMScProject - Imperial MSc project/nltk_data")
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from VaderSentimentAdapter import VaderSentimentAdapter

######################################################
class SentimentAnalyzer():
    
    def __init__(self):
        self.sentimentHistory = pd.DataFrame()
        self.sentimentSet = pd.DataFrame()
        #adapter returns single sentiment as a dict with keys
        #["neg", "neu", "pos", "compound"].
        self.adapter = VaderSentimentAdapter()
        pass
        
    def calcSentiments(self, inputData = pd.DataFrame, numPts = 10) -> pd.DataFrame:
        """Calculate sentiments by entry. Will process all data points
        in set if numPts is set to 0. Warning: If data set is large, 
        will have a high time cost.
        
        Args:
            -inputData  --  pd.DataFrame: UserId and Value (string) 
                            required.
            -numPts     --  Number of data pts to be calculated.
                            if 0, will calculate all pts in set.
        Returns:
            -pd.DataFrame with structure:
             ["UserId", "CompletedDate", 
             "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
        """
        #calc sentiments   
        data = inputData.filter(["Value"])
        sens = np.zeros((numPts, 4))
        col = ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
        sentiSet = pd.DataFrame(columns = col)

        setLength = len(data) if numPts == 0 else numPts
 
        count = 0
        for idx, row in data.iterrows():
            if idx % int(setLength/10) == 0:
                print(f"Processing sentiments {idx/numPts * 100}% ...")
            if numPts != 0 and count == numPts:
                break
            res = VaderSentimentAdapter.calculateSentiment(str(row['Value']))
            sens[idx] = res["compound"], res["neg"] , res["neu"] , res["pos"]
            processedDate = datetime.strptime(str(row["CompletedDate"]), "%d/%m/%Y")
            content = [row["UserId"], processedDate, res["neg"], res["neu"], res["pos"], res["compound"]]
            sentiSet.loc[count] = content
            count+=1
            
        return sens
            

    def buildSentimentHistory(self, inputData = pd.DataFrame, minN = 3, cap = 0) -> pd.DataFrame:
        """Build sentiment table sorted by UserId with cap specifying number of users. 
        User must have a minimum of minN data points to be added to the table.

        Args:
            inputData (DataFrame):  UserId and Value (string) required.
            minN (int, optional):   Minimum number of data points to be considered. 
                                    Defaults to 3.
            cap (int, optional):    Function is stopped when number 
                                    of found users reaches cap. Defaults to 0.
        Returns:
            pd.DataFrame: ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
             sorted by UserId
        """
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
                
                s = self.adapter.calculateSentiment(str(row['Value']))
                #process date format. some are just strings.
                date = str(row["CompletedDate"])            
                dateProcessed = datetime.strptime(date , "%d/%m/%Y")
                content = [uniqueUserId[i], dateProcessed, s["neg"], s["neu"], s["pos"], s["compound"]]
                sentiments.loc[idx] = content
                idx += 1
            userCount += 1
        print("Finished Calculating Sentiments")
        return sentiments
    

    def BuildSentimentHistory(self, inputData = pd.DataFrame, userId = int, minN = 3) -> pd.DataFrame:
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
            s = VaderSentimentAdapter.calculateSentiment(str(row['Value']))
            #process date format. some are just strings.
            date = str(row["CompletedDate"])            
            dateProcessed = datetime.strptime(date , "%d/%m/%Y")
            content = [userId, dateProcessed, s["neg"], s["neu"], s["pos"], s["compound"]]
            sentiments.loc[idx] = content
            idx += 1
        
        return sentiments
    
    
        
    def buildEDSSHistory(self, inputData = pd.DataFrame, dateFormat = str, minN = 3, cap = 0):
        """_summary_

        Args:
            inputData (pd.DataFrame): _description_
            dateFormat (str): example "%Y-%m-%d"
            minN (int, optional): Minimum number of data pts per user. Defaults to 3.
            cap (int, optional): Function finishes when cap is reached. Defaults to 0.

        Returns:
            _type_: _description_
        """
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
                dateProcessed = datetime.strptime(date , dateFormat)
                
                
                content = [uniqueUserId[i], dateProcessed, row["webEDSS"]]
                #temp = pd.DataFrame(content, columns = col)
                EDSS.loc[idx] = content
                idx+=1
            userCount += 1
            
        print("Finished building EDSS")
        return EDSS
    
    
            
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