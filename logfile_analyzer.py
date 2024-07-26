# logfile analyzer  
import re
import collections
import datetime


LOG_PATTERN = r'(?P<ip>\S+) - (?P<user>\S+) \[(?P<date>\d{2}/\d{2}/\d{4}:\d{2}:\d{2}:\d{2} +\d{2}:\d{2})' \
             r' "(?P<method>\S+) (?P<path>/.*) (?P<protocol>\S+)" (?P<status>\d{3}) (?P<bytes>\d+)' \
             r' "(?P<referer>.*?)" "(?P<agent>.*?)"'

def parse_log_line(line):
    match = re.match(LOG_PATTERN, line)
    if match:
        return match.groupdict()
    return None

def analyze_log_data(log_data):
    status_codes = collections.Counter()
    ip_addresses = collections.Counter()
    paths = collections.Counter()
    referers = collections.Counter()
    agents = collections.Counter()
    for line in log_data:
        parsed_line = parse_log_line(line)
        if parsed_line:
            status_codes[parsed_line['status']] += 1
            ip_addresses[parsed_line['ip']] += 1
            paths[parsed_line['path']] += 1
            referers[parsed_line['referer']] += 1
            agents[parsed_line['agent']] += 1

    most_requested_paths = sorted(paths.items(), key=lambda x: x[1], reverse=True)[:10]
    most_requested_ips = sorted(ip_addresses.items(), key=lambda x: x[1], reverse=True)[:10]
    most_requested_referers = sorted(referers.items(), key=lambda x: x[1], reverse=True)[:10]
    most_requested_agents = sorted(agents.items(), key=lambda x: x[1], reverse=True)[:10]
    num_404_errors = status_codes.get('404', 0)
    report = f"Web Server Log Analysis Report\n"
    report += f"Generated on: {datetime.datetime.now()}\n"
    report += f"\nMost Requested Paths:\n"
    for path, count in most_requested_paths:
        report += f"{path}: {count}\n"
    report += f"\nMost Requested IP Addresses:\n"
    for ip, count in most_requested_ips:
        report += f"{ip}: {count}\n"
    report += f"\nMost Requested Referers:\n"
    for referer, count in most_requested_referers:
        report += f"{referer}: {count}\n"
    report += f"\nMost Requested Agents:\n"
    for agent, count in most_requested_agents:
        report += f"{agent}: {count}\n"
    report += f"\nNumber of 404 Errors: {num_404_errors}\n"

    return report
with open('log.txt', 'r') as f:
    log_data = f.readlines()

report = analyze_log_data(log_data)
print(report)