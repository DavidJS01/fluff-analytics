from supabase import create_client, Client
import os


def create_supabase_client() -> Client:
    """
    function that, using the supabase url and key env vars establishes a connection
    to supabase before returning a client object that allows
    interaction with the database
    :returns: supabase.Client object
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    try:
        client = create_client(url, key)
    except Exception as e:
        raise e
    else:
        return client


def insert_table_data(table_name: str, data: dict) -> None:
    """
    function that takes a dictionary of data, and inserts that data into the
    specified Supabase table
    :param data: dictionary holding data in {column:row_value} format
    :returns: None
    """
    try:
        client = create_supabase_client()
        client.table(table_name).insert(data).execute()
    except Exception as e:
        raise e


def get_all_game_hashes() -> list:
    """
    function that queries the supabase database, returning a list of all
    game_hashes recording in the `games` table.
    :return: list of strings, each with a particular game hash
    """
    try:
        client = create_supabase_client()
        data = client.table("games").select("match_hash").execute()
        hash_list = []
        for row in data.data:
            hash_list.append(row["match_hash"])
        return hash_list
    except Exception as e:
        raise e


def get_all_summoners_data() -> list:
    """
    function that runs a select * query on the `summoners` table,
    returning a list of tuples in [(summoner_name, summoner_puuid)] format
    :returns: list of tuples, each tuple with a name and puuid
    """
    try:
        client = create_supabase_client()
        data = client.table("summoners").select("*").execute()
        return data.data
    except Exception as e:
        raise e


def insert_game_data(game_data: dict):
    try:
        client = create_supabase_client()
        data = client.table("games").insert(game_data).execute()
    except Exception as e:
        raise e
