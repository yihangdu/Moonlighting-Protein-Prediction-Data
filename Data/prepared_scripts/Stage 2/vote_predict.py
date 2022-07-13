import csv
import math
def readPrediction(inFile):
    
    protNames = []
    prediction = []
    for line in inFile:

        if "|" in line:
            protNames.append(line.split())
            
        elif "fold" not in line and "test" not in line:
            line = line.split(",")
            line.remove(line[0])
            line[-1] = line[-1].replace("\n", "")
            prediction.append(line)

    return protNames, prediction

def calc_stats(vote_table):
    oriType = []
    for i in range(10):
        fileName = "DDE/prediction" + str(i) + "/test" + str(i) + ".txt"
        oriTest = open(fileName, "r")

        for line in oriTest:
            oriType.append(line[0])

    statsTable = []


    for i in range(len(vote_table[0])):
        TP = 0
        TN = 0
        FN = 0
        FP = 0
        statsList = []
        for j in range(len(vote_table)):

            if oriType[j] == "0" and vote_table[j][i] == "0":
                TP += 1
            elif oriType[j] == "0" and vote_table[j][i] == "1":
                FN += 1
            elif oriType[j] == "1" and vote_table[j][i] == "0":
                FP += 1
            elif oriType[j] == "1" and vote_table[j][i] == "1":
                TN += 1
        statsList += [TP, TN, FN, FP]
        statsTable.append(statsList)


    return statsTable


def assessment(TP, TN, FN, FP):

    acc = (TP + TN) / (TP + FP + TN + FN)

    precision = TP / (TP + FP)

    recall = TP /(TP + FN)

    F_Measure = 2*(precision*recall) / (precision + recall)

    if (TP+FP)*(TP+FN)*(TN+FP)*(TN+FN) == 0:
        MCC = "NA"
    else:
        MCC = (TP*TN - FP*FN) / math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))

    return acc, precision, recall, F_Measure, MCC



def main():


    inFile = open("Predict_Test_Table.csv", "r")

    result = readPrediction(inFile)

    protNames = result[0]
    predictions = result[1]
   
    inFile.close()

    with open("vote_prediction.csv", "w") as vote:

        threshold = ["proteins/threshold"] + [i for i in range(0,37)]
        vote_table = []


        for i in range(len(protNames)):
            votePred = []
            for j in range(0,37):
                
                if predictions[i].count("0") >= j:
                    votePred.append("0")
                else:
                    votePred.append("1")
            vote_table.append(votePred)
        statsTable = calc_stats(vote_table)

        protNames += ["acc", "precision", "recall", "F_Measure", "MCC"]

        for i in range(len(statsTable)):
            statsTable[i] = list(assessment(statsTable[i][0], statsTable[i][1],\
                                            statsTable[i][2], statsTable[i][3]))

        writer = csv.writer(vote)
        writer.writerow(threshold)

        for i in range(len(protNames)):
            row = [protNames[i]]
            
            if i < len(protNames) - 5:
                row += vote_table[i]
                
            else:
                j = 5 - (len(protNames) - i)
                
                for k in range(len(statsTable)):
                    myData = statsTable[k][j]
                    if type(myData) == str:
                        row.append(myData)
                    else:
                        row.append(round(myData, 2))
            
            writer.writerow(row)
            





main()
