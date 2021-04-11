from flask import Blueprint, jsonify

from app.daos.season import season_doa
from app.schemas.season import season_schema, seasons_schema
from app.schemas.game import game_schema, games_schema


season_bp = Blueprint("season", __name__)


@season_bp.route("/", methods=['GET'])
def get_all_seasons():
    seasons = season_doa.get_all()
    return jsonify(seasons_schema.dump(seasons))

@season_bp.route("/<season_id>", methods=['GET'])
def get_season_by_id(season_id):
    season = season_doa.get_by_id(season_id)
    return jsonify(games_schema.dump(season))

@season_bp.route("/<season_id>/game", methods=['GET'])
def get_season_games(season_id):
    season = season_doa.get_by_id(season_id)
    return jsonify(games_schema.dump(season.games))
