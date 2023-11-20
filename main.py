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
    
    # 使用 shutil.copy 进行复制
    shutil.copy(cif_file, destination_file)

print(f"{len(cif_files)} files copied to {output_folder}.")

# 获取所有的 "2.inp_films" 子文件夹
structure_folders = [os.path.join('2.inp_films', folder) for folder in os.listdir('2.inp_films') if os.path.isdir(os.path.join('2.inp_films', folder))]

# 遍历每个子文件夹，并在其中执行 cif2pos.py 脚本
for structure_folder in structure_folders:
    # 构造 cif2pos.py 脚本的路径
    script_path = os.path.abspath('cif2pos.py')

    # 获取不带扩展名的文件名
    file_name = os.path.basename(structure_folder)

    # 获取子文件夹中的 CIF 文件名
    cif_file = os.path.join(structure_folder, f"{file_name}.cif")

    # 启动一个进程并执行脚本
    process = subprocess.Popen(['python', script_path, cif_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate(input=b'\n')  # Send an Enter key press to standard input

    # 等待进程结束
    process.wait()

print("Scripts executed in all 2.inp_films folders.")


