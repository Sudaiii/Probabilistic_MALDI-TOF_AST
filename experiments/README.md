# Probabilistic_MALDI-TOF_AST

Scripts used in the experiments to construct ML models.

## Folder structure

### Processing
Contains the scripts used to process the MALDI-TOF Mass Spectra data into something more easy to use.
- [binning.py](binning.py): Creates binned versions of the raw data. By default, creates a version of bin size 5 and one of bin size 20 (as dictated by the `bin_sizes` variable).
- [preprocessing.py](preprocessing.py): Removes instances with missing data, trims unnecessary columns, splits it into a train and test dataset then the scales data.