# Moonlighting Protein Prediction Data Introduction
This GitHub repository contains data used and processed for a Moonlighting Protein prediction research project happened in Franklin & Marshall College. 

Stage 1 original feature vectors were retrieved from https://github.com/karimrahimian/moonlight_proteins/tree/main/Data. 

Other data and scripts were generated by Yihang Du, under Professor Jing Hu's instruction.

# Before Start

To successfully use the prepared python scripts, users shall strictly follow the given instructions below, especially which directory a script should be as running. Otherwise, modifications for file path would be needed, since most scripts were created and edited for initially instant needs. Hopefully, there will be chances to merge most of scripts to form a one-step work flow. All python scripts are put in `Data/prepared_scripts`. This repository also contains libsvm interface from https://github.com/cjlin1/libsvm.

# Stage 1

For each feature vector, proteins are randomized based on sequence numbers in `rand_select_x.txt`. Then MPs and Non-MPs are partitioned into 10 parts, generating 10 training set and testing set to do 10-fold cross validation. Accuracy, prediction, and etc. assessment values are calculated based on prediction results. Calculated results are assembled in `Conclusion.csv`.

## Step 1

Store Excel files as `.csv` files for ease of pre-processing. For each feature vector, a working directory should be made and will be used to store derived data. (Done)

## Step 2

Run `randSeed.py`, which is used to generate random index number used to randomly partition training set and testing set. `randSeedT1.py` does the same thing but for PseKRAAC_T1 only since there are different numbers of MPs and non-MPs from other feature vectors. Generated files should be stored in the same directory as each feature vectors'. Otherwise, changes of path in `file_pre.py` will be needed before starting next step.

## Step 3

Run the command `file_pre.py filename.csv`, where `filename.csv` should be replaced by file names of feature vectors, in each feature vector's directory for two purposes:

	1. Convert them to libsvm format stored as .txt files;
	
	2. Randomly partition MPs and Non-MPs to 10 parts for later use of 10-fold cross validation.
	
## Step 4

Run `manage.py` in each feature vector's directory so that can store data in separate folders named `predictionX` for convenience of data management.

## Step 5

Put the target folder in tools in libsvm along with runPrediction.py, use command `python runPrediction.py foldername` to automatically predict and manage output files through train0 to train9, where `foldername` should be replaced by the corresponding feature vector folder's name.

## Step 6

Put `evaluate.py` in the directory of each feature vector and use command `python evaluate.py` to calculate assessment values. The output file will be a csv file containing necessary information.

# Stage 2

Based on the results from Stage 1, the voting strategy and a simple prediction on `Weka` using various machine learning models were applied.

## Step 1

Use `trainPre.py` to help, using the model trained in stage 1, predict on training set. To run the script, the whole `Data` directory should be placed in `libsvm` folder, and `trainPre.py` should be in the `Data` directory.

## Step 2

`s2_tableFormat.py` outputs two tables containing all predicted values for each protein by each feature. One table contains predicted values from training sets, another containing values from test sets. To run the script, it should be kept in the `Data` directory.

## Step 3

`vote-predict.py` predicts proteins by voting. It uses threshold t from 0 to 36. If more than t SVM predictions based on different features says a protein is MP, then predict it as positive, denoted by 0. Otherwise, predict it as negative, denoted by 1. In the end of the output file from `vote-predict.py`, statistics for evaluating performance are calculated. To run the script, it should be placed in the `Data` directory.

## Step 4

`conver_arff.py` converts `Predict_Train_Table.csv` and `Predict_Test_Table.csv` to `.arff` files separately. To use it, users should put it in `Data_s2` along with the two `.csv` tables. It extracts original types of proteins from DDE's training and testing files, which are all the same as files in other features' folder. 

## Step 5

Using the `.arff` files from Step 4, one needs to manually operate `Weka` and record prediction results. The completed statistics are stored in `result_stats.csv`.

# Stage 3

This stage is not closely related to the previous two. We perform `PSI-BLAST` against the non-redundant protein database for each protein sequence to generate PSSM profiles. Based on the PSSM profiles, we re-construct feature vectors for each protein. This stage now has not been fully finished yet.

## Step 1

In `proteins` directory, `mProteins.txt` contains all 215 moonlighting protein sequences and `nonMP.txt` contains all 136 non-moonlighting protein sequences. Users should run `ProteinSplit.py` to split protein sequences to separate files. All files will be kept in corresponding `MPs` and `nonMPs` folders.

## Step 2

One should run `runPsiBlast.py` in the same directory as where non-redundant protein database is kept. File paths to access protein sequences may need to be revised. This script performs `PSI-BLAST` and generate a PSSM profile for each protein. All generated files will be automatically kept in corresponding `pssm_MP` and `pssm_nonMP` folders. As we have the whole database downloaded to a local server machine, this should be convenient. For other users who do not have the downloaded database and a powerful machine, they may want to use other methods to perform `PSI-BLAST`. 

## Step 3

As we have all PSSM profiles prepared well now. One can run `pssm_Process.py` to process these profiles and generate feature vectors for each protein sequence. There should be 20 pairs of files generated ,kept in seperate folders, corresponding to different alpha values ranging from 1 to 20.
