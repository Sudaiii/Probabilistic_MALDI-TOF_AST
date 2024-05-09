import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
import pandas as pd
import io

import PIL



LINEWIDTH = 1
LABEL_SIZE = 8
AXIS_TICK_SIZE = 8
LEGEND_SIZE = '8'
Y_LABEL_FORMAT = '{:,.3f}'
BASE_PALETTE = sns.color_palette("tab20")



def visualize(X):
    if len(X) > 1:
        X = X.iloc[[0]]
    return spectrometry(X)


def melt_data(X):
    melt_X = X.melt(var_name='Da', value_name='Value')
    melt_X["Da"] = melt_X["Da"].astype(str).astype(int)
    return melt_X


def spectrometry(X):
    melt_X = melt_data(X)
    plt.clf()
    plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(20))

    lower_limit = int(X.columns[0])
    upper_limit = int(X.columns[-1])
    jump = int((upper_limit - lower_limit + 20) / 20)

    fig, axes = plt.subplots(1, 1, figsize=(8, 4))
    
    sns.set_theme(font_scale = 2)
    line = sns.lineplot(ax=axes, data=melt_X, x="Da", y="Value", linewidth=LINEWIDTH)
    line.set(xticks=np.arange(lower_limit, upper_limit, jump))
    line.set_xlabel("Da", fontsize=LABEL_SIZE)
    line.set_ylabel("Value", fontsize=LABEL_SIZE)

    line.set_xticks(np.arange(lower_limit, upper_limit, jump))
    line.set_xticklabels(np.arange(lower_limit, upper_limit, jump), size=AXIS_TICK_SIZE)
    ticks_loc = axes.get_yticks()
    axes.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    axes.set_yticklabels([Y_LABEL_FORMAT.format(x) for x in ticks_loc], size=AXIS_TICK_SIZE)

    axes.margins(x=0.005)

    fig.tight_layout()

    temp_buf = io.BytesIO()
    plt.savefig(temp_buf, format='png', bbox_inches='tight')
    im = PIL.Image.open(temp_buf)

    return im

    # plt.savefig("test.png")