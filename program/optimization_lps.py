
import xgboost as xgb
from sklearn.svm import SVC

from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer

from sklearn.neural_network import MLPClassifier
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.svm import SVC


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
    
    def predit_proba(self, X):
        return self.model.predict_proba(X)

    def score(self, X, y):
        return self.model.score(X, y)