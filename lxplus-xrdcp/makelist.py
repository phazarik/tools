import os, subprocess, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--min', type=float, default=10,  help='Minimum file size in MB (optional)')
parser.add_argument('--max', type=float, default=100, help='Maximum file size in MB (optional)')
parser.add_argument('-n', type=int, help='Number of files to keep per dataset (optional)')
args = parser.parse_args()

# Convert MB to bytes using 1024-based conversion
min_size = args.min * 1024 * 1024 if args.min is not None else None
max_size = args.max * 1024 * 1024 if args.max is not None else None
n_keep = args.n

# ANSI colors
YELLOW = "\033[93m"
RESET = "\033[0m"

outname = "list.txt"

# Check for proxy
if subprocess.call(['voms-proxy-info', '-exists']) != 0:
    os.system('voms-proxy-init --voms cms')
    print('Proxy generated.')
else: print('Valid proxy already exists.')

print('Investigating samples ..')

das_names = [
    "/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v1/NANOAODSIM"
]

selected_files = []
info = []
total_size_bytes = 0
total_events = 0

header = f"\n{'ind0':>5} {'ind1':>5}  {'Size (MB)':>10}  {'Events':>10}  File" + "\n" + "-"*100
print(header)
info.append(header)

count = 0
for name in das_names:

    short_name = name.split('/')[1]
    if n_keep!=1: print(f"{YELLOW}{short_name}{RESET}")

    query = f'file dataset={name} | grep file.name,file.size,file.nevents'
    try:
        result = subprocess.check_output(['dasgoclient', '-query', query], encoding='utf-8')
    except subprocess.CalledProcessError:
        print("  Error querying DAS. Skipping dataset.")
        continue

    count1 = 0

    for line in result.strip().split('\n'):
        parts = line.strip().split()

        if len(parts) != 3: continue
        fname, fsize, nevents = parts[0], int(parts[1]), int(parts[2])

        if min_size is not None and fsize < min_size: continue
        if max_size is not None and fsize > max_size: continue

        size_mb = fsize / (1024 * 1024)
        line = f"{count+1:>5} {count1+1:>5} {size_mb:10.1f} {nevents:10d}  {fname}"
        print(line)
        
        selected_files.append(fname)
        info.append(line)
        total_size_bytes += fsize
        total_events += nevents

        count  += 1
        count1 += 1

        if n_keep is not None and count1 >= n_keep: break

# Convert total size to GB and MB
gb = total_size_bytes // (1024 ** 3)
mb = (total_size_bytes % (1024 ** 3)) // (1024 ** 2)

footer = "-"*100 + "\n" + f"{YELLOW}Total size: {gb} GB + {mb} MB\nTotal events = {total_events}{RESET}\n"
print(footer)
info.append(footer)

with open(outname, "w") as f:
    for fname in selected_files:
        f.write(fname + '\n')

with open("info.txt", "w") as f:
    for line in info:
        f.write(line + '\n')
