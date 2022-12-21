"""
This program is to integrate feature data in Data_s3/alpha1/mp_alpha1.txt and
Data_s3/alpha1/nMp_alpha1.txt into Professor Jing Hu's feature data.
"""

def processAlpha(f):
    dataMatrix = []

    for line in f:
        if ">" not in line and len(line) > 1:
            lineList = line.split()
            if len(lineList) != 40:
                print("Missing Data")
                exit(1)
            strLine = "" # convert to string delimited by tab

            for d in lineList:
                strLine += f"{d}\t"

            strLine += "\n"
            dataMatrix.append(strLine)

    return dataMatrix


def addFeature(fin, dataMatrix, fout):

    count = 0
    proteinCount = 0
    for line in fin:
        if ">" in line:
            count += 1
        elif count == 1:
            count += 1
        elif count == 2:
            fout.write(dataMatrix[proteinCount])
            proteinCount += 1
            count = 0

        fout.write(line)

            




mp_alpha = open("../../alpha1/mp_alpha_1.txt", "r")
nMp_alpha = open("../../alpha1/nMp_alpha_1.txt", "r")
mpMatrix = processAlpha(mp_alpha)
nMpMatrix = processAlpha(nMp_alpha)

mfin = open("mProteinsAllFeatures.txt", "r")
nmfin = open("nonMPAllFeatures.txt", "r")

mfout = open("Alpha1_mProteinsAllFeatures.txt", "w")
nmfout = open("Alpha1_nonMPAllFeatures.txt", "w")

addFeature(mfin, mpMatrix, mfout)
addFeature(nmfin, nMpMatrix, nmfout)

mp_alpha.close()
nMp_alpha.close()
mfin.close()
nmfin.close()
mfout.close()
nmfout.close()
