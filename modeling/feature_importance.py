import shap
import numpy as np

SAMPLES = 100


def feature_importance(model, train_features, train_labels, test_features, algorithm, output_file):
    if algorithm == "svc":
        model.probability=True
        model.fit(train_features, train_labels)
        explainer = shap.KernelExplainer(model.predict_proba, shap.sample(train_features, SAMPLES))
        shap_values = explainer.shap_values(shap.sample(test_features, SAMPLES))

        np.save(output_file, shap_values)