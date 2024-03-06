import re
import logging
import ipaddress
from datetime import datetime
from freq3 import FreqCounter  # Make sure freq3.py is accessible

# Define the path to the DNS log file and top million domains file
dns_log_file_path = '/var/log/named/dnsquery.log'
top_domains_file_path = ' top-1m.csv'  # Update with the correct path

# Define the path to the logs folder
logs_folder = 'logs/'

# Ensure the folder path ends with a slash
if not logs_folder.endswith('/'):
    logs_folder += '/'

# Configure logging
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f'{logs_folder}dns_monitoring_{current_time}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load top million domains
def load_top_domains(file_path):
    with open(file_path, 'r') as file:
        return {line.strip().lower() for line in file}

top_domains = load_top_domains(top_domains_file_path)

# Initialize frequency counter
freq_counter = FreqCounter()
# Load your frequency data here if needed

def is_ip_address(string):
    try:
        ipaddress.ip_address(string)
        return True
    except ValueError:
        return False

def extract_domain_names(log_entry):
    pattern = r'\(([^)]+)\)'
    matches = re.findall(pattern, log_entry)
    return [match for match in matches if '.' in match and not is_ip_address(match)]

def analyze_domain_frequency(domain):
    average_domain_length = 15  # Example: adjust based on your analysis
    if len(domain) > average_domain_length * 1.5:
        return True  # Flag as suspicious
    else:
        # Integrate your freq3.py analysis logic here
        return False  # Modify this line as per your analysis logic

# Main loop to read and process the log file
with open(dns_log_file_path, 'r') as log_file:
    for line in log_file:
        domains = extract_domain_names(line)
        for domain in domains:
            if domain.lower() not in top_domains:
                if analyze_domain_frequency(domain):
                    logging.warning(f'Suspicious domain detected: {domain}')
                else:
                    logging.info(f'Domain not in top million but seems normal: {domain}')
            else:
                logging.info(f'Domain is in top million: {domain}')
