
import xgboost as xgb
from sklearn.svm import SVC

from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer

from sklearn.neural_network import MLPClassifier
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.svm import SVC



def optimize_xgb(n_cv, n_iter):
    bayesopt = BayesSearchCV(
            xgb.XGBClassifier(),
            {
                "objective": Categorical(["binary:logistic"]),
                "max_depth": Integer(1, 10),
                "min_child_weight": Real(1e-6, 10, prior="log-uniform"),
                "max_delta_step": Real(1e-6, 10, prior="log-uniform"),
                "subsample": Real(1e-6, 1, prior="log-uniform"),
                "tree_method": Categorical(["exact", "approx", "hist"]),
                "gamma": Real(1e-6, 10, prior="log-uniform"),
                "eta": Real(1e-6, 1, prior="log-uniform")
            },
            n_iter=n_iter,
            cv=n_cv,
            random_state=0,
            n_jobs=10,
            n_points=2,
            verbose=1
    )
    return bayesopt


def optimize_svc(n_cv, n_iter):
    bayesopt = BayesSearchCV(
        SVC(),
        {
            "C": Real(1e-6, 1000, prior="log-uniform"),
            "kernel": Categorical(["rbf"]),
            "gamma": Real(1e-6, 1000, prior="log-uniform"),
        },
        n_iter=n_iter,
        cv=n_cv,
        random_state=0,
        n_jobs=10,
        n_points=2,
        verbose=1
    )
    return bayesopt


def optimize_rf(n_cv, n_iter):
    bayesopt = BayesSearchCV(
        RandomForestClassifier(),
        {
            "n_estimators": Integer(1, 1000),
            "max_depth": Integer(1, 10),
            "min_samples_leaf": Integer(1, 10),
            "bootstrap": Categorical([False, True]),
            "random_state": Categorical([0])
        },
        n_iter=n_iter,
        cv=n_cv,
        random_state=0,
        n_jobs=10,
        n_points=2,
        verbose=1
    )
    return bayesopt


class MLPWrapper(BaseEstimator, ClassifierMixin):
    def __init__(
        self,
        activation="relu", 
        solver="adam", 
        alpha=0.0001, 
        learning_rate="constant",
        max_iter=1200, 
        random_state=0,
        layer1=10, 
        layer2=10, 
        layer3=10
    ):
        self.layer1 = layer1
        self.layer2 = layer2
        self.layer3 = layer3
        self.activation = activation
        self.solver = solver
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.random_state = random_state
        

    def fit(self, X, y):
        model = MLPClassifier(
            hidden_layer_sizes=[self.layer1, self.layer2, self.layer3],
            activation = self.activation,
            solver = self.solver,
            alpha = self.alpha,
            learning_rate = self.learning_rate,
            max_iter = self.max_iter,
            random_state = self.random_state
        )
        model.fit(X, y)
        self.model = model
        return self

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        return self.model.score(X, y)
    
    
def optimize_mlp(n_cv, n_iter):
    bayesopt = BayesSearchCV(
        MLPWrapper(),
        {
            "activation": Categorical(["identity", "logistic", "tanh", "relu"]),
            "solver": Categorical(["sgd", "adam"]),
            "alpha": Real(1e-6, 1e-2, prior="log-uniform"),
            "learning_rate": Categorical(["constant", "invscaling", "adaptive"]),
            "layer1": Integer(10, 500),
            "layer2": Integer(10, 500),
            "layer3": Integer(10, 500)
        },
        n_iter=n_iter,
        cv=n_cv,
        random_state=0,
        n_jobs=5,
        n_points=2,
        verbose=1
    )
    
    return bayesopt