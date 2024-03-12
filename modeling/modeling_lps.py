import os
import argparse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from problem_transformation import agg_columns
from evaluation import multilabel_f1_wrapper, metrics_report, confusion_matrix
from lps_optimization import optimize_svc, optimize_xgb
from sklearn.metrics import make_scorer

from sklearn.preprocessing import LabelEncoder

from joblib import dump, load



np.int = int
N_CV = 5
N_ITER = 200
MODE = "lps"
lc = LabelEncoder()



def lps_to_multilabel_instance(lps_instance):
    multilabel_instance = []
    for result in lps_instance[0]:
        multilabel_instance.append(int(result))
    return multilabel_instance

def lps_to_multilabel_list(lps_list):
    multilabel_list = []
    for lps_instance in lps_list:
        multilabel_list.append(lps_to_multilabel_instance(lc.inverse_transform([lps_instance])))
    return multilabel_list

def lps_f1_wrapper(true, pred, average="weighted"):
    non_lps_true = lps_to_multilabel_list(true)
    non_lps_pred = lps_to_multilabel_list(pred)
    return multilabel_f1_wrapper(non_lps_true, non_lps_pred, average=average)



def optimize(train_features, train_labels, algorithm, output_model_file, output_validation_file):
    if algorithm == "xgb":
        bayesopt = optimize_xgb(N_CV, N_ITER)
    elif algorithm == "svc":
        bayesopt = optimize_svc(N_CV, N_ITER)
    elif algorithm == "mlp":
        bayesopt = optimize_svc(N_CV, N_ITER)
    bayesopt.scoring = make_scorer(lps_f1_wrapper)
    bayesopt.fit(train_features, train_labels)
    dump(bayesopt.best_estimator_, output_model_file)

    best_iteration = 0
    for i in range(0, N_ITER):
        if bayesopt.cv_results_["mean_test_score"][i] == bayesopt.best_score_:
            best_iteration = i

    output_text = []
    output_text.append("Best iteration: " + str(best_iteration) + "\n")
    output_text.append("Split scores:\n")
    for i in range(0, N_CV):
        output_text.append("" + str(i) + " " + str(bayesopt.cv_results_["split"+str(i)+"_test_score"][best_iteration]) + "\n")
    output_text.append("Mean score: " + str(bayesopt.best_score_) + "\n")
    output_text.append("Best parameter combination found: " + str(bayesopt.best_params_) + "\n")
    output = open(output_validation_file, "w") 
    output.writelines(output_text)
    output.close() 


def classify(model, test_features, test_labels, label_names, output_results_file, output_confusion_file):
    pred = model.predict(test_features)
    test_labels = lps_to_multilabel_list(test_labels)
    pred = lps_to_multilabel_list(pred)
    metrics_report(test_labels, pred, label_names, output_results_file)
    confusion_matrix(test_labels, pred, label_names, output_confusion_file)


def probability(model, test_features, test_labels, output_file):
    proba = model.predict_proba(test_features)
    antibiotics = test_labels.columns
    
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--Folder", help="What folder to get the data from", default="binned", choices=["unbinned", "binned"])
    parser.add_argument("-n", "--Norm", help="Data normalization method. Supports \"none\",\"min-max\" and \"standard\"", default="standard", choices=["none", "min-max", "standard"])
    parser.add_argument("-a", "--Algorithm", help="ML Algorithm to use (options: xgb, svc, mlp)", choices=["xgb", "svc", "mlp"], required=True)
    args = parser.parse_args()

    input_folder = "data/processed/"+args.Folder+"/"+args.Norm+"/"

    output_folder = "modeling/results/"
    input_files = os.listdir(input_folder)
    input_train_files = [x for x in input_files if "test" not in x and not os.path.isdir(os.path.join(input_folder, x))]
    input_file_paths = [input_folder + file for file in input_train_files]

    for file in input_file_paths:
        lc = LabelEncoder()
        plt.close("all")
        
        print("\nProcessing", file)
        train_bac = pd.read_csv(file)
        test_bac = pd.read_csv(file.replace("train", "test"))

        file_name_ext = os.path.basename(file)
        file_name = os.path.splitext(file_name_ext)[0].replace("train_", "")

        base_name = output_folder+file_name+"_"+args.Algorithm+"_"+args.Norm+"_"+MODE
        model_file = "modeling/models/"+file_name+"_"+args.Algorithm+"_"+args.Norm+"_"+MODE+".joblib"

        antibiotics = train_bac.columns.drop(train_bac[train_bac.columns.drop(list(train_bac.filter(regex='[^0-9]')))].columns)

        train_x = train_bac[train_bac.columns.drop(list(train_bac.filter(regex='[^0-9]')))]
        test_x = test_bac[test_bac.columns.drop(list(test_bac.filter(regex='[^0-9]')))]

        train_y = train_bac[antibiotics].astype(int)
        test_y = test_bac[antibiotics].astype(int)

        train_y = agg_columns(train_y)
        test_y = agg_columns(test_y)

        lc.fit(train_y.values.ravel())
        train_y = lc.transform(train_y.values.ravel())
        test_y = lc.transform(test_y.values.ravel())

        if not os.path.exists(model_file) or not os.path.exists(base_name+"_cv.txt"):
            print("     Model training...")
            optimize(train_x, train_y, args.Algorithm, model_file, base_name+"_cv.txt")

        model = load(model_file) 

        if not os.path.exists(base_name+"_results.txt") or not os.path.exists(base_name+"_confusion_matrix.png"):
            print("     Classification...")
            classify(model, test_x, test_y, antibiotics, base_name+"_results.txt", base_name+"_confusion_matrix.png")

        if not os.path.exists(base_name+"_proba.txt"):
            print("     Probability prediction...")
            if args.Algorithm == "svc":
                print("To-do")
            else:
                probability(model, test_x, test_y, base_name+"_proba.txt")

        print("Done.\n")

