import requests
import os

user_directory = os.path.expanduser("~")

def fast_download_mod(search,version,loader):
    results = requests.get(f"https://api.modrinth.com/v2/search?query={search}&facets=[[\"project_type:mod\"]]")
    project = results.json()["hits"][0]
    if not version in project["versions"]:
        return False,"versionNotSupported"
    if not loader in project["categories"]:
        return False,"loaderNotSupported"

    versions = requests.get(f"https://api.modrinth.com/v2/project/{project["project_id"]}/version")
    for version_data in versions.json():
        if version in version_data["game_versions"] and loader in version_data["loaders"]:
            path = os.path.join(user_directory, "AppData", "Roaming", ".minecraft", "mods", version_data["files"][0]["filename"])

            with open(path, "wb") as f:
                f.write(requests.get(version_data["files"][0]["url"]).content)
            return True,path

    return False,"notFound"
