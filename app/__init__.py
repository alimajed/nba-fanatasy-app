from flask import Flask

from app.database.db import db, migrate
from app.schemas.ma import ma
from app.cli import sync_games, sync_new_games, sync_players, sync_seasons, sync_teams

from config import ConfigFactory


def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigFactory.factory().__class__)

    # # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # # add custom commands
    app.cli.add_command(sync_teams)
    app.cli.add_command(sync_players)
    app.cli.add_command(sync_seasons)
    app.cli.add_command(sync_games)
    app.cli.add_command(sync_new_games)

    with app.app_context():

        # import database models
        from app.database.models.season import SeasonModel
        from app.database.models.team import TeamModel
        from app.database.models.player import PlayerModel
        from app.database.models.game import GameModel
        from app.database.models.player_team_season import PlayerSeasonTeamModel
        from app.database.models.teams_stats import TeamsStatsModel
        from app.database.models.players_stats import PlayersStatsModel

        # # import blueprints
        # views
        from app.views.home import home_bp
        from app.views.season import season_bp
        from app.views.team import team_bp
        from app.views.player import player_bp
        from app.views.game import game_bp
        
        # register blueprints
        # views
        app.register_blueprint(home_bp, url_prefix="/home")
        app.register_blueprint(season_bp, url_prefix="/api/season")
        app.register_blueprint(team_bp, url_prefix="/api/team")
        app.register_blueprint(player_bp, url_prefix="/api/player")
        app.register_blueprint(game_bp, url_prefix="/api/game")
        # # end import blueprints

        return app