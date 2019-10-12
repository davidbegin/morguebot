TODO:
=====
  - Respond to all IRC messages (PING!)
  - Figure out a cool plan for color library
  - Build a system for banning users from calling commands
  - Add error handling around the program crashing


Deployment TODO:
================
  - Ship Artifact with a version number to S3
  - Used S3 Lambda Artifact for Deploying all Lambdas
  - Figure a way to encrypt Secrets with KMS using Pulumi for Oauth token
  - Create Lambda that has S3 Event Source for picking up and Parsing new Morgue Files
  - Have a Lambda call out to SNS -> SNS Topic -> SQS -> SQS Event Source Lambda for different Bot Commands


Dungeon Crawl Specific Features:
================================
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
