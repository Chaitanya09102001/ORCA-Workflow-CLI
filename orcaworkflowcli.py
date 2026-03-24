# ---------------------------------------------------------------------------
# ORCA Workflow CLI 
# Copyright (c) 2026 Chaitanya09102001
# Licensed under the MIT License (see LICENSE file for details)
#
# NOTE: This software is provided "as-is". The author is not responsible 
# for any incorrect computational results or wasted HPC resources. 
# Always verify your input files!
# ---------------------------------------------------------------------------
import psutil
import os
import subprocess
import orca_parser as op
print("Welcome to CLI ORCA Workflow App\nDeveloper:\nCHAITANYA GADEKAR\nPlease read the README created along to use this app fluently.")
input("Press ENTER to initiate >>>")
global calculation_type
global theory_level
global basis_set
global core
global memory
# %%
#collecting and processing .xyz file path
raw_path = input("Paste the path of required .xyz file:\n")
clean_path = raw_path.strip().replace('"', '').replace("'", "")
if os.path.exists(clean_path) and clean_path.lower().endswith(".xyz"):
    file_dir = os.path.dirname(clean_path)
    molecule_name = os.path.basename(clean_path).replace(".xyz","")
#processing coordinates from .xyz file
with open(clean_path,'r') as f:
    lines = f.readlines()
coord_lines = lines[2:]
unique_coords = []
seen = set()
for line in coord_lines:
    content = line.strip()
    if content and content not in seen:
        seen.add(content)
        unique_coords.append(line)
final_coords = "".join(unique_coords)
#learn this part again and again
# %% 
#collect calculation type
print("Enter the number of required Calculation type options")
while True:
    calculation_type_input=input("1 for Geometry Optimization,\n2 for Single Point Energy Calculation, \n3 for Frequanecy Analysis \n")
    if calculation_type_input == "1":
        calculation_type = "Opt"
        print("Geometry optimization selected")
        break
    elif calculation_type_input == "2":
        calculation_type = "SP"
        print("Single Point Energy Calculation selected")
        break
    elif calculation_type_input == "3":
        calculation_type = "Opt Freq"
        print("Geometry optimization followed by Frequency analysis selected")
        break
    else:
        print("Please enter number from options 1, 2 or 3")
#%%
#quality preset (loose to verytight SCF)
quality_dict = {
    "1":"LooseSCF","2":"NormalSCF","3":"TightSCF","4":"VeryTightSCF"
    }
quality_choice = input("Do you want to customize SCF criteria? (y/n): ").lower()
if quality_choice == "y":
    for key,name in quality_dict.items():
        print(f"{key}. {name}")
    quality_input = input("Enter number for SCF criteria quality: ")
    quality_level = quality_dict.get(quality_input)
    print(f"Quality selected: {quality_level}.")
else:
    print("Default SCF criteria will be utilised according to calculation type selected. (Read Manual)")
# %%
#collect theory level
theory_level_dict = {
    "1":"PBE","2":"PBE0","3":"wB97X-D3","4":"B3LYP","5":"HF","6":"revPBE"
    }
print("Following Theory levels are available:\n1. PBE\n2. PBE0\n3. wB97X-D3\n4. B3LYP\n5. HF (Default)\n6. revPBE")
theory_level_input = input("Enter the number for required level of theory: ")
theory_level = theory_level_dict.get(theory_level_input,"HF")
print(f"Selected level of theory is {theory_level}.")
if "D3" not in theory_level:
    dispersion_choice = input(f"Do you want to apply D3BJ dispersion correction to {theory_level}? (y/n) \n").lower()
    if dispersion_choice == "y":
        theory_level += " D3BJ"
        print(f"Theory level modified to {theory_level}.")
# %%
#collect basis set
basis_set_dict = {
    "1":"def2-SVP","2":"def2-TZVP","3":"6-31G(d) (Default)","4":"def2-QZVP","5":"cc-pVDZ","6":"def2-TZVPP"
    }
print("Following Basis Sets are available:")
for key,name in basis_set_dict.items():
    print(f"{key}. {name}")
basis_set_input = input("Enter the number for required basis set: ")
basis_set = basis_set_dict.get(basis_set_input,"6-31G(d)")
print(f"Selected basis set is {basis_set}.")
# %%
#core and memory
nprocs_limit = psutil.cpu_count(logical=False)
print(f"Your device has {nprocs_limit} cores.")
while True:
    nprocs_input = int(input("Enter core count you want to use: "))
    if nprocs_input <= nprocs_limit:
        nprocs = nprocs_input
        break
    else:
        print("Enter valid core count to be used.")
mem  = psutil.virtual_memory()
total_gb = mem.total/(1024**3)
total_mb = total_gb*1024
available_gb = mem.available/(1024**3)
print(f"Available RAM is {available_gb:.2f} GB.")
available_mb = available_gb*1024
print("75% of available RAM will be alloted for calculation.")
maxcore_mb = int((available_mb*0.75)/nprocs)
print(f"Maxcore is set to {maxcore_mb} MB.")
# %%
#charge and multiplicity of system uploaded
charge = input("Enter charge on system: ")
multiplicity = input("Enter multiplicity for the system: ")
# %%
#collect whether RIJCOSX or not
rijcosx_choice = input("Do you want to apply RIJCOSX? (y/n): ").lower()
# %%
#generation of input lines
first =  "! "+ calculation_type +" "+ theory_level +" "+ basis_set
if rijcosx_choice == "y" and quality_choice == "y":
    first += str(" RIJCOSX" + " " + quality_level)
second = "\n%maxcore "+ str(int(maxcore_mb))
third = "\n%pal\n   nprocs "+ str(nprocs) +"\nend"
fourth = "\n* xyz " + charge + " " + multiplicity
fifth = final_coords.rstrip()
last_asterisk = "*"
# %%
#input file generation
input_filename = molecule_name + ".inp"
full_save_path = os.path.join(file_dir,input_filename)
orca_input_content = first+"\n"+second+"\n"+third+"\n"+fourth+"\n"+fifth+"\n"+last_asterisk
with open(full_save_path,"w") as f:
    f.write(orca_input_content)
print(f"\nInput file created: {input_filename}\n saved in {file_dir}.")
output_path = ""
def execution():
    global output_path
    output_path = full_save_path.replace(".inp",".out")
    outout_filename = input_filename.replace(".inp", ".out")
    open(output_path,'a').close()
    monitor_command = f'start powershell -Command "type \'{output_path}\' -Wait"'
    subprocess.Popen(monitor_command, shell=True)
    print(f"Starting ORCA {calculation_type} for {molecule_name}...")
    print("calculation in process...")
    drive = file_dir[:2]
    cmd = f'{drive} & cd "{file_dir}" & D:/ORCA/orca "{input_filename}" > "{outout_filename}"'
    subprocess.run(cmd, shell=True)
    if os.path.exists(output_path):
        with open(output_path,'r') as f:
            content_check = f.read()
            if "ORCA TERMINATED NORMALLY" in content_check:
                print("\nORCA calculation terminated succesfully!")
    print("ORCA calculation complete!")
    return output_path
execution_choice = input("Start ORCA calculation now? (y/n): ").lower()
if execution_choice == "y":
    output_path=execution()
else:
    print("Input file is only created. You can manually start the calculation at anytime.")
# %%
#parsing the output file
#parse code
if execution_choice == "y":
    opt = op.ORCAParse(output_path)
    print("Some important information from calculation output: ")
    print("Job took:",opt.seconds(),"seconds.")
    opt.parse_energies()
    opt.parse_energies
    opt.parse_dipole()
    opt.parse_dipole
    print("Final energy: ",opt.energies[-1], "Eh")
    final_energy_Eh = opt.energies[-1]
    final_energy_eV = final_energy_Eh*27.211386
    print("Final energy: ",str(final_energy_eV), "eV")
    print("All energies: ", opt.energies, "(in Eh)")
    print("Dipole information:\n", opt.parse_dipole())
    if calculation_type == "Opt Freq":
        opt.parse_IR()
        opt.parse_IR
        print("IR Frequencies are found in the output file.")
        print("IR Frequencies are tabulated below: \n")
        print(opt.IR)
# %%
input("Press enter to exit.")
