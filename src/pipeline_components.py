import os
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

ARTIFACTS_DIR = "artifacts"

def step_data_extraction(data_path="data/raw_data.csv"):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    mlflow.log_param("data_path", data_path)

    df = pd.read_csv(data_path)
    extracted_path = os.path.join(ARTIFACTS_DIR, "extracted.csv")
    df.to_csv(extracted_path, index=False)
    mlflow.log_artifact(extracted_path, "data")

    return extracted_path


def step_data_preprocessing(extracted_path):
    df = pd.read_csv(extracted_path)

    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    train_path = os.path.join(ARTIFACTS_DIR, "train.csv")
    test_path = os.path.join(ARTIFACTS_DIR, "test.csv")

    pd.concat([X_train, y_train], axis=1).to_csv(train_path, index=False)
    pd.concat([X_test, y_test], axis=1).to_csv(test_path, index=False)

    mlflow.log_artifact(train_path, "data")
    mlflow.log_artifact(test_path, "data")

    return train_path, test_path


def step_model_training(train_path):
    df = pd.read_csv(train_path)
    X = df.drop(columns=["target"])
    y = df["target"]

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)

    model_path = os.path.join(ARTIFACTS_DIR, "model.joblib")
    joblib.dump(model, model_path)

    mlflow.sklearn.log_model(model, "model")
    mlflow.log_param("n_estimators", 100)

    return model_path


def step_model_evaluation(model_path, test_path):
    model = joblib.load(model_path)
    df = pd.read_csv(test_path)

    X = df.drop(columns=["target"])
    y = df["target"]

    preds = model.predict(X)

    mse = mean_squared_error(y, preds)
    r2 = r2_score(y, preds)

    metrics_path = os.path.join(ARTIFACTS_DIR, "metrics.txt")
    with open(metrics_path, "w") as f:
        f.write(f"MSE: {mse}\nR2: {r2}\n")

    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2", r2)
    mlflow.log_artifact(metrics_path, "metrics")

    return metrics_path
