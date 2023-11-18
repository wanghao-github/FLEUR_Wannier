import numpy as np
import math
import argparse

bohr_in_ang = 0.52917721067
ang_in_bohr = 1.88972612546

kpoint_dense = 45

ele_list = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
            'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb',
            'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs',
            'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
            'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa',
            'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt',
            'Ds', 'Rg', 'Cn', 'Uut', 'Fl', 'Uup', 'Lv', 'Uus', 'Uuo']

class AtomNotFoundError(Exception):
    pass

def read_contcar(filename):
    with open(filename, "r") as infile:
        file_content = infile.readlines()
    file_body = [line for line in file_content if line.strip()]
    return file_body

def calculate_kpoint_density(a_length):
    return math.ceil(kpoint_dense / a_length)

def get_atom_index(atom_type):
    if atom_type.lower() in map(str.lower, ele_list):
        return float(next(j for j, ele in enumerate(ele_list) if ele.lower() == atom_type.lower())) + 1.0
    else:
        raise AtomNotFoundError(f"{atom_type} not found in ele_list.")

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Generate input files for a specific application.")
    parser.add_argument("filename", help="Input CONTCAR filename")
    parser.add_argument("title", nargs="?", default="inp_generator", help="Title for the output files")
    return parser.parse_args()

def main():
    args = parse_command_line_args()
    filename = args.filename
    title = args.title
    n_type = int(input("Please input the type of the structure-1 for supercell, 2 for film:"))

    file_body = read_contcar(filename)
    scale_factor = file_body[1]
    lattice_parameters = [list(map(float, line.split())) for line in file_body[2:5]]
    a1x, a1y, a1z = lattice_parameters[0]
    a2x, a2y, a2z = lattice_parameters[1]
    a3x, a3y, a3z = lattice_parameters[2]

    a1_length = np.sqrt(a1x**2 + a1y**2 + a1z**2)
    a2_length = np.sqrt(a2x**2 + a2y**2 + a2z**2)
    a3_length = np.sqrt(a3x**2 + a3y**2 + a3z**2)

    k1 = calculate_kpoint_density(a1_length)
    k2 = calculate_kpoint_density(a2_length)
    k3 = calculate_kpoint_density(a3_length)

    atom_type = file_body[5].split()
    atom_numbers = list(map(int, file_body[6].split()))
    lower_atom_type = [t.lower() for t in atom_type]

    total_atom_number = sum(atom_numbers)
    atom_index = [get_atom_index(t) for t in atom_type]

    for type, number, index in zip(atom_type, atom_numbers, atom_index):
        print(f"Atom Name: {type}, Atom Number: {number}, Atom Index: {index}")

    if n_type == 1:
        generate_supercell_input(file_body, filename, title, a1x, a1y, a1z, a2x, a2y, a2z, a3x, a3y, a3z,
                                 total_atom_number, atom_type, atom_numbers, atom_index, k1, k2, k3)
    else:
        generate_film_input(file_body, filename, title, a1x, a1y, a1z, a2x, a2y, a2z, a3x, a3y, a3z,
                             total_atom_number, atom_type, atom_numbers, atom_index, k1, k2)

def generate_supercell_input(file_body, filename, title, a1x, a1y, a1z, a2x, a2y, a2z, a3x, a3y, a3z,
                             total_atom_number, atom_type, atom_numbers, atom_index, k1, k2, k3):
    with open("inp_sup", "w") as outfile:
        outfile.write("{:s}\n".format(filename))
        outfile.write("&input film=F, cartesian=F /\n")
        outfile.write("{:16.12f}{:16.12f}{:16.12f}\n".format(a1x, a1y, a1z))
        outfile.write("{:16.12f}{:16.12f}{:16.12f}\n".format(a2x, a2y, a2z))
        outfile.write("{:16.12f}{:16.12f}{:16.12f}\n".format(a3x, a3y, a3z))
        outfile.write("1.0\n")
        outfile.write("1.889726125 1.889726125 1.889726125 \n")
        outfile.write("{:3d}\n".format(total_atom_number))

        start = 8
        for i in range(len(atom_type)):
            for j in range(atom_numbers[i]):
                atom_position = file_body[start + j].split()
                x, y, z = map(float, atom_position[0:3])
                outfile.write("{:3.1f} {:16.12f} {:16.12f} {:16.12f}\n".format(atom_index[i], x, y, z))
            start = start + atom_numbers[i]
        outfile.write("\n")
        outfile.write("&soc 0.0 0.0 /\n")
        outfile.write("&kpt div1={:d} div2={:d} div3={:d} /\n".format(k1, k2, k3))

def generate_film_input(file_body, filename, title, a1x, a1y, a1z, a2x, a2y, a2z, a3x, a3y, a3z,
                         total_atom_number, atom_type, atom_numbers, atom_index, k1, k2):
    with open("inp_film", "w") as outfile:
        outfile.write("{:s}\n".format(title))
        outfile.write("&input film=T, symor=F, cartesian=F /\n")
        outfile.write("{:16.12f}{:16.12f}{:16.12f}\n".format(a1x, a1y, a1z))
        outfile.write("{:16.12f}{:16.12f}{:16.12f}\n".format(a2x, a2y, a2z))
        outfile.write("{:16.12f}{:16.12f}{:16.12f} 0.9\n".format(a3x, a3y, a3z))
        outfile.write("1.0\n")
        outfile.write("1.889726125 1.889726125 1.889726125\n")
        outfile.write("{:3d}\n".format(total_atom_number))

        z_values = [float(line.split()[2]) for line in file_body[8:8 + total_atom_number]]
        arv_z = (max(z_values) + min(z_values)) / 2

        start = 8
        for i in range(len(atom_type)):
            for j in range(atom_numbers[i]):
                atom_position = file_body[start + j].split()
                x, y, z = map(float, atom_position[0:3])
                direct2car_z = (z - arv_z) * a3z * 1.889726125
                outfile.write("{:3.1f}{:16.12f}{:16.12f}{:16.12f}\n".format(atom_index[i], x, y, direct2car_z))
            start = start + atom_numbers[i]
        outfile.write("\n")
        outfile.write("&soc 0.0 0.0 /\n")
        outfile.write("&kpt div1={:d} div2={:d} div3=1 /\n".format(k1, k2))

if __name__ == "__main__":
    main()
