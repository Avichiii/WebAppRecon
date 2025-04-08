import whois

def cleanWhoIsOutput(raw_whois: str) -> str:
    lines = raw_whois.splitlines()
    cleanedLines = []

    skipPhrases = [
        "NOTICE:",
        "TERMS OF USE:",
        "This listing is a Network Solutions Private Registration",
        "By submitting this query",
        "Mail correspondence to this address",
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



def getWhoIs(domain: str):
    w = whois.whois(domain)
    info = w.text or str(w)
    return cleanWhoIsOutput(info)

def getVulnerabilities(domain):
    pass