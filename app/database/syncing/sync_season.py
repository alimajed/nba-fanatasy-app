import logging
from time import time

import pandas as pd

from app.database.db import db
from app.helpers.logger import LoggerHelper
from app.database.models.season import SeasonModel


@LoggerHelper("DATA SYNCING - SEASON")
def insert_season(season):
    season_id = int(season.split("-")[0])
    if SeasonModel.query.filter_by(id=season_id).first():
        return 
    
    db.session.add(SeasonModel(
        id=season_id,
        description=season
    ))
    db.session.commit()
    