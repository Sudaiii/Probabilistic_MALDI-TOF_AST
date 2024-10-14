import os
import argparse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from problem_transformation import agg_columns
from evaluation import multilabel_f1_wrapper, metrics_report, confusion_matrix, proba_report
from feature_importance import feature_importance
from optimization_lps import optimize_svc, optimize_xgb, optimize_mlp, optimize_rf
from sklearn.metrics import make_scorer

from sklearn.preprocessing import LabelEncoder

from joblib import dump, load


np.int = int
N_CV = 5
N_ITER = 200
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


def optimize(train_features, train_labels, algorithm, output_model_file, output_validation_file, lps):
    if algorithm == "xgb":
        bayesopt = optimize_xgb(N_CV, N_ITER)
    elif algorithm == "svc":
        bayesopt = optimize_svc(N_CV, N_ITER)
    elif algorithm == "rf":
        bayesopt = optimize_rf(N_CV, N_ITER)
    elif algorithm == "mlp":
        bayesopt = optimize_mlp(N_CV, N_ITER)

    if lps:
        bayesopt.scoring = make_scorer(lps_f1_wrapper)
    else:
        bayesopt.scoring = "f1_weighted"
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


def multilabel(train_features, train_labels, test_features, algorithm, base_name, model_file, oversampled=False, retrain=True):
    model_file = model_file+".joblib"

    train_y = agg_columns(train_labels)
    train_y = lc.transform(train_y.values.ravel())

    bac_options = ["s_aureus", "p_aeruginosa", "k_pneumoniae", "e_coli"]
    for bac_option in bac_options:
        if bac_option in model_file:
            model_bac = bac_option
    standarization_options = ["none", "min-max", "standard"]
    for standarization_option in standarization_options:
        if standarization_option in model_file:
            model_standarization = standarization_option
    bin_options = ["bin5", "bin20"]
    for bin_option in bin_options:
        if bin_option in model_file:
            model_bin = bin_option
    model_file_base = "modeling/models/"+model_bac+"_driams_"+model_bin+"_"+algorithm+"_"+model_standarization+"_lps.joblib"

    if retrain and not oversampled and "driamsB" not in base_name and "driamsC" not in base_name and "driamsD" not in base_name and (not os.path.exists(model_file) or not os.path.exists(base_name+"_cv.txt")):
        print("     Model training...")
        optimize(train_features, train_y, algorithm, model_file, base_name+"_cv.txt", True)

    if retrain and (oversampled or "driamsB" in base_name or "driamsC" in base_name or "driamsD" in base_name) and not os.path.exists(model_file):
        print("     Model training...")
        if os.path.exists(model_file_base):
            model = load(model_file_base) 
            model.fit(train_features, train_y)
            dump(model, model_file)
        else:
            print("First run the script with Driams A data that's not oversampled")
    
    if retrain:
        model = load(model_file) 
    elif os.path.exists(model_file_base):
        model = load(model_file_base)

    pred = model.predict(test_features)
    pred = lps_to_multilabel_list(pred)

    # if "bin5" not in base_name:
    #     print("     SHAP...")
    #     feature_importance(model, train_features, train_y, test_features, algorithm, base_name)

    return pred


def independent(train_features, train_labels, test_features, antibiotics, algorithm, base_name, model_file, oversampled=False, retrain=True):
    classifications = []

    for antibiotic in antibiotics:
        print(" ", antibiotic, "...")

        antibiotic_base_name = base_name+"_"+antibiotic
        antibiotic_model_file = model_file+"_"+antibiotic+".joblib"

        antibiotic_train_y = train_labels[antibiotic]

        bac_options = ["s_aureus", "p_aeruginosa", "k_pneumoniae", "e_coli"]
        for bac_option in bac_options:
            if bac_option in model_file:
                model_bac = bac_option
        standarization_options = ["none", "min-max", "standard"]
        for standarization_option in standarization_options:
            if standarization_option in model_file:
                model_standarization = standarization_option
        bin_options = ["bin5", "bin20"]
        for bin_option in bin_options:
            if bin_option in model_file:
                model_bin = bin_option
        antibiotic_model_file_base = "modeling/models/"+model_bac+"_driams_"+model_bin+"_"+algorithm+"_"+model_standarization+"_independent_"+antibiotic+".joblib"

        if retrain and not oversampled and "driamsB" not in base_name and "driamsC" not in base_name and "driamsD" not in base_name and (not os.path.exists(antibiotic_model_file) or not os.path.exists(antibiotic_base_name+"_cv.txt")):
            print("     Model training...")
            optimize(train_features, antibiotic_train_y, algorithm, antibiotic_model_file, antibiotic_base_name+"_cv.txt", False)
        
        if retrain and (oversampled or "driamsB" in base_name or "driamsC" in base_name or "driamsD" in base_name) and not os.path.exists(antibiotic_model_file):
            print("     Model training...")
            if os.path.exists(antibiotic_model_file_base):
                model = load(antibiotic_model_file_base) 
                model.fit(train_features, antibiotic_train_y)
                dump(model, antibiotic_model_file)
            else:
                print("First run the script with Driams A data that's not oversampled")

        if retrain:
            model = load(antibiotic_model_file) 
        elif os.path.exists(antibiotic_model_file_base):
            model = load(antibiotic_model_file_base)

        antibiotic_pred = model.predict(test_features)
        classifications.append(antibiotic_pred)
        
        # if "bin5" not in base_name:
        #     print("     SHAP...")
        #     feature_importance(model, train_features, antibiotic_train_y, test_features, algorithm, antibiotic_base_name)

    pred = []
    for i in range(len(classifications[0])):
        pred_instance = []
        for j in range(len(classifications)):
            pred_instance.append(classifications[j][i])
        pred.append(pred_instance)

    return pred



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--Folder", help="What folder to get the data from", default="binned")
    parser.add_argument("-n", "--Norm", help="Data normalization method. Supports \"none\",\"min-max\" and \"standard\"", default="standard", choices=["none", "min-max", "standard"])
    parser.add_argument("-o", "--Oversampling", help="Method used to oversample data. Supports \"none\", \"random\" and \"smotetomek\"", default="none")
    parser.add_argument("-a", "--Algorithm", help="ML Algorithm to use (options: xgb, svc, rf, mlp)", choices=["xgb", "svc", "rf", "mlp"], required=True)
    parser.add_argument("-m", "--Multilabel", help="Evaluate all labels through a single model using LPS or not", default="independent", choices=["lps", "independent"])
    args = parser.parse_args()
    
    mode = args.Multilabel

    input_folder = "data/processed/"+args.Folder+"/"+args.Oversampling+"/"+args.Norm+"/"

    output_folder = "modeling/results/"
    os.makedirs(output_folder, exist_ok=True)
    input_files = os.listdir(input_folder)
    input_train_files = [x for x in input_files if "train" not in x and not os.path.isdir(os.path.join(input_folder, x))]
    input_file_paths = [input_folder + file for file in input_train_files]

    for file in input_file_paths:
        plt.close("all")
        
        print("\nProcessing", file)
        test_bac = pd.read_csv(file)
        train_file = file.replace("test", "train")
        if os.path.exists(train_file):
            train_bac = pd.read_csv(train_file)
            retrain = True
        else:
            retrain = False

        file_name_ext = os.path.basename(file)
        file_name = os.path.splitext(file_name_ext)[0].replace("test_", "")

        if args.Oversampling == "none":
            base_name = output_folder+file_name+"_"+args.Algorithm+"_"+args.Norm+"_"+mode
            model_file = "modeling/models/"+file_name+"_"+args.Algorithm+"_"+args.Norm+"_"+mode
        else:
            base_name = output_folder+file_name+"_"+args.Algorithm+"_"+args.Oversampling+"_"+args.Norm+"_"+mode
            model_file = "modeling/models/"+file_name+"_"+args.Algorithm+"_"+args.Oversampling+"_"+args.Norm+"_"+mode

        antibiotics = test_bac.columns.drop(test_bac[test_bac.columns.drop(list(test_bac.filter(regex='[^0-9]')))].columns)

        test_x = test_bac[test_bac.columns.drop(list(test_bac.filter(regex='[^0-9]')))]
        test_y = test_bac[antibiotics].astype(int)

        if retrain:
            train_x = train_bac[train_bac.columns.drop(list(train_bac.filter(regex='[^0-9]')))]
            train_y = train_bac[antibiotics].astype(int)
        else:
            train_x = test_x
            train_y = test_y

        bac_options = ["s_aureus", "p_aeruginosa", "k_pneumoniae", "e_coli"]
        for bac_option in bac_options:
            if bac_option in file_name:
                model_bac = bac_option
        bin_options = ["bin5", "bin20"]
        for bin_option in bin_options:
            if bin_option in file_name:
                model_bin = bin_option
        lc_file_name = "data/processed/"+args.Folder+"/"+args.Oversampling+"/"+args.Norm+"/encoder/"+model_bac+"_driams_"+model_bin+"_encoder.save"
        lc = load(lc_file_name)

        oversampled = args.Oversampling != "none"

        if args.Multilabel == "lps":
            pred = multilabel(train_x, train_y, test_x, args.Algorithm, base_name, model_file, oversampled, retrain=retrain)
        else:
            pred = independent(train_x, train_y, test_x, antibiotics, args.Algorithm, base_name, model_file, oversampled, retrain=retrain)

        print("  Results...")
        metrics_report(test_y, pred, antibiotics, base_name+"_results.txt")
        confusion_matrix(test_y, pred, antibiotics, base_name+"_confusion_matrix.png")                

        # if not os.path.exists(base_name+"_proba.txt"):
        #     print("     Probability prediction...")
        #     if args.Algorithm == "svc" or args.Algorithm == "mlp":
        #         print("To-do")
        #     else:
        #         proba_report(proba, test_y, antibiotics, base_name+"_proba.txt")

        print("Done.\n")

