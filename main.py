import os
import shutil
import numpy as np
import math
import argparse
import subprocess
from contcar2inpfilm import process_cif_files

folder_path = "./"
#process_cif_files(folder_path)

import os
import glob

current_directory = os.getcwd()

cif_files = glob.glob(os.path.join(current_directory, '*.cif'))

file_names = [os.path.basename(file) for file in cif_files]

print("CIF Files:")
print(file_names)

for cif_file in cif_files:
    destination_dir = os.path.join
