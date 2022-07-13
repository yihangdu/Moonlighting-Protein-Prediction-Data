import csv
import math
import os

def extract(testFile, predicFile):

    test_value = []
    pred_value = []
    
    for row1 in testFile:
        test_value.append(row1[0])

    for row2 in predicFile:
        pred_value.append(row2[0])

    if len(test_value) != len(pred_value):
        print("Possible data messing! 1")
        exit(1)

    TP = 0
    TN = 0

    FP = 0
    FN = 0

    for i in range(len(test_value)):
        if test_value[i] == "0" and pred_value[i] == "0":
            TP += 1

        elif test_value[i] == "0" and pred_value[i] == "1":
            FN += 1

        elif test_value[i] == "1" and pred_value[i] == "0":
            FP += 1
            
        elif test_value[i] == "1" and pred_value[i] == "1":
            TN += 1

    return TP, TN, FN, FP


def assessment(TP, TN, FN, FP):

    acc = (TP + TN) / (TP + FP + TN + FN)

    precision = TP / (TP + FP)

    recall = TP /(TP + FN)

    F_Measure = 2*(precision*recall) / (precision + recall)

    MCC = (TP*TN - FP*FN) / math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))

    return acc, precision, recall, F_Measure, MCC



def main():
    header1 = ["fold","TP", "TN", "FN", "FP"]
    header2 = ["acc", "precision", "recall", "F-Measure", "MCC"]
    tmp_store = []
        
    TP = 0
    TN = 0

    FP = 0
    FN = 0

    for i in range(10):
        
        testFilePath = "prediction" + str(i) + "/"
        testFileName = "test" + str(i) + ".txt"
        predFilePath = "prediction" + str(i) + "/"
        predFileName = "test" + str(i) + ".txt.predict"

        testFile = open(testFilePath + testFileName, 'r')
        predicFile = open(predFilePath + predFileName, 'r')
        outcome = extract(testFile, predicFile)
        testFile.close()
        predicFile.close()

        print(outcome)
        
        tmp_store.append(["fold"+str(i + 1)]+[i for i in outcome])
        
        TP += outcome[0]
        TN += outcome[1]
        FN += outcome[2]
        FP += outcome[3]

    assess = assessment(TP, TN, FN, FP)
    print("Accuracy:", assess[0])
    
    with open('Performance_Evaluation.csv', 'w') as csv_file:

        writer = csv.writer(csv_file)
        writer.writerow(header1)
        for lst in tmp_store:
            writer.writerow(lst)

        writer.writerow(["total", TP, TN, FN, FP])
        
        writer.writerow(header2)
        writer.writerow([i for i in assess])
    

    
        

main()

        




















    
