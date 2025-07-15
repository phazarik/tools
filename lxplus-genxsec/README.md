# Cross Section Extraction Utilities for CMS Datasets

![CMS Members Only](https://img.shields.io/badge/CMS-members--only-red)

Tools to extract generator-level cross sections from CMS datasets using `GenXSecAnalyzer`. It works within a CMSSW environment and uses DAS to locate the required MiniAOD files.

## 📁 Files Overview

-   **`find_xsec_fromDAS.py`**:  
    Takes a single dataset, finds its parent MiniAOD, downloads one file, and runs `cmsRun` with `GenXSecAnalyzer` to extract the cross section.
-   **`bulksubmission.py`**:  
    Contains a hardcoded list of datasets and calls `find_xsec_fromDAS.py` on each of them in sequence. Useful for batch extraction.
    
Both scripts rely on the standard `genXsec_cfg.py` and `ana`, which will be downloaded automatically if missing.
    
## 🚀 Usage
Go to your lxplus work area and create a CMSSW area that is compatible with the target samples.
```bash
cmsrel CMSSW_13_0_13
cd CMSSW_13_0_13/src
cmsenv
```
> ⚠️ **CMS VOMS Proxy Required**  
> Before running the scripts, a valid CMS VOMS proxy is needed.  
> This can be generated with:  
> ```bash
> voms-proxy-init --voms cms
> ```

Place the scripts in `src`.
```bash
wget https://github.com/phazarik/tools/releases/download/lxplus-v1.0/bulksubmission.py
wget https://github.com/phazarik/tools/releases/download/lxplus-v1.0/find_xsec_fromDAS.py
```

### 🔹Process a single dataset
```bash
python3 find_xsec_fromDAS.py --dataset <DATASET_NAME>  # Takes a few seconds
```
### 🔹Process multiple datasets
The datasets are predefined in the script. Edit as per requirement.
```bash
python3 bulksubmission.py  # Takes a few minutes
```
The cross section will be printed directly in the terminal after each run.

## 🔗 Reference
 GEN Documentation: [How to Compute Cross Sections with GenXSecAnalyzer](https://cms-generators.docs.cern.ch/useful-tools-and-links/HowToGenXSecAnalyzer/#automated-scripts-to-compute-the-cross-section-for-existing-datasets)