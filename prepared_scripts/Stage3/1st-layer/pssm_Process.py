"""
This program is responsible for transforming PSSM profiles to our desired features.
It manages files automatically.
"""

# This function should be in /Data_s3 with pssm profiles prepared well. 


import math
import os

'''
This function takes an input pssm file as its argument, it returns one 2D matrix and a 1D vector.
The 2D matrix contains all normalized data in the file.
The 1D vector contains the protein sequence in the second column of the profile.
'''
def readinData(fin):

    # skip first three lines that we don't want
    for i in range(3):
        fin.readline()

    proteinSeq = [] # stores protein sequences (1D vector)
    pssmTable = [] # stores normalized data (2D matrix)

    for line in fin:
        tmp = line.split()[1:22] # drop index number and additional information
        if tmp == []:
            break;
        else:
            proteinSeq.append(tmp[0])
            pssmTable.append([int(tmp[i]) for i in range(1, len(tmp))])
    return proteinSeq, pssmTable

'''
This function takes in a 2D matrix contains all normalized data in the pssm profile.
This function returns a 1D vector of length 20 denoted T' and a 2D matrix of normalized pssmTable.
'''
def calcT(pssmTable):
    # a matrix with the same dimension as pssmTable but contains normalized data
    normalized = [[0]*20 for i in range(len(pssmTable))]
                                         

    meanVec = []  # a 1D vector contains mean's for each row in pssmTable
    for i in range(len(pssmTable)):
        meanVec.append(sum(pssmTable[i])/len(pssmTable[i]))

    stdVec = []  # a 1D vector contains std's for each row in pssmTable
    for i in range(len(pssmTable)):
        tmp = 0
        for j in range(len(pssmTable[0])):
            tmp += (pssmTable[i][j] - meanVec[i])**2
        stdVec.append(math.sqrt(tmp/20))


    for i in range(len(pssmTable)):
        for j in range(len(pssmTable[0])):
            if stdVec[i] == 0:
                normalized[i][j] = 0
            else:
                normalized[i][j] = (pssmTable[i][j] - meanVec[i])/stdVec[i]

    

    vecT = [] # a vector of size 20 (T')

    for j in range(len(normalized[0])):
        tmp = 0
        for i in range(len(normalized)):
            tmp += normalized[i][j]
        vecT.append(tmp/len(normalized))
    
    return vecT, normalized

'''
This function takes in the normalized pssmTable and returns a 2D matrix denoted H'_alpha
'''
def calcH(norm_pssm):

    vecH = [] # a matrix of size 20*20, denoted H'. Each row corresponds to a value of alpha

    for a in range(1, 21):
        tmpList = []
        for j in range(len(norm_pssm[0])):
            tmp = 0
            for i in range(len(norm_pssm)-a):
                tmp += (norm_pssm[i][j] - norm_pssm[i+a][j])**2
            tmpList.append(tmp/(len(norm_pssm) - a))
        vecH.append(tmpList)

    return vecH
    

def main():
    num_p = 215
    type_p = "mp"
    count = 0
    dirName = "MP"
    
    
    while count < num_p:
        
        
        f = open("pssm_{}/pssm_{}{}.txt".format(dirName, type_p, count), "r") # open pssm profile
        fp = open("proteins/{}s/{}{}.txt".format(dirName, type_p, count), "r") # open protein sequence file
        seqName = fp.readline()
        fp.close()

        pssmInf = readinData(f)

        proteinSeq = pssmInf[0] # un-used, just in case needed later 
        pssmTable = pssmInf[1]
        

        T_and_nrmlsd = calcT(pssmTable)

        T_prime = T_and_nrmlsd[0] # T'
        norm_pssm = T_and_nrmlsd[1]

        H_prime = calcH(norm_pssm) # H'

        f.close()
        
        for i in range(1,21):
            if count == 0 and type_p == "mp":
                os.system("mkdir alpha{}".format(i))
            fout = open("alpha{}/{}_alpha_{}.txt".format(i, type_p, i), "a")

            fout.write("\n" + seqName)
            for j in range(40):
                if j < 20:
                    fout.write(str(T_prime[j]) + " ")
                else:
                    fout.write(str(H_prime[i-1][j%20]) + " ")
            fout.write("\n")
            fout.close()
        
        if count == 214:
            count = 0
            num_p = 136
            type_p = "nMp"
            dirName = "nonMP"
        else:
            count += 1
        
                
            
    

    

    

main()
