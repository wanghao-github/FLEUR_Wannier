import os
import shutil
import subprocess
import glob

# 获取 "1.cif" 文件夹中所有的 CIF 文件
cif_files = glob.glob('1.cif_struc/*.cif')

# 创建目标文件夹 "2.inp_films"（如果不存在）
output_folder = '2.inp_films'
os.makedirs(output_folder, exist_ok=True)

# 遍历每个 CIF 文件，创建同名子文件夹并将 CIF 文件复制到相应的子文件夹中
for cif_file in cif_files:
    # 获取不带扩展名的文件名
    file_name = os.path.splitext(os.path.basename(cif_file))[0]

    # 构造目标子文件夹路径
    destination_folder = os.path.join(output_folder, file_name)
    os.makedirs(destination_folder, exist_ok=True)

    # 构造目标文件路径
    destination_file = os.path.join(destination_folder, os.path.basename(cif_file))

    # 使用 shutil.copy2 进行复制，保留文件元数据
    shutil.copy2(cif_file, destination_file)

print(f"{len(cif_files)} files copied to {output_folder}.")

# 获取所有的 "2.inp_films" 子文件夹
structure_folders = [os.path.join(output_folder, folder) for folder in os.listdir(output_folder) if os.path.isdir(os.path.join(output_folder, folder))]

# 遍历每个子文件夹，并在其中执行 cif2pos.py 脚本
for structure_folder in structure_folders:
    # 构造 cif2pos.py 脚本的路径
    script_path = os.path.abspath('cif2pos.py')

    # 获取不带扩展名的文件名
    file_name = os.path.basename(structure_folder)

    # 获取子文件夹中的 CIF 文件名
    cif_file = os.path.join(structure_folder, f"{file_name}.cif")

    # 使用 subprocess.run 简化代码
    result = subprocess.run(['python', script_path, cif_file], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: Script execution failed for folder {structure_folder}")
        print("Error output:", result.stderr)

print("Scripts executed in all 2.inp_films folders.")
