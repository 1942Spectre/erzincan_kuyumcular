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


make_the_request()



def calculate_context(alis,satis,latest_reload):
    context = {
        "last_reload":latest_reload.isoformat(" ","seconds"),
        "alis":alis,
        "satis":satis,
        ## CEILED
        ## BILEZIKLER
        "_22_ayar_bilezik":math.ceil(947 * satis / 1000),
        "_22_ayar_bilezik_alis": math.floor(910*alis / 1000),
        ## SERTIFIKALI
        "_22_05":round(965 * satis / 2000 / 5) * 5,
        "_22_1":round(953 * satis / 1000 / 5) * 5,
        "_24_1":round(1025 * satis / 1000 / 5) * 5,
        "_22_05_alis":round(916 * alis / 2000 / 5) * 5,
        "_22_1_alis":round(916 * alis / 1000 / 5) * 5,
        "_24_1_alis":round(995 * alis / 1000 / 5) * 5,

        ## Rounded to the upper closest 5
        ## SARRAFIYE GRUBU
        "ceyrek_yeni":math.ceil(1.67 * satis / 5) * 5,
        "ceyrek_eski":math.ceil(1.67 * satis / 5) * 5 - 30,
        "ceyrek_alis":math.ceil(1.75 * 913/1000 * alis / 5) * 5 + 30,
        "ceyrek_eski_alis":math.ceil(1.75 * 913/1000 * alis / 5) * 5,
        "yarim_yeni":math.ceil(1.67 * satis / 5) * 10,
        "yarim_eski":(math.ceil(1.67 * satis / 5) * 5 - 30) * 2 ,
        "yarim_alis":(math.ceil(1.75 * 913/1000 * alis / 5) * 5 + 30) * 2,
        "yarim_eski_alis":(math.ceil(1.75 * 913/1000 * alis / 5) * 5) * 2,
        "ziynet_yeni":math.ceil(1.67 * satis / 5) * 20,
        "ziynet_eski":(math.ceil(1.67 * satis / 5) * 5 - 30) * 4,
        "ziynet_alis":(math.ceil(1.75 * 913/1000 * alis / 5) * 5 + 30) * 4,
        "ziynet_eski_alis":(math.ceil(1.75 * 913/1000 * alis / 5) * 5) * 4,
        "ata_satis":math.ceil(6.8 * satis / 5) * 5,
        "ata_alis":math.ceil(6.575 * alis / 5) * 5,
        "besli_satis":math.ceil(6.8 * satis / 5) * 25,
        "besli_alis":math.ceil(6.575 * alis / 5) * 25,
    }
    return context

@app.route("/")
def eski_home():
    global latest_reload
    global alis
    global satis

    if (datetime.datetime.now() - latest_reload).total_seconds() >= 20:
        make_the_request()
    context = calculate_context(alis,satis,latest_reload)
    return render_template("home.html",context=context)

@app.route("/yeni")
def home():
    context = calculate_context(alis,satis,latest_reload)
    return render_template("home2.html",context=context)

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

    if (datetime.datetime.now() - latest_reload).total_seconds() >= 20:
        make_the_request()

    context = calculate_context(alis,satis,latest_reload)
    return context

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
    app.run(debug=True, host = "192.168.1.5")



