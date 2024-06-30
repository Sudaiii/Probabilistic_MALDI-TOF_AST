""" 
    script de python para realizar el proceso de binning a los espectros de masa 
    de la base de datos DRIAMS.
        variables a considerar:
            ms_files_path   : Ubicacion de los archivos con los espectros de masa.
            driams_dataset  : Ubicacion del dataset original DRIAMS.
            ms_min          : Limite inferior para los binning a realizar.
            ms_max          : Limite superior para los binning a realizar.
            ms_bin_size     : Tamano del bin.
                                                                                    """
"""Hecho por: Jose Manriquez"""
import pathlib
import pandas as pd
import numpy as np
import re 

def get_add_intensities(sample_bins, intensities):
    new_intentisities = ([intensities[sample_bins == i ].mean() for i in np.unique(sample_bins)])
    new_sample_bins = ([sample_bins[sample_bins == i ] for i in np.unique(sample_bins)])  
    return new_intentisities , new_sample_bins

ms_files_names = []
ms_files_path = 'DRIAMS_MS/DRIAMS-D/raw/2018'# DEFINIR FICHERO CON LOS ESPECTROS DE MASAS 
directorio = pathlib.Path(ms_files_path)
for fichero in directorio.iterdir():
    ms_files_names.append(fichero.name)
ms_min = 2000
ms_max = 20000
ms_bin_size = 3

ms_codes = []
ms_data = [] # Lista contiene las masas y sus intensidades de todas las muestras del dataset 
driams_dataset = pd.read_csv('DRIAMS_csv_sin_espectros/driams_D/k_pneumoniae_driams_d.csv') #FICHERO DEL CSV CON LAS MUESTRAS

for file_name in ms_files_names:
    aux = re.sub('.txt', '', file_name)
    for code in driams_dataset['code']:
        if aux == code:
            mass_df = pd.read_csv(ms_files_path +'/'+ file_name, names=['mass', 'intensity'], sep=' ', skiprows=3)
            ms_data.append(mass_df)
            ms_codes = np.append(ms_codes, code)

#SEPARACION DE LOS ESPECTROS DE MASA Y SUS INTENCIDADES 
read_mass = []
aux_arr = []
for i in range(len(ms_data)):
    aux_arr = ms_data[i]['mass']
    read_mass = np.append(read_mass, aux_arr)
    
#CREACION DE LOS COLUMNS HEADERS
bins = np.arange(ms_min, ms_max, ms_bin_size)
indices  = np.digitize(read_mass, bins)
#columns_headers = np.array([read_mass[indices == i].mean() for i in np.unique(indices)])
columns_headers = bins
columns_headers = np.sort(columns_headers)
columns_headers = columns_headers[~np.isnan(columns_headers)]
columns_headers = columns_headers.astype(int)

#CREACION DE LA MATRIZ
matrix=np.zeros((len(ms_data),len(columns_headers+1)))

for index, s in enumerate(ms_data):
    indices_bins = np.digitize(s['mass'], columns_headers)
    add_intensities, new_sample_bins = get_add_intensities(indices_bins, s['intensity'].values)
    for i, value in enumerate(new_sample_bins):
        matrix[index][value-1] = add_intensities[i]

# CREACION DEL NUEVO DATA SET CON LOS ESPECTROS DE MASA + LOS PERFILES DE RESISTENCIA
bin_driams_dataset = pd.DataFrame(matrix, columns=columns_headers)
bin_driams_dataset['code'] = ms_codes
bin_driams_dataset = bin_driams_dataset.merge(driams_dataset, left_on='code', right_on='code')
bin_driams_dataset.to_csv('driams_datasets/driams_d/k_pneumoniae_driams_d_2000_20000Da_v2.csv', sep=',',index=False)