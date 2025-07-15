# Directly bringing files from CMS DAS using `xrdcp`
![CMS Members Only](https://img.shields.io/badge/CMS-members--only-red)

A two-step Python workflow to **query**, **filter**, and **download** CMS DAS files based on size and count constraints. Designed for CMS users working on `lxplus` .

## ✅ Requirements
-   Access to **CMS lxplus** or any system with CMS environment
- A valid **CMS VOMS proxy** (`voms-proxy-init`)

## 🚀 Usage

Login to `lxplus`. Ensure that your working directory has enough disk space. Copy the two scripts (`makelist.py` and `xrdcp_files.py`) to the area, then proceed as follows.

> ⚠️ **CMS VOMS Proxy Required**  
> Before running the scripts, a valid CMS VOMS proxy is needed.  
> This can be generated with:  
> ```bash
> voms-proxy-init --voms cms
> ```
Get the files in an lxplus work area.
```bash
wget https://github.com/phazarik/tools/releases/download/lxplus-v1.0/makelist.py
wget https://github.com/phazarik/tools/releases/download/lxplus-v1.0/xrdcp_files.py
```

### 🔹Step 1: Make a list
Edit the `das_names` list inside `makelist.py` to include the datasets you want.
```bash
python3 makelist.py --min 10 --max 100 -n 3
```
- `--min`: Minimum file size in MB (optional, default = 10 MB)
- `--max`: Maximum file size in MB (optional, default = 100 MB)
- `-n`: Number of files to keep per dataset (optional, default = all)

This will create a `list.txt` file containing paths to all the files that will be downloaded in the next step. You may edit `list.txt` manually if needed before downloading.

### 🔹Step 2: Iterate over the list using `xrdcp `
```bash
python3 xrdcp_files.py
```
This downloads each file in `list.txt` from FNAL’s XRootD endpoint (`root://cmsxrootd.fnal.gov/`).  
Other available options include:
-   `root://xrootd-cms.infn.it/` — Global CMS redirector (recommended default)
-   `root://eoscms.cern.ch/` — CERN EOS redirector

You can change the redirector in `xrdcp_files.py` by modifying the `input_file` path.  
Files are saved in a nested folder structure based on **campaign** and **dataset** name, as shown below:
```bash
Run3Summer22NanoAODv12/
└── DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/
    ├── file1.root
    ├── file2.root
    └── ...
```