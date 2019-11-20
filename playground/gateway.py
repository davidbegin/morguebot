import requests


url = "https://zl5r1fjaxf.execute-api.us-west-2.amazonaws.com/Stage/xl-bot/cool"
query = ""
# query = "?command=help"

response = requests.get(url + query)
print(response)
print(response.text)
# import pdb; pdb.set_trace()
