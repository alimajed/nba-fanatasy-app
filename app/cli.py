import click
from flask.cli import with_appcontext

@click.command("sync-season")
@click.option("--season")
@click.option("--start-date")
@click.option("--end-date")
@with_appcontext
def sync_seasons(season, start_date, end_date):
    from app.database.syncing.sync_season import insert_season
    from app.database.syncing.sync_teams import get_teams
    from app.database.syncing.sync_players import get_players
    from app.database.syncing.sync_games import get_games
    insert_season(season)
    get_teams(season)
    get_players(season)
    get_games(season, start_date, end_date)

@click.command("sync-teams")
@click.option("--season")
@with_appcontext
def sync_teams(season):
    from app.database.syncing.sync_teams import get_teams
    get_teams(season)

@click.command("sync-players")
@click.option("--season")
@with_appcontext
def sync_players(season):
    from app.database.syncing.sync_players import get_players
    get_players(season)

@click.command("sync-games")
@click.option("--season")
@click.option("--start-date")
@click.option("--end-date")
@with_appcontext
def sync_games(season, start_date, end_date):
    from app.database.syncing.sync_games import get_games
    get_games(season, start_date, end_date)

@click.command("sync-new-games")
@with_appcontext
def sync_new_games():
    from app.database.syncing.sync_new_games import get_new_games
    get_new_games()