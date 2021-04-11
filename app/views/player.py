from flask import Blueprint, jsonify

from app.daos.player import player_doa
from app.schemas.player import player_schema, players_schema


player_bp = Blueprint("player", __name__)


@player_bp.route("/", methods=['GET'])
def get_all_players():
    players = player_doa.get_all()
    return jsonify(players_schema.dump(players))

@player_bp.route("/<player_id>", methods=['GET'])
def get_player_by_id(player_id):
    player = player_doa.get_by_id(player_id)
    return jsonify(player_schema.dump(player))