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
data.drop([1,2,4,6], axis=1, inplace=True)
data.to_csv(f'{args.sfile}', sep='\t', header=None, index=False)

