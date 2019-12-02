This is a Bot to interact with your local Morgue file, which will let users in Twitch Chat, to ask questions about various aspects of your game:


## Set Up

```bash
export MORGUEBOT_TWITCH_OAUTH_TOKEN="a token from here https://twitchapps.com/tmi/"
export MORGUEBOT_BOT_NAME="the name of your bot"
export MORGUEBOT_CHANNEL="what channel your bot is going to join"
```

Then you can start the bot
```
python bot.py
```

And in chat `!h?`, should print out the available commands

## Morgue File Finding Options

Here are the the flags used to determine the Morgue File Location.
```
python bot.py --char beginbot
python bot.py -c beginbot
# This will grab the Morgue File from: http://crawl.akrasiac.org/rawdata/beginbot/beginbot.txt

python bot.py --char beginbot --local
python bot.py --char beginbot -l
# This will grab the Morgue Locally using the default morgue location
# /Users/{whoami}/Library/Application Support/Dungeon Crawl Stone Soup/morgue

# Or you can pass in a morgue folder to look for the user locally
MORGUE_FOLDER="/Users/youngthug/songs" python bot.py -c beginbot -l
# /Users/youngthug/songs/beginbot.txt

# OR you can pass in a morgue file directly
python bot.py --morgue-file /Users/youngthug/songs/beginbot.txt

# OR you can pass in a morgue url directly
python bot.py --morgue-url http://crawl.akrasiac.org/rawdata/beginbot/beginbot.txt
```

## Bot Mode:

TODO:

## Command Mode

The `-e` flag or `--exec-cmd` will execute a single command you pass it, instead of starting the bot.
```
python bot.py -e rFire
```

You can disable sending bot messages to twitch and output to STDOUT with `-d` or `--disable-twitch`

```
python bot.py -e mutations -d
```

## Deploying

```
time make artifact_deploy ARTIFACT_NAME=handler_v1.zip
```

## Deployed Architecture

More Info in the [Deploy README](deploy/README.md)

![Morguebot](images/MorgueArch.png)






Invoking the Morgue Stalker

```
aws lambda invoke --function-name morgue-stalker-fce7e1b --payload '{"character":"artmatt"}' output.txt
```

### How do you extract Morguefile Information and save it to DynamoDB:
















