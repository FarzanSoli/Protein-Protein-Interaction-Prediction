import os
import numpy as np
import pandas as pd
from Functions import Functions
# -------------------------------------------------------------------------
class dataprocess():
    def __init__(self):
        Norm  = Functions('/Dataset/').Normalize_AA
        directory = os.path.join(os.getcwd(), 'Dataset', 'Protein_data')
        file =  os.path.join(directory, 'Negatome2_Letter.csv')
        dataset = pd.read_csv(file).fillna('bfill').copy()    
        dataset['Score'] = dataset['Interacting'].apply(lambda x:1 if x else 0)
        # =============================================================== #
        #                             Creating Dataset                    #
        # =============================================================== #
        Heading = list(dataset.columns)
        Neg_Dataset = {}
        Pos_Dataset = {}
        for i in Heading:
            props = []
            for n in list(np.where(dataset['Interacting'] == False)[0]):
                props.append(dataset[i][n])
            Neg_Dataset[i] = props
            # -------------------------
            props = []
            for n in list(np.where(dataset['Interacting'] == True)[0]):
                props.append(dataset[i][n])
            Pos_Dataset[i] = props
        # -----------------------------
        pd.DataFrame(Neg_Dataset).to_csv('Neg_DF.csv')
        pd.DataFrame(Pos_Dataset).to_csv('Pos_DF.csv')
        # -----------------------------