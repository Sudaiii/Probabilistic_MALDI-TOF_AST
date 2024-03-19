import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (f1_score, jaccard_score, multilabel_confusion_matrix,
                             accuracy_score, hamming_loss)
import numpy as np
import pandas as pd


def multilabel_jaccard_wrapper(true, pred, average="weighted"):
    if isinstance(true, list):
        true = np.array(true)
    elif isinstance(true, pd.DataFrame):
        true = true.to_numpy()
    if isinstance(pred, list):
        pred = np.array(pred)
    elif isinstance(pred, pd.DataFrame):
        pred = pred.to_numpy()
    column = 0
    total = 0
    while column < true[0].size:
        total+=jaccard_score(true[:, column], pred[:, column], average=average, zero_division=0)
        column+=1
    return total/(column)


def multilabel_f1_wrapper(true, pred, average="weighted"):
    if isinstance(true, list):
        true = np.array(true)
    elif isinstance(true, pd.DataFrame):
        true = true.to_numpy()
    if isinstance(pred, list):
        pred = np.array(pred)
    elif isinstance(true, pd.DataFrame):
        pred = pred.to_numpy()
    column = 0
    total = 0
    while column < true[0].size:
        total+=f1_score(true[:, column], pred[:, column], average=average)
        column+=1
    return total/(column)



def metrics_report(true, pred, label_names, output_file):        
    if isinstance(true, list):
        true = np.array(true)
    elif isinstance(true, pd.DataFrame):
        true = true.to_numpy()
    if isinstance(pred, list):
        pred = np.array(pred)
    elif isinstance(pred, pd.DataFrame):
        pred = pred.to_numpy()
    
    jsu = 0
    jsw = 0
    f1u = 0
    f1w = 0
    
    print("Individual Results:")
    individual_results = {}
    label_n = len(label_names)
    for i in range(label_n):
        sliced_true = true[:, i]
        sliced_pred = pred[:, i]

        label_acc = accuracy_score(sliced_true, sliced_pred)
        label_hl = hamming_loss(sliced_true, sliced_pred)

        label_jsu = jaccard_score(sliced_true, sliced_pred, average="macro")
        jsu+=label_jsu

        label_jsw = jaccard_score(sliced_true, sliced_pred, average="weighted")
        jsw+=label_jsw

        label_f1u = f1_score(sliced_true, sliced_pred, average="macro")
        f1u+=label_f1u

        label_f1w = f1_score(sliced_true, sliced_pred, average="weighted")
        f1w+=label_f1w

        label_results = {
            "Accuracy": label_acc,
            "Hamming Loss": label_hl,
            "Jaccard Score Unweighted": label_jsu,
            "Jaccard Score Weighted": label_jsw,
            "F1 Score Unweighted": label_f1u,
            "F1 Score Weighted": label_f1w,
        }
        print("---"+str(label_names[i])+"---")
        for j in label_results:
            print("", j,":",label_results[j])
        individual_results[label_names[i]] = label_results
    

    print("=======================")
    print("Multi-label Results:")
    acc = accuracy_score(true, pred)
    
    hl = hamming_loss(true, pred)
    
    jsu/=label_n
    jsw/=label_n
    jssu = jaccard_score(true, pred, average="macro")
    jssw = jaccard_score(true, pred, average="weighted")
    
    f1u/=label_n
    f1w/=label_n
    f1su = f1_score(true, pred, average="macro")
    f1sw = f1_score(true, pred, average="weighted")
    
    if label_n <= 1:
        jsu = jssu
        jsw = jssw
        f1u = f1su
        f1w = f1sw
        

    multi_label_results = {
        "Accuracy": acc,
        "Hamming Loss": hl,
        "Jaccard Score Unweighted": jsu,
        "Jaccard Score Weighted": jsw,
        "F1 Score Unweighted": f1u,
        "F1 Score Weighted": f1w,
        
        "Jaccard Score Unweighted (Sci-kit)": jssu,
        "Jaccard Score Weighted (Sci-kit)": jssw,
        "F1 Score Unweighted (Sci-kit)": f1su,
        "F1 Score Weighted (Sci-kit)": f1sw,
    }
    for i in multi_label_results:
        print("", i,":",multi_label_results[i])


    output_text = [
        "Main metrics:\n",
        " Hamming Loss: " + str(hl) + "\n",
        " Accuracy: " + str(acc) + "\n",
        " F1 Score (Weighted): " + str(f1w) + "\n",
        "================================================\n",
        "Other metrics:\n",
        " F1 Score (Unweighted): " + str(f1u) + "\n",
        " F1 Score (sklearn Unweighted): " + str(f1su) + "\n",
        " F1 Score (sklearn Weighted): " + str(f1sw) + "\n"
    ]
    output = open(output_file, "w") 
    output.writelines(output_text)
    output.close()


def confusion_matrix(true, pred, label_names, output_file):
    plt.clf()

    fig, axes = plt.subplots(1, len(label_names), figsize=(len(label_names)*5, 5))
    fig.supxlabel("Predicted Label")
    fig.supylabel("True Label")

    cm = multilabel_confusion_matrix(true, pred)

    for i in range(len(label_names)):
        sns.heatmap(ax=axes[i], data=cm[i], annot=True, fmt='d', cbar=None, cmap="Blues", xticklabels=["S", "R"], yticklabels=["S", "R"]).set(title=label_names[i])
    
    plt.savefig(output_file)


def proba_report(test_labels, proba, label_names, output_file):
    label_names = test_labels.columns
    
    output_text = []
    for antibiotic in range(len(label_names)):
        count_tp = 0
        count_tn = 0
        count_fp = 0
        count_fn = 0
        sum_tp = 0
        sum_tn = 0
        sum_fp = 0
        sum_fn = 0
        for i in range(len(proba[:, antibiotic])):
            disc_pred = int(proba[i, antibiotic] > 0.5)
            if disc_pred == 1:
                if disc_pred == test_labels.iloc[i, antibiotic]:
                    count_tp += 1
                    sum_tp += proba[i, antibiotic]
                else:
                    count_fp += 1
                    sum_fp += proba[i, antibiotic]
            else:
                if disc_pred == test_labels.iloc[i, antibiotic]:
                    count_tn += 1
                    sum_tn += proba[i, antibiotic]
                else:
                    count_fn += 1
                    sum_fn += proba[i, antibiotic]
        output_text.append("Results for antibiotic " + label_names[antibiotic] + "\n")
        if count_tp == 0:
            output_text.append(" Mean TP: None\n")
        else: 
            output_text.append(" Mean TP: " + str(sum_tp/count_tp) + "\n")
        if count_tn == 0:
            output_text.append(" Mean TN: None\n")
        else: 
            output_text.append(" Mean TN: " + str(sum_tn/count_tn) + "\n")
        if count_fp == 0:
            output_text.append(" Mean FP: None\n")
        else: 
            output_text.append(" Mean FP: " + str(sum_fp/count_fp) + "\n")
        if count_fn == 0:
            output_text.append(" Mean FN: None\n")
        else: 
            output_text.append(" Mean FN: " + str(sum_fn/count_fn) + "\n")
    output = open(output_file, "w") 
    output.writelines(output_text)
    output.close()