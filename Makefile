t:
		python3 -m pytest test/ -s

l:
		black deploy/*.py
		black lib/
		black test/
		black *.py
		black deploy/ --exclude venv
		black deploy/modules

# We needs this to take a random thang
# make artifact ARTIFACT_NAME=handler422.zip
dependencies:
	cd /Users/begin/code/morguebot/.morguebot2/lib/python3.7/site-packages/; zip -r9 ../../../../build/dependencies.zip .;

# artifact: dependencies
artifact:
	cp build/dependencies.zip build/$(ARTIFACT_NAME)
	zip -rg build/$(ARTIFACT_NAME) lib/
	zip -g build/$(ARTIFACT_NAME) lambda_handler.py
	zip -g build/$(ARTIFACT_NAME) morgue_parser.py


# make artifact_deploy ARTIFACT_NAME=handler422.zip
artifact_deploy: artifact
	aws s3 cp build/$(ARTIFACT_NAME) s3://morgue-artifacts/$(ARTIFACT_NAME)
	cd deploy; source venv/bin/activate; echo $(ARTIFACT_NAME) | pulumi config set artifact_name; pulumi up --yes


invoke:
	aws lambda invoke --function-name bot --payload '{"command":"${COMMAND}", "character":"${CHARACTER}"}' logs/lambda.txt

# Not Working
# deps:
# 	virtualenv .morguebotd2
# 	( source /Users/begin/code/morguebot/.mdeploy/bin/activate;)
# 	pip install -r requirements/runtime.txt

