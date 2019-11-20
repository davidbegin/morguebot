t:
		TEST_MODE=true python3 -m pytest --cov=lib test/ -s
		# (TEST_MODE=true python3 -m pytest --cov=lib test/ -s && python scripts/tests_pass.py) || python scripts/tests_fail.py

f:
		TEST_MODE=true python3 -m pytest test/ -s -m focus
		# (TEST_MODE=true python3 -m pytest test/ -s -m focus && python scripts/tests_pass.py) || python scripts/tests_fail.py

l:
	black deploy/*.py && black lib/ && black test/ && black *.py && black deploy/ --exclude venv && black deploy/modules && black glm/generic_lambda_handler/*.py
	# (black deploy/*.py && black lib/ && black test/ && black *.py && black deploy/ --exclude venv && black deploy/modules) || scripts/tests_fail.py

set_env_vars:
	cd deploy; pulumi stack output --json | jq '.lambda_env_vars' | tee ../.env

dependencies:
	rm -rf build/python
	rm build/dependencies.zip
	rsync -av venv/lib/python3.7/site-packages build \
 		--exclude awscli* \
		--exclude boto3* \
	 	--exclude botocore* \
	 	--exclude pip* \
	 	--exclude pip* \
	 	--exclude setuptools* \
	 	--exclude faker* \
	 	--exclude s3transfer* \
	 	--exclude sixx* \
	 	--exclude websockets* \
	 	--exclude _pytest*
	mv build/site-packages build/python
	cd /Users/begin/code/morguebot/build/; zip -r9 dependencies.zip python

# We needs this to take a random thang
# make artifact ARTIFACT_NAME=handler422.zip
dependencies_2:
	rm -rf build/python
	rm build/dependencies.zip
	rsync -av venv/lib/python3.7/site-packages build \
 		--exclude awscli* \
		--exclude boto3* \
	 	--exclude botocore* \
	 	--exclude pip* \
	 	--exclude pip* \
	 	--exclude setuptools* \
	 	--exclude faker* \
	 	--exclude s3transfer* \
	 	--exclude werkzeug* \
	 	--exclude sixx* \
	 	--exclude Jinja2* \
	 	--exclude jinja2* \
	 	--exclude itsdangerous* \
	 	--exclude markupsafe* \
	 	--exclude click* \
	 	--exclude websockets* \
	 	--exclude _pytest*
	mv build/site-packages build/python
	cd /Users/begin/code/morguebot/build/; zip -r9 dependencies.zip python


# save_deps: dependencies
save_deps:
	aws s3 cp build/dependencies.zip s3://morgue-artifacts/dependencies.zip


ARTIFACT_NAME := handler_$(shell date +%s).zip
# artifact: dependencies
artifact:
	zip -r build/$(ARTIFACT_NAME) lib/
	zip -rg build/$(ARTIFACT_NAME) commands/
	zip -rg build/$(ARTIFACT_NAME) glm/
	zip -g build/$(ARTIFACT_NAME) lambda_handler.py
	zip -g build/$(ARTIFACT_NAME) lambda_commands.json
	zip -g build/$(ARTIFACT_NAME) handler.py


# make artifact_deploy
deploy: l artifact
	aws s3 cp build/$(ARTIFACT_NAME) s3://morgue-artifacts/$(ARTIFACT_NAME)
	cd deploy; source venv/bin/activate; echo $(ARTIFACT_NAME) | pulumi config set artifact_name; pulumi up --yes
	# cd deploy; source venv/bin/activate; echo $(ARTIFACT_NAME) | pulumi config set artifact_name; (pulumi up --yes && python ../scripts/deploy_done.py) || ../scripts/tests_fail.py


invoke:
	aws lambda invoke --function-name bot --payload '{"command":"${COMMAND}", "character":"${CHARACTER}"}' logs/lambda.txt

run_bot:
	# cd deploy; pulumi stack output --json
	python bot.py -c artmatt

