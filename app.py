from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import json
import math

app = Flask(__name__)




@app.route("/")
def home():
    r = requests.post("https://www.haremaltin.com/dashboard/ajax/altin",headers={
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest",
        "dil_kodu":"tr"
    })

    

    data = json.loads(r.text)["data"]["ALTIN"]

    satis = math.ceil(float(data["satis"]))
    alis = math.ceil(float(data["alis"]))

    data = {

    ## CEILED

    ## BILEZIKLER
    "cnc_burma":math.ceil(945 * satis),
    "sarnel_10_uzeri":math.ceil(955 * satis),
    "kasli_burma":math.ceil(955 * satis),
    "orgu_bilezik":math.ceil(960 * satis),
    "sarnel_8_10":math.ceil(965 * satis),
    "sarnel_5_8":math.ceil(975 * satis),

    ## SERTIFIKALI
    "_22_05":math.ceil(965 * satis),
    "_22_1":math.ceil(950 * satis),
    "_24_1":math.ceil(1025 * satis),

    ## ISCILIKLI
    "_14_ayar":math.ceil(885 * satis),
    "_22_ayar":math.ceil(1080 * satis),

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

    print(satis)
    print(alis)


    return render_template("home.html",context=data)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.errorhandler(404)
def error(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True)

