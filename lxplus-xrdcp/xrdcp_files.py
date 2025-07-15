import os
with open('list.txt', 'r') as file_list: file_paths = file_list.readlines()

for line in file_paths:
   
    line = line.strip()
    split_path = line.split('/')
    folder_name = os.path.join(split_path[3], split_path[4])  # Example: Run3Summer22NanoAODv12/DYto2L-4Jets_MLL-50_TuneCP5_13p6TeV_madgraphMLM-pythia8
    
    if not os.path.exists(folder_name): os.makedirs(folder_name)
    
    # Construct the xrdcp command
    input_file = f"root://cmsxrootd.fnal.gov//{line}"
    command = f"xrdcp {input_file} {folder_name}/"
    
    # Execute the xrdcp command
    print(command)
    os.system(command)
    #print(f"Copied {input_file} to {folder_name}/")
    #break
    
print("All files copied.")
