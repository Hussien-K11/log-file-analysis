"""
Log File Analysis Script
------------------------
This script reads Apache access logs and performs basic security analysis:
1. Parses each log line using regex
2. Detects failed login attempts (401 errors)
3. Counts requests by IP address
4. Identifies IPs with repeated failed logins (possible brute-force)

Author: Hussien Kofi
Created: July 2025
"""



# log_parser.py

import re  # re = regular expressions module
from collections import Counter  # Add this import at the top with re

# Step 1: Path to your log file
log_file_path = 'data/sample_logs/access.log'

# Step 2: Define a regex pattern to match each log line
# This pattern uses named groups to make it easier to extract specific parts
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s'                 # IP address (e.g. 192.168.1.1)
    r'- - \[(?P<datetime>[^\]]+)\]\s'               # Date/time in brackets
    r'"(?P<method>[A-Z]+)\s(?P<url>\S+)\s\S+"\s'    # Request method and URL
    r'(?P<status>\d{3})\s'                          # Status code (e.g. 200, 404)
    r'(?P<size>\d+)'                                # Bytes sent
)

# Step 3: Initialise list to track all IPs
ip_list = []
failed_login_ips = []  # Only IPs that had a failed login (401)

# Step 4: Open the log file and read each line
with open(log_file_path, 'r') as log_file:
    for line_number, line in enumerate(log_file, start=1):  # Used `enumerate()` to track line numbers
        # Step 5: Try to match the line with our regex pattern
        match = log_pattern.search(line)
        
        if match:
            # Step 5: Extract data from the match object
            data = match.groupdict()  # Converts match into a dictionary
            ip_list.append(data['ip'])   # Step 6: Add IP to list (for frequency tracking)

           # Step 7: Check for failed login attempts (status 401)  
            if data['status'] == '401':
                failed_login_ips.append(data['ip'])  # Counted later
                print(f"⚠️  FAILED LOGIN DETECTED (Line {line_number})")
                print(f"  IP Address  : {data['ip']}")
                print(f"  Timestamp   : {data['datetime']}")
                print(f"  Method      : {data['method']}")
                print(f"  URL         : {data['url']}")
                print(f"  Status Code : {data['status']}")
                print("-" * 40)
        else:
            print(f"Line {line_number}: No match found.")

# Step 8: Count and display the top 5 most frequent IPs
ip_counts = Counter(ip_list)
top_5_ips = ip_counts.most_common(5)

print("\n📊 Top 5 IP Addresses by Request Volume:")
for ip, count in top_5_ips:
    print(f"  {ip} → {count} requests")

# Step 9: Group failed logins by IP and show those with 2+ failures
failed_counts = Counter(failed_login_ips)

print("\n🚨 Suspicious IPs with Repeated Failed Logins:")
for ip, count in failed_counts.items():
    if count >= 2:  # You can change this threshold
        print(f"  {ip} → {count} failed logins")