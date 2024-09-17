
import typer
import subprocess
from pathlib import Path
from zuse.snippet import get_snippet_dir
import shutil

cli = typer.Typer(help="Manage the database")

@cli.command()
def init():
    typer.echo("Initializing database tables...")
    snippet_dir = get_snippet_dir() 
    alembic_dir = snippet_dir.joinpath("alembic")
    shutil.copytree(alembic_dir, ".", dirs_exist_ok=True)
    typer.echo("Database tables initialized successfully!")

@cli.command()
def upgrade():
    typer.echo("Upgrading database tables...")
    ret = subprocess.run(["poetry", "run", "alembic", "upgrade", "head"])
    if ret.returncode != 0:
        typer.echo("Database tables upgraded failed!")
    else:
        typer.echo("Database tables upgraded successfully!")