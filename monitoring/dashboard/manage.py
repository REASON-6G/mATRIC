import click
from flask.cli import with_appcontext
from flask_migrate import init, migrate, upgrade

@click.command()
@with_appcontext
def migrations():
    init_db = init()
    migrate_db = migrate()
    upgrade_db = upgrade()

