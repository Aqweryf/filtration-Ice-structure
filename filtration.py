import pandas as pd
from tqdm import tqdm
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, required=True, help="The path of the data to be processed")
parser.add_argument('-s','--sfile', type=str, required=True, help='Specifies the file name to save ')
args = parser.parse_args()
data = pd.read_csv(f'{args.path}', index_col=None, header=None, sep='\s+')

Num = data.shape[0]
data.drop([3, 6, 10,11, 12, 13, 14], axis=1, inplace=True)
for i in tqdm(range(Num)):
    row = list(data.loc[i, :])
    if row[7] < 1.01605:
       if (row[5]/(row[3]+row[4])) > (-0.01933*row[7]-5.43086):
           data.drop([i], axis=0, inplace=True)
    if 1.01605 <= row[7] <= 1.29675:
       if (row[5]/(row[3]+row[4])) > (0.01518*row[7]-5.46594):
           data.drop([i], axis=0, inplace=True)
    if row[7] > 1.29675:
       if (row[5]/(row[3]+row[4])) > (0.02962*row[7]-5.48467):
           data.drop([i], axis=0, inplace=True)

#        os.system(f'rm -r  EA{i+1}.vasp')
data = data.sort_values(by=[9,1], ascending=[False,True])
energy = list(data.loc[:, 7])
O = list(data.loc[:, 4])
H = list(data.loc[:, 5])
for i in tqdm(range(data.shape[0])):
    energy[i] = energy[i] / (O[i] + H[i])
data.loc[:, 7] = energy
data = data.drop_duplicates([7, 9])


energy2 = list(data.loc[:, 7])
O2 = list(data.loc[:, 4])
H2 = list(data.loc[:, 5])

#for z in tqdm(range(data.shape[0])):
#    energy2[z] = energy2[z] * (O2[z] + H2[z])
#data.loc[:, 7] = energy2
final = list(data.loc[:, 1])
for m in tqdm(range(Num)):
    if (m+1) not in final:
        os.system(f'rm -r  EA{m+1}.vasp')
data.to_csv(f'{args.sfile}', sep='\t', header=None, index=False)
