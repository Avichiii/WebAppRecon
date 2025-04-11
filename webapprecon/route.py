import json
import datetime
from webapprecon import app, db
from webapprecon.models import ScanResults
from flask import render_template, request
from webapprecon.main import getWhoIs, getVulnerabilities, detectProtocol

def dbStore(resolvedDomain, whois, vulnerabilities):
    '''
    takes: resolvedDomain, whois & vulnerabilities as input
    Stores provided parameters into the database
    Returns: None
    '''
    scan = ScanResults(
        url=resolvedDomain,
        date=datetime.datetime.now(),
        whoisInfo=whois,
        vulnInfo=json.dumps(vulnerabilities)
    )
    db.session.add(scan)
    db.session.commit()

def scan(resolvedDomain: str):
    '''
    takes: whole url or IP of a domain
    Invode whois and vulnerability scanning Logic
    Returns: tuple
    '''
    whois = getWhoIs(str(resolvedDomain))
    vulnerabilities = getVulnerabilities(resolvedDomain)

    return (whois, vulnerabilities)

@app.route("/")
@app.route("/home")
def home():
    '''
    Main Page
    Returns: home.html page to the client
    '''
    return render_template("home.html")

@app.route("/api", methods=["POST"])
def api():
    '''
    only Allows POST method.
    Manages Data sending/retrival between client & server.
    Returns: results.html or home.html based on the request.
    '''
    try:
        jsonData = request.get_json()
        domain = jsonData.get('domainName')

        resolvedDomain = detectProtocol(domain)

        existing_scan = ScanResults.query.filter_by(url=resolvedDomain).first()

        if existing_scan:
            now = datetime.datetime.now()
            difference = (now - existing_scan.date).days

            if (difference <= 30):
                whois = existing_scan.whoisInfo
                vulnerabilities = json.loads(existing_scan.vulnInfo)
            
            else:
                db.session.delete(existing_scan)
                db.session.commit()

                whois, vulnerabilities = scan(str(resolvedDomain))
                dbStore(resolvedDomain, whois, vulnerabilities)
        
        else:
            whois, vulnerabilities = scan(str(resolvedDomain))
            dbStore(resolvedDomain, whois, vulnerabilities)

        return render_template("results.html", domain=resolvedDomain, whois_info=whois, vuln_info=vulnerabilities, show_home=True)
    
    except Exception as e:
        print(e)
        return render_template("home.html")