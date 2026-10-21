from typer import Typer
from src.cli.simulate import simulate
from src.cli.benchmark import benchmark
from src.cli.config import generate_config

def main():
    app = Typer()

    app.command()(simulate)
    app.command()(benchmark)
    app.command()(generate_config)

    app()