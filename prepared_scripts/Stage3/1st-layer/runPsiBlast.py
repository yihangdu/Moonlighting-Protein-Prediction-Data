import subprocess as sub
import os

def main():
    os.system("mkdir pssm_haolan")
    
    count = 1
    check_val = 0
    while count <= 646:
        
        cmdRun = f"psiblast -query ~/haolanDB/HLProts/hlp{count}.txt -db nr \
-num_iterations 3 -num_threads 24 -out_pssm mypssm.txt -out_ascii_pssm nr_pssm_hlp{count}.txt"
        
        if check_val == 0:
            
            check_val = sub.call(cmdRun, shell = True)
            count += 1
        else:
            continue



    '''
    The following part moves drived files to targeted directory.
    Coding this part seperately just in case file is moved before it's completed
    '''
  
    count = 0
    
    
    while count <= 646:
        

        os.system(f"mv nr_pssm_mp{count}.txt pssm_haolan")

        count += 1

main()
