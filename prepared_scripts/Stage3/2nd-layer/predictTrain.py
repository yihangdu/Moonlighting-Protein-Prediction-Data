# This file predict on training set and should be /LibSVM/libsvm/tools when executing

import os

def main():

    for i in range(1, 21):
        alpha = f"alpha{i}"
        for j in range(1, 11):
            trainName = f"train{j}.txt.scale"
            modelName = f"train{j}.txt.scale.model"
            foldName = f"fold{j}"
            outName = f"train{j}.txt.scale.predict"

            trainPath = f"../../Data_s3/{alpha}/{foldName}/{trainName}"
            modelPath = f"../../Data_s3/{alpha}/{foldName}/{modelName}"

            run_pred_cmd = f"./svm-predict {trainPath} {modelPath} {outName}"


            os.system(run_pred_cmd)

            
            os.system(f"mv {outName} ../../Data_s3/{alpha}/{foldName}")


main()
