import logging
from datetime import datetime, timedelta
from time import time

import pandas as pd

from app.database.syncing.utils import get_response, get_suffix, get_season_query_param, get_game_date_query_param, load_games_data, save_dataset
from app.helpers.logger import LoggerHelper

@LoggerHelper("DATA SYNCING - NEW GAMES")
def get_new_games():
    t0 = time()

    logging.warning("GET NEW GAMES...")
    season = get_season_query_param()
    game_date = get_game_date_query_param()
    games, games_details, ranking = load_games_data(season, game_date)

    logging.warning("SAVE DATASETS...")

    suffix = get_suffix(game_date)
    save_dataset(games, f"games_info_{suffix}", season)
    save_dataset(games_details, f"games_details_{suffix}", season)
    save_dataset(ranking, f"ranking_{suffix}", season)

    logging.warning(f"END EXECUTION TIME : {(time()-t0):.2f}s")
