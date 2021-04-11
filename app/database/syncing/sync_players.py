import logging
from time import time

import pandas as pd
from tqdm import tqdm

from app.database.db import db
from app.database.syncing.utils import get_response, get_season_query_param, get_league_id, get_current_season_player, save_dataset, split_player_name
from app.database.models.player import PlayerModel
from app.helpers.logger import LoggerHelper
from app.helpers.parsers import try_parse_int

@LoggerHelper("DATA SYNCING - PLAYERS")
def get_players(season=None):
    t0 = time()

    logging.warning("GET ALL PLAYERS...")
    league_id = get_league_id()
    if not season:
        season = get_season_query_param()
    # NOTE setting current season to true will return 
    current_season="00" # False

    all_players_url = f"https://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason={current_season}&LeagueID={league_id}&Season={season}"
    players = get_response(all_players_url, ["CommonAllPlayers"])
    players = players["CommonAllPlayers"]

    logging.warning("SAVE PLAYER DATASET...")
    save_dataset(players, "players", season)

    process_players_dataset(season)

    logging.warning(f"END EXECUTION TIME : {time()-t0:.2f}s")


@LoggerHelper("DATA SYNCING - PLAYERS")
def process_players_dataset(season):
    logging.warning("PROCESSING PLAYER DATASET")
    df= pd.read_csv(f"data/{season}/players.csv", delimiter=",")

    for row, series in tqdm(df.iterrows(), total=df.shape[0]):
        record = dict(series)

        player_id = try_parse_int(record["PERSON_ID"])
        first_name, last_name = split_player_name(record["DISPLAY_LAST_COMMA_FIRST"])
        player = PlayerModel.query.filter_by(id=player_id).first()
        if player:
            player.first_name = first_name
            player.last_name = last_name
            player.from_year = try_parse_int(record["FROM_YEAR"])
            player.to_year = try_parse_int(record["TO_YEAR"])
            player.still_playing = True if try_parse_int(record["ROSTERSTATUS"]) == 1 else False
            # logging.warning(f"UPDATING PLAYER {first_name} {last_name}")
        else:
            player=PlayerModel(
                id=player_id,
                first_name=first_name,
                last_name=last_name,
                from_year=try_parse_int(record["FROM_YEAR"]),
                to_year=try_parse_int(record["TO_YEAR"]),
                still_playing=True if try_parse_int(record["ROSTERSTATUS"]) == 1 else False
            )
            # logging.warning(f"INSERT PLAYER {first_name} {last_name}")
        db.session.add(player)
        db.session.flush()
    db.session.commit()
    logging.warning("END PROCESS PLAYER DATASET")