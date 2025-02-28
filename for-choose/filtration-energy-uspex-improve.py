#!/usr/bin/env python3

import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--results', type=str, required=True, help="USPEX results folder (fixcomp)")
parser.add_argument('-p', '--percentage', type=float, default=0.03, help="Energy far from convex hull")
parser.add_argument('-w', '--nwater', type=int, default=32, help="The number of water molecules")
args = parser.parse_args()

# path=f'{args.results}/Individuals'
os.chdir(f'{args.results}')
seprate='../sep.py'
os.system(f'python {seprate} ./gatheredPOSCARS')
os.chdir(f'./..')

percentage=float(f'{args.percentage}')
nwater=int(f'{args.nwater}')

##### display setting
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.width',100)

############# loading data
data=pd.read_csv(f'{args.results}/Individuals',header=0,index_col=None,sep='\s+')
datas=data.sort_values(by='Enthalpy')


Emax=data.loc[:,'Enthalpy'].max()
Emin=data.loc[:,'Enthalpy'].min()
#rangE=Emax-Emin

######## rate of filtration

#Ecritical=Emin+percentage*nwater
Ecritical=0
data_remain=datas[datas['Enthalpy'] <= Ecritical]
ID_remain=data_remain['ID'].tolist()

######## Screen display
print('##########  \n Hi Guys, are you happy today ? \n OK,let us go \n')
print('The energy range of all collected structures is over {} to {}, \n we will reserve the structures with energy less than {} \n'.format(Emax,Emin,Ecritical))
print('There are {} structures, {} of them are retained. \n'.format(len(datas),len(data_remain)))


#################################
### split the gatheredPOSCARS and concentrate the remaining POSCARS
#os.system(f'python {seprate} {args.results}/gatheredPOSCARS')


os.chdir(f'{args.results}')
if os.path.exists('LPOSCARS'):
    print('The existing file will be renamed as XXX-back')
    os.rename('LPOSCARS', 'LPOSCARS-back')
if os.path.exists('LIndividuals'):
    print('The existing file will be renamed as XXX-back')
    os.rename('LIndividuals', 'Individuals-back')


print(ID_remain)
for i in ID_remain:
    os.system('cat EA{}.vasp >> LPOSCARS'.format(i))
print('cat EA{}.vasp >> LPOSCARS'.format(i))
for a in range(10000):
    os.system('rm EA{}.vasp'.format(a))
os.system('rm -r *.vasp')
##################################
##### save Individuals_remaining
data_remain.to_csv('LIndividuals',index=0)

#os.system('python3 {} {}'.format(seprate,'gatheredPOSCARS'))






