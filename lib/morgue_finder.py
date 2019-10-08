from lib.morgue_parser import read_morgue_file


def find_morgue_file(
    character=None, local_mode=None, morgue_file_path=None, morgue_url=None
):
    if (character and local_mode) and morgue_file_path is None:
        morgue_file_path = f"/Users/begin/Library/Application Support/Dungeon Crawl Stone Soup/morgue/{character}.txt"
    elif character:
        print("ONLINE MODE!!!")
        morgue_url = f"http://crawl.akrasiac.org/rawdata/{character}/{character}.txt"

    return read_morgue_file(morgue_file_path, morgue_url)
