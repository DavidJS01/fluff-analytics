from flask import Flask, request, render_template
from database_utils.supabase_league import insert_table_data
from summoner_extract import get_summoner_puuid

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def my_form_post():
    summoner_name = request.form["summoner_name"]
    puuid = get_summoner_puuid(summoner_name)
    data = {"puuid": puuid, "summoner_name": summoner_name}
    insert_table_data("summoners", data=data)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
