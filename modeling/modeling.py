import os
import itertools
import argparse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.multioutput import ClassifierChain
from sklearn.metrics import (f1_score, multilabel_confusion_matrix,
                             accuracy_score, hamming_loss, jaccard_score, make_scorer)
from sklearn.model_selection import train_test_split, cross_validate


from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer

import xgboost as xgb
from sklearn.svm import SVC
from tabpfn import TabPFNClassifier

from joblib import dump, load


N_CV = 5

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


def optimize(data_x, data_y, algorithm, output_model_file, output_validation_file):
    if algorithm == "xgb":
        bayesopt = BayesSearchCV(
            ClassifierChain(xgb.XGBClassifier(), random_state=0),
            {
                "base_estimator__objective": Categorical(["binary:logistic"]),
                "base_estimator__max_depth": Integer(1, 10),
                "base_estimator__min_child_weight": Real(1e-6, 10, prior="log-uniform"),
                "base_estimator__max_delta_step": Real(1e-6, 10, prior="log-uniform"),
                "base_estimator__subsample": Real(1e-6, 1, prior="log-uniform"),
                "base_estimator__tree_method": Categorical(["exact", "approx", "hist"]),
                "base_estimator__scale_pos_weight": Real(1e-6, 10, prior="log-uniform"),
                "base_estimator__gamma": Real(1e-6, 10, prior="log-uniform"),
                "base_estimator__eta": Real(1e-6, 1, prior="log-uniform")
            },
            n_iter=250,
            cv=N_CV,
            random_state=0,
            n_jobs=10,
            n_points=2,
            scoring=make_scorer(multilabel_f1_wrapper),
            verbose=1,
        )
    elif algorithm == "svc":
        bayesopt = BayesSearchCV(
            ClassifierChain(SVC(), random_state=0),
            {
                "base_estimator__C": Real(1e-6, 1000, prior="log-uniform"),
                "base_estimator__kernel": Categorical(["rbf"]),
                "base_estimator__gamma": Real(1e-6, 1000, prior="log-uniform"),
            },
            n_iter=250,
            cv=N_CV,
            random_state=0,
            n_jobs=10,
            n_points=2,
            scoring=make_scorer(multilabel_f1_wrapper),
            verbose=1,
        )
    bayesopt.fit(data_x, data_y)
    dump(bayesopt.best_estimator_, output_model_file)

    best_iteration = 0
    for i in range(0, 250):
        if bayesopt.cv_results_["mean_test_score"][i] == bayesopt.best_score_:
            best_iteration = i

    output_text = []
    output_text.append("Best iteration: " + str(best_iteration) + "\n")
    output_text.append("Split scores:\n")
    for i in range(0, 5):
        output_text.append("" + str(i) + " " + str(bayesopt.cv_results_["split"+str(i)+"_test_score"][best_iteration]) + "\n")
    output_text.append("Mean score: " + str(bayesopt.best_score_) + "\n")
    output_text.append("Best parameter combination found: " + str(bayesopt.best_params_) + "\n")
    output = open(output_validation_file, "w") 
    output.writelines(output_text)
    output.close() 


def validate_tabpfn(data_x, data_y, output_validation_file):
    model = ClassifierChain(TabPFNClassifier(device='cpu', N_ensemble_configurations=30))
    cv = cross_validate(model, data_x, data_y, scoring=make_scorer(multilabel_f1_wrapper), cv=N_CV, return_train_score=True)

    output_text = []
    output_text.append("Split scores:" + "\n")
    for i in range(0, 5):
        output_text.append("" + str(i) + " " + str(cv["test_score"][i]) + "\n")
    output_text.append("Mean score: " + str(cv["test_score"].mean()) + "\n")
    output = open(output_validation_file, "w") 
    output.writelines(output_text)
    output.close() 


def metrics_report(true, pred, output_file):
    hl = hamming_loss(true, pred)
    f1w = multilabel_f1_wrapper(true, pred, "weighted")
    acc = accuracy_score(true, pred)
    
    f1u = multilabel_f1_wrapper(true, pred, "macro")
    f1su = f1_score(true, pred, average="macro")
    f1sw = f1_score(true, pred, average="weighted")

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


def confusion_matrix(test_y, pred, output_file):
    plt.clf()

    antibiotics = test_y.columns

    fig, axes = plt.subplots(1, len(antibiotics), figsize=(len(antibiotics)*5, 5))
    fig.supxlabel("Predicted Label")
    fig.supylabel("True Label")

    cm = multilabel_confusion_matrix(test_y, pred)

    for i in range(len(antibiotics)):
        sns.heatmap(ax=axes[i], data=cm[i], annot=True, fmt='d', cbar=None, cmap="Blues", xticklabels=["S", "R"], yticklabels=["S", "R"]).set(title=antibiotics[i])
    
    plt.savefig(output_file)


def classify(model, test_x, test_y, output_results_file, output_confusion_file):
    pred = model.predict(test_x)
    metrics_report(test_y, pred, output_results_file)
    confusion_matrix(test_y, pred, output_confusion_file)


def probability(model, test_x, test_y, output_file):
    proba = model.predict_proba(test_x)
    antibiotics = test_y.columns
    
    output_text = []
    for antibiotic in range(len(antibiotics)):
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
                if disc_pred == test_y.iloc[i, antibiotic]:
                    count_tp += 1
                    sum_tp += proba[i, antibiotic]
                else:
                    count_fp += 1
                    sum_fp += proba[i, antibiotic]
            else:
                if disc_pred == test_y.iloc[i, antibiotic]:
                    count_tn += 1
                    sum_tn += proba[i, antibiotic]
                else:
                    count_fn += 1
                    sum_fn += proba[i, antibiotic]
        output_text.append("Results for antibiotic " + antibiotics[antibiotic] + "\n")
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



parser = argparse.ArgumentParser()
parser.add_argument("-f", "--Folder", help="What folder to get the data from", default="raw")
parser.add_argument("-m", "--Mode", help="Whether to use data as is (no argument) or to select specific features based on a .txt file", choices=["raw", "selected"])
parser.add_argument("-a", "--Algorithm", help="ML Algorithm to use (options: xgb, svc, tabpfn, nn)", choices=["xgb", "svc", "tabpfn", "nn"], required=True)
args = parser.parse_args()

input_folder = "data/processed/"+args.Folder+"/"
if args.Algorithm == "tabpfn":
    input_folder = "data/processed/raw/none/"

output_folder = "modeling/results/"
input_files = os.listdir(input_folder)
input_train_files = [x for x in input_files if "test" not in x and not os.path.isdir(os.path.join(input_folder, x))]
input_file_paths = [input_folder + file for file in input_train_files]

for file in input_file_paths:
    plt.close("all")
    
    print("\nProcessing", file)
    train_bac = pd.read_csv(file)
    test_bac = pd.read_csv(file.replace("train", "test"))

    file_name_ext = os.path.basename(file)
    file_name = os.path.splitext(file_name_ext)[0].replace("train_", "")
    base_name = output_folder+file_name

    antibiotics = train_bac.columns.drop(train_bac[train_bac.columns.drop(list(train_bac.filter(regex='[^0-9]')))].columns)

    if args.Algorithm == "tabpfn":
        train_bac, _ = train_test_split(train_bac, train_size=1000, random_state=0, stratify=train_bac[antibiotics])

    train_x = train_bac[train_bac.columns.drop(list(train_bac.filter(regex='[^0-9]')))]
    test_x = test_bac[test_bac.columns.drop(list(test_bac.filter(regex='[^0-9]')))]

    train_y = train_bac[antibiotics]
    test_y = test_bac[antibiotics]

    if args.Mode == "selected" or args.Algorithm == "tabpfn":
        print("Using selected features")
        with open("data/features/"+file_name+"_selected_features.txt") as file:
            selected_features = file.read().split(",")
        selected_features.pop()

        base_name = base_name+"_selected"

        train_x = train_x[selected_features]
        test_x = test_x[selected_features]

    base_name = base_name+"_"+args.Algorithm
    model_file = "modeling/models/"+file_name+"_"+args.Algorithm+".joblib"

    if not os.path.exists(model_file) or not os.path.exists(base_name+"_cv.txt"):
        print("     Model training...")
        if args.Algorithm == "tabpfn":
            validate_tabpfn(train_x, train_y, base_name+"_cv.txt")

            model = ClassifierChain(TabPFNClassifier(device='cpu', N_ensemble_configurations=30))
            model.fit(train_x, train_y)
            dump(model, model_file) 
        else:
            optimize(train_x, train_y, args.Algorithm, model_file, base_name+"_cv.txt")

    model = load(model_file) 

    if not os.path.exists(base_name+"_results.txt") or not os.path.exists(base_name+"_confusion_matrix.png"):
        print("     Classification...")
        classify(model, test_x, test_y, base_name+"_results.txt", base_name+"_confusion_matrix.png")

    if not os.path.exists(base_name+"_proba.txt"):
        print("     Probability prediction...")
        if args.Algorithm == "svc":
            print("To-do")
        else:
            probability(model, test_x, test_y, base_name+"_proba.txt")

    print("Done.\n")




