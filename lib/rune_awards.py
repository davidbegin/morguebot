import os

import boto3

from lib.kinesis import send_chat_to_stream

client = boto3.client("dynamodb")
TABLE_NAME = os.environ.get("CHARACTER_DB", "crawl-characters-f4f0a26")

AWARD_EMOTES = {
    1: "HolidayPresent",
    2: "MaxLOL",
    3: "KAPOW",
    4: "FBtouchdown",
    5: "TwitchVotes",
}

PLACES = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th"}


def alt_rune_awards():
    rune_info = _fetch_all_runes()
    char_runes = [char["runes"] for char in rune_info]
    all_runes = [item for sublist in char_runes for item in sublist]

    rune_counter = {}
    for rune in all_runes:
        if rune in rune_counter:
            rune_counter[rune] = rune_counter[rune] + 1
        else:
            rune_counter[rune] = 1

    sorted_runes = []
    for rune in rune_counter:
        sorted_runes.append({"name": rune, "count": rune_counter[rune]})

    sorted_runes = sorted(sorted_runes, key=lambda k: k["count"])
    sorted_runes.reverse()

    send_chat_to_stream(f"BibleThump Top 5 Least Rare Runes BibleThump")
    for rune in sorted_runes[0:5]:
        print(rune)
        send_chat_to_stream(f"{rune['name']} - Count: {rune['count']}")

    # send_chat_to_stream(f"DxCat Top 5 Rarest Runes DxCat")
    # sorted_runes.reverse()
    # runes = sorted_runes[0:5]
    # for rune in runes:
    #     print(rune)
    #     send_chat_to_stream(f"{rune['name']} - Count: {rune['count']}")


def rune_awards():
    send_chat_to_stream(["PorscheWIN First Annual Rune Awards!!! PorscheWIN"])

    for winner in _top_5_rune_holders():
        send_chat_to_stream(
            f"{AWARD_EMOTES[winner['place']]} {PLACES[winner['place']]} Place - {winner['name']} {AWARD_EMOTES[winner['place']]} Rune Count: {len(winner['runes'])}"
        )


def _top_5_rune_holders():
    runes = _fetch_all_runes()
    runes.reverse()
    return runes[0:5]


def _fetch_all_runes():
    response = client.scan(TableName=TABLE_NAME, Select="ALL_ATTRIBUTES")

    all_runes = []
    for item in response["Items"]:
        character_name = item["character"]["S"]
        if "runes" in item:
            runes = item["runes"]["SS"]
        else:
            runes = []

        all_runes.append({"name": character_name, "runes": runes})
    sorted_runes = sorted(all_runes, key=lambda k: len(k["runes"]))
    sorted_runes.reverse()

    formatted_winners = []
    for index, winner in enumerate(sorted_runes, start=1):
        winner["place"] = index
        formatted_winners.append(formatted_winners)

    sorted_runes.reverse()
    return sorted_runes
