import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# === Step 1: Load Cleaned Dataset ===
X = pd.read_csv("clean//X_cleaned.csv")
y = pd.read_csv("clean//y_cleaned.csv").squeeze()

# === Step 2: Drop overpowered features if any remain ===
X.drop(columns=["TotalScore", "OS_Score", "Browser_Score"], inplace=True, errors='ignore')

# === Step 3: Flip 7% of the labels randomly (simulate real-world errors) ===
np.random.seed(42)
flip_count = int(0.07 * len(y))
flip_indices = np.random.choice(y.index, size=flip_count, replace=False)
y.loc[flip_indices] = 1 - y.loc[flip_indices]

# === Step 4: Train-Test Split ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

# === Step 5: Train Random Forest ===
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=10,
    min_samples_leaf=6,
    max_features='sqrt',
    class_weight='balanced',
    random_state=42
)

model.fit(X_train, y_train)

# === Step 6: Evaluation ===
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred) * 100
precision = precision_score(y_test, y_pred) * 100
recall = recall_score(y_test, y_pred) * 100
f1 = f1_score(y_test, y_pred) * 100

print("🎯 Final Model Performance:")
print(f"✅ Accuracy:  {accuracy:.2f}%")
print(f"✅ Precision: {precision:.2f}%")
print(f"✅ Recall:    {recall:.2f}%")
print(f"✅ F1 Score:  {f1:.2f}%")

# === Step 7: Confusion Matrix ===
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrBr',
            xticklabels=['Denied', 'Approved'],
            yticklabels=['Denied', 'Approved'])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# === Step 8: Save Model ===
joblib.dump(model, "C://dday//zta_rf_model.pkl")
print("✅ Model saved to zta_rf_model.pkl")
