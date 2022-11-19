CREATE_TABLES = """
    CREATE TABLE IF NOT EXISTS summoners (
        name TEXT,
        puuid TEXT,
        UNIQUE(name, puuid)
    );
    CREATE TABLE IF NOT EXISTS match_data (
        puuid TEXT,
        match_id TEXT,
        match_start INTEGER,
        match_end INTEGER,
        champion TEXT,
        kills INTEGER,
        deaths_by_enemies INTEGER,
        gold_per_minute REAL,
        kda REAL,
        q_casts INTEGER,
        w_casts INTEGER,
        e_casts INTEGER,
        r_casts INTEGER,
        won_game INTEGER,
        UNIQUE(match_id)
    )
"""

INSERT_MATCH_HISTORY = """ 
    INSERT OR IGNORE INTO MATCH_HISTORY (puuid, match_id, match_start, match_end) VALUES (?,?,?,?)
"""

INSERT_MATCH_DATA = """ 
    INSERT OR IGNORE INTO MATCH_DATA (
        puuid,
        match_id,
        match_start,
        match_end,
        champion,
        kills,
        deaths_by_enemies,
        gold_per_minute,
        kda,
        q_casts,
        w_casts,
        e_casts,
        r_casts,
        won_game
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
"""
