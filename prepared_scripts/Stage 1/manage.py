import os

def main():

    
    for i in range(10):

        trainName = "train" + str(i) + ".txt"
        testName = "test" + str(i) + ".txt"
        dirName = "prediction" + str(i)
        mkdir_c = "mkdir " + dirName
        mvTrain_c = "mv " + trainName + " " + dirName
        mvTest_c = "mv " + testName + " " + dirName
        
        os.system(mkdir_c)
        os.system(mvTrain_c)
        os.system(mvTest_c)


main()
