EXAMPLE_SELECT_SUMMONERS = """
    select * from summoners;

"""

EXAMPLE_SELECT_WIN_LOSSES = """
    /*
    author: David
    query that gets the total games and won/lost games per player
    */
    
    select summoner_name, total_games, games_won, sum(total_games::int + ((-1) * (games_won))::int) as games_lost from (
    select count(*) as total_games, sum(won_game::int) as games_won, summoner_name
    from games, summoners
    where summoners.puuid = games.puuid
    group by summoners.summoner_name
    ) subq
    group by summoner_name,total_games, games_won


"""