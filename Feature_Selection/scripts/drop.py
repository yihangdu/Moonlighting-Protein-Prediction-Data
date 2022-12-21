# This script will drop one feature from given protein feature set from command line
# and then covert it to SVM required file format by calling convert_svm.py.
# Then it will split each to ten folds.

# For the command line input, format should be: python drop.py [MP.txt] [nonMP.txt]
 

import os
import sys

def readFile(inFile):
    dataList = []
    proteinName = []

    dataLine = False
    for line in inFile:
        if ">" in line:
            dataLine = True
            proteinName.append(line)
            continue

        elif dataLine:
            dataList.append(line.split())
            dataLine = False

        else:
            continue
    inFile.close()

    return dataList, proteinName


def writeFile(isMP, prot_name, prot_feature, round_num, drop_num):
    fileName = f"{isMP}_drop{drop_num}.txt"
    outFile = open(fileName, "w")

    for i in range(len(prot_name)):
        outFile.write(prot_name[i])

        tmp_dataLine = prot_feature[i][:]
        del tmp_dataLine[drop_num]
        data_str = str(tmp_dataLine)
    
        data_str = data_str.replace(",","")
        data_str = data_str.replace("'","")
        data_str = data_str.replace("[","")
        data_str = data_str.replace("]","\n")

        outFile.write(data_str + "\n")

    os.system(f"mv {fileName} ../round{round_num}/drop{drop_num}")

    outFile.close()


def main():
    MP_filePath = sys.argv[1]
    nMP_filePath = sys.argv[2]
    round_num = sys.argv[3]

    MP_file = open(MP_filePath, 'r')
    nMP_file = open(nMP_filePath, 'r')
    
    MP = readFile(MP_file)
    MP_name = MP[1]
    MP_features = MP[0]

    if len(MP_name) != len(MP_features):
        print("MP protein number not match feature number!")
        exit(1)
    
    nMP = readFile(nMP_file)
    nMP_name = nMP[1]
    nMP_features = nMP[0]

    if len(nMP_name) != len(nMP_features):
        print("nMP protein number not match feature number!")
        exit(2)


    os.system(f"mkdir round{round_num}")
    os.system(f"mv round{round_num} ../")
    for i in range(len(MP_features[0])):
        os.system(f"mkdir drop{i}")
        os.system(f"mv drop{i} ../round{round_num}")
        writeFile("MP", MP_name, MP_features, round_num, i)
        writeFile("nMP", nMP_name, nMP_features, round_num, i)

        MP_path = f"../round{round_num}/drop{i}/MP_drop{i}.txt"
        nMP_path = f"../round{round_num}/drop{i}/nMP_drop{i}.txt"

        os.system(f"python3 convert_svm.py {MP_path} {nMP_path} {round_num} {i}")

    
            

main()

    
