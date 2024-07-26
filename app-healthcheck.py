import subprocess
import time
import logging
import requests

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 90
PROCESS_THRESHOLD = 100

SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/your_webhook_url'

logging.basicConfig(filename='system_health.log', level=logging.INFO)

def check_cpu_usage():
    cpu_usage = subprocess.check_output(['top', '-b', '-n', '1', '|', 'grep', 'Cpu(s)']).decode('utf-8').strip().split()[-1]
    if float(cpu_usage) > CPU_THRESHOLD:
        logging.info(f"CPU usage exceeded threshold: {cpu_usage}%")
        send_slack_alert(f"CPU usage exceeded threshold: {cpu_usage}%")

def check_memory_usage():
    memory_usage = subprocess.check_output(['free', '-m']).decode('utf-8').strip().split()[2]
    if float(memory_usage) > MEMORY_THRESHOLD:
        logging.info(f"Memory usage exceeded threshold: {memory_usage}%")
        send_slack_alert(f"Memory usage exceeded threshold: {memory_usage}%")

def check_disk_space():
    disk_usage = subprocess.check_output(['df', '-h']).decode('utf-8').strip().split()[4]
    if float(disk_usage) > DISK_THRESHOLD:
        logging.info(f"Disk space exceeded threshold: {disk_usage}%")
        send_slack_alert(f"Disk space exceeded threshold: {disk_usage}%")

def check_running_processes():
    running_processes = subprocess.check_output(['ps', '-ef']).decode('utf-8').strip().count('\n')
    if running_processes > PROCESS_THRESHOLD:
        logging.info(f"Running processes exceeded threshold: {running_processes}")
        send_slack_alert(f"Running processes exceeded threshold: {running_processes}")

def send_slack_alert(message):
    payload = {'text': message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload, headers=headers)
    if response.status_code != 200:
        logging.error(f"Failed to send Slack alert: {response.text}")

def main():
    while True:
        check_cpu_usage()
        check_memory_usage()
        check_disk_space()
        check_running_processes()
        time.sleep(300)  # Run every 5 minutes

if __name__ == '__main__':
    main()