

t:
		python3 -m pytest test/ -s

l:
		black lib/
		black test/
		black bot.py

deps:
	virtualenv .morguebotdeploy
	( source /Users/begin/code/morguebot/.mdeploy/bin/activate;)
	pip install -r requirements/runtime.txt




artifact:
	# cd /Users/begin/code/morguebot/.morguebot/lib/python3.7/site-packages/; zip -r9 ../../../../build/dependencies.zip .;
	# cp build/dependencies.zip build/handler.zip

	zip -rg build/handler.zip lib/
	zip -g build/handler.zip handler.py


deploy: artifact
	 aws lambda update-function-code --function-name bot --zip-file fileb://build/handler.zip


invoke:
	aws lambda invoke --function-name bot --payload '{"command": "${COMMAND}"}' logs/lambda.txt

