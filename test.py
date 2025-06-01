import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import os

# === Load model and encoders ===
model = joblib.load("C://dday//zta_rf_model.pkl")
label_encoders = joblib.load("C://dday//clean//feature_label_encoders.pkl")
target_encoder = joblib.load("C://dday//clean//target_label_encoder.pkl")

# === Travel Time Matrix ===
TRAVEL_TIME = {
    'sydney': {'melbourne': 10, 'brisbane': 10, 'adelaide': 14, 'perth': 20, 'canberra': 4, 'hobart': 12, 'darwin': 18, 'newcastle': 2, 'wollongong': 2},
    'melbourne': {'sydney': 10, 'brisbane': 15, 'adelaide': 8, 'perth': 18, 'canberra': 7, 'hobart': 9, 'darwin': 20, 'newcastle': 11, 'wollongong': 11},
    'brisbane': {'sydney': 10, 'melbourne': 15, 'adelaide': 17, 'perth': 22, 'canberra': 12, 'hobart': 18, 'darwin': 15, 'newcastle': 9, 'wollongong': 9},
    'adelaide': {'sydney': 14, 'melbourne': 8, 'brisbane': 17, 'perth': 15, 'canberra': 13, 'hobart': 12, 'darwin': 16, 'newcastle': 13, 'wollongong': 13},
    'perth': {'sydney': 20, 'melbourne': 18, 'brisbane': 22, 'adelaide': 15, 'canberra': 19, 'hobart': 21, 'darwin': 12, 'newcastle': 21, 'wollongong': 21},
    'canberra': {'sydney': 4, 'melbourne': 7, 'brisbane': 12, 'adelaide': 13, 'perth': 19, 'hobart': 11, 'darwin': 16, 'newcastle': 4, 'wollongong': 3},
    'hobart': {'sydney': 12, 'melbourne': 9, 'brisbane': 18, 'adelaide': 12, 'perth': 21, 'canberra': 11, 'darwin': 24, 'newcastle': 13, 'wollongong': 13},
    'darwin': {'sydney': 18, 'melbourne': 20, 'brisbane': 15, 'adelaide': 16, 'perth': 12, 'canberra': 16, 'hobart': 24, 'newcastle': 17, 'wollongong': 17},
    'newcastle': {'sydney': 2, 'melbourne': 11, 'brisbane': 9, 'adelaide': 13, 'perth': 21, 'canberra': 4, 'hobart': 13, 'darwin': 17, 'wollongong': 3},
    'wollongong': {'sydney': 2, 'melbourne': 11, 'brisbane': 9, 'adelaide': 13, 'perth': 21, 'canberra': 3, 'hobart': 13, 'darwin': 17, 'newcastle': 3}
}

# === Enhanced CLI ===
print("\n✨ Welcome to the Secure Access Evaluator ✨")
print("🔐 Let's determine if your session is trustworthy...\n")

total_score = 0

# === MAC Address Input ===
mac = input("📥 Enter MAC Address: ")
path = "trustedComputers.csv"
if not os.path.exists(path):
    print("🚫 trustedComputers.csv not found! Defaulting device trust to UNKNOWN.")
    device_type, device_score = 'unknown', 10
else:
    df = pd.read_csv(path, dtype=str)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '')
    mac_col = next((col for col in df.columns if 'mac' in col), None)
    owner_col = next((col for col in df.columns if 'owner' in col), None)
    if mac_col and owner_col:
        df[mac_col] = df[mac_col].str.strip().str.lower()
        df[owner_col] = df[owner_col].str.strip().str.lower()
        mac_clean = mac.strip().lower()
        match = df[df[mac_col] == mac_clean]
        if not match.empty:
            owner = match.iloc[0][owner_col]
            device_type, device_score = ('companyOwned', 20) if owner == 'company' else ('personalOwned', 15)
        else:
            device_type, device_score = 'unknown', 10
    else:
        device_type, device_score = 'unknown', 10
print(f"📦 Device Trust: {device_type.upper()} → Score: {device_score}/20")
total_score += device_score
print(f"📊 Cumulative Score: {total_score}/100\n")

# === IP Input ===
ip = input("🌐 Enter IP Address: ")
if ip.startswith("172.169"): ip_score, vpn, isp = 20, "No", "CompanyISP"
elif ip.startswith("169.169"): ip_score, vpn, isp = 20, "Yes", "CompanyISP"
elif ip.startswith("192.168"): ip_score, vpn, isp = 15, "Yes", "ExternalISP"
else: ip_score, vpn, isp = 5, "No", "ExternalISP"
print(f"📶 IP Trust: ISP={isp}, VPN={vpn} → Score: {ip_score}/20")
total_score += ip_score
print(f"📊 Cumulative Score: {total_score}/100\n")

# === Time and Location ===
prev_time = input("🕓 Enter Previous Access Time (YYYY-MM-DD HH:MM): ")
curr_time = input("🕓 Enter Current Access Time (YYYY-MM-DD HH:MM): ")
prev_loc = input("🌍 Previous Location: ").lower()
curr_loc = input("🌍 Current Location: ").lower()

# Time reasoning
curr_hour = pd.to_datetime(curr_time).hour
if 6 <= curr_hour <= 23:
    time_reason = f"Access occurred at {curr_hour}:00, which is within the normal working window (6 AM - 11 PM)."
    time_score = 10
else:
    time_reason = f"Access occurred at {curr_hour}:00, which is outside the usual trusted window (6 AM - 11 PM)."
    time_score = 0

# Geo reasoning
travel_hours = (pd.to_datetime(curr_time) - pd.to_datetime(prev_time)).total_seconds() / 3600
expected_time = TRAVEL_TIME.get(prev_loc, {}).get(curr_loc, 999)
if prev_loc != curr_loc and expected_time > travel_hours + 2:
    geo_score = 0
    geo_reason = f"It typically takes {expected_time} hours to travel from {prev_loc.title()} to {curr_loc.title()}, but only {travel_hours:.2f} hours passed."
else:
    geo_score = 10
    geo_reason = f"Travel duration of {travel_hours:.2f} hours is feasible between {prev_loc.title()} and {curr_loc.title()} (expected ≈ {expected_time} hrs)."

location_score = time_score + geo_score
print(f"🕒 Time Reasoning: {time_reason} → TimeScore: {time_score}/10")
print(f"📍 Location Reasoning: {geo_reason} → GeoScore: {geo_score}/10")
print(f"📦 Total Location+Time Score: {location_score}/20")
total_score += location_score
print(f"📊 Cumulative Score: {total_score}/100\n")

# === OS and Browser ===
os = input("💻 Operating System: ")
os_ver = input("🧩 OS Version: ")
browser = input("🌐 Browser: ")
browser_ver = input("🧩 Browser Version: ")

OS_SCORES = {
    'windows': ['11', '10 22h2', '10 20h2', '8', '7'],
    'macos': ['sonoma 14', 'ventura 13', 'monterey 12', 'big sur 11', 'catalina 10.15'],
    'linux': ['24.04 lts', '22.04 lts', '20.04 lts', '18.04 lts', '16.04 lts'],
    'android': ['14', '13', '12', '11', '10'],
    'ios': ['18', '17', '16', '15', '14']
}

BROWSER_SCORES = {
    'chrome': ['ver130', 'ver129', 'ver128', 'ver127', 'ver126'],
    'edge': ['ver40', 'ver39', 'ver38', 'ver37', 'ver36'],
    'safari': ['18.0', '17.6', '17.5', '17.4', '17.3'],
    'firefox': ['ver20', 'ver19', 'ver18', 'ver17', 'ver16'],
    'brave': ['90.9','90.8','90.7','90.6','90.5']
}

os_score = 10 if os_ver.lower() in OS_SCORES.get(os.lower(), []) else 5
br_score = 10 if browser_ver.lower() in BROWSER_SCORES.get(browser.lower(), []) else 5
access_score = os_score + br_score
print(f"🖥️ Platform Trust: OS Score = {os_score}/10, Browser Score = {br_score}/10 → Total = {access_score}/20")
total_score += access_score
print(f"📊 Cumulative Score: {total_score}/100\n")

# === User Behavior ===
typing = int(input("⌨️ Typing Speed (WPM): "))
hold = int(input("🔡 Key Hold Time (ms): "))
flight = int(input("🕹️ Flight Time (ms): "))

if 60 <= typing <= 75 and 95 <= hold <= 110 and 85 <= flight <= 100:
    key_score, pattern = 20, "full match"
elif 50 <= typing <= 85 and 85 <= hold <= 120 and 80 <= flight <= 110:
    key_score, pattern = 15, "partial match"
else:
    key_score, pattern = 10, "no match"

print(f"🧠 Behavior Score: Pattern Match = {pattern.upper()} → Score: {key_score}/20")
total_score += key_score
print(f"📊 Cumulative Score: {total_score}/100\n")

# === Final Decision ===
threshold = 75
final_decision = "✅ ACCESS GRANTED" if total_score >= threshold else "⛔ ACCESS DENIED"
print(f"🎯 FINAL DECISION: {final_decision}")
