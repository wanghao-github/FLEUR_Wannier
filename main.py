import os
import shutil
import glob
# import cif2pos  # Assuming cif2pos.py is in the same directory
import subprocess
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

    # 切换回原始工作目录
    os.chdir(current_working_directory)

print(f"{len(cif_files)} files processed.")