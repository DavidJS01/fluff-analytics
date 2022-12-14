from flask import Flask, request, render_template, jsonify
from database import insert_table_data
from summoner_extract import get_summoner_puuid

app = Flask(__name__)


@app.route("/summoner")
def hello_world():
    return render_template("index.html")


@app.route("/summoner", methods=["POST"])
def my_form_post():
    summoner_name = request.form["summoner_name"]
    puuid = get_summoner_puuid(summoner_name)
    data = {"puuid": puuid, "summoner_name": summoner_name}
    insert_table_data("summoners", data)
    resp = jsonify(success=True)
    return render_template("index.html")
