import subprocess as sub
import os

def main():
    os.system("mkdir pssm_MP pssm_nonMP")
    
    count = 0
    check_val = 0
    while count < 215:
        
        cmdRun = "psiblast -query ~/MPs/mp{}.txt -db nr \
-num_iterations 3 -num_threads 24 -out_pssm mypssm.txt -out_ascii_pssm pssm_mp{}.txt"\
.format(count,count)
        cmdMv = "mv pssm_mp{}.txt pssm_MP".format(count)
        
        if check_val == 0:
            
            check_val = sub.call(cmdRun, shell = True)
            count += 1
        else:
            continue

 
    count = 0
    check_val = 0
    while count < 136:
        
        cmdRun = "psiblast -query ~/nonMPs/nMp{}.txt -db nr \
-num_iterations 3 -num_threads 24 -out_pssm mypssm.txt -out_ascii_pssm pssm_nMp{}.txt"\
.format(count,count)
        cmdMv = "mv pssm_nMp{}.txt pssm_nonMP".format(count)

        if check_val == 0:
            
            check_val = sub.call(cmdRun, shell = True)
            count += 1
        else:
            continue

    '''
    The following part moves drived files to targeted directory.
    Coding this part seperately just in case file is moved before it's completed
    '''
    num_p = 215
    type_p = "mp"
    dirName = "MP"
    count = 0
    
    
    while count < num_p:
        

        os.system("mv pssm_{}{}.txt pssm_{}".format(type_p, count, dirName))

        if count == 214:
            count = 0
            num_p = 136
            type_p = "nMp"
            dirName = "nonMP"
        else:
            count += 1

main()
