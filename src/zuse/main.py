
import sys
import os
import subprocess
from pathlib import Path
from typing import Optional
import typer

from .commands.py import cli as py_cli
from .commands.db import cli as db_cli

cli = typer.Typer()

@cli.command()
def init():
    pass

@cli.command("add", help="Add a new package")
def add(
    packages: Optional[list[str]] = typer.Argument(None),
    proxy: bool = typer.Option(True, "--no-proxy", help="Disable proxy")
):
    work_dir = Path.cwd()
    if work_dir.joinpath("pyproject.toml").exists():
        if proxy:
            cmd = ["bash", Path.home().joinpath("proxy.sh").as_posix(), "poetry", "add"]
        else:
            cmd = ["poetry", "add"]
        if packages:
            cmd.extend(packages)
        subprocess.run(cmd, shell=False)
    else:
        print("pyproject.toml not exists")

@cli.command("run")
def run(
    reload: bool = typer.Option(False, "--reload", help="Reload the server"),
    port: int = typer.Option(8000, "--port", help="Port to run the server"),
    host: str = typer.Option("0.0.0.0", "--host", help="Host to run the server")
):
    work_dir = Path.cwd()
    if work_dir.joinpath("pyproject.toml").exists():
        cmd = ["poetry", "run", "uvicorn", "main:app", "--port", str(port), "--host", host]
        if reload:
            cmd.append("--reload")
        subprocess.run(cmd, shell=False)
    else:
        print("pyproject.toml not exists")

@cli.command("test")
def test(args: Optional[list[str]] = typer.Argument(None)):
    work_dir = Path.cwd()
    if work_dir.joinpath("pyproject.toml").exists():
        cmd = ["poetry", "run", "pytest"]
        if args:
            cmd.extend(args)
        subprocess.run(cmd, shell=False)
    else:
        print("pyproject.toml not exists")

def app():
    cli.add_typer(py_cli, name="py")
    cli.add_typer(db_cli, name="db")
    cli()


