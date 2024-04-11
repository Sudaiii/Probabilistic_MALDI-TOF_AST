import os
import itertools
import argparse
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from sklearn.preprocessing import LabelEncoder
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA


LINEWIDTH = 2
LABEL_SIZE = 28
AXIS_TICK_SIZE = 28
LEGEND_SIZE = '24'
Y_LABEL_FORMAT = '{:,.3f}'
BASE_PALETTE = sns.color_palette("tab20")


def single_label_class_distribution(data, labels, output_file):
    plt.clf()

    sns.set(rc={'figure.figsize':(5, 5)})
    sns.set(font_scale=1.2)
    class_dist = sns.heatmap(data[labels].apply(pd.Series.value_counts).T, annot=True, fmt="d", linewidth=.5, cmap="rocket_r")
    
    fig = class_dist.get_figure()
    fig.savefig(output_file, bbox_inches = "tight")


def agg_label_class_distribution(data, labels, output_file):
    plt.clf()

    value_counts = data[labels].value_counts()
    df_value_counts = value_counts.rename("Count").to_frame().reset_index()

    options = profile[labels[0]].unique()
    combined = []
    for i in range(len(labels)):
        combined.append(options)
    combinations = list(itertools.product(*combined))
    df_combinations = pd.DataFrame(columns=labels, data=combinations)

    df_combination_count = df_combinations.merge(df_value_counts, how="left").fillna(0).astype({"Count": "int"})
    df_sorted = df_combination_count.sort_values(by=["Count"], ascending=False)

    df_sorted.to_csv(output_file)


def label_correlation(y, output_file):
    plt.clf()

    sns.set(rc={'figure.figsize':(7, 7)})
    corr = y.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.set(font_scale=1.4)
    corr_plot = sns.heatmap(corr, mask=mask, annot=True, cmap="rocket_r")

    fig = corr_plot.get_figure()
    fig.savefig(output_file, bbox_inches = "tight")


def mean_mass_spectra_lineplot(data, label, output_file):
    plt.clf()

    lower_limit = int(malditof.columns[0])
    upper_limit = int(malditof.columns[-1])
    jump = int((upper_limit - lower_limit + 1) / 20)
    
    if label == "agg_class":
        class_count = profile.value_counts().count()
        palette = BASE_PALETTE[:class_count]
    else:
        palette = {"S": "C0", "R": "C1"}

    fig, axes = plt.subplots(1, 1, figsize=(30, 20))
    
    sns.set(font_scale = 2)
    line = sns.lineplot(ax=axes, data=data, x="Da", y="Value", hue=label, 
                            palette=palette, linewidth=LINEWIDTH)
    line.set(xticks=np.arange(lower_limit, upper_limit, jump))
    line.set_xlabel("Da", fontsize=LABEL_SIZE)
    line.set_ylabel("Value", fontsize=LABEL_SIZE)

    line.set_xticklabels(axes.get_xticks(), size=AXIS_TICK_SIZE)
    ticks_loc = axes.get_yticks()
    axes.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    axes.set_yticklabels([Y_LABEL_FORMAT.format(x) for x in ticks_loc], size=AXIS_TICK_SIZE)

    plt.setp(line.get_legend().get_texts(), fontsize=LEGEND_SIZE) 
    plt.setp(line.get_legend().get_title(), fontsize=LEGEND_SIZE) 
    axes.margins(x=0.005)

    plt.savefig(output_file)


def pca_scatterplot(x, y, class_names, output_file):
    plt.clf()

    class_count = np.unique(y).size
    palette = BASE_PALETTE[:class_count]

    pca = PCA(n_components=2, random_state=0)
    pca.fit(x)
    attributes_pca = pca.transform(x)
    fig, axes = plt.subplots(figsize=(10, 10))

    s = sns.scatterplot(x=attributes_pca[:, 0], y=attributes_pca[:, 1], hue=y, s=80, palette=palette[::-1])

    plt.setp(s.get_legend().get_texts(), fontsize="16") 
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.01))

    for t, l in zip(s.legend_.texts, class_names):
        t.set_text(l)

    fig = s.get_figure()
    fig.savefig(output_file, bbox_inches = "tight")


def tsne_scatterplot(x, y, perplexities, class_names, output_file):
    plt.clf()

    class_count = np.unique(y).size
    palette = BASE_PALETTE[:class_count]

    for index, perplexity in enumerate(perplexities):
        x_reduced = TSNE(verbose=0, perplexity=perplexity, n_jobs=-1, learning_rate=200.0, init="random", random_state=0).fit_transform(x)
        df = pd.DataFrame({"x":x_reduced[:,0], "y":x_reduced[:,1] , "label":y})

        fig, axes = plt.subplots(figsize=(10, 10))

        s = sns.scatterplot(data=df, x="x", y="y", hue=y, s=50, palette=palette[::-1])
        s.set(xlabel=None)
        s.set(ylabel=None)

        plt.setp(s.get_legend().get_texts(), fontsize="16") 
        plt.legend(loc='upper right', bbox_to_anchor=(1, 1.01))

        for t, l in zip(s.legend_.texts, class_names):
            t.set_text(l)
        plt.show()

        fig = s.get_figure()
        fig.savefig(output_file, bbox_inches = "tight")



parser = argparse.ArgumentParser()
parser.add_argument("-f", "--Folder", help="What folder to get the data from", default="binned", choices=["unbinned", "binned"])
parser.add_argument("-n", "--Norm", help="Data normalization method. Supports \"none\",\"min-max\" and \"standard\"", default="standard", choices=["none", "min-max", "standard"])
parser.add_argument("-m", "--Mode", help="Whether to use data as is (no argument) or to select specific features based on a .txt file", default="all")
args = parser.parse_args()

input_folder = "data/processed/"+args.Folder+"/"+args.Norm+"/"
output_folder = "exploration/outputs/"
input_files = os.listdir(input_folder)
input_train_files = [x for x in input_files if "test" not in x and not os.path.isdir(os.path.join(input_folder, x))]
input_file_paths = [input_folder + file for file in input_train_files]

for file in input_file_paths:
    plt.close("all")
    
    print("Processing", file)
    bacteria = pd.read_csv(file)

    file_name_ext = os.path.basename(file)
    file_name = os.path.splitext(file_name_ext)[0].replace("train_", "")
    base_name = output_folder+file_name

    malditof = bacteria[bacteria.columns.drop(list(bacteria.filter(regex='[^0-9]')))]
    antibiotics = bacteria.columns.drop(malditof.columns)
    bacteria[antibiotics] = bacteria[antibiotics].replace([0.0, 1.0], ["S", "R"])
    profile = bacteria[antibiotics]

    if args.Mode == "selected":
        print("Using selected features")
        with open("data/features/"+file_name+"_selected_features.txt") as file:
            selected_features = file.read().split(",")
        selected_features.pop()

        base_name = output_folder+file_name+"_selected"

        malditof = malditof[selected_features]
        bacteria = bacteria[malditof.columns.append(antibiotics)]    

    class_count = profile.value_counts().count()

    if not os.path.exists(base_name+"_single_label_class_dist.png"):
        print("     Single-Label Class Distribution...")
        single_label_class_distribution(bacteria, antibiotics, base_name+"_single_label_class_dist.png")

    if not os.path.exists(base_name+"_agg_label_class_dist.csv"):
        print("     Aggregated-Label Class Distribution...")
        agg_label_class_distribution(bacteria, antibiotics, base_name+"_agg_label_class_dist.csv")

    if not os.path.exists(base_name+"_corr.png"):
        print("     Label Correlation...")
        numeric_profile = profile.replace({'S': 0, 'R': 1})
        label_correlation(numeric_profile, base_name+"_corr.png")


    print("     Antibiotic Mean Mass Spectra Correlation...")
    meltdata = bacteria.melt(antibiotics, var_name='Da', value_name='Value')
    meltdata["Da"] = meltdata["Da"].astype(str).astype(int)

    for antibiotic in antibiotics:
        if not os.path.exists(base_name+"_"+antibiotic+"_lineplot.png"):
            mean_mass_spectra_lineplot(meltdata, antibiotic, base_name+"_"+antibiotic+"_lineplot.png")


    if not os.path.exists(base_name+"_agg_class"+"_lineplot.png"):
        print("     Aggregated Antibiotic Mean Mass Spectra Correlation...")
        meltdata_agg = meltdata
        meltdata_agg["agg_class"] = meltdata[antibiotics].agg(''.join, axis=1)
        meltdata_agg["agg_class"] = meltdata_agg["agg_class"].astype(str)
        mean_mass_spectra_lineplot(meltdata_agg, "agg_class", base_name+"_agg_class"+"_lineplot.png")


    profile_agg = pd.DataFrame()
    profile_agg["Class"] = bacteria[antibiotics].agg(''.join, axis=1)

    lc = LabelEncoder()
    lc.fit(profile_agg.values.ravel())
    profile_agg_lc = lc.transform(profile_agg.values.ravel())

    if not os.path.exists(base_name+"_pca.png"):
        print("     PCA Scatter Plot...")
        pca_scatterplot(malditof, profile_agg_lc, lc.inverse_transform(range(class_count)), base_name+"_pca.png")

    if not os.path.exists(base_name+"_tsne.png"):
        print("     T-SNE Scatter Plot...")
        tsne_scatterplot(malditof, profile_agg_lc, [20], lc.inverse_transform(range(class_count)), base_name+"_tsne.png")


    print("Done.\n")




