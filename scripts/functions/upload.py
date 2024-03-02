import os
import asyncio
from pathlib import Path

import aiohttp


COMPONENTS_ROUTE = "/service/rest/v1/components"
REPOSITORY_ROUTE = "/service/rest/v1/repositories"


async def upload_component(session, repo_url, repo_format, source_filename: Path):
    data = aiohttp.FormData()
    data.add_field(
        f"{repo_format}.asset",
        open(source_filename, "rb"),
        filename=source_filename.name,
        content_type="application/octet-stream",
    )
    headers = {"accept": "application/json"}

    async with session.post(repo_url, data=data, headers=headers) as response:
        if response.status == 204:
            print(f"Upload {source_filename!r} Successfully!")


async def get_repo_type(
    nexus_base_url: str,
    session: aiohttp.ClientSession,
    repo_name,
):
    repo_url = f"{nexus_base_url}{REPOSITORY_ROUTE}/{repo_name}"
    headers = {"accept": "application/json"}
    async with session.get(repo_url, headers=headers) as response:
        if response.status == 200:
            res_json = await response.json()
            return res_json["format"]


async def upload_repository_components(
    nexus_base_url: str,
    repo_name: str,
    username: str,
    password: str,
    source_directory: str,
):
    repo_url = f"{nexus_base_url}{COMPONENTS_ROUTE}?repository={repo_name}"
    auth = aiohttp.BasicAuth(username, password) if username and password else None

    for root, dirs, files in os.walk(source_directory):
        root_path = Path(root)
        async with aiohttp.ClientSession(auth=auth) as session:
            repo_format = await get_repo_type(nexus_base_url, session, repo_name)
            input(f"$$$ Uploading to a {repo_format}.asset repo. $$$\n"
                  "Please press Enter to confirm and continue ...")
            component_path_list = [root_path / Path(x) for x in files]
            tasks = []
            for component in component_path_list:
                tasks.append(
                    asyncio.create_task(
                        upload_component(
                            session,
                            repo_url,
                            repo_format,
                            component,
                        )
                    )
                )
            await asyncio.gather(*tasks)
