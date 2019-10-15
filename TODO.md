TOP TODO:
=========
  - Pulumi the Event Source Mappings
  - Deploy a 2nd Stack
  - Parse each of the Message Types in the Log Watching
  - Clean Up the Main Bot Code
  - Start having them monitor 10+ characters at a time
  - Start Using the God Bot Properly
  - Add a Better Dungeon Crawl Overview
  - Compare Files before saving in s3
  - Add X-Ray
  - Add a Fargate twitch IRC bot listening for all messages
  - Hook up local IRC to the Lambda Architecture
  - Fix Tests and Add Many More
  - Add SNS fitering on message type


QA Section:
===========
   - Server Gods Version


TODO:
=====
  - Respond to all IRC messages (PING!)
  - Figure out a cool plan for color library
  - Build a system for banning users from calling commands
  - Add error handling around the program crashing
  - Update the README


Deployment TODO:
================
  - Figure a way to encrypt Secrets with KMS using Pulumi for Oauth token
  - Create Lambda that has S3 Event Source for picking up and Parsing new Morgue Files
  - Have a Lambda call out to SNS -> SNS Topic -> SQS -> SQS Event Source Lambda for different Bot Commands
  - Use Lambda Layers


Dungeon Crawl Specific Features:
================================
  - We need to update Overview, like give us some details about the character for real, like an overview
  - Add a system for calculating your max resistances
  - Add a system for calculating max weapon amounts
  - Make the bot Celebrate Level upgrades
  - Add auto dumping RC with Lua for Local Games
  - Figure Out Way to grab a random character from the Crawl Server
  - Add a Equiped command
  - Add a Wands command
  - Extract out what Items are actually worn, and quivered
  - Make sure we Ponging to Pings
  - Add Verbose mode
  - Add a configurable Sleep Time

Goals:
======
  - Easy instructions for others to user
  - Deployed, and the !join system like !lomlobot
  - Every file having some decent tests
  - One of Each Event Source for Lambda
    - Kinesis
    - SQS / SNS
    - DynamoDB
    - S3
    - CloudWatch

