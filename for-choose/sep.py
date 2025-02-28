import sys
import os

def split_poscars(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    poscar_lines = []
    file_number = 1

    for line in lines:
        if line.startswith('EA') and poscar_lines:
            write_poscar(poscar_lines, file_number)
            poscar_lines = []
            file_number += 1

        poscar_lines.append(line)

    if poscar_lines:
        write_poscar(poscar_lines, file_number)


def write_poscar(poscar_lines, file_number):
    output_file = 'EA{}.vasp'.format(file_number)
    with open(output_file, 'w') as file:
        file.writelines(poscar_lines)


input_file = sys.argv[1]

split_poscars(input_file)
