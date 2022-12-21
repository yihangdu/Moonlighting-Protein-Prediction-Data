"""
This program outputs and manages .arff files required for weka. 
"""

# This file should be in /Data_s3/stage3_blast_prediction/2nd-layer when executing.


import os

"""
This function will be called for each fold to extract predicted result across different alpha.
It returns a list of lists. Each small list should have length of 20 with predicted result of
training/test set of certain proteins.

foldNum: an integer that ranges from 1 to 10 representing fold number
is_train: a string with option {"train", "test"} indicating training/test set to read
"""
def readFold(foldNum, is_train):
    finalList = []

    for i in range(1,21):
        # read predicted result
        fin = open(f"../../alpha{i}/fold{foldNum}/{is_train}{foldNum}.txt.scale.predict")
        foldList = fin.readlines()
        
        for j in range(len(foldList)):
            foldList[j] = foldList[j][0]

        finalList.append(foldList)

        fin.close()

    # read label
    fin = open(f"../../alpha1/fold{foldNum}/{is_train}{foldNum}.txt")
    finList = fin.readlines()
    labelList = []

    for line in finList:
        labelList.append(line[0])

    if len(labelList) != len(finalList[0]):
        print(foldNum, is_train, len(labelList),len(finalList[0]))
        print("Result reading error: lengths of label and predicted result don't match!")
        exit(1)
        
    finalList.append(labelList)
    
    # get transpose of finalList for the convenience of formating files later
    transpose = [[-1 for i in range(len(finalList))] for j in range(len(finalList[0]))]

    for i in range(len(finalList)):
        for j in range(len(transpose)):
            transpose[j][i] = finalList[i][j]

    return transpose


"""
This function outputs and manages required input file for weka.

featureList: 3-D list of size 10, containing feature matrix for each fold
is_train: string with option {"train", "test"} indicating if it is training or testing set
"""
def writeFile(featureList, is_train):

    for i in range(len(featureList)):

        foldMatrix = featureList[i]
        fout = open(f"weka_{is_train}{i+1}.arff", "w")

        fout.write("@relation protein_type\n\n")

        for j in range(1, 21):
            fout.write(f"@attribute alpha{j} {{0, 1}}\n")

        fout.write("@attribute protein_type {0, 1}\n")
        fout.write("\n@data\n")

        for j in range(len(foldMatrix)):
            for k in range(len(foldMatrix[j])):

                if k != len(foldMatrix[j])-1:
                    fout.write(f"{foldMatrix[j][k]},")
                else:
                    fout.write(f"{foldMatrix[j][k]}\n")

        fout.close()
        
        
        os.system(f"mv weka_{is_train}{i+1}.arff ../../weka_fold{i+1}")


def main():

    trainFeatureList = []
    testFeatureList = []
    for i in range(1,11):
        os.system(f"mkdir ../../weka_fold{i}")
        trainFeatureList.append(readFold(i, "train"))
        testFeatureList.append(readFold(i, "test"))

    writeFile(trainFeatureList, "train")
    writeFile(testFeatureList, "test")


main()
        
        
    
