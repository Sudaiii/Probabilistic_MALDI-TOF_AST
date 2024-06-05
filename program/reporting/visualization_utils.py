import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
from reportlab.platypus import Image
from reportlab.lib.units import inch
import io



LINEWIDTH = 1
LABEL_SIZE = 8
AXIS_TICK_SIZE = 8
LEGEND_SIZE = '8'
Y_LABEL_FORMAT = '{:,.3f}'
BASE_PALETTE = sns.color_palette("tab20")



def spectrometry(X, bin_size):
    plt.style.use("seaborn-v0_8-white")
    plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(bin_size))

    lower_limit = 2000
    upper_limit = 9999
    jump = int((upper_limit - lower_limit + bin_size) / bin_size)

    fig, axes = plt.subplots(1, 1, figsize=(8, 4))
    
    sns.set_theme(font_scale = 2)
    line = sns.lineplot(ax=axes, data=X, x="mass", y="intensity", linewidth=LINEWIDTH)
    line.set(xticks=np.arange(lower_limit, upper_limit, jump))
    line.set_xlabel("Masa (Da)", fontsize=LABEL_SIZE)
    line.set_ylabel("Intensidad", fontsize=LABEL_SIZE)

    line.set_xticks(np.arange(lower_limit, upper_limit, jump))
    line.set_xticklabels(np.arange(lower_limit, upper_limit, jump), size=AXIS_TICK_SIZE)
    ticks_loc = axes.get_yticks()
    axes.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    axes.set_yticklabels([Y_LABEL_FORMAT.format(x) for x in ticks_loc], size=AXIS_TICK_SIZE)

    axes.margins(x=0.005)

    fig.tight_layout()

    temp_buf = io.BytesIO()
    plt.savefig(temp_buf, format='png', bbox_inches='tight', dpi=300)
    temp_buf.seek(0)
    x, y = fig.get_size_inches()
    
    plt.clf()
    plt.cla()
    plt.close()

    return Image(temp_buf, x * inch, y * inch)