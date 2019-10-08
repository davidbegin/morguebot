

t:
		python3 -m pytest test/ -s

l:
		black lib/
		black test/
		black bot.py
