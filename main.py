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
            break  # 可以根据需要终止循环
        else:
            print("Latest task may not have completed successfully. Checking again in {} seconds.".format(interval))
            time.sleep(interval)

def check_latest_task_completion(keyword, file_pattern):
    # 获取所有匹配的 mpi-err 文件
    mpi_err_files = glob.glob(file_pattern)
    
    if mpi_err_files:
        # 获取最新的 mpi-err 文件
        latest_mpi_err = max(mpi_err_files, key=os.path.getctime)

        # 读取文件内容并检查关键字
        with open(latest_mpi_err, 'r') as file:
            content = file.read()
            return keyword in content

    return False

# 示例用法
# check_completion_periodically()

def update_itmax_attribute(xml_file_path, new_value):
    """
    Update the 'itmax' attribute in the 'scfLoop' element of an XML file.

    Parameters:
        - xml_file_path (str): The path to the XML file.
        - new_value (str): The new value for the 'itmax' attribute.

    Returns:
        - bool: True if the update is successful, False otherwise.
    """
    if os.path.exists(xml_file_path):
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Find the scfLoop element
        scf_loop_element = root.find(".//scfLoop")

        # Update the itmax attribute
        if scf_loop_element is not None:
            scf_loop_element.set("itmax", new_value)

            # Save the modified XML back to the file
            tree.write(xml_file_path)
            print(f"{xml_file_path} updated successfully.")
            return True
        else:
            print("Error: 'scfLoop' element not found in the XML file.")
    else:
        print(f"Error: {xml_file_path} not found.")
        return False

# Example usage:
inp_xml_file = "inp.xml"
new_loop_number = "80"

# 获取 "1.cif" 文件夹中所有的 CIF 文件
cif_files = glob.glob('1.cif_struc/*.cif')
current_working_directory = os.getcwd()
print(current_working_directory)
# 创建目标文件夹 "2.inp_films"（如果不存在）
output_folder = '../2.inp_struc'
os.makedirs(output_folder, exist_ok=True)
print(cif_files)
# 遍历每个 CIF 文件，创建同名子文件夹并将 CIF 文件复制到相应的子文件夹中
for cif_file in cif_files:
    # 获取不带扩展名的文件名
    file_name = os.path.splitext(os.path.basename(cif_file))[0]
    print(file_name)
    # 构造目标子文件夹路径
    destination_folder = os.path.join(output_folder, file_name)
    os.makedirs(destination_folder, exist_ok=True)

    # 构造目标文件路径
    destination_file = os.path.join(destination_folder, os.path.basename(cif_file))
    print(destination_file)
    # 使用 shutil.copy2 进行复制，保留文件元数据
    shutil.copy2(cif_file, destination_file)
    destination_POSCAR = os.path.join(destination_folder, 'POSCAR')
    # 在主程序中调用 cif2pos 模块
    subprocess.run(['python', 'cif2pos.py', destination_file, destination_folder])
    subprocess.run(['python', 'contcar2inpfilm.py', destination_POSCAR , destination_folder])
    
    inp_sup_path = os.path.join(destination_folder, 'inp_sup')
    
    os.chdir(destination_folder)
    print(current_working_directory)
    # 使用 inpgen 命令
    subprocess.run(['inpgen', '-f', 'inp_sup'])

    # Specify the XML file and the new value

    inp_xml_file = "inp.xml"
    new_loop_number = "80"
    print(os.path.join(current_working_directory, 'subjob_2022'))
    update_itmax_attribute(inp_xml_file, new_loop_number)
    # shutil.copy2(os.path.join(current_working_directory, 'subjob_2022'), os.path.join(destination_folder, 'subjob_2022'))
    
    initial_subjob_path = os.path.join(current_working_directory, 'subjob_2022')
    if os.path.isfile(initial_subjob_path):
        shutil.copy2(initial_subjob_path, './')
    else:
        print(f"Error: {initial_subjob_path} is not a file.")
        
    print("Current working directory:", os.getcwd())
    print("Subjob path:", initial_subjob_path)

    subprocess.run(['sbatch', 'subjob_2022'])
    # 切换回原始工作目录
    os.chdir(current_working_directory)

print(f"{len(cif_files)} files processed.")