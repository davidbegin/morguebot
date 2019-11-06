t:
		TEST_MODE=true python3 -m pytest --cov=lib test/ -s
		# (TEST_MODE=true python3 -m pytest --cov=lib test/ -s && python scripts/tests_pass.py) || python scripts/tests_fail.py

f:
		TEST_MODE=true python3 -m pytest test/ -s -m focus
		# (TEST_MODE=true python3 -m pytest test/ -s -m focus && python scripts/tests_pass.py) || python scripts/tests_fail.py

l:
	black deploy/*.py && black lib/ && black test/ && black *.py && black deploy/ --exclude venv && black deploy/modules
	# (black deploy/*.py && black lib/ && black test/ && black *.py && black deploy/ --exclude venv && black deploy/modules) || scripts/tests_fail.py

set_env_vars:
	cd deploy; pulumi stack output --json | jq '.lambda_env_vars' | tee ../.env

# We needs this to take a random thang
# make artifact ARTIFACT_NAME=handler422.zip
dependencies:
	cd /Users/begin/code/morguebot/.morguebot2/lib/python3.7/site-packages/; zip -r9 ../../../../build/dependencies2.zip .;


run_bot:
	# cd deploy; pulumi stack output --json
	python bot.py -c artmatt

ARTIFACT_NAME := handler_$(shell date +%s).zip
# artifact: dependencies
artifact:
	cp build/dependencies.zip build/$(ARTIFACT_NAME)
	zip -rg build/$(ARTIFACT_NAME) lib/
	zip -g build/$(ARTIFACT_NAME) lambda_handler.py


# make artifact_deploy
deploy: l artifact
	aws s3 cp build/$(ARTIFACT_NAME) s3://morgue-artifacts/$(ARTIFACT_NAME)
	cd deploy; source venv/bin/activate; echo $(ARTIFACT_NAME) | pulumi config set artifact_name; pulumi up --yes
	# cd deploy; source venv/bin/activate; echo $(ARTIFACT_NAME) | pulumi config set artifact_name; (pulumi up --yes && python ../scripts/deploy_done.py) || ../scripts/tests_fail.py


invoke:
	aws lambda invoke --function-name bot --payload '{"command":"${COMMAND}", "character":"${CHARACTER}"}' logs/lambda.txt

# Not Working
# deps:
# 	virtualenv .morguebotd2
# 	( source /Users/begin/code/morguebot/.mdeploy/bin/activate;)
# 	pip install -r requirements/runtime.txt

