import time
import whois
import requests
import ipaddress
from zapv2 import ZAPv2

def cleanWhoIsOutput(raw_whois: str) -> str:
    '''
    Takes Raw whois Data.
    Cleans out Unnecessary Lines
    Returns: str  
    '''
    lines = raw_whois.splitlines()
    cleanedLines = []

    skipPhrases = [
        "NOTICE:",
        "TERMS OF USE:",
        "This listing is a Network Solutions Private Registration",
        "By submitting this query",
        "Mail correspondence to this domain",
        "The data in Networksolutions.com",
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if ':' not in line:
            continue  # Skip lines without colon (most legal garbage)
        if any(phrase in line for phrase in skipPhrases):
            continue

        key, value = line.split(":", 1)
        key = key.strip().replace("_", " ").title()
        value = value.strip()
        cleanedLines.append(f"{key:<30}: {value}")

    return "\n".join(cleanedLines)

def isIPaddress(domain):
    '''
    Checks if the userinut is an IP Address or not
    Returns: bool
    '''
    isIP = False
    try:
        ipaddress.ip_address(domain)
        isIP = True
    except ValueError:
        return False
    return isIP

def detectProtocol(domain: str):
    '''
    takes str
    finds what protocol is used between http & https
    Returns whole url (ex. https://example.com)
    '''
    if domain.startswith('https://') or domain.startswith('http://'):
        return domain
    else:
        urlHttps = f'https://{domain}'
        try:
            response = requests.get(urlHttps, timeout=5)
            if response.status_code < 400:
                return 'https://' + domain
        except requests.exceptions.RequestException:
            pass

        urlHttp = f'http://{domain}'
        try:
            response = requests.get(urlHttp, timeout=5)
            if response.status_code < 400:
                return 'http://' + domain
        except requests.exceptions.RequestException:
            pass
    
    return 'unknown address'

def getWhoIs(domain: str):
    '''
    takes str
    Finds Whois inforation about the domain given
    Returns: str
    '''
    w = whois.whois(domain)
    info = w.text or str(w)
    return cleanWhoIsOutput(info)

def getVulnerabilities(domain):
    '''
    takes str
    Main logic for finding vulnerabilities, uses ZAP for the findings.
    Returns: JSON
    '''
    ZAP_API = 'http://localhost:8080'
    zap = ZAPv2(proxies={'http': ZAP_API, 'https': ZAP_API})

    zap.urlopen(domain)
    time.sleep(2)

    while int(zap.pscan.records_to_scan) > 0:
        time.sleep(2)

    scan_id = zap.ascan.scan(domain)
    while int(zap.ascan.status(scan_id)) < 100:
        time.sleep(5)

    alerts = zap.core.alerts(baseurl=domain)
    return alerts