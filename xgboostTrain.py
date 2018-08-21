from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
import pandas as pd
import xgboost as xgb

df_test = pd.read_csv("features.csv")
df_test.drop("Unnamed: 0", axis=1,  inplace=True)

X_train = df_test[["AdjEM", "AdjO", "AdjD", "AdjT", "WLoc"]]
y_train = df_test["Result"]

model = xgb.XGBClassifier()
max_depth = range(1,11, 2)
n_estimators = range(10, 110, 10)
#param_grid = dict(n_estimators=n_estimators)
param_grid = dict(n_estimators=n_estimators, max_depth=max_depth)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
grid_search = GridSearchCV(model, param_grid, scoring="neg_log_loss", n_jobs=-1, cv=kfold, verbose=1)
grid_result = grid_search.fit(X_train, y_train)

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
	print("%f (%f) with: %r" % (mean, stdev, param))
