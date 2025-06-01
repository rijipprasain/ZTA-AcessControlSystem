import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# === CONFIGURATION ===
CSV_PATH = "SessionLogs.csv"
OUTPUT_DIR = "clean"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === STEP 1: LOAD DATA ===
df = pd.read_csv(CSV_PATH)

# === STEP 2: DROP DERIVED OR NON-GENERALIZABLE FIELDS ===
df.drop(columns=[
    'SessionID', 'MacAddress', 'DeviceID', 'DeviceSerial', 'userID', 'userRole',
    'DeviceTrustScore', 'IPTrustScore', 'LocationScore',
    'TimeScore', 'GeoVelocityScore', 'GeoVelocityFlag',
    'AccessTrustScore', 'keyDynamicScore', 'OS_Score', 'Browser_Score', 'TotalScore',
    'VulnerableIPAddress', 'ISP', 'VPNStatus', 'UserDepartment'
], inplace=True, errors='ignore')

# === STEP 3: ENCODE CATEGORICAL FIELDS AND SAVE ENCODERS ===
feature_encoders = {}
for col in df.select_dtypes(include='object').columns:
    if col != 'AccessDecision':  # Target will be handled separately
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        feature_encoders[col] = le

# Save feature encoders
joblib.dump(feature_encoders, os.path.join(OUTPUT_DIR, "feature_label_encoders.pkl"))
print("✅ Feature label encoders saved.")

# === STEP 4: INJECT NOISE INTO BIOMETRIC COLUMNS ===
def add_noise(df, column, pct=0.10):
    noise = np.random.normal(0, df[column].std() * pct, size=df.shape[0])
    df[column] = df[column] + noise
    return df

for col in ['userTypingSpeed', 'userKeyHold', 'userFlightTime']:
    df = add_noise(df, col)

# === STEP 5: ENCODE TARGET LABEL AND SAVE ENCODER ===
target_encoder = LabelEncoder()
df['AccessDecision'] = target_encoder.fit_transform(df['AccessDecision'])
joblib.dump(target_encoder, os.path.join(OUTPUT_DIR, "target_label_encoder.pkl"))
print("✅ Target label encoder saved.")

# === STEP 6: SPLIT FEATURES AND LABELS ===
X = df.drop(columns=['AccessDecision'])
y = df['AccessDecision']

# === STEP 7: SAVE OUTPUT ===
X.to_csv(os.path.join(OUTPUT_DIR, "X_cleaned.csv"), index=False)
y.to_csv(os.path.join(OUTPUT_DIR, "y_cleaned.csv"), index=False)

print("✅ Cleaned dataset saved with noise added to biometric columns.")
print(f"🧪 Features: {X.shape[1]} columns")
print(f"🎯 Samples: {X.shape[0]} rows")
