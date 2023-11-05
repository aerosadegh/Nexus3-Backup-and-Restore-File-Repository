from tabulate import tabulate
import typer
import aiohttp


REPOSITORY_LIST_ROUTE = "/service/rest/v1/repositories"


async def get_repository_list(
    nexus_base_url: str,
    repo_name: str,
    username: str,
    password: str,
):
    repo_url = f"{nexus_base_url}{REPOSITORY_LIST_ROUTE}?repository={repo_name}"
    # Create a session object with the authentication header
    auth = aiohttp.BasicAuth(username, password) if username else None

    async with aiohttp.ClientSession(auth=auth) as session:
        # Send a GET request to the repository URL
        async with session.get(repo_url) as response:
            # Check if the response status is OK
            if response.status == 200:
                # Read the response content as JSON
                data = await response.json()
                # Extract the relevant information from the JSON response
                table_data = [(item["name"], item["format"], item["type"]) for item in data]
                # Print the table using tabulate
                table = tabulate(
                    table_data,
                    headers=["Name", "Format", "Type"],
                    tablefmt="mixed_grid",
                )
                typer.echo(table)
            else:
                # Print the response status and reason
                typer.echo(f"Request failed: {response.status} - {response.reason}")
