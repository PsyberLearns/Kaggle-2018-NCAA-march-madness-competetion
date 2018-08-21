#code used to predict and submit xgboost model
import xgboost as xgb
import pandas as pd

df_test = pd.read_csv("SampleSubmissionStage2WithFeatures.csv")
df_features = pd.read_csv("features.csv")
df_features.drop("Unnamed: 0", axis=1, inplace=True)

X_train = df_features[["AdjEM", "AdjO", "AdjD", "AdjT", "WLoc"]]
y_train = df_features["Result"]

X_test = df_test[["AdjEM", "AdjO", "AdjD", "AdjT"]]
X_test["WLoc"] = [0] * 2278

model = xgb.XGBClassifier(n_estimators=90, max_depth=3, objective='reg:logistic')
model.fit(X_train, y_train)
predictions = model.predict_proba(X_test)

df_predict = pd.read_csv("SampleSubmissionStage2.csv")
df_predict["Pred"] = predictions
df_predict.to_csv("realsubmission7.csv", index=False)




