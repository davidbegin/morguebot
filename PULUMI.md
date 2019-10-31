


Things we need to update:
 -   ├─ aws:cloudwatch:EventTarget     morgue-stalker-event-target            delete
 ~   ├─ aws:lambda:EventSourceMapping  god-bot-sqs-esm                        update
 ~   ├─ aws:lambda:Permission          AllowInvocationFromCloudWatch          update
 ~   ├─ aws:iam:RolePolicy             twitch-chat-bot-role-policy            update
 ~   ├─ aws:lambda:EventSourceMapping  weapons-bot-sqs-esm                    update
 ~   ├─ aws:lambda:EventSourceMapping  xl-bot-sqs-esm                         update
 ~   ├─ aws:lambda:EventSourceMapping  twitch-chat-bot-kinesis-very-cool-esm  update
 ~   ├─ aws:lambda:EventSourceMapping  dungeon_gossiper-dynamodb-esm          update



cat policy.txt | sed s/=\>/\\n/ | split -l 1;
cat xaa | sed 's/\s\+$//' | sed s/\"// | sed 's/\"$//' | sed 's/\\\n//g' | sed 's/\\\"/\"/g' | python -m json.tool > initial.json;
cat xab | sed 's/\s\+$//' | sed s/\"// | sed 's/\"$//' | sed 's/\\\n//g' | sed 's/\\\"/\"/g' | python -m json.tool > new.json;
diff initial.json new.json | colordiff
