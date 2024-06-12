# Probabilistic_MALDI-TOF_AST

Scripts used in the experiments to construct ML models.

## Folder structure

### Data
Folder containing the data. 

Raw data must be in a subfolder of /data/unprocessed/.

File [antibiotics.json](data/antibiotics.json) contains a dictionary mapping each antibiotic to each bacteria. Used so that [preprocessing.py](preprocessing.py) can tell which labels to keep.

### Processing
Contains the scripts used to process the MALDI-TOF Mass Spectra data into something more easy to use.
- [binning.py](binning.py): Creates binned versions of the raw data. By default, creates a version of bin size 5 and one of bin size 20 (as dictated by the `bin_sizes` variable).
- [preprocessing.py](preprocessing.py): For each file inside the target folder, remove instances with missing data, trim unnecessary columns, split into a train and test dataset, then scale the data. Has several parameters:
  - --Folder (-f): The target folder that contains the data to process. Must be inside the /data/unprocessed/ folder. Default: "binned".
  - --Norm (-m):  The type of normalization to scale the data with. Options: "none", "min-max" and "standard" (the latter being strongly suggested).

### Exploration
Contains only one script: [exploration.py](exploration.py).

Explores the data in the specified folder via a varied set of graphics:
- Class distribution.
- Correlation between labels (antibiotics).
- Mean mass spectra of each class.
- PCA and t-SNE 2D distribution graphs.

Has the following parameters:
- --Folder (-f): The target folder that contains the processed data to explore. Must be inside the /data/processed/ folder. **Explores each dataset separately**. Default: "binned".
- --Norm (-m):  The type of normalization that was used to scale the data with [preprocessing.py](preprocessing.py). Parameter is only used so the program can tell which subfolder to use. Could be simplified into being included in the -f parameter in a future version. Default: "standard".
  
### Modeling
A package containing one script ([modeling_lps.py](modeling/modeling_lps.py)) and several other Python files with useful functions.

Builds the ML models, optimizes their hyperparameters using Bayesian Optimization with Cross Validation, validates results, obtains feature importance via SHAP and obtains test dataset results.

Has the following parameters:
- --Folder (-f): The target folder that contains the processed data to build and validate the models with. **Builds a model per train dataset.** Must be inside the /data/processed/ folder. Default: "binned".
- --Norm (-m):  The type of normalization that was used to scale the data with [preprocessing.py](preprocessing.py). Parameter is only used so the program can tell which subfolder to use. Could be simplified into being included in the -f parameter in a future version. Default: "standard".

