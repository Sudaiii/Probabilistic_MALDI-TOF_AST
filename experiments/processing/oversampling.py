import numpy as np
from imblearn.over_sampling import RandomOverSampler
from imblearn.combine import SMOTETomek


def random_oversampling(x, y):
    unique, counts = np.unique(y, return_counts=True)
    # print(np.asarray((unique, counts)).T)

    sorted_counts = np.sort(counts)
    target = sorted_counts[-1]
    # print("Target:", target)
    
    to_oversample = {}
    for pos in range(len(counts)):
        if counts[pos] < target:
            to_oversample[unique[pos]] = target
    # print("To oversample:", to_oversample.keys())

    oversampler = RandomOverSampler(sampling_strategy=to_oversample, random_state=0)
    x, y = oversampler.fit_resample(x, y)

    unique, counts = np.unique(y, return_counts=True)
    # print(np.asarray((unique, counts)).T)
    
    return x, y

def smote_tomek_oversampling(x, y):
    unique, counts = np.unique(y, return_counts=True)
    # print(np.asarray((unique, counts)).T)

    sorted_counts = np.sort(counts)
    target = sorted_counts[-1]
    # print("Target:", target)
    
    to_oversample = {}
    for pos in range(len(counts)):
        if counts[pos] < target:
            to_oversample[unique[pos]] = target
    # print("To oversample:", to_oversample.keys())

    oversampler = SMOTETomek(sampling_strategy="not majority", random_state=0)
    x, y = oversampler.fit_resample(x, y)

    unique, counts = np.unique(y, return_counts=True)
    print(np.asarray((unique, counts)).T)
    
    return x, y