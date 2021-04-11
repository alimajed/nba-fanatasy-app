from flask import Blueprint, jsonify

from app.daos.game import game_doa
from app.schemas.game import game_schema
from app.schemas.teams_stats import teams_stats_schema
from app.schemas.players_stats import players_stats_schema


game_bp = Blueprint("game", __name__)


@game_bp.route("/<game_id>", methods=['GET'])
def get_game_by_id(game_id):
    game = game_doa.get_by_id(game_id)
    return jsonify(game_schema.dump(game))

@game_bp.route("/<game_id>/teams", methods=['GET'])
def get_game_teams_stats(game_id):
    game = game_doa.get_by_id(game_id)
    return jsonify(teams_stats_schema.dump(game.teams_stats))

@game_bp.route("/<game_id>/players", methods=['GET'])
def get_game_players_stats(game_id):
    game = game_doa.get_by_id(game_id)
    return jsonify(players_stats_schema.dump(game.players_stats))