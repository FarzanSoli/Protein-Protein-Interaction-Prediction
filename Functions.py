import os
import math
import torch
import zipfile
import numpy as np
import gzip, shutil
import pandas as pd 
from torch import nn
import networkx as nx
from Config import config
from AA_features import features
from itertools import combinations
from sklearn.decomposition import PCA
from Sampling import Diffusion_Process
# ========================================= #
class Functions():
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
    # ========================================= #
    #                Fix AA sequenc             #
    # ========================================= #
    def missing_seq(self, Dataset):
        df = Dataset.loc[Dataset['Sequence'].str.contains('X') & 
                           Dataset['Sequence'].str.startswith('X') &
                           Dataset['Sequence'].str.endswith('X')]
        for i in ['A','C','D','E','F','G','H','I','K','L',
                  'M','N','P','Q','R','S','T','V','W','Y']:
            kn_seq = df.loc[Dataset['Sequence'].str.contains(i)]
        result = pd.concat([df, kn_seq]).drop_duplicates(keep=False)
        return result
    # ========================================= #
    #                 Read Dataset              #
    # ========================================= #
    def Dataset_Reader(self, dataset):
        Dataset = pd.concat([pd.read_csv('Dataset/'+dataset), 
                             self.missing_seq(pd.read_csv(
                            'Dataset/'+dataset))]).drop_duplicates(keep=False)
        return Dataset
    # ========================================= #
    #                   Padding                 #
    # ========================================= #
    def padding(self, pad_len, matrix):
        mat = np.zeros((pad_len, 3))
        mat[:matrix.shape[0], :matrix.shape[-1]] = matrix
        return mat
    # ========================================= #
    #                  Unzip files              #
    # ========================================= #
    def unzip(self, directory, file):
        # file = 'PDB alpha-C.zip'
        # directory = "/Dataset/"
        with zipfile.ZipFile(os.getcwd()+directory+file, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd()+directory)
    # ========================================= #
    #                 Extract gzip              #
    # ========================================= #
    def gz_extract(self):
        extension = ".gz"
        os.chdir(self.directory)
        for item in os.listdir(self.directory): # loop through items in dir
          if item.endswith(extension): # check for ".gz" extension
              gz_name = os.path.abspath(item) # get full path of files
              # get file name for file within -> removes '.cif'
              file_name = (os.path.basename(gz_name)).rsplit('.',1)[0] 
              with gzip.open(gz_name, "rb") as f_in, open(file_name, "wb") as f_out:
                  # Copy the contents of source file to destination file
                  shutil.copyfileobj(f_in, f_out)
              os.remove(gz_name) # delete zipped file
    # ========================================= #
    #               Encoding Amio acids         #
    # ========================================= #
    def Normalize_AA(self):
        Norm_props = {}
        for key, value in features().Props.items():
            Norm_props[key] = (value-np.min(value))/(np.max(value)-np.min(value))
        # ------------------------------------- #
        Norm_AAs = {}
        for symb, ind in features().AA_dict.items():
            props = []
            for key, value in Norm_props.items():
                props.append(value[ind])
            Norm_AAs[symb] = props

        return Norm_props, Norm_AAs
    # ========================================= #
    #               Amino acid Encoding         #
    # ========================================= #
    def encode_CT(self, Pad_Length, dataframe):
        Encoded_AA = {}
        for index, row in dataframe.iterrows():
            Encoded_AA[row['PDB_ID']] = np.array(
                [self.Normalize_AA()[1][c.upper()] for c in row['Sequence']])
        # ------------------------------------- #
        encoded_AA = np.zeros((Pad_Length, len(features().AA_prop_keys)))
        Encoded_AA_padded = {}
        for key, value in Encoded_AA.items():
            if value.shape[0] > Pad_Length:
                Encoded_AA_padded[key] = value[:Pad_Length,:]
            else: 
                padding = np.zeros((Pad_Length, value.shape[1]))
                padded_value = np.vstack((value, padding))
                Encoded_AA_padded[key] = padded_value
        return Encoded_AA_padded
    # ========================================= #
    #                 READ Fasta file           #
    # ========================================= #
    def read_fasta(self, fasta_file, comment="#"):
        # with gzip.open(fasta_file,"r") as f:
        with open(fasta_file, "r") as file:
            id_ = None
            seq_id = []
            sequence = []
            sequences = []
            # loop through each line in the file
            for line in file:
                # If the line starts with a ">" character, 
                # it is a new sequence identifier
                if line.startswith(">"):
                    # If this is not the first sequence, print the previous one
                    if id_ is not None:
                        seq_id.append(id_)
                        sequences.append(''.join(sequence))
                    # Get the new sequence identifier and reset the sequence variable
                    id_ = line.strip()[1:]
                    sequence = []
                # Otherwise, it is part of the sequence, 
                # so append it to the sequence variable
                else:
                    sequence.append(line.upper())
            if id_ is not None:
                seq_id.append(id_)
                sequences.append(''.join(sequence))
            return list(zip(seq_id, sequences))
