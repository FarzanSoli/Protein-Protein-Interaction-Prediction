import os
import pickle
import numpy as np
import pandas as pd
from Functions import Functions
# -------------------------------------------------------------------------
# =============================================================================
# class dataprocess():
#     def __init__(self):
# =============================================================================
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
#             Balanced Datasets with interaction scores           #
# =============================================================== #        

def balanced_2_class(DF):
    balanced_dfs = {}
    for keys, org in DF.items():
        # -----------------------------
        org['combined_score'] = Norm(org['combined_score'])
        org['class_2'] = org['combined_score'].apply(lambda x: 0 if x < 0.5 else 1)
        # ---------------------------------
        class_0 = org[org['class_2'] == 0]
        class_1 = org[org['class_2'] == 1]
        balanced_len = min(len(class_0), len(class_1))
        balanced_class_0 = class_0.sample(n=balanced_len, random_state=42)
        balanced_class_1 = class_1.sample(n=balanced_len, random_state=42)
        balanced_df = pd.concat([balanced_class_0, balanced_class_1]).sample(frac=1, random_state=42).reset_index(drop=True)
        balanced_dfs[keys] = balanced_df
    return balanced_dfs
# ------------------------------------
balanced_2_classes = balanced_2_class(Organisms)
with open('balanced_2_classes.pkl', 'wb') as file:
    pickle.dump(balanced_2_classes, file)
# =====================================
def balanced_3_class(DF):
    balanced_dfs = {}
    for keys, org in DF.items():
        # -----------------------------
        classes_3 = [0, 0.5, 1]
        conditions_3 = [(org['combined_score'] < 0.4), 
                        (org['combined_score'] >= 0.4) & (org['combined_score'] < 0.7), 
                        (org['combined_score'] >= 0.7)]
        # -----------------------------
        org['combined_score'] = Norm(org['combined_score'])
        org['class_3'] = np.select(conditions_3, classes_3)
        # -----------------------------
        class_ = [org[org['class_3'] == i] for i in classes_3]
        balanced_len = min(len(cls_) for cls_ in class_)
        # -----------------------------
        balanced_classes = [cls_.sample(n=balanced_len, random_state=42) for cls_ in class_]
        balanced_df = pd.concat(balanced_classes).sample(frac=1, random_state=42).reset_index(drop=True)
        balanced_dfs[keys] = balanced_df.drop('class_2', axis = 1)
    return balanced_dfs
# ------------------------------------
balanced_3_classes = balanced_3_class(Organisms)
with open('balanced_3_classes.pkl', 'wb') as file:
    pickle.dump(balanced_3_classes, file)
# =====================================
def balanced_5_class(DF):
    balanced_dfs = {}
    for keys, org in DF.items():
        # -----------------------------
        classes_5 = [0, 0.3, 0.5, 0.8, 1]
        conditions_5 = [(org['combined_score'] < 0.15), 
                        (org['combined_score'] >= 0.15) & (org['combined_score'] < 0.4),
                        (org['combined_score'] >= 0.40) & (org['combined_score'] < 0.7),
                        (org['combined_score'] >= 0.70) & (org['combined_score'] < 0.9),
                        (org['combined_score'] > 0.90)]
        # -----------------------------
        org['combined_score'] = Norm(org['combined_score'])
        org['class_5'] = np.select(conditions_5, classes_5)
        # -----------------------------
        class_ = [org[org['class_5'] == i] for i in classes_5]
        balanced_len = min(len(cls) for cls in class_)
        # -----------------------------
        balanced_classes = [cls.sample(n=balanced_len, random_state=42) for cls in class_]
        balanced_df = pd.concat(balanced_classes).sample(frac=1, random_state=42).reset_index(drop=True)
        # -----------------------------
        balanced_dfs[keys] = balanced_df.drop(['class_2','class_3'], axis = 1)
    return balanced_dfs
# ------------------------------------
balanced_5_classes = balanced_5_class(Organisms)
with open('balanced_5_classes.pkl', 'wb') as file:
    pickle.dump(balanced_5_classes, file)