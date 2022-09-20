import csv

'''
This function reads protein names in corresponding, pre-allocated order.
It takes two arguments: [num] represents the fold number from 0 to 9 in str type;
                        [fileType] represents "test" or "train" file.
'''
def proteinSeq(num, fileType):

    filePath = "ProteinNameSeq/" + fileType + "Name" + num + ".txt"

    nameSeqFile = open(filePath,"r")

    protNames = []
    for line in nameSeqFile:
        protNames.append(line)

    nameSeqFile.close()
    return protNames

'''
This function reads prediction results, and it takes three arguments:
[num] represents the fold number from 0 to 9 in str type;
[fileType] represents "test" or "train" file;
[feature] represents the feature vector of preteins.
'''
def readResult(num, fileType, feature):

    filePath = feature + "/prediction" + num + "/" + fileType + num + ".txt.predict"

    resultFile = open(filePath, "r")

    pre_result = []
    for line in resultFile:
        pre_result.append(line[0])

    resultFile.close()

    return pre_result
    
            

def main():

    featureFile = open("Conclusion.csv", "r")

    features = []
    for lines in featureFile:
        features.append(lines.split(",")[0])

    features.remove("PseKRAAC_T1")
    features.remove("")
    featureFile.close()
    
    

    with open("Predict_Test_Table.csv", "w") as table:
        writer = csv.writer(table)

        for i in range(10):
            writer.writerow(["fold" + str(i+1)])
            writer.writerow(["test 1 set"] + features)

            protNames = proteinSeq(str(i), "test")

            result_matrix = []
            for feature in features:
                result_matrix.append(readResult(str(i), "test", feature))
            
            table_matrix = []
            for i in range(len(protNames)):
                table_line = [protNames[i]]

                for j in range(len(features)):
                    table_line.append(result_matrix[j][i])

                table_matrix.append(table_line)

            for i in range(len(table_matrix)):
                writer.writerow(table_matrix[i])

main()
                






















            
    
    
