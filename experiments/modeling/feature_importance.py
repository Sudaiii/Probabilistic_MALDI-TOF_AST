import os
import shap
import numpy as np
import matplotlib.pyplot as plt

SAMPLES = 100


def feature_importance(model, train_features, train_labels, test_features, algorithm, output_file):
    train_sample = shap.sample(train_features, SAMPLES, random_state=0)
    test_sample = shap.sample(test_features, SAMPLES, random_state=0)
    if not os.path.exists(output_file+"_shap.txt.npy"):
        if algorithm == "svc" or algorithm == "mlp":
            if algorithm == "svc":
                model.probability=True
                model.fit(train_features, train_labels)
                explainer = shap.KernelExplainer(model.predict_proba, train_sample)
            elif algorithm == "mlp":
                model.fit(train_features, train_labels)
                explainer = shap.KernelExplainer(model.predict, train_sample)
            shap_values = explainer.shap_values(test_sample)
        elif algorithm == "xgb" or algorithm == "rf":
            explainer = shap.TreeExplainer(model)
            explanation = explainer(test_sample)
            shap_values = explanation.values
        np.save(output_file+"_shap.txt", shap_values)

    if not os.path.exists(output_file+"_shap_summary.png"):
        shap_values = np.load(output_file+"_shap.txt.npy")
        plt.clf()
        shap.summary_plot(shap_values, test_sample)
        plt.savefig(output_file+"_shap_summary.png",dpi=150, bbox_inches='tight')
        plt.clf()