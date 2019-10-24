import os
import subprocess


def find_morgue_folder():
    if "DEFAULT_MORGUE_FOLDER" in os.environ:
        DEFAULT_MORGUE_FOLDER = os.environ["DEFAULT_MORGUE_FOLDER"]
    else:
        DEFAULT_MORGUE_FOLDER = f"/Users/{_find_user()}/Library/Application Support/Dungeon Crawl Stone Soup/morgue"

    return os.environ.get("MORGUE_FOLDER", DEFAULT_MORGUE_FOLDER)


def _find_user():
    process = subprocess.Popen("whoami", stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8").strip()
