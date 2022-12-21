# Based on how each function is structured, when writing main function for this program, one should notice:
# before calling randomize and writeFile functions, both svm format lists of MP and nonMP should be prepared.
# This program should be placed in /stage3_blast_prediction/1st-layer when executing. If any problem of
# accessing files or move files occure, check file path in code.

import os

"""
This function opens and read in alpha features, then returns a list of strings, each item is a protein's feature
"""
def readFile(filePath):
    dataList = []
    inFile = open(filePath, "r")

    dataLine = False
    for line in inFile:
        if ">" in line:
            dataLine = True
            continue

        elif dataLine:
            dataList.append(line[:-1])
            dataLine = False

        else:
            continue
    inFile.close()

    return dataList

"""
This function takes in two parameters:
data: list type, strings of protein sequences, returned by readFile
isMP: bool type, denote if data is MP, if True, length of data should be 215, label is 0;
                                       if False, length of data should be 136, label is 1.
This function returns a list of strings that are svm format of protein sequence
"""
def covert2svm(data, isMP):

    # check if number of protein sequences from readFile is correct
    if isMP:
        if len(data) != 215:
            print("Number of MP proteins not correct, check readFile function!")
            exit(1)
    else:
        if len(data) != 136:
            print("Number of non-MP proteins not correct, check readFile function!")
            exit(1)

    svmList = []

    for protein in data:
        svmString = "0 " if isMP else "1 "
        proteinList = protein.split()

        for i in range(len(proteinList)):
            if float(proteinList[i]) != 0:
                svmString += f"{str(i+1)}:{proteinList[i]} "

            else:
                continue
        svmString += "\n"
        svmList.append(svmString)

    return svmList

"""
This function randomize the order of protein sequences for both MP and nonMP. The randomized order is based on
new_rand_x.txt stored in Data_s3/stage3_blast_prediction/random_select.
"""
def randomize(MP_svmList, nMP_svmList):
    randSeed_0 = open("../random_select/new_random_0.txt", "r") # there should be 215 non-redundant random index numbers
    randSeed_1 = open("../random_select/new_random_1.txt", "r") # there should be 136 non-redundant random index numbers

    rand_MP_svmList = []
    rand_nMP_svmList = []

    for i in randSeed_0:
        rand_MP_svmList.append(MP_svmList[int(i)])

    for i in randSeed_1:
        rand_nMP_svmList.append(nMP_svmList[int(i)])

    if len(rand_MP_svmList) != 215 or len(rand_nMP_svmList) != 136:
        print("Incorrect number of proteins! ||function: randomize")
        exit(1)

    randSeed_0.close()
    randSeed_1.close()

    return rand_MP_svmList, rand_nMP_svmList


"""
This function takes in a tuple containing one list of MP strings and another of non_MP strings returned by randomize 
and outputs three files: train_x.txt, test_x.txt.
Another parameter alpha denote the target folder name, including this for the convenience 
of managing file location.
The MP and Non-MP samples are partitioned to 10 parts. A pair of MP and Non-MP parts is taken as
test set, and the remaining parts are training set. We do this rotatively for each part and generate
10 training set and 10 test set to apply cross-validation.
"""
def writeFile(svmLists, alpha):

    MP_svmList = svmLists[0]
    nMP_svmList = svmLists[1]

    count_1_start = 0
    count_1_end = 13

    count_0_start = 0
    count_0_end = 21

    for i in range(10):
        os.system(f"mkdir fold{i+1}")

        trainFileName = f"train{str(i+1)}.txt"
        testFileName = f"test{str(i+1)}.txt"

        outTest = open(testFileName, 'w')
        outTrain = open(trainFileName, 'w')

        for j in range(136):
            if count_1_start <= j <= count_1_end:
                outTest.write(nMP_svmList[j])
            else:
                outTrain.write(nMP_svmList[j])
        for j in range(215):
            if count_0_start <= j <= count_0_end:
                outTest.write(MP_svmList[j])
            else:
                outTrain.write(MP_svmList[j])

        count_1_start += 14
        count_1_end += 14

        count_0_start += 22
        count_0_end += 22

        outTest.close()
        outTrain.close()

        os.system(f"mv {trainFileName} fold{i+1}")
        os.system(f"mv {testFileName} fold{i+1}")
        os.system(f"mv fold{i+1} ../../alpha{alpha}")


def main():

    for i in range(1, 21):
        MP_filePath = f"../../alpha{i}/mp_alpha_{i}.txt"
        nMP_filePath = f"../../alpha{i}/nMp_alpha_{i}.txt"

        MP_dataList = readFile(MP_filePath)
        nMP_dataList = readFile(nMP_filePath)

        MP_svmList = covert2svm(MP_dataList, True)
        nMP_svmList = covert2svm(nMP_dataList, False)

        randomized = randomize(MP_svmList, nMP_svmList)

        writeFile(randomized, i)

main()








