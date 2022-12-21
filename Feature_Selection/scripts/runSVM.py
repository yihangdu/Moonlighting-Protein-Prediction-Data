"""
This program runs svm programs after all features are prepared well. It manages all ouput files automatically.
"""
# This program should be in libsvm/tools when executing


import os
import sys

def main():
    round_num = sys.argv[1]
    drop_total = sys.argv[2]

    for i in range(int(drop_total)):
        
        for j in range(1, 11):
            trainName = f"train{j}.txt"
            testName = f"test{j}.txt"

            trainPath = f"../../Feature_Selection/round{round_num}/drop{i}/fold{j}/{trainName}"
            testPath = f"../../Feature_Selection/round{round_num}/drop{i}/fold{j}/{testName}"

            run_easy_cmd = f"python3 easy.py {trainPath} {testPath}"


            os.system(run_easy_cmd)

            outFiles = [ f"{trainName}.range",
                         f"{trainName}.scale",
                         f"{trainName}.scale.out",
                         f"{trainName}.scale.png",
                         f"{trainName}.model",
                         f"{testName}.scale",
                         f"{testName}.predict" ]


            for k in outFiles:
                os.system(f"mv {k} ../../Feature_Selection/round{round_num}/drop{i}/fold{j}")


main()
