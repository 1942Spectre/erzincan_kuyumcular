from flask import Flask, render_template
from flask.json.provider import DefaultJSONProvider
import requests
from bs4 import BeautifulSoup
import json
import math
import datetime

class MyJsonProvider(DefaultJSONProvider):
    def default(self,o):
        if isinstance(o,datetime.datetime):
            return o.isoformat(" ","seconds")
        return super().default(o)

app = Flask(__name__)
app.json = MyJsonProvider(app)


latest_reload = datetime.datetime.now()
alis = 0
satis = 0


## The request that gets prices from haremaltin
def make_the_request():
    global latest_reload,satis,alis

    r = requests.post("https://www.haremaltin.com/dashboard/ajax/altin",headers={
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest",
        "dil_kodu":"tr"
    })
    data = json.loads(r.text)["data"]["ALTIN"]
    satis = float(data["satis"])
    alis = float(data["alis"])
    latest_reload = datetime.datetime.now()
    print(f'\nAlis: {alis} | Satis: {satis} | datetime: {latest_reload}\n')

# Home route renders an empty template, reload will be callled right after it and every 20 seconds.
@app.route("/")
def home():
    return render_template("home.html",context=None)

# Not created the registration process yet.
@app.route("/register")
def register():
    return render_template("register.html")

# Reload function reloads the global alis,satis and latest reload time variables
# IF THERE IS MORE THAN 20 SECONDS BETWEEN NOW AND LATEST RELOAD
@app.route("/ajax/reload")
def reload():
    global latest_reload
    global alis
    global satis
    
    try:
        c = (datetime.datetime.now() - latest_reload).total_seconds()

    except:
        c = 21
    if c >= 20:
        make_the_request()
    return {
    "last_reload":latest_reload,
    "alis":alis,
    "satis":satis,
    ## CEILED
    ## BILEZIKLER
    "cnc_burma":math.ceil(948 * satis / 1000),
    "sarnel_10_uzeri":math.ceil(955 * satis / 1000),
    "kasli_burma":math.ceil(955 * satis / 1000),
    "orgu_bilezik":math.ceil(960 * satis / 1000),
    "sarnel_8_10":math.ceil(965 * satis / 1000),
    "sarnel_5_8":math.ceil(975 * satis / 1000),
    ## SERTIFIKALI
    "_22_05":math.ceil(965 * satis / 2000),
    "_22_1":math.ceil(950 * satis / 1000),
    "_24_1":math.ceil(1025 * satis / 1000),

    ## ISCILIKLI
    "_14_ayar":math.ceil(885 * satis / 1000),
    "_22_ayar":math.ceil(1080 * satis / 1000),

    ## Rounded to the upper closest 5
    ## SARRAFIYE GRUBU
    "ceyrek_yeni":math.ceil(1.67 * satis / 5) * 5,
    "ceyrek_eski":math.ceil(1.64* satis / 5) * 5,
    "ceyrek_alis":math.ceil(1.6 * alis / 5) * 5,
    "yarim_yeni":math.ceil(1.67*2*satis / 5) * 5,
    "yarim_eski":math.ceil(1.64*2*satis / 5) * 5,
    "yarim_alis":math.ceil(1.6*2*satis / 5) * 5,
    "ziynet_yeni":math.ceil(6.65 * satis / 5) * 5,
    "ziynet_eski":math.ceil(6.52* satis / 5) * 5,
    "ziynet_alis":math.ceil(6.4 * alis / 5) * 5,
    "ata_satis":math.ceil(6.8 * satis / 5) * 5,
    "ata_alis":math.ceil(6.6 * alis / 5) * 5,
    "besli":math.ceil(33.85* satis / 5) * 5
    }

## NO LOGIN YET
@app.route("/login")
def login():
    return render_template("login.html")

## A SIMPLE 404 PAGE
@app.errorhandler(404)
def error(e):
    return render_template("404.html")

if __name__ == "__main__":
    make_the_request()
    app.run(debug=True, host = "0.0.0.0")



