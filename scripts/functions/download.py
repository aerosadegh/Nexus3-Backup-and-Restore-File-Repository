import asyncio
from pathlib import Path
from urllib.parse import urlparse


import aiohttp
from tqdm import tqdm

from .repository import Repository


COMPONENTS_ROUTE = "/service/rest/v1/components"


async def _download_components(component_list, destination: str):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for component in component_list:
            tasks.append(asyncio.create_task(download_component(session, component, destination)))
        await asyncio.gather(*tasks)


async def download_component(session, component, destination):
    async with session.get(component["downloadUrl"]) as response:
        # Check if the response status is OK
        if response.status == 200:
            total = int(response.headers.get("content-length", 0))

            # Parse the URL to get the path
            url_path = urlparse(component["downloadUrl"]).path

            destination_path = Path(destination)
            full_path = destination_path.joinpath(url_path.lstrip("/"))
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if the file already exists and its size is correct
            if full_path.exists() and full_path.stat().st_size == total:
                print(f"File {component['path']} already exists and is correct. Skipping download.")
                return
            print(f"\nDownloading {component['path'].split('/')[-1]}  {total:,} bytes")
            progress_bar = tqdm(total=total, unit="B", unit_scale=True)

            # Write the data to a file
            with open(full_path, "wb") as f:
                chunk_size = 1024  # 1 KB
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    progress_bar.update(len(chunk))

            progress_bar.close()

        else:
            # Print the response status and reason
            print(f"Download failed: {response.status} - {response.reason}")


async def _add_components(repo: Repository, items):
    tasks = []
    for item in items:
        tasks.extend([asyncio.create_task(repo.add_item(asset)) for asset in item["assets"]])
    await asyncio.gather(*tasks)


async def _pop_components(repo: Repository, destination: str):
    component_list = []
    while not repo.queue.empty():
        component = await repo.pop_item()
        component_list.append(component)
        if len(component_list) >= 5:
            await _download_components(component_list, destination)
            component_list = []

    if component_list:
        await _download_components(component_list, destination)


async def _wait_for_components(repo: Repository):
    while not repo.queue.empty():
        await asyncio.sleep(1)


async def get_repository_components(
    nexus_base_url: str,
    repo_name: str,
    username: str,
    password: str,
    destination: str,
):
    repo_url = f"{nexus_base_url}{COMPONENTS_ROUTE}?repository={repo_name}"
    # Create a session object with the authentication header
    auth = aiohttp.BasicAuth(username, password) if username and password else None

    # Create a Repository object
    repo = Repository()

    async with aiohttp.ClientSession(auth=auth) as session:
        continuation_token = None

        while True:
            params = {}
            if continuation_token:
                params["continuationToken"] = continuation_token

            async with session.get(repo_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    # Add the components to the repository
                    add_task = asyncio.create_task(_add_components(repo, [item for item in data["items"]]))

                    # Wait for all components to be added to the repository
                    await asyncio.create_task(_wait_for_components(repo))

                    # Pop the components from the repository and download them
                    pop_task = asyncio.create_task(_pop_components(repo, destination))

                    # Wait for both tasks to complete
                    await asyncio.gather(add_task, pop_task)

                    # Get the continuation token for the next page
                    continuation_token = data.get("continuationToken")

                    # If there is no continuation token, break the loop
                    if not continuation_token:
                        break

                else:
                    print(f"Request failed: {response.status} - {response.reason}")
                    break
