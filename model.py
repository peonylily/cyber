from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data.csv"
FEATURES = ["phishing_score", "privacy_score", "password_score", "errors"]
LABELS = ["التصيد الإلكتروني", "حماية الخصوصية", "كلمات المرور"]

def train_and_evaluate():
    data = pd.read_csv(DATA_PATH)
    X, y = data[FEATURES], data["recommended_topic"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=47, stratify=y
    )
    model = DecisionTreeClassifier(max_depth=4, min_samples_leaf=4, random_state=47, class_weight="balanced")
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return model, {
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, average="weighted", zero_division=0),
        "recall": recall_score(y_test, pred, average="weighted", zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, pred, labels=LABELS),
        "labels": LABELS, "train_size": len(X_train), "test_size": len(X_test),
        "total_size": len(data)
    }

def predict_topic(model, scores, errors):
    row = pd.DataFrame([{
        "phishing_score": scores["phishing"],
        "privacy_score": scores["privacy"],
        "password_score": scores["password"],
        "errors": errors
    }], columns=FEATURES)
    probabilities = model.predict_proba(row)[0]
    index = probabilities.argmax()
    return model.classes_[index], float(probabilities[index])
