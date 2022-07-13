import csv
import sys

'''
Read in csv files and store the data as a list
'''
def readFile(file):

    dataList = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, dialect = 'excel')
        line_count = 0

        for row in csv_reader:
            if line_count > 0:
                dataList.append(row)
            line_count += 1
            
    return dataList

'''
Convert the data to libsvm format.
'''
def convert(oList):

    libsvmList = []
    
    for lst in oList:
        tmpStr = ""
        lst.remove(lst[0]) # remove protein name column
        tmpStr += lst[-1] + " " # put label in front of a row
        
        for i in range(len(lst)-1):
            if lst[i] != "0":
                tmpStr += str(i+1) + ":" + lst[i] + " "
        tmpStr += "\n" # every item in list is in form of <label> 1:<feature> 2:<feature>...
        libsvmList.append(tmpStr)

    return libsvmList


'''
This function randomizes the sequence of data based on pre-prepared seed.
'''
def randomize(libsvmList, oList):
    rFile_1 = open('../random_select_1.txt','r')
    rFile_0 = open('../random_select_0.txt','r')

    rsvmList = []
    roList = []
    for i in rFile_1:
        rsvmList.append(libsvmList[int(i)])
        roList.append(oList[int(i)])

    for i in rFile_0:
        rsvmList.append(libsvmList[int(i)])
        roList.append(oList[int(i)])
        
    if len(rsvmList) != len(libsvmList) or len(rsvmList) != len(oList):
        print("possible data missing!")
        exit(1)

    rFile_1.close()
    rFile_0.close()
    return rsvmList, roList


'''
This functions output three files: train_x.txt, test_x.txt, random_ori.txt
[random_ori.txt] is the original data set in .txt format but randomized based on the same sequence
as train.txt and test.txt

The MP and Non-MP samples are partitioned to 10 parts. A pair of MP and Non-MP parts is taken as
test set, and the remaining parts are training set. We do this rotatively for each part and generate
10 training set and 10 test set to apply cross-validation.
'''
def writetxt(rsvmList, roList):
    outOrig = open("random.ori.txt",'w')

    if len(rsvmList) != len(roList):
        print("possible data missing!(2)")
        exit(2)

    for i in range(len(rsvmList)):
        outOrig.write(str(roList[i]))
    
    count_1_start = 0
    count_1_end = 13
        
    count_0_start = 0
    count_0_end = 21

    Non_MP = rsvmList[:136]
    MP = rsvmList[136:]

    for i in range(10):
        
        trainFileName = "train" + str(i) + ".txt"
        testFileName = "test" + str(i) + ".txt"
        
        outTest = open(testFileName, 'w')
        outTrain = open(trainFileName, 'w')

        for j in range(136):
            if count_1_start <= j and j <= count_1_end:
                outTest.write(Non_MP[j])
            else:
                outTrain.write(Non_MP[j])
        for j in range(215):
            if count_0_start <= j and j <= count_0_end:
                outTest.write(MP[j])
            else:
                outTrain.write(MP[j])

        count_1_start += 14
        count_1_end += 14

        count_0_start += 22
        count_0_end += 22

        outTest.close()
        outTrain.close()
        
        
    
    outOrig.close()
    return 0
        
def main():
    inFile = sys.argv[1]

    fileList = readFile(inFile)

    converted = convert(fileList)

    randomized = randomize(converted, fileList)

    writeFile = writetxt(randomized[0],randomized[1])

    

main()
