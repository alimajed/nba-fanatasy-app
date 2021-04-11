import logging
from time import time

import pandas as pd
from tqdm import tqdm

from app.database.db import db
from app.database.syncing.utils import get_response, save_dataset
from app.database.models.team import TeamModel
from app.helpers.logger import LoggerHelper
from app.helpers.parsers import try_parse_int


@LoggerHelper("DATA SYNCING - TEAMS")
def get_teams(season=None):
    t0 = time()
    logging.warning("GET ALL TEAMS...") 
    all_teams_url = "https://stats.nba.com/stats/commonteamyears?LeagueID=00"
    teams = get_response(all_teams_url, ["TeamYears"])
    teams = teams["TeamYears"]

    logging.warning("GET TEAMS DETAILS...") 
    team_info_url = "https://stats.nba.com/stats/teamdetails?TeamID={team_id}"    
    teams_details = teams["TEAM_ID"].apply(lambda x: get_response(team_info_url.format(team_id=x), ["TeamBackground"])["TeamBackground"])
    teams_details = pd.concat(teams_details.values)

    logging.warning("MERGE DATASETS...") 
    teams_full = teams.merge(teams_details, on=["TEAM_ID","ABBREVIATION"])

    logging.warning("SAVE DATASET...") 
    save_dataset(teams_full, "teams", season)

    process_teams_dataset(season)

    logging.warning(f"END EXECUTION TIME : {time()-t0:.2f}s")

@LoggerHelper("DATA SYNCING - TEAMS")
def process_teams_dataset(season):
    logging.warning("PROCESSING TEAM DATASET...") 
    df= pd.read_csv(f"data/{season}/teams.csv", delimiter=",")

    for row, series in tqdm(df.iterrows(), total=df.shape[0]):
        record = dict(series)

        team_id = try_parse_int(record["TEAM_ID"])
        team = TeamModel.query.filter_by(id=team_id).first()
        if team:
            team.end_year = try_parse_int(record["MAX_YEAR"])
            team.team_code = str(record["ABBREVIATION"])
            team.nick_name = str(record["NICKNAME"])
            team.city = str(record["CITY"])
            team.arena = str(record["ARENA"])
            # logging.warning(f"UPDATE TEAM {record['CITY']} {record['NICKNAME']}")
        else:
            team=TeamModel(
                id=try_parse_int(record["TEAM_ID"]),
                start_year=try_parse_int(record["MIN_YEAR"]),
                end_year=try_parse_int(record["MAX_YEAR"]),
                team_code=str(record["ABBREVIATION"]),
                nick_name=str(record["NICKNAME"]),
                city=str(record["CITY"]),
                year_founded=try_parse_int(record["YEARFOUNDED"]),
                arena=str(record["ARENA"])
            )
            # logging.warning(f"INSERT TEAM {record['CITY']} {record['NICKNAME']}")
        db.session.add(team)
        db.session.flush()
    db.session.commit()
    logging.warning("END PROCESS TEAM DATASET...") 
