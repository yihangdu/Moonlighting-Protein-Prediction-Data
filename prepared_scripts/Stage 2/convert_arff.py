import os

'''
This function reads in the originally knwon result of each proteins. It returns
a matrix holding the results.
'''
def readOriTrain():
    oriType = []
    for i in range(10):
        ori_tmp = []
        fileName = "../Data/DDE/prediction" + str(i) + "/train" + str(i) + ".txt"
        oriFile = open(fileName, "r")

        for line in oriFile:
            ori_tmp.append(line[0])

        oriType.append(ori_tmp)
        oriFile.close()

    return oriType

def readOriTest():
    oriType = []
    for i in range(10):
        ori_tmp = []
        fileName = "../Data/DDE/prediction" + str(i) + "/test" + str(i) + ".txt"
        oriFile = open(fileName, "r")

        for line in oriFile:
            ori_tmp.append(line[0])

        oriType.append(ori_tmp)
        oriFile.close()

    return oriType


def main():

    oriType = readOriTrain()
    oriType_t = readOriTest()
    
    
    Predict_train = open("Predict_Train_Table.csv", "r")
    Predict_test = open("Predict_Test_table.csv", "r")

    Predict_train.readline() # skip the first line
    Predict_test.readline()
    
    trainList = []
    testList = []
    attributeList = Predict_train.readline().split(",")
    attributeList.remove(attributeList[0])
    attributeList[-1] = attributeList[-1].replace("\n", "")
    attributeList.append("ProteinType")

    
    for line in Predict_train:
        if("train" not in line) and ("fold" not in line) and ("|" not in line):
            line = line.split(",")
            line.remove(line[0])
            line[-1] = line[-1].replace("\n", "")
            trainList.append(line)

    for line in Predict_test:
        if("test" not in line) and ("fold" not in line) and ("|" not in line):
            line = line.split(",")
            line.remove(line[0])
            line[-1] = line[-1].replace("\n", "")
            testList.append(line)

    train_idx = 0
    for i in range(len(oriType)): # len(oriType) should be 10
        os.system("mkdir weka_pred" + str(i))
        
        outTrain = open("weka_train" + str(i) + ".arff", "w")

        outTrain.write("@relation protein_type\n\n")
        
        for attribute in attributeList:
            outTrain.write("@attribute " + attribute + " {0, 1}\n")

        outTrain.write("\n" + "@data" + "\n")

        for j in range(len(oriType[i])):
            for k in range(len(trainList[train_idx])):
                outTrain.write(trainList[train_idx][k] + ",")
            outTrain.write(oriType[i][j] + "\n")
            train_idx += 1
        outTrain.close()
        os.system("mv weka_train" + str(i) + ".arff weka_pred" + str(i))

    test_idx = 0
    for i in range(len(oriType_t)):
        
        outTest = open("weka_test" + str(i) + ".arff", "w")

        outTest.write("@relation protein_type\n\n")
        
        for attribute in attributeList:
            outTest.write("@attribute " + attribute + " {0, 1}\n")

        outTest.write("\n" + "@data" + "\n")

        for j in range(len(oriType_t[i])):
            for k in range(len(testList[test_idx])):
                outTest.write(testList[test_idx][k] + ",")
            outTest.write(oriType_t[i][j] + "\n")
            test_idx += 1
        outTest.close()
        os.system("mv weka_test" + str(i) + ".arff weka_pred" + str(i))
        
        

main()
        













        
        
