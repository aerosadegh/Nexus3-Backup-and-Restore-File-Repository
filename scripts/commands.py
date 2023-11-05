import asyncio

import typer

from functions import get_repository_list, get_repository_components, upload_repository_components


app = typer.Typer()


@app.command()
def repo_list(
    nexus_base_url: str = typer.Option(
        "http://localhost:8081",
        help="The repository URL",
    ),
    repo_name: str = typer.Option(
        "pypi-all",
        help="The repository name",
    ),
    username: str = typer.Option("admin", help="The username for authentication"),
    password: str = typer.Option("admin123", help="The password for authentication"),
):
    return asyncio.run(get_repository_list(nexus_base_url, repo_name, username, password))


@app.command()
def download(
    nexus_base_url: str = typer.Option(
        "http://localhost:8081",
        help="The repository URL",
    ),
    repo_name: str = typer.Option(
        "pypi-all",
        help="The repository name",
    ),
    username: str = typer.Option("admin", help="The username for authentication"),
    password: str = typer.Option("admin123", help="The password for authentication"),
    destination: str = typer.Option("backup", help="The destination for backup"),
):
    return asyncio.run(get_repository_components(nexus_base_url, repo_name, username, password, destination))


@app.command()
def upload(
    nexus_base_url: str = typer.Option(
        "http://localhost:8081",
        help="The repository URL",
    ),
    repo_name: str = typer.Option(
        "pypi-all",
        help="The repository name",
    ),
    username: str = typer.Option("admin", help="The username for authentication"),
    password: str = typer.Option("admin123", help="The password for authentication"),
    source_directory: str = typer.Option("backup", help="The destination for backup"),
):
    return asyncio.run(upload_repository_components(nexus_base_url, repo_name, username, password, source_directory))
