#!/usr/bin

# Author: Formula
# Data:2021/03/02
# This script is used to partition the POSCARS as many POSCAR files..
# USage: python script.py target-file


import pandas as pd
from tqdm import tqdm

def readfile(filename):
    """
    read file to a list and delete the blank lines
    """
    try:
        f = open(filename, 'r')
    except:
        print('Error :cannnot open the file :' + filename)
        exit()
    rst = []
    try:
        for line in f:
            if len(line.strip()) != 0:
                rst.append(line.strip())
    finally:
        f.close()
    return rst


def seprate(inputfile):
    """
    input list file and split it  into single POSCAR
    """
    deposit = []
    try:
        start = [i for i, x in enumerate(inputfile) if x == '1.0']
        # print(start)
        for m in tqdm(range(len(start))):
            start2 = [i for i, x in enumerate(inputfile) if x == '1.0']
            tmp = []
            if len(start2) == 1:
                for n in inputfile[:]:
                    tmp.append(n)
            else:
                for n in inputfile[:start2[1] - 1]:
                    tmp.append(n)
            deposit.append(tmp)
            try:
                del inputfile[:start2[1] - 1]
            except:
                pass
        return deposit
    except:
        print('Error:cannot find 1.0')
        pass


def wPOSCAR(POSCAR):
    num=len(POSCAR)
    for i in tqdm( range(num)):
        try:
            f = open('%s.vasp' % POSCAR[i][0].split()[0] , 'a')
        except:
            print('ERROR: cannnot open the file POCSAR')
            exit(0)
        for i in POSCAR[i]:
            f.write(str(i) + '\n')
        f.close()

if __name__ == "__main__":
    import sys

    args = sys.argv
    filename = args[1]
    inputfile = readfile(filename)

    POSCAR = seprate(inputfile)
    # print(POSCAR)
    wPOSCAR(POSCAR)
