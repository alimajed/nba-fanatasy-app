from flask import Blueprint, jsonify

from app.daos.team import team_doa
from app.schemas.team import teams_schema


team_bp = Blueprint("team", __name__)


@team_bp.route("/", methods=['GET'])
def get_all_teams():
    teams = team_doa.get_all()
    return jsonify(teams_schema.dump(teams))

@team_bp.route("/<team_id>", methods=['GET'])
def get_team_by_id(team_id):
    team = team_doa.get_by_id(team_id)
    return jsonify(team_schema.dump(team))