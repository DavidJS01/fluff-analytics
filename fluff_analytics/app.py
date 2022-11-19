import requests
import os
from database.database import (
    create_connection,
    get_registered_summoners_name,
    get_registered_summoners_puuid,
    setup_tables,
    insert_game_data,
)
import itertools

URLS = {
    "summoner": "https://na1.api.riotgames.com/lol",
    "match": "https://americas.api.riotgames.com/lol",
}

HEADERS = {"X-Riot-Token": os.environ.get("API_KEY")}

API_ENDPOINTS = {
    "get_summoner_metadata": "summoner/v4/summoners/by-name/{summoner_name}",
    "get_match_history": "match/v5/matches/by-puuid/{summoner_puuid}/ids",
    "get_match_metadata": "match/v5/matches/{match_id}",
}


def get_match_list(puuid: str) -> list:
    endpoint = API_ENDPOINTS["get_match_history"].format(summoner_puuid=puuid)
    url = f"{URLS['match']}/{endpoint}"
    r = requests.get(url, headers=HEADERS).json()
    return r


def extract_match_data(match_id: str) -> None:
    endpoint = API_ENDPOINTS["get_match_metadata"].format(match_id=match_id)
    url = f"{URLS['match']}/{endpoint}"
    r = requests.get(url, headers=HEADERS).json()
    return r


def load_match_data(puuid, conn, registered_users) -> None:
    match_list = get_match_list(puuid)
    for match_id in match_list:
        game_metadata = extract_match_data(match_id)["info"]
        game_start = game_metadata["gameStartTimestamp"]
        game_end = game_metadata["gameEndTimestamp"]
        for user in game_metadata["participants"]:
            if user["summonerName"] in registered_users:
                data = (
                    user["puuid"],
                    match_id,
                    game_start,
                    game_end,
                    user["championName"],
                    user["kills"],
                    user["challenges"]["deathsByEnemyChamps"],
                    user["challenges"]["goldPerMinute"],
                    user["challenges"]["kda"],
                    user["spell1Casts"],
                    user["spell2Casts"],
                    user["spell3Casts"],
                    user["spell4Casts"],
                    user["win"],
                )
                insert_game_data(data, conn)
            else:
                continue


if __name__ == "__main__":
    conn = create_connection("./fluff.db")
    setup_tables(conn)
    x = get_registered_summoners_name(conn)
    registered_users = list(itertools.chain(*x))
    summoners = get_registered_summoners_puuid(conn)
    for summoner_puuid in summoners:
        load_match_data(summoner_puuid, conn, registered_users)
