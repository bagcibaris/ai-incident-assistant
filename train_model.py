import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib


df = pd.read_csv("logs_dataset.csv")

df["input_text"] = (
    df["error_type"].astype(str) + " " +
    df["severity"].astype(str) + " " +
    df["description"].astype(str) + " " +
    df["probable_cause"].astype(str) + " " +
    df["suggested_action"].astype(str)
)

X = df["input_text"]
y = df["layer"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Model accuracy:", accuracy)

print("\nClassification report:")
print(classification_report(y_test, y_pred, zero_division=0))

joblib.dump(model, "models/layer_classifier_model.pkl")

print("\nModel saved to models/layer_classifier_model.pkl")
