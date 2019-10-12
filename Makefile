t:
		python3 -m pytest test/ -s

l:
		black lib/
		black test/
		black bot.py
		black lambda_handler.py

# Not Working
# deps:
# 	virtualenv .morguebotd2
# 	( source /Users/begin/code/morguebot/.mdeploy/bin/activate;)
# 	pip install -r requirements/runtime.txt

# We needs this to take a random thang
# make artifact ARTIFACT_NAME=handler422.zip
dependencies:
	cd /Users/begin/code/morguebot/.morguebot2/lib/python3.7/site-packages/; zip -r9 ../../../../build/dependencies.zip .;

# artifact: dependencies
artifact:
	cp build/dependencies.zip build/$(ARTIFACT_NAME)
	zip -rg build/$(ARTIFACT_NAME) lib/
	zip -g build/$(ARTIFACT_NAME) lambda_handler.py


# make artifact_deploy ARTIFACT_NAME=handler422.zip
artifact_deploy: artifact
	aws s3 cp build/$(ARTIFACT_NAME) s3://morgue-artifacts/$(ARTIFACT_NAME)
	cd deploy; source venv/bin/activate; echo $(ARTIFACT_NAME) | pulumi config set artifact_name; pulumi up --yes




# cat my_key.pub | pulumi config set publicKey
# make deploy ARTIFACT_NAME=handler422.zip
# deploy:
# 	 # aws lambda update-function-code --function-name bot --zip-file fileb://build/handler.zip


invoke:
	aws lambda invoke --function-name bot --payload '{"command":"${COMMAND}", "character":"${CHARACTER}"}' logs/lambda.txt

