# Python script version for labelling the kaggle dataset
# %%
import pandas as pd

# Load the CSV file
df = pd.read_csv('dataset/kaggle-dataset.csv')

# Display the first few rows of the DataFrame
print(df.head())


# %%
# Define function to determine label

from enum import Enum

class Fault(Enum):
    NA = 'No Fault'
    LL = 'Line-to-line fault'
    LLL = 'Line-to-line-to-line fault'
    LG = 'Line-to-ground fault'
    LLG = 'Line-to-line-to-ground fault'
    LLLG = 'Line-to-line-to-line-to-ground fault'

def determine_fault_label(row):
    ground = bool(row['G'])
    phase_list = []
    if(row['A']): phase_list.append('A')
    if(row['B']): phase_list.append('B')
    if(row['C']): phase_list.append('C')
    no_of_phases = len(phase_list)
    if(not ground and no_of_phases == 0):
        return Fault.NA.value
    fault_type = ''
    if(ground):
        if(len(phase_list)==1): fault_type = Fault.LG
        elif(len(phase_list)==2): fault_type = Fault.LLG
        elif(len(phase_list)==3): fault_type = Fault.LLLG
    else:
        if(len(phase_list)==2): fault_type = Fault.LL
        if(len(phase_list)==3): fault_type = Fault.LLL
    fault_phase = ''
    if(len(phase_list)==1): fault_phase =' at phase: '
    else: fault_phase =' at phases: '
    return fault_type.value + fault_phase + ', '.join(phase_list)

# Add Fault label
df['Fault'] = df.apply(determine_fault_label, axis=1)
df = df.drop(columns=['G', 'A', 'B', 'C'])
print(df.head())

df.to_csv('./dataset/labeled-dataset.csv', index=False)

# %%
df = df.sample(frac=1).reset_index(drop=True)

print(df.head())

df.to_csv('./dataset/labeled-jumbled-dataset.csv', index=False)


