"""
This program runs svm programs after all features are prepared well. It manages all ouput files automatically.
"""
# This program should be in LibSVM/libsvm/tools when executing


import os

def main():

    for i in range(1, 21):
        alpha = f"alpha{i}"
        for j in range(1, 11):
            trainName = f"train{j}.txt.scale"
            testName = f"test{j}.txt.scale"
            foldName = f"fold{j}"

            trainPath = f"../../../Data_s3/{alpha}/{foldName}/{trainName}"
            testPath = f"../../../Data_s3/{alpha}/{foldName}/{testName}"

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
                os.system(f"mv {k} ../../../Data_s3/{alpha}/{foldName}")


main()
