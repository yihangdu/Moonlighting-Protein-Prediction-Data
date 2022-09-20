import os
def process(file, isMp):

    count = 0
    outFile = open(isMp + str(count) + ".txt", "w")
    outFile.write(file.readline())
    
    for line in file:
        if ">" in line:
            outFile.close()
            count += 1
            outFile = open(isMp + str(count) + ".txt", "w")  
        outFile.write(line)

    outFile.close()
    
    return count

def main():

    os.system("mkdir MPs nonMPs")

    mp = open("mProteins.txt", "r")

    nMp = open("nonMP.txt", "r")

    countMP = process(mp, "mp")

    for i in range(countMP + 1):
        os.system("mv mp" + str(i) + ".txt MPs")


    countNmp = process(nMp, "nMp")

    for i in range(countNmp + 1):
        os.system("mv nMp" + str(i) + ".txt nonMPs")

main()


    
