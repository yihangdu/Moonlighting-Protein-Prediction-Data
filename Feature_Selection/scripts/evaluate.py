"""
This program should be executed after all first-layer prediction job finished.
It gives several stats, such as accuracy, and output a .csv file containing all info.
"""

# This program should be in /stage3_blast_prediction/1st-layer when executing

import csv
import math
import os
import sys

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
    round_num = sys.argv[1]
    drop_total = sys.argv[2]
    header = ["alpha\evaluation", "acc", "precision", "recall", "F-Measure", "MCC"]
    assess_store = []
        
    TP = 0
    TN = 0

    FP = 0
    FN = 0
    
    for i in range(int(drop_total)):
        for j in range(1, 11):
            
            testFilePath = f"../round{round_num}/drop{i}/fold{j}/test{j}.txt"
            predFilePath = f"../round{round_num}/drop{i}/fold{j}/test{j}.txt.predict"

            testFile = open(testFilePath, 'r')
            predicFile = open(predFilePath, 'r')
            outcome = extract(testFile, predicFile)
            testFile.close()
            predicFile.close()

            TP += outcome[0]
            TN += outcome[1]
            FN += outcome[2]
            FP += outcome[3]

        assess = assessment(TP, TN, FN, FP)
        print("Accuracy:", assess[0])
        assess_store.append([f"drop{i}"] + [k for k in assess])

    with open(f'Performance_Evaluation_{round_num}.csv', 'w') as csv_file:

        writer = csv.writer(csv_file)
        writer.writerow(header)
        for lst in assess_store:
            writer.writerow(lst)


    os.system(f'mv Performance_Evaluation_{round_num}.csv ../')


    

    
        

main()

        



