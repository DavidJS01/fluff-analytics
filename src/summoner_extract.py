import hashlib
import requests
import os

from database_utils.supabase_league import (
    get_all_summoners_data,
    insert_game_data,
    get_all_game_hashes,
)

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


def get_summoner_puuid(name: str):
    endpoint = API_ENDPOINTS["get_summoner_metadata"].format(summoner_name=name)
    url = f"{URLS['summoner']}/{endpoint}"
    r = requests.get(url, headers=HEADERS).json()
    return r["puuid"]


def extract_match_data(match_id: str) -> None:
    endpoint = API_ENDPOINTS["get_match_metadata"].format(match_id=match_id)
    url = f"{URLS['match']}/{endpoint}"
    r = requests.get(url, headers=HEADERS).json()
    if "info" not in r.keys():
        return None
    else:
        return r["info"]


def transform_match_data(
    game_metadata: dict, match_id: str, summoner_name: str
) -> tuple:
    # some game modes dont have an end timestamp associated
    if not "gameEndTimestamp" in game_metadata.keys():
        return
    else:
        match_start = game_metadata["gameStartTimestamp"]
        match_end = game_metadata["gameEndTimestamp"]
        for user in game_metadata["participants"]:
            if user["summonerName"] == summoner_name:
                data = {
                    "match_hash": hashlib.md5(
                        f"{match_id}{summoner_name}".encode("utf-8")
                    ).hexdigest(),
                    "match_id": match_id,
                    "puuid": user["puuid"],
                    "match_start": match_start,
                    "match_end": match_end,
                    "champion": user["championName"],
                    "kills": user["kills"],
                    "deaths_by_enemies": user["challenges"]["deathsByEnemyChamps"],
                    "gold_per_minute": user["challenges"]["goldPerMinute"],
                    "kill_death_ratio": user["challenges"]["kda"],
                    "q_casts": user["spell1Casts"],
                    "w_casts": user["spell2Casts"],
                    "e_casts": user["spell3Casts"],
                    "r_casts": user["spell4Casts"],
                    "won_game": user["win"],
                }
                return data
            else:
                continue


def load_match_data(puuid, summoner_name, game_hashes) -> None:
    match_list = get_match_list(puuid)
    for game_id in match_list:
        game_hash = hashlib.md5(f"{game_id}{summoner_name}".encode("utf-8")).hexdigest()
        raw_match_data = extract_match_data(game_id)
        if (game_hash in game_hashes) or (raw_match_data is None):
            continue
        transformed_match_data = transform_match_data(
            raw_match_data, game_id, summoner_name
        )
        if transformed_match_data:
            insert_game_data(transformed_match_data)
        else:
            continue


def main():
    # get all registered summoners in the db
    summoners = get_all_summoners_data()
    # get a list of all games that are already in the db
    game_hashes = get_all_game_hashes()
    for summoner in summoners:
        summoner_puuid = summoner["puuid"]
        summoner_name = summoner["summoner_name"]
        load_match_data(summoner_puuid, summoner_name, game_hashes)


if __name__ == "__main__":
    main()
