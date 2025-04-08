from webapprecon import app
from flask import render_template, request, jsonify
from webapprecon.main import getWhoIs, getVulnerabilities

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/api", methods=["POST"])
def api():
    try:
        jsonData = request.get_json()
        domain = jsonData.get('domainName')
        whois = getWhoIs(str(domain))
        # vulnerablilies = getVulnerabilities(domain)
        return render_template("results.html", domain=domain, whois_info=whois)
    except:
        return render_template("home.html")