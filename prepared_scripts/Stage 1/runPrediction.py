import os
import sys

def main():
    dirName = sys.argv[1]

    for i in range(10):
        trainName = "train" + str(i) + ".txt"
        testName = "test" + str(i) + ".txt"

        easy = "python3 easy.py "+ dirName +"/prediction" \
               + str(i) + "/train"+ str(i) + ".txt \
                "+ dirName +"/prediction" + str(i) + "/test" + str(i) +".txt"
        
        mvdir_c = "mv train" + str(i) + ".txt.range train" + str(i) \
                  + ".txt.scale train" + str(i) + ".txt.scale.out train" \
                  + str(i) + ".txt.scale.png test" + str(i) + ".txt.predict test" \
                  + str(i) + ".txt.scale train" + str(i) + ".txt.model " + dirName \
                  + "/prediction" + str(i)
        os.system(easy)
        os.system(mvdir_c)


main()
