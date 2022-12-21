import random


def main():
    outfile_1 = open("new_random_1.txt", 'w')
    outfile_0 = open("new_random_0.txt", 'w')

    oList_1 = [i for i in range(136)]
    oList_0 = [i for i in range(215)]

    rList_1 = []
    rList_0 = []

    i = 135
    j = 214
    while (len(rList_1) != 136):
        rSeed_1 = random.randint(0, i)
        rList_1.append(oList_1[rSeed_1])
        oList_1.remove(oList_1[rSeed_1])
        i -= 1

    while (len(rList_0) != 215):
        rSeed_0 = random.randint(0, j)
        rList_0.append(oList_0[rSeed_0])
        oList_0.remove(oList_0[rSeed_0])
        j -= 1

    for i in rList_1:
        outfile_1.write(str(i) + "\n")

    for i in rList_0:
        outfile_0.write(str(i) + "\n")

    outfile_1.close()
    outfile_0.close()


main()
