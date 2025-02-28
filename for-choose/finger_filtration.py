#!/usr/bin/env python3

import argparse
import numpy as np
import pandas as pd
import ase
import ase.ga
from ase.ga.ofp_comparator import OFPComparator
from pymatgen.core.structure import Structure
from pymatgen.io.ase import AseAtomsAdaptor
import os
import multiprocessing as mp

def is_same(oc, first, second, symprec, distance):

#    if not np.isclose(first['energy'], second['energy'], atol=0.03):
#        return False
    # if not np.isclose(first['struct'].density, second['struct'].density, atol=0.03):
    #     return False
    # if first['struct'].get_space_group_info(symprec=symprec)[1] != second['struct'].get_space_group_info(symprec=symprec)[1]:
    #     return False
    # if first['struct'].composition.formula != second['struct'].composition.formula :
    #     return False
    # if not np.isclose(first['Sorder'], second['Sorder'], atol=0.02):
    #     return False
    return oc._cosine_distance(first['fingerprint'][0], second['fingerprint'][0], first['fingerprint'][1]) < distance

def extract_good_structures(results,symprec,fptol):
    oc = OFPComparator(rcut=12)
    ######## redefine the loading methods.
    data=pd.read_csv(f'{results}/LIndividuals')
    id_list,enthalpies,Sorder=data.loc[:,'ID'],data.loc[:,'Enthalpy'],data.loc[:,'S_order']
    id_list = list(map(int, id_list))
    dict_enthalpies = {i: e for i, e in zip(id_list, enthalpies)}
    dict_Sorder = {i: d for i, d in zip(id_list, Sorder)}
    ########################################

    with open(f'{results}/LPOSCARS') as f:
        dict_structures = {int(ps.split()[0]): Structure.from_str(ps, 'poscar') for ps in f.read().split("EA")[1:]}
    print(f'Total structures: {len(dict_structures)}')
    unique_individuals = []
    for a,i in enumerate(dict_structures.keys()):
        second = {'energy': dict_enthalpies[i],'Sorder': dict_Sorder[i],'struct': dict_structures[i], 'index': i}
        second['fingerprint'] = oc._take_fingerprints(AseAtomsAdaptor.get_atoms(second['struct']))
        match_found = False
        for first in unique_individuals:
            if is_same(oc, first, second, symprec, fptol):
                match_found = True
                break
        if not match_found:
            unique_individuals.append(second)

        print(f'Processed total/unique structures: {a}/{len(unique_individuals)}')

    output = []
    density_sort = []
    energy_sort = []
    output_poscars = []
    print_output = f'{"Name":8s} {"Composition":16s} {"Sym":3s} {"Enthalpy":17s} {"Volume":18s} {"Density":16s} {"Sorder":16s}\n'
    poscars_output_file = ''
    for uniq in unique_individuals:
        energy_sort.append(uniq['energy'])
#        density_sort.append(uniq['struct'].density)
        struct = uniq['struct']
        index = f'EA{uniq["index"]}'
        Sorder = uniq['Sorder']
        output.append(f'{index:8s} {struct.composition.formula:16s} {struct.get_space_group_info(args.symprec)[1]:3d} {uniq["energy"]:14.12f} {struct.volume:17.12f} {struct.density:16.12f} {Sorder:16.12f}\n')
        output_poscars.append(struct.to('poscar', comment=index))
    sorting_idx = np.argsort(energy_sort)
    for idx in sorting_idx:
        print_output += output[idx]
        poscars_output_file += f'{output_poscars[idx]}'

    os.chdir(f'{args.results}')
    if os.path.exists('Ase_goodStructures'):
        print('The existing file will be renamed as XXX-back')
        os.rename('Ase_goodStructures','Ase_goodStructures-back')
    if os.path.exists('Ase_goodStructures_POSCARS'):
        print('The existing file will be renamed as XXX-back')
        os.rename('Ase_goodStructures_POSCARS','Ase_goodStructures_POSCARS-back')

    with open('Ase_goodStructures', 'wt') as f:
        f.write(print_output)

    with open('Ase_goodStructures_POSCARS', 'wt') as f:
        f.write(poscars_output_file)

    print(f'Saved good structures list to {results}/ase_goodStructures')
    print(f'Saved good structures POSCARS to {results}/ase_goodStructures_POSCARS')

if __name__ == '__main__':
    import time
    start=time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--results', type=str, required=True, help="USPEX results folder (fixcomp)")
    parser.add_argument('-s','--symprec', type=float, default=0.1, help="Symmetry precision")
    parser.add_argument('-f','--fptol', type=float, default=0.008, help="Fingerprint tolerance")
    args = parser.parse_args()
    results=args.results
    fptol=args.fptol
    symprec=args.symprec
    # extract_good_structures(args)
    #print(args,type(args))
    i=1
    while i >=1:
        p1=mp.Process(target=extract_good_structures,args=(results,symprec,fptol))
        p1.start()
        i-=1
    p1.join()
    end=time.time()
    print(end-start)
