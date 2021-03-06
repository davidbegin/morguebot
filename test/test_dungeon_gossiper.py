import pytest

from lib.dungeon_gossiper import DungeonGossiper


def test_dungeon_gossiper():
    record = {
        "eventID": "fef6c6b73fe1805ec5d8c82bb6087997",
        "eventName": "MODIFY",
        "eventVersion": "1.1",
        "eventSource": "aws:dynamodb",
        "awsRegion": "us-west-2",
        "dynamodb": {
            "ApproximateCreationDateTime": 1572219318.0,
            "Keys": {"character": {"S": "beginbot"}},
            "NewImage": {
                "character": {"S": "beginbot"},
                "weapons": {
                    "SS": [
                        "a +0 battleaxe (weapon)",
                        "a +0 hand axe",
                        "a +0 short sword of speed",
                        "a +0 spear",
                    ]
                },
            },
            "OldImage": {
                "character": {"S": "beginbot"},
                "weapons": {
                    "SS": [
                        "a +0 battleaxe (weapon)",
                        "a +0 hand axe",
                        "a +0 short sword of speed",
                    ]
                },
            },
            "SequenceNumber": "65363900000000006100979018",
            "SizeBytes": 693,
            "StreamViewType": "NEW_AND_OLD_IMAGES",
        },
        "eventSourceARN": "arn:aws:dynamodb:us-west-2:851075464416:table/characters-696d3eb/stream/2019-10-26T23:46:17.531",
    }
    subject = DungeonGossiper(record)

    new_weapons = subject.new_weapons()
    expected_weapons = ["a +0 spear"]
    assert new_weapons == expected_weapons


@pytest.mark.skip
def test_new_unrands():
    record = {
        "eventID": "fef6c6b73fe1805ec5d8c82bb6087997",
        "eventName": "MODIFY",
        "eventVersion": "1.1",
        "eventSource": "aws:dynamodb",
        "awsRegion": "us-west-2",
        "dynamodb": {
            "ApproximateCreationDateTime": 1572219318.0,
            "Keys": {"character": {"S": "beginbot"}},
            "NewImage": {
                "character": {"S": "beginbot"},
                "weapons": {
                    "SS": [
                        "a +0 battleaxe (weapon)",
                        "a +0 hand axe",
                        "a +0 short sword of speed",
                        "the +12 Vampire's Tooth {vamp}",
                    ]
                },
            },
            "OldImage": {
                "character": {"S": "beginbot"},
                "weapons": {
                    "SS": [
                        "a +0 battleaxe (weapon)",
                        "a +0 hand axe",
                        "a +0 short sword of speed",
                    ]
                },
            },
            "SequenceNumber": "65363900000000006100979018",
            "SizeBytes": 693,
            "StreamViewType": "NEW_AND_OLD_IMAGES",
        },
        "eventSourceARN": "arn:aws:dynamodb:us-west-2:851075464416:table/characters-696d3eb/stream/2019-10-26T23:46:17.531",
    }
    subject = DungeonGossiper(record)
    new_unrands = subject.new_unrands()
    expected_unrands = ["the +12 Vampire's Tooth {vamp}"]
    assert new_unrands == expected_unrands


def test_new_runes():
    # all_runes = [
    #         "abyssal",
    #         "bone",
    #         "dark",
    #         "decaying",
    #         "demonic",
    #         "fiery",
    #         "glowing",
    #         "golden",
    #         "icy",
    #         "iron",
    #         "magical",
    #         "obsidian",
    #         "serpentine",
    #         "silver",
    #         "slimy",
    #         ]

    record = {
        "eventID": "fef6c6b73fe1805ec5d8c82bb6087997",
        "eventName": "MODIFY",
        "eventVersion": "1.1",
        "eventSource": "aws:dynamodb",
        "awsRegion": "us-west-2",
        "dynamodb": {
            "ApproximateCreationDateTime": 1572219318.0,
            "Keys": {"character": {"S": "beginbot"}},
            "NewImage": {
                "character": {"S": "beginbot"},
                "runes": {"SS": ["abyssal", "bone", "dark", "barnacled"]},
            },
            "OldImage": {
                "character": {"S": "beginbot"},
                "runes": {"SS": ["abyssal", "bone", "dark"]},
            },
            "SequenceNumber": "65363900000000006100979018",
            "SizeBytes": 693,
            "StreamViewType": "NEW_AND_OLD_IMAGES",
        },
        "eventSourceARN": "arn:aws:dynamodb:us-west-2:851075464416:table/characters-696d3eb/stream/2019-10-26T23:46:17.531",
    }
    assert DungeonGossiper(record).new_runes() == ["barnacled"]


# def test_no_new_image():
# {"Record
# s": [{"eventID": "9f793a4c9612329edb0da0438409cf8f", "eventName": "REMOVE", "eventVersion": "1.1", "eventSource": "aws:dynamodb", "awsRegion": "us-west-2", "dynamodb": {"ApproximateCreationDateTime": 1572665362.0, "Keys": {"character": {"S": "12feetdeep"}}, "OldImage": {"character": {"S": "12feetdeep"}, "xl_xl": {"
# S": "18"}, "xl": {"S": "3"}, "weapons": {"SS": ["a +0 hand crossbow", "a +2 hand axe (weapon)"]}, "armour": {"SS": [" d - a +0 ring mail (worn)", "Jewellery"]}}, "SequenceNumber": "90159100000000006243112970", "SizeBytes": 136, "StreamViewType": "NEW_AND_OLD_IMAGES"}, "eventSourceARN": "arn:aws:dynamodb:us-west-2:8
# 51075464416:table/characters-696d3eb/stream/2019-10-26T23:46:17.531"}]}
