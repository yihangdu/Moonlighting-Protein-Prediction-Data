import os
import sys


def main():

    featureFile = open("Conclusion.csv")

    features = []
    for lines in featureFile:
        features.append(lines.split(",")[0])

    features.remove("PseKRAAC_T1")
    features.remove("")
    
    
    for i in range(len(features)):
        for j in range(10):
            
            OS_predict = "./../svm-predict " + features[i] \
                         + "/prediction" + str(j) + "/train" + str(j) + ".txt.scale "\
                         + features[i] \
                         + "/prediction" + str(j) + "/train" + str(j) + ".txt.model "\
                         + "train" + str(j) + ".txt.predict"
            
            OS_mv = "mv train" + str(j) + ".txt.predict " + features[i]\
                    + "/prediction" + str(j)
            
            os.system(OS_predict)
            os.system(OS_mv)

main()
