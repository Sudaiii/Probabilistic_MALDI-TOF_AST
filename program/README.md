# Fast AST

Predict the ARM profile of a bacterium quick and easy through MALDI-TOF Mass Spectra data and a simple graphical user interface.

## Features

- Obtain AMR profile of one or more samples of MALDI-TOF Mass Spectra of a bacterium.
- Visualize the MALDI-TOF Mass Spectra of a bacterium sample.
- Export results as a .pdf report.
- 4 different bacteria supported (Staphylococcus Aureus, Escherichia Coli, Klebsiella Pneumoniae, Pseudomonas Aeruginosa).

## Installation

Read instructions of parent [README.md](../README.md) file.

## Use

To run the program, simply run the file `app.py` via Python, as follows: `python app.py`. **Make sure the command is ran within the program folder**.

### Input file format
The program supports two different input file formats:
- [DRIAMS](https://datadryad.org/stash/dataset/doi:10.5061/dryad.bzkh1899q) MALDi-TOF Mass Spectra: .txt files following the same format as the DRIAMS raw files. See [maldi_raw_sample.txt](maldi_raw_sample.txt).
- Preprocessed: .csv files in which each column corresponds to the intensity of the sample in each mass value of the Mass Spectra. Columns must contain the range from [2000 to 9999] Da. See [maldi_sample.csv](maldi_sample.csv).

### Compile .exe file

To compile the program into an .exe file, simply run the following command: `pyinstaller folder.spec --no-confirm`