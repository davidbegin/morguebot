import difflib

import json


{
    "Version": "2012-10-17",
    "Id": "MorgueFileBucketPolicy",
    "Statement": [
        {
            "Sid": "Allow",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::851075464416:role/morgue-bot-lambda-role-782df96",
                    "arn:aws:iam::851075464416:role/morgue-stalker-role-39eb325",
                ]
            },
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::morgue-files-2944dfb/*",
        }
    ],
}


{
    "Version": "2012-10-17",
    "Id": "MorgueFileBucketPolicy",
    "Statement": [
        {
            "Sid": "AllowThingsInTheBucket",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::851075464416:role/morgue-bot-lambda-role-782df96",
                    "arn:aws:iam::851075464416:role/morgue-stalker-role-39eb325",
                ]
            },
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::morgue-files-2944dfb/*",
        },
        {
            "Sid": "AllowTheBucket",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::851075464416:role/morgue-bot-lambda-role-782df96",
                    "arn:aws:iam::851075464416:role/morgue-stalker-role-39eb325",
                ]
            },
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::morgue-files-2944dfb",
        },
    ],
}

d = difflib.Differ()
result = list(d.compare(x, y))
print(result)
