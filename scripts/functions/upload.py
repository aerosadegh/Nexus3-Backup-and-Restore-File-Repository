import os
import asyncio
from pathlib import Path

import aiohttp


COMPONENTS_ROUTE = "/service/rest/v1/components"


async def upload_component(session, repo_url, source_filename: Path):
    data = aiohttp.FormData()
    data.add_field(
        "pypi.asset",
        open(source_filename, "rb"),
        filename=source_filename.name,
        content_type="application/octet-stream",
    )
    headers = {"accept": "application/json"}

    async with session.post(repo_url, data=data, headers=headers) as response:
        if response.status == 204:
          print(f"Upload {source_filename!r} Successfully!")


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
            component_path_list = [root_path / Path(x) for x in files]
            tasks = []
            for component in component_path_list:
                tasks.append(asyncio.create_task(upload_component(session, repo_url, component)))
            await asyncio.gather(*tasks)
