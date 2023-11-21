import os
import shutil
import glob
import subprocess
import xml.etree.ElementTree as ET
import time

def check_completion_periodically(interval=30, keyword="Run finished successfully", file_pattern="mpi-err.*"):
    while True:
        result = check_latest_task_completion(keyword, file_pattern)
        if result:
            print("Latest task completed successfully.")
            break
        else:
            print("Latest task may not have completed successfully. Checking again in {} seconds.".format(interval))
            time.sleep(interval)

def check_latest_task_completion(keyword, file_pattern):
    mpi_err_files = glob.glob(file_pattern)
    
    if mpi_err_files:
        latest_mpi_err = max(mpi_err_files, key=os.path.getctime)

        with open(latest_mpi_err, 'r') as file:
            content = file.read()
            return keyword in content

    return False

def update_itmax_attribute(xml_file_path, new_value):
    if os.path.exists(xml_file_path):
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        scf_loop_element = root.find(".//scfLoop")

        if scf_loop_element is not None:
            scf_loop_element.set("itmax", new_value)
            tree.write(xml_file_path)
            print(f"{xml_file_path} updated successfully.")
            return True
        else:
            print("Error: 'scfLoop' element not found in the XML file.")
    else:
        print(f"Error: {xml_file_path} not found.")
        return False

def submit_job(subjob_path, destination_folder):
    shutil.copy2(subjob_path, destination_folder)
    os.chdir(destination_folder)
    subprocess.run(['sbatch', 'subjob_2022'])
    os.chdir(current_working_directory)

def process_cif_files(cif_files, output_folder):
    for cif_file in cif_files:
        file_name = os.path.splitext(os.path.basename(cif_file))[0]
        destination_folder = os.path.join(output_folder, file_name)
        os.makedirs(destination_folder, exist_ok=True)

        destination_file = os.path.join(destination_folder, os.path.basename(cif_file))
        shutil.copy2(cif_file, destination_file)

        destination_POSCAR = os.path.join(destination_folder, 'POSCAR')
        subprocess.run(['python', 'cif2pos.py', destination_file, destination_folder])
        subprocess.run(['python', 'contcar2inpfilm.py', destination_POSCAR, destination_folder])

        inp_sup_path = os.path.join(destination_folder, 'inp_sup')
        os.chdir(destination_folder)
        subprocess.run(['inpgen', '-f', 'inp_sup'])

        inp_xml_file = "inp.xml"
        new_loop_number = "80"
        update_itmax_attribute(inp_xml_file, new_loop_number)

        initial_subjob_path = os.path.join(current_working_directory, 'subjob_2022')
        if os.path.isfile(initial_subjob_path):
            submit_job(initial_subjob_path, destination_folder)
        else:
            print(f"Error: {initial_subjob_path} is not a file.")

    os.chdir(current_working_directory)

# Example usage:
cif_files = glob.glob('1.cif_struc/*.cif')
current_working_directory = os.getcwd()
output_folder = '../2.inp_struc'
os.makedirs(output_folder, exist_ok=True)

process_cif_files(cif_files, output_folder)
check_completion_periodically()