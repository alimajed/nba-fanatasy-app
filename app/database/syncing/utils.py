from os import makedirs, path
from datetime import datetime, timedelta
from time import time, sleep

import requests
import pandas as pd
import numpy as np


HEADERS = {
    "Host": "stats.nba.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept": "application/json, text/plain, /",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
    "Connection": "keep-alive",
    "Referer": "https://stats.nba.com/",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}


def get_response(url, datasets_name):
    response = requests.get(url, headers=HEADERS)
    status_200_ok = response.status_code == 200
    nb_error = 0
    
    # If there are too much call, just try 5 times to be sure that we can"t have the data
    while not status_200_ok and nb_error < 5:
        sleep(0.1)
        response = requests.get(url)
        status_200_ok = response.status_code == 200
        nb_error += 1
    
    if nb_error == 5:
        return None
    
    json = response.json()

    dfs = {}
    for elem in json["resultSets"]:
        if elem["name"] not in datasets_name:
            continue
        
        df = pd.DataFrame(elem["rowSet"], columns=elem["headers"])
        dfs[elem["name"]] = df
    
    return dfs

def save_dataset(df, df_name, season):
    if not season:
        season = get_season_query_param()
    dest = f"data/{season}"
    if not path.exists(dest):
        makedirs(dest)
    df.to_csv(f"{dest}/{df_name}.csv", index=False)

def get_suffix(date=None):
    if not date:
        return datetime.utcnow().strftime("%Y%m%d")
    return datetime.strptime(date, "%m/%d/%Y").strftime("%Y%m%d")

def get_season_query_param(season=None):
    # NOTE season 2009 --> 2009-10
    if not season:
        today = datetime.utcnow()
        # NOTE second halh of the season
        if today.month in [1,2,3,4,5,6]:
            season = today.year - 1
        else:
            season = year
    return f"{season}-{str(season+1)[-2:]}"

def get_league_id():
    return "00"

def get_current_season_player(current_season):
    if current_season:
        return "1"
    return "00"

def get_game_date_query_param(date=None, days=1):
    if not date:
        date = datetime.utcnow()
    game_date = date - timedelta(days=days)
    return game_date.strftime("%m/%d/%Y")


def merge_on_team(line_score, df, team_col):
    return df.merge(line_score,
                    how="inner",
                    left_on=["GAME_ID", team_col],
                    right_on=["GAME_ID", "TEAM_ID"],
                    suffixes=("_home", "_away"))

    return np.where(df["PTS_home"] > df["PTS_away"], 1, 0)

def format_game_id(df):
    return df["GAME_ID"].apply(lambda x: "00"+str(x))

def format_date(df):
    return pd.to_datetime(df["GAME_DATE_EST"])

def home_team_win(df):
        return np.where(df['PTS_home'] > df['PTS_away'], 1, 0)

def filter_game_no_nba_team(df, season):
    teams = pd.read_csv(f"data/{season}/teams.csv")
    teams_id_nba = teams["TEAM_ID"].unique()
    home_team_is_nba = df["HOME_TEAM_ID"].apply(
        lambda x: x in teams_id_nba)
    away_team_is_nba = df["VISITOR_TEAM_ID"].apply(
        lambda x: x in teams_id_nba)
    return df[(home_team_is_nba) & (away_team_is_nba)]

def only_finished_game(df):
    return df[df["GAME_STATUS_TEXT"] == "Final"]

def preformat_games(line_score, games_header, season):
    games_df = games_header.copy()
    games_df = merge_on_team(line_score, df=games_df, team_col="HOME_TEAM_ID")
    games_df = merge_on_team(line_score, df=games_df, team_col="VISITOR_TEAM_ID")
    
    games_df["HOME_TEAM_WINS"] = home_team_win(games_df)
    games_df["GAME_ID"] = format_game_id(games_df)
    games_df["GAME_DATE_EST"] = format_date(games_df)

    games_df = filter_game_no_nba_team(games_df, season)
    games_df = only_finished_game(games_df)

    games_df["GAME_ID"] = games_df["GAME_ID"].astype(int)
    games_df = games_df.drop_duplicates().reset_index(drop=True)

    return games_df

def preformat_ranking(west_ranking, east_ranking):
    ranking = pd.concat([west_ranking, east_ranking])
    ranking["STANDINGSDATE"] = pd.to_datetime(ranking["STANDINGSDATE"])

    return ranking

def load_games_data(season, game_date):
    suffix = get_suffix(game_date)
    datasets_name = ["GameHeader", "LineScore", "EastConfStandingsByDay", "WestConfStandingsByDay"]
    ignore_keys = ["date"]
    dfs = {}
    for dataset in datasets_name + ignore_keys:
        dfs[dataset] = list()

    
    games_url = f"https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate={game_date}"
    game_day_dfs = get_response(games_url, datasets_name)
    game_day_dfs["date"] = game_date

    # NOTE prepare dfs
    for dataset in game_day_dfs.keys():
        dfs[dataset].append(game_day_dfs[dataset])
    
    for dataset in dfs.keys():
        if dataset in ignore_keys:
            continue
        dfs[dataset] = pd.concat(dfs[dataset])
    header_cols = ["GAME_DATE_EST", "GAME_ID", "GAME_STATUS_TEXT",
                   "HOME_TEAM_ID", "VISITOR_TEAM_ID", "SEASON"]
    linescore_cols = ["GAME_ID", "TEAM_ID", "PTS",
                      "FG_PCT", "FT_PCT", "FG3_PCT", "AST", "REB"]

    # NOTE Get wanted datasets with wanted columns
    west_ranking = dfs["WestConfStandingsByDay"]
    east_ranking = dfs["EastConfStandingsByDay"]
    games_header = dfs["GameHeader"][header_cols]
    line_score = dfs["LineScore"][linescore_cols]

    del dfs

    games = preformat_games(line_score, games_header, season)
    ranking = preformat_ranking(west_ranking, east_ranking)

    if games.empty:
        return
    
    del games_header, line_score, west_ranking, east_ranking

    dfs_details = list()
    for game_id in games["GAME_ID"]:
        game_details_url = f"https://stats.nba.com/stats/boxscoretraditionalv2" \
            + f"?EndPeriod=10" \
            + f"&EndRange=0&GameID=00{game_id}" \
            + f"&RangeType=0" \
            + f"&Season={season}" \
            + f"&SeasonType=Regular Season" \
            + f"&StartPeriod=1" \
            + f"&StartRange=0"
        game_details = get_response(game_details_url, datasets_name=["PlayerStats"])
        game_details = game_details["PlayerStats"]
        dfs_details.append(game_details)

    games_details = pd.concat(dfs_details)

    games["GAME_ID"] = pd.to_numeric(games["GAME_ID"])
    games["GAME_DATE_EST"] = pd.to_datetime(games["GAME_DATE_EST"])
    games_details["GAME_ID"] = pd.to_numeric(games_details["GAME_ID"])
    ranking["STANDINGSDATE"] = pd.to_datetime(ranking["STANDINGSDATE"])

    return games, games_details, ranking

def split_player_name(name):
    if ',' in str(name):
        return str(name).split(',', 1)
    else:
        return str(name), None