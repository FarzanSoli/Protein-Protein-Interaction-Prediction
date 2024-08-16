import os
import numpy as np
import pandas as pd
from Functions import Functions
# -------------------------------------------------------------------------
class dataprocess():
    def __init__(self):
        Norm  = Functions('/Dataset/').Min_Max_Norm
        directory = os.path.join(os.getcwd(), 'Dataset', 'Protein_data')
        Negatome =  os.path.join(directory, 'Negatome2_Letter.csv')
        dataset = pd.read_csv(Negatome).fillna('bfill').copy()    
        dataset['Score'] = dataset['Interacting'].apply(lambda x:1 if x else 0)
        # =============================================================== #
        #                             Negatome Dataset                    #
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
        # ############################################################### #
        #                         STRING Intractions                      #
        # ############################################################### #
        E_coli = pd.read_csv(os.path.join(directory,'E_coli.csv')).fillna('bfill').copy()
        H_sapien = pd.read_csv(os.path.join(directory, 'H_sapien.csv')).fillna('bfill').copy()
        C_elegans = pd.read_csv(os.path.join(directory,'C_elegans.csv')).fillna('bfill').copy()
        M_musculus = pd.read_csv(os.path.join(directory,'M_musculus.csv')).fillna('bfill').copy()
        S_cerevisiae = pd.read_csv(os.path.join(directory,'S_cerevisiae.csv')).fillna('bfill').copy()
        D_melanogaster = pd.read_csv(os.path.join(directory,'D_melanogaster.csv')).fillna('bfill').copy()
        Organisms = {'E_coli': E_coli, 'H_sapien': H_sapien,
                     'C_elegans': C_elegans, 'M_musculus': M_musculus, 
                     'S_cerevisiae': S_cerevisiae, 'D_melanogaster': D_melanogaster}
        # =============================================================== #
        #                  STRING Dataset Interaction Scores              #
        # =============================================================== #        
        for keys, org in Organisms.items():
            # -----------------------------
            classes_3 = [0, 0.5, 1]
            conditions_3 = [(org['combined_score'] < 0.4), 
                            (org['combined_score'] >= 0.4) & (org['combined_score'] < 0.7), 
                            (org['combined_score'] >= 0.7)]
            # -----------------------------
            classes_5 = [0, 0.3, 0.5, 0.8, 1]
            conditions_5 = [(org['combined_score'] < 0.15), 
                            (org['combined_score'] >= 0.15) & (org['combined_score'] < 0.4),
                            (org['combined_score'] >= 0.40) & (org['combined_score'] < 0.7),
                            (org['combined_score'] >= 0.70) & (org['combined_score'] < 0.9),
                            (org['combined_score'] > 0.90)]
            # -----------------------------
            org['combined_score'] = Norm(org['combined_score'])
            org['class_2'] = org['combined_score'].apply(lambda x: 0 if x < 0.5 else 1)
            org['class_3'] = np.select(conditions_3, classes_3)
            org['class_5'] = np.select(conditions_5, classes_5)
            org.to_csv(keys+'.csv')



