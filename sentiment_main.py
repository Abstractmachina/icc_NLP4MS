import numpy as np

#import sys
#sys.path.append("S:\ICLMScProject - Imperial MSc project\Taole\sentimentAnalysis")
#import dataProcessing as dp

from SentimentAnalyzer import SentimentAnalyzer
from SentimentGrapher import SentimentGrapher as graph

#from sentimentAnalysis import getPolarityScore
#import nltk
#nltk.data.path.append("S:\ICLMScProject - Imperial MSc project/nltk_data")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

import DataProcessing as dp
    
    
######################################################
def main():
    
    path = "C:\\Users\\taole\\Imperial_local\\2_NLP4MS\\nlp-ui-project\\example_csv.csv"
    
    dat = dp.DataQueryBuilder.query(path).withUserId().withValue().withCompletedDate().build().execute()
    
    analyzer = SentimentAnalyzer()
    sentimentHistory = analyzer.buildSentimentHistory(dat, minN=2, cap = 50)
    graph.plotSentimentHistory(sentimentHistory)
    return
    
    path2 = "C:\\Users\\taole\\Imperial_local\\2_NLP4MS\\nlp-ui-project\\edss_example.csv"
    dat2 = dp.DataQueryBuilder.query(path2).withUserId().withCompletedDate_webEDSS().withWebEDSS().build().execute()
    
    print(dat2)
    
    edss_history = analyzer.buildEDSSHistory(inputData = dat2, dateFormat = "%d.%m.%Y", minN = 2, cap = 50)
    uniqueUser = pd.unique(edss_history.loc[:,"UserId"])
    
    for i in range(len(uniqueUser)):
        graph.plot_EDSS_sentiment(uniqueUser[i], edss_history, sentimentHistory)
    
    return

    #################################################
    #sentiment distribution
    #################################################
    

    #calc sentiments   
    numPts= 1000
    data = dat_raw.filter(["Value"])
    sens = np.zeros((numPts, 4))
    count = 0
    
    printCountNeg = 0
    printCountPos = 0
    printCountNeu = 0
    num_extracts = 20
    for idx, row in data.iterrows():
        if idx % int(numPts/10) == 0:
            print(f"Processing sentiments {idx/numPts * 100}% ...")
        if count == numPts:
             break
        res = SentimentIntensityAnalyzer().polarity_scores(str(row['Value']))
        sens[idx] = res["compound"], res["neg"] , res["neu"] , res["pos"]
        count+=1
        if res["neg"] > 0.8 and printCountNeg < num_extracts:
            with open("negPrint.txt", "a") as f:
                f.write(str(row["Value"]))
                f.write("\n")
                print(f"neg val: {str(row['Value'])}")
                printCountNeg += 1
        if res["pos"] > 0.8 and printCountPos < num_extracts:
            with open("posPrint.txt", "a") as f:
                f.write(str(row["Value"]))
                f.write("\n")
                print(f"pos val: {str(row['Value'])}")
                printCountPos += 1
        if res["neu"] > 0.9 and printCountNeu < num_extracts:
            with open("neuPrint.txt", "a") as f:
                f.write(str(row["Value"]))
                f.write("\n==================\n")
                f.write("\n")
                printCountNeu += 1
   
                
            
    #calc distribution
    #compound distro
    numSlices = 100
    sc = sens[sens[:, 0] != 0]
    plt.hist(sc[:,0], numSlices)
    plt.title("Compound Sentiment Distribution")
    plt.ylabel("count")
    plt.xlabel("score")
    plt.show()
    
    #negative distro
    sc = sens[sens[:, 1] != 0]
    plt.hist(sc[:,1], numSlices)
    plt.title("Negative Sentiment Distribution")
    plt.ylabel("count")
    plt.xlabel("score")
    plt.show()
    
    #neutral distro
    sc = sens[sens[:, 2] != 0]
    plt.hist(sc[:,2], numSlices)
    plt.title("Neutral Sentiment Distribution")
    plt.ylabel("count")
    plt.xlabel("score")
    plt.show()
    
    #positive distro
    sc = sens[sens[:, 3] != 0]
    plt.hist(sc[:,3], numSlices)
    plt.title("Positive Sentiment Distribution")
    plt.ylabel("count")
    plt.xlabel("score")
    plt.show()
    
    #scatter positive to negative sentiment
    plt.figure()
    plt.scatter(sens[:, 1], sens[:, 3])
    plt.title("Positive to Negative Sentiment")
    plt.xlabel("negative sentiment")
    plt.ylabel("positive sentiment")
    plt.show()
    
    
    #get specific freetext based on sentiment value
    return
    
if __name__ == "__main__":
    main()