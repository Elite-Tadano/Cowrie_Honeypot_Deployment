import re
import os
import json
from collections import Counter
from datetime import datetime
from visual_report import generate_visual_report

LOG_PATH = "/home/cowrie/cowrie.log"  # Adjust path as needed
REPORT_PATH = "output/attack_report.json"

def parse_log():
    if not os.path.exists(LOG_PATH):
        raise FileNotFoundError(f"Log file not found: {LOG_PATH}")

    ip_counter = Counter()
    command_counter = Counter()
    successful_logins = set()

    with open(LOG_PATH, 'r') as log:
        for line in log:
            # Count IPs
            ip_match = re.search(r'New connection: ([\d.]+):', line)
            if ip_match:
                ip_counter[ip_match.group(1)] += 1

            # Successful login
            if "login attempt" in line and "succeeded" in line:
                ip = extract_ip(line)
                if ip:
                    successful_logins.add(ip)

            # Extract commands
            cmd_match = re.search(r"CMD: (.+)", line)
            if cmd_match:
                command = cmd_match.group(1).strip()
                command_counter[command] += 1

    report = {
        "top_ips": ip_counter.most_common(10),
        "successful_logins": list(successful_logins),
        "top_commands": command_counter.most_common(10),
        "total_commands": sum(command_counter.values()),
        "total_sessions": sum(ip_counter.values()),
        "generated_at": datetime.now().isoformat()
    }

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2)

    return report, list(ip_counter.keys())

def extract_ip(line):
    ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
    return ip_match.group(1) if ip_match else None

if __name__ == "__main__":
    print("[*] Parsing plaintext Cowrie log...")
    data, ips = parse_log()
    print("[+] Parsed successfully. Generating visualization...")
    generate_visual_report(data, ips)
