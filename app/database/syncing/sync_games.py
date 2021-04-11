import logging
from datetime import datetime, timedelta
from time import time
import glob

import pandas as pd
from tqdm import tqdm

from app.database.db import db
from app.database.syncing.utils import get_response, get_season_query_param, get_game_date_query_param, get_suffix, load_games_data, save_dataset
from app.helpers.logger import LoggerHelper
from app.helpers.parsers import try_parse_float, try_parse_int, try_parse_string_to_time
from app.database.models.player_team_season import PlayerSeasonTeamModel
from app.database.models.game import GameModel
from app.database.models.players_stats import PlayersStatsModel
from app.database.models.teams_stats import TeamsStatsModel
from app.database.models.team import TeamModel


@LoggerHelper("DATA SYNCING - GAMES")
def get_games(season, start_date, end_date):
    t0 = time()

    start_year = int(season.split("-")[0])
    end_year = start_year + 1
    start_date =  datetime.strptime(start_date, "%m/%d/%Y")
    end_date = datetime.strptime(end_date, "%m/%d/%Y")

    games_df_list = []
    games_df_details_list = []
    ranking_df_list = []  
    days = 0
    diff_days = (end_date - start_date).days
    while days <= diff_days:
        game_date = get_game_date_query_param(end_date, days)
        logging.warning(f"GET GAMES {game_date}...")
        dfs = load_games_data(season, game_date)
        if dfs:
            games, games_details, ranking = dfs
            suffix = get_suffix(game_date)
            save_dataset(games, f"games_info_{suffix}", season)
            save_dataset(games_details, f"games_details_{suffix}", season)
            save_dataset(ranking, f"ranking_{suffix}", season)
        else:
            logging.warning(f"no games on {game_date}")
        days += 1

    logging.warning("GET PLAYOFFS SERIES...")
    playoff_series_url = f"https://stats.nba.com/stats/commonplayoffseries?LeagueID=00&season={season}"
    playoff_series = get_response(playoff_series_url, "PlayoffSeries")
    playoff_series = playoff_series["PlayoffSeries"]
    save_dataset(playoff_series, "playoff_series", season)

    logging.warning("CONCAT FILES...")
    all_games_files = glob.glob(f"data/{season}/games_info_*.csv")
    all_games_details_files = glob.glob(f"data/{season}/games_details_*.csv")
    all_ranking_files = glob.glob(f"data/{season}/ranking_*.csv")

    logging.warning("CONCAT FILES - GAMES...")
    lis = []
    for filename in all_games_files:
        df = pd.read_csv(filename, sep=',', index_col=None, header=0)
        lis.append(df)

    df_games = pd.concat(lis, axis=0, ignore_index=False)
    lis.clear()

    logging.warning("CONCAT FILES - GAMES DETAILS...")
    for filename in all_games_details_files:
        df = pd.read_csv(filename, sep=',', index_col=None, header=0)
        lis.append(df)

    df_games_details = pd.concat(lis, axis=0, ignore_index=False)
    lis.clear()

    logging.warning("CONCAT FILES - RANKINGS...")
    for filename in all_ranking_files:
        df = pd.read_csv(filename, sep=',', index_col=None, header=0)
        lis.append(df)

    df_ranking = pd.concat(lis, axis=0, ignore_index=False)
    lis.clear()

    logging.warning(f"END EXECUTION TIME : {time()-t0:.2f}s")

    season_id = int(season.split("-")[0])
    insert_players_teams(season_id, df_games_details.groupby(['TEAM_ID','PLAYER_ID']))
    insert_games(season, df_games)
    insert_teams_stats(df_games)
    insert_players_stats(df_games_details)


@LoggerHelper("DATA SYNCING - PROCESS PLAYERS TEAMS SEASON")
def insert_players_teams(season_id, grouped):
    logging.warning("PROCESSING PLAYERS TEAMS SEASON...")
    for group, data  in tqdm(grouped):
        team_id, player_id = group
        player_team=PlayerSeasonTeamModel(
            season_id=season_id,
            team_id=try_parse_int(team_id),
            player_id=try_parse_int(player_id)
        )
        db.session.add(player_team)
    db.session.commit()
    logging.warning("END PROCESS PLAYERS TEAMS SEASON...") 

@LoggerHelper("DATA SYNCING - GAMES")
def insert_games(season, df):
    logging.warning("PROCESSING GAMES DATASET...")
    df_playoffs = pd.read_csv(f"data/{season}/playoff_series.csv", delimiter=",")
    teams = {team.id:f"{team.city} {team.nick_name}" for team in TeamModel.query.all()} 
    for row, series in tqdm(df.iterrows(), total=df.shape[0]):
        record = dict(series)
        playoff_serie = df_playoffs.loc[df_playoffs["GAME_ID"] == record["GAME_ID"]]
        game = GameModel(
            id= record["GAME_ID"],
            game_date_est=datetime.strptime(record["GAME_DATE_EST"], "%Y-%m-%d"),
            game_status_text=str(record["GAME_STATUS_TEXT"]),
            home_team=f"{teams[record['HOME_TEAM_ID']]} {teams[record['HOME_TEAM_ID']]}",
            home_score=try_parse_int(record["PTS_home"]),
            away_team=f"{teams[record['VISITOR_TEAM_ID']]} {teams[record['VISITOR_TEAM_ID']]}",
            away_score=try_parse_int(record["PTS_away"]),
            home_team_wins=bool(record["HOME_TEAM_WINS"]),
            season_id=try_parse_int(record["SEASON"]),
            is_playoff=(not playoff_serie.empty),
            playoff_seried_id=None if playoff_serie.empty else str(int(playoff_serie['SERIES_ID']))
        )
        db.session.add(game)
        db.session.flush()
    db.session.commit()
    logging.warning("END PROCESS GAMES DATASET...")

@LoggerHelper("DATA SYNCING - TEAMS STATS")
def insert_teams_stats(df):
    logging.warning("PROCESSING GAMES TEAMS STATS...")
    for row, series in tqdm(df.iterrows(), total=df.shape[0]):
        record = dict(series)
        home_team_stats = TeamsStatsModel(
            game_id = try_parse_int(record["GAME_ID"]),
            team_id = try_parse_int(record["HOME_TEAM_ID"]),
            pts = try_parse_int(record["PTS_home"]),
            fg_pct = try_parse_float(record["FG_PCT_home"]),
            ft_pct = try_parse_float(record["FT_PCT_home"]),
            fg3_pct = try_parse_float(record["FG3_PCT_home"]),
            ast = try_parse_int(record["AST_home"]),
            reb = try_parse_int(record["REB_home"]),
            is_home_team=True
        )

        visitor_team_stats = TeamsStatsModel(
            game_id = try_parse_int(record["GAME_ID"]),
            team_id = try_parse_int(record["VISITOR_TEAM_ID"]),
            pts = try_parse_int(record["PTS_away"]),
            fg_pct = try_parse_float(record["FG_PCT_away"]),
            ft_pct = try_parse_float(record["FT_PCT_away"]),
            fg3_pct = try_parse_float(record["FG3_PCT_away"]),
            ast = try_parse_int(record["AST_away"]),
            reb = try_parse_int(record["REB_away"]),
            is_home_team=False
        )
        db.session.add(home_team_stats)
        db.session.add(visitor_team_stats)
        db.session.flush()
    db.session.commit()
    logging.warning("END PROCESS GAMES TEAMS STATS...")

@LoggerHelper("DATA SYNCING - PLAYERS STATS")
def insert_players_stats(df):
    logging.warning("PROCESSING GAMES PLAYERS STATS...")
    for row, series in tqdm(df.iterrows(), total=df.shape[0]):
        record = dict(series)
        playing_time = try_parse_string_to_time(record["MIN"])
        minutes = (playing_time.minute + playing_time.second/60) if playing_time else 0.0
        player_stats = PlayersStatsModel(
            game_id=try_parse_int(record["GAME_ID"]),
            player_id=try_parse_int(record["PLAYER_ID"]),
            start_position=str(record["START_POSITION"]),
            comment=str(record["COMMENT"]),
            minutes=minutes,
            fgm=try_parse_float(record["FGM"]),
            fga=try_parse_float(record["FGA"]),
            fg_pct=try_parse_float(record["FG_PCT"]),
            fg3m=try_parse_float(record["FG3M"]),
            fg3a=try_parse_float(record["FG3A"]),
            fg3_pct=try_parse_float(record["FG3_PCT"]),
            ftm=try_parse_float(record["FTM"]),
            fta=try_parse_float(record["FTA"]),
            ft_pct=try_parse_float(record["FT_PCT"]),
            oreb=try_parse_int(record["OREB"]),
            dreb=try_parse_int(record["DREB"]),
            ast=try_parse_int(record["AST"]),
            stl=try_parse_int(record["STL"]),
            blk=try_parse_int(record["BLK"]),
            to=try_parse_int(record["TO"]),
            pf=try_parse_int(record["PF"]),
            pts=try_parse_int(record["PTS"]),
            plus_minus=try_parse_int(record["PLUS_MINUS"]),
        )
        db.session.add(player_stats)
        db.session.flush()
    db.session.commit()
    logging.warning("END PROCESS GAMES PLAYERS STATS...")