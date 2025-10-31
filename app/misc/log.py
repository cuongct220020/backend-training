# app/misc/log.py
from termcolor import colored

# Using app/utils/logger_utils for alternative approach
def log(message: str, keyword: str = "INFO"):
    if keyword == "WARN":
        print(colored('[WARN]', 'yellow'), message)
    elif keyword == "ERROR":
        print(colored('[ERROR] ' + message, 'red'))
    elif keyword == "INFO":
        print(colored('[INFO]', 'blue'), message)
    else:
        print(colored('[{}]'.format(keyword), 'cyan'), message)