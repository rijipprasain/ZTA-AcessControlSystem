import csv
import random
import datetime

# === Configuration ===
NUM_SESSIONS = 25000
TRUSTED_FILE = 'C://Final DataSet//trustedComputers.csv'
FINAL_SESSION_LOG_FILE = 'C://Final DataSet//SessionLogs.csv'

CITIES = [
    'Sydney', 'Melbourne', 'Brisbane', 'Adelaide', 'Perth',
    'Canberra', 'Hobart', 'Darwin', 'Newcastle', 'Wollongong'
]

TRAVEL_TIME = {
    'Sydney': {'Melbourne': 10, 'Brisbane': 10, 'Adelaide': 14, 'Perth': 20, 'Canberra': 4, 'Hobart': 12, 'Darwin': 18, 'Newcastle': 2, 'Wollongong': 2},
    'Melbourne': {'Sydney': 10, 'Brisbane': 15, 'Adelaide': 8, 'Perth': 18, 'Canberra': 7, 'Hobart': 9, 'Darwin': 20, 'Newcastle': 11, 'Wollongong': 11},
    'Brisbane': {'Sydney': 10, 'Melbourne': 15, 'Adelaide': 17, 'Perth': 22, 'Canberra': 12, 'Hobart': 18, 'Darwin': 15, 'Newcastle': 9, 'Wollongong': 9},
    'Adelaide': {'Sydney': 14, 'Melbourne': 8, 'Brisbane': 17, 'Perth': 15, 'Canberra': 13, 'Hobart': 12, 'Darwin': 16, 'Newcastle': 13, 'Wollongong': 13},
    'Perth': {'Sydney': 20, 'Melbourne': 18, 'Brisbane': 22, 'Adelaide': 15, 'Canberra': 19, 'Hobart': 21, 'Darwin': 12, 'Newcastle': 21, 'Wollongong': 21},
    'Canberra': {'Sydney': 4, 'Melbourne': 7, 'Brisbane': 12, 'Adelaide': 13, 'Perth': 19, 'Hobart': 11, 'Darwin': 16, 'Newcastle': 4, 'Wollongong': 3},
    'Hobart': {'Sydney': 12, 'Melbourne': 9, 'Brisbane': 18, 'Adelaide': 12, 'Perth': 21, 'Canberra': 11, 'Darwin': 24, 'Newcastle': 13, 'Wollongong': 13},
    'Darwin': {'Sydney': 18, 'Melbourne': 20, 'Brisbane': 15, 'Adelaide': 16, 'Perth': 12, 'Canberra': 16, 'Hobart': 24, 'Newcastle': 17, 'Wollongong': 17},
    'Newcastle': {'Sydney': 2, 'Melbourne': 11, 'Brisbane': 9, 'Adelaide': 13, 'Perth': 21, 'Canberra': 4, 'Hobart': 13, 'Darwin': 17, 'Wollongong': 3},
    'Wollongong': {'Sydney': 2, 'Melbourne': 11, 'Brisbane': 9, 'Adelaide': 13, 'Perth': 21, 'Canberra': 3, 'Hobart': 13, 'Darwin': 17, 'Newcastle': 3}
}
# === Ideal Keystroke Dynamics by Role (in milliseconds) ===
IDEAL_KEY_DYNAMICS = {
    "Admin": {"typing_speed_wpm": 65, "key_hold_ms": 100, "flight_time_ms": 85},
    "HOD": {"typing_speed_wpm": 60, "key_hold_ms": 95, "flight_time_ms": 90},
    "Finance": {"typing_speed_wpm": 70, "key_hold_ms": 105, "flight_time_ms": 95},
    "Professor": {"typing_speed_wpm": 68, "key_hold_ms": 98, "flight_time_ms": 92},
    "HR": {"typing_speed_wpm": 63, "key_hold_ms": 102, "flight_time_ms": 90},
    "Student": {"typing_speed_wpm": 55, "key_hold_ms": 90, "flight_time_ms": 80},
    "Receptionist": {"typing_speed_wpm": 72, "key_hold_ms": 110, "flight_time_ms": 98}
}

# === Pattern Match Distribution ===
PATTERN_MATCH_TYPES = [
    ("Full Match", 0.50),
    ("Partial Match", 0.30),
    ("No Match", 0.20)
]
# === Ideal Keystroke Dynamics by Role (in milliseconds) ===
IDEAL_KEY_DYNAMICS = {
    "Admin": {"typing_speed_wpm": 65, "key_hold_ms": 100, "flight_time_ms": 85},
    "HOD": {"typing_speed_wpm": 60, "key_hold_ms": 95, "flight_time_ms": 90},
    "Finance": {"typing_speed_wpm": 70, "key_hold_ms": 105, "flight_time_ms": 95},
    "Professor": {"typing_speed_wpm": 68, "key_hold_ms": 98, "flight_time_ms": 92},
    "HR": {"typing_speed_wpm": 63, "key_hold_ms": 102, "flight_time_ms": 90},
    "Student": {"typing_speed_wpm": 55, "key_hold_ms": 90, "flight_time_ms": 80},
    "Receptionist": {"typing_speed_wpm": 72, "key_hold_ms": 110, "flight_time_ms": 98}
}

# === User Roles with Weights ===
USER_ROLES = [
    ("Admin", 0.05),
    ("HOD", 0.05),
    ("Finance", 0.10),
    ("Professor", 0.20),
    ("HR", 0.10),
    ("Student", 0.40),
    ("Receptionist", 0.10)
]

# === Operation Types with Weights ===
OPERATION_TYPES = [
    ("Read", 0.50),
    ("Write", 0.166),
    ("Update", 0.166),
    ("Delete", 0.166)
]
# === Load Trusted Devices ===
def load_trusted_devices(filename):
    trusted_devices = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mac = row['MacAddress']
            trusted_devices[mac] = {
                'DeviceID': row['DeviceID'],
                'DeviceSerial': row['DeviceSerial'],
                'OwnershipType': row['OwnershipType']
            }
    return trusted_devices

# === Generate Random MAC Address ===
def generate_mac():
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

# === Generate Device Section Entries ===
def generate_device_section(trusted_devices):
    trusted_macs = list(trusted_devices.keys())
    num_trusted = random.randint(int(NUM_SESSIONS * 0.9), int(NUM_SESSIONS * 0.95))
    num_random = NUM_SESSIONS - num_trusted
    entries = []
    sampled_trusted_macs = random.sample(trusted_macs, min(num_trusted, len(trusted_macs)))
    for mac in sampled_trusted_macs:
        device = trusted_devices[mac]
        trust_level = "companyOwned" if device['OwnershipType'] == 'Company' else "personalOwned"
        trust_score = 20 if trust_level == "companyOwned" else 15
        entries.append({
            'MacAddress': mac,
            'DeviceID': device['DeviceID'],
            'DeviceSerial': device['DeviceSerial'],
            'DeviceTrustLevel': trust_level,
            'DeviceTrustScore': trust_score
        })
    for _ in range(num_random):
        mac = generate_mac()
        while mac in trusted_devices:
            mac = generate_mac()
        entries.append({
            'MacAddress': mac,
            'DeviceID': "Unknown",
            'DeviceSerial': "Unknown",
            'DeviceTrustLevel': "Unknown",
            'DeviceTrustScore': 10
        })
    random.shuffle(entries)
    return entries

# === Generate IP Section Entries ===
def generate_ip_section():
    ip_entries = []

    # List of external/random ISPs
    isps = ['Telstra', 'Optus', 'Vodafone', 'iiNet', 'TPG', 'AussieBB', 'Exetel', 'MyRepublic', 'Dodo', 'Internode']

    def get_random_isp(company=True):
        return "CompanyISP" if company else f"{random.choice(isps)} (external)"

    # Distribution based on your new percentages
    num_internal_no_vpn = int(NUM_SESSIONS * 0.45)   # 45%
    num_internal_with_vpn = int(NUM_SESSIONS * 0.05) # 5%
    num_external_with_vpn = int(NUM_SESSIONS * 0.45) # 45%
    num_direct_external = NUM_SESSIONS - (num_internal_no_vpn + num_internal_with_vpn + num_external_with_vpn)  # ~5%

    # 1. Internal Company Network (No VPN)
    for _ in range(num_internal_no_vpn):
        ip = f"172.169.{random.randint(0, 255)}.{random.randint(0, 255)}"
        ip_entries.append({
            'IPAddress': ip,
            'VPNStatus': "No",
            'ISP': get_random_isp(company=True),
            'VulnerableIPAddress': False,
            'IPTrustScore': 20
        })

    # 2. Internal but using CompanyVPN (mistakenly)
    for _ in range(num_internal_with_vpn):
        ip = f"169.169.{random.randint(0, 255)}.{random.randint(0, 255)}"
        ip_entries.append({
            'IPAddress': ip,
            'VPNStatus': "Yes",
            'ISP': get_random_isp(company=True),
            'VulnerableIPAddress': False,
            'IPTrustScore': 20
        })

    # 3. External ISP using CompanyVPN
    for _ in range(num_external_with_vpn):
        ip = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
        ip_entries.append({
            'IPAddress': ip,
            'VPNStatus': "Yes",
            'ISP': get_random_isp(company=False),
            'VulnerableIPAddress': False,
            'IPTrustScore': 15
        })

    # 4. Direct connection from unknown/random ISP (No VPN)
    for _ in range(num_direct_external):
        ip = f"{random.randint(1, 250)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        ip_entries.append({
            'IPAddress': ip,
            'VPNStatus': "No",
            'ISP': get_random_isp(company=False),
            'VulnerableIPAddress': False,
            'IPTrustScore': 5
        })

    random.shuffle(ip_entries)
    return ip_entries

# === Generate Location Section with Sydney Bias ===
def generate_location_section():
    entries = []

    valid_login_start_hour = 6   # 6:00 AM
    valid_login_end_hour = 23    # 11:59 PM

    for _ in range(NUM_SESSIONS):
        base_date = datetime.datetime(2025, random.randint(1, 12), random.randint(1, 28))

        is_valid_time = random.random() < 0.90

        prev_day_offset = random.randint(0, 1)
        prev_time = base_date + datetime.timedelta(days=prev_day_offset)

        if is_valid_time:
            prev_hour = random.randint(valid_login_start_hour, 20)
        else:
            prev_hour = random.randint(0, valid_login_start_hour - 1)

        prev_minute = random.randint(0, 59)
        prev_time = prev_time.replace(hour=prev_hour, minute=prev_minute)

        curr_time = prev_time + datetime.timedelta(
            hours=random.randint(1, 4),
            minutes=random.randint(0, 59)
        )

        prev_str = prev_time.strftime("%Y-%m-%d %I:%M %p")
        curr_str = curr_time.strftime("%Y-%m-%d %I:%M %p")

        # 80% chance user is from Sydney
        if random.random() < 0.8:
            user_location = 'Sydney'
        else:
            user_location = random.choice(CITIES[1:])  # Other cities

        # 70% chance access location is Sydney
        def weighted_city_choice():
            return 'Sydney' if random.random() < 0.7 else random.choice(CITIES[1:])

        pal = weighted_city_choice()
        cal = weighted_city_choice()

        travel_time = TRAVEL_TIME.get(pal, {}).get(cal, float('inf'))
        hours_diff = (curr_time - prev_time).total_seconds() / 3600

        time_score = 10 if valid_login_start_hour <= curr_time.hour <= valid_login_end_hour else 0

        geo_velocity_flag = False
        geo_velocity_score = 10
        if pal != cal and travel_time > hours_diff + 2:
            geo_velocity_flag = True
            geo_velocity_score = 0

        location_score = time_score + geo_velocity_score

        entries.append({
            "CurrentAccessTime": curr_str,
            "UserLocation": user_location,
            "CurrentAccessLocation": cal,
            "PreviousAccessTime": prev_str,
            "PreviousAccessLocation": pal,
            "TimeScore": time_score,
            "GeoVelocityScore": geo_velocity_score,
            "GeoVelocityFlag": geo_velocity_flag,
            "LocationScore": location_score
        })

    return entries

# === Generate Access Medium Section with Realistic Browser Versions ===
def generate_access_medium_section():
    entries = []

    # OS distribution weights
    os_choices = [
        ('Windows', 0.25),
        ('macOS', 0.40),
        ('Linux', 0.15),
        ('Android', 0.15),
        ('iOS', 0.05)
    ]

    # OS version mapping (latest first)
    os_versions = {
        'Windows': ['11', '10 22H2', '10 20H2', '8', '7'],
        'macOS': ['Sonoma 14', 'Ventura 13', 'Monterey 12', 'Big Sur 11', 'Catalina 10.15'],
        'Linux': ['24.04 LTS', '22.04 LTS', '20.04 LTS', '18.04 LTS', '16.04 LTS'],
        'Android': ['14', '13', '12', '11', '10'],
        'iOS': ['18','17', '16', '15', '14',]
    }

    # Browser version mapping
    browser_versions = {
        'Chrome': ['ver130', 'ver129', 'ver128', 'ver127', 'ver126'],
        'Edge': ['ver40', 'ver39', 'ver38', 'ver37', 'ver36'],
        'Safari': ['18.0', '17.6', '17.5', '17.4', '17.3'],
        'Firefox': ['ver20', 'ver19', 'ver18', 'ver17', 'ver16'],
        'Brave': ['90.9','90.8','90.7','90.6','90.5']
    }

    # Browser distribution
    browser_choices = [
        ('Chrome', 0.40),
        ('Edge', 0.10),
        ('Safari', 0.30),
        ('Firefox', 0.15),
        ('Brave', 0.05)
    ]

    for _ in range(NUM_SESSIONS):
        # === OS Selection ===
        os_choice = random.choices(
            population=[x[0] for x in os_choices],
            weights=[x[1] for x in os_choices],
            k=1
        )[0]

        versions = os_versions[os_choice]
        # 70% chance to pick among first 3 versions
        os_version_weights = [0.4, 0.2, 0.1, 0.15, 0.15]
        os_version = random.choices(versions, weights=os_version_weights, k=1)[0]
        os_index = versions.index(os_version)
        os_score = 10 if os_index <= 3 else 5

        # === Browser Selection ===
        browser = random.choices(
            population=[x[0] for x in browser_choices],
            weights=[x[1] for x in browser_choices],
            k=1
        )[0]

        br_versions = browser_versions[browser]
        # 70% chance to pick among first 3 versions
        br_version_weights = [0.4, 0.2, 0.1, 0.15, 0.15]
        browser_version = random.choices(br_versions, weights=br_version_weights, k=1)[0]
        br_index = br_versions.index(browser_version)
        browser_score = 10 if br_index <= 4 else 5

        access_trust_score = os_score + browser_score

        entries.append({
            "OS": os_choice,
            "OS_Version": os_version,
            "OS_Score": os_score,
            "Browser": browser,
            "Browser_Version": browser_version,
            "Browser_Score": browser_score,
            "AccessTrustScore": access_trust_score
        })

    return entries

#=== Useer Behavior Logs ===
def generate_user_behaviour_section():
    entries = []

    for _ in range(NUM_SESSIONS):
        # Generate userID
        user_id = f"u{random.randint(1001, 9999)}"

        # Choose user role based on weights
        role = random.choices(
            population=[r[0] for r in USER_ROLES],
            weights=[r[1] for r in USER_ROLES],
            k=1
        )[0]

        # Get ideal values for the selected role
        ideal = IDEAL_KEY_DYNAMICS[role]

        # Decide pattern match type
        match_type = random.choices(
            population=[m[0] for m in PATTERN_MATCH_TYPES],
            weights=[m[1] for m in PATTERN_MATCH_TYPES],
            k=1
        )[0]

        # Generate realistic behavior based on match type
        if match_type == "Full Match":
            typing_speed_wpm = round(random.uniform(ideal["typing_speed_wpm"] * 0.95, ideal["typing_speed_wpm"] * 1.05))
            key_hold_ms = round(random.uniform(ideal["key_hold_ms"] * 0.95, ideal["key_hold_ms"] * 1.05))
            flight_time_ms = round(random.uniform(ideal["flight_time_ms"] * 0.95, ideal["flight_time_ms"] * 1.05))
        elif match_type == "Partial Match":
            typing_speed_wpm = round(random.uniform(ideal["typing_speed_wpm"] * 0.85, ideal["typing_speed_wpm"] * 1.15))
            key_hold_ms = round(random.uniform(ideal["key_hold_ms"] * 0.85, ideal["key_hold_ms"] * 1.15))
            flight_time_ms = round(random.uniform(ideal["flight_time_ms"] * 0.85, ideal["flight_time_ms"] * 1.15))
        else:  # No Match
            typing_speed_wpm = random.randint(60, 99)
            key_hold_ms = random.randint(70, 110)
            flight_time_ms = random.randint(60, 110)

        # Determine score based on match type
        if match_type == "Full Match":
            key_dynamic_score = 20
        elif match_type == "Partial Match":
            key_dynamic_score = 15
        else:
            key_dynamic_score = 10

        entries.append({
            "userID": user_id,
            "userRole": role,
            "userTypingSpeed": typing_speed_wpm,
            "userKeyHold": key_hold_ms,
            "userFlightTime": flight_time_ms,
            "patternMatch": match_type,
            "keyDynamicScore": key_dynamic_score
        })

    return entries
# Decision Factor 
def generate_decision_factor_section(all_sections_data):
    entries = []
    for entry in all_sections_data:
        user_id = entry.get("userID", "u0000")

        # Generate SessionID
        random_suffix = ''.join(random.choices("xkbrgdmlwzyhnafjecisuoqpvt", k=12))
        session_id = f"{user_id + random_suffix}"

        # OperationType
        operation_type = random.choices(
            ["Read", "Write", "Update", "Delete"],
            weights=[0.5, 0.1666, 0.1666, 0.1668],
            k=1
        )[0]

        # Get Scores
        device_score = entry.get("DeviceTrustScore", 0)
        ip_score = entry.get("IPTrustScore", 0)
        location_score = entry.get("FinalLocationScore", 0)
        key_score = entry.get("keyDynamicScore", 0)
        access_score = entry.get("AccessTrustScore", 0)

        total_score = device_score + ip_score + location_score + key_score + access_score
        access_decision = "Approved" if total_score >= 75 else "Denied"

        entries.append({
            "SessionID": session_id,
            "OperationType": operation_type,
            "AccessDecision": access_decision,
            f"{"TotalScore"},Appproved when > 75": total_score,
        })

    return entries
# === Generate Final Session Logs ===
def generate_final_session_logs():
    trusted_devices = load_trusted_devices(TRUSTED_FILE)
    device_entries = generate_device_section(trusted_devices)
    ip_entries = generate_ip_section()
    location_entries = generate_location_section()
    access_medium_entries = generate_access_medium_section()
    user_behaviour_entries = generate_user_behaviour_section()

    # Merge all data
    final_entries = []
    for dev, ip, loc, acc_med, beh in zip(device_entries, ip_entries, location_entries, access_medium_entries, user_behaviour_entries):
        merged = {**dev, **ip, **loc, **acc_med, **beh}
        final_entries.append(merged)

    # Now generate Decision Factor using full merged data
    decision_factor_entries = generate_decision_factor_section(final_entries)

    # Final merge with DecisionFactor
    output_entries = []
    for entry, dec in zip(final_entries, decision_factor_entries):
        output_entry = {**entry, **dec}
        output_entries.append(output_entry)

    # Write to CSV
    with open(FINAL_SESSION_LOG_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=output_entries[0].keys())
        writer.writeheader()
        writer.writerows(output_entries)

    print(f"{NUM_SESSIONS} session logs written to {FINAL_SESSION_LOG_FILE}")
# === Run ===
if __name__ == "__main__":
    generate_final_session_logs()