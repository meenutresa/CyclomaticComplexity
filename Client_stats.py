import requests as r


#CLient to retrieve the cpu utilization and memory utilzation
url = "http://localhost:8080/stats/"

response = r.get(url)
print(response.text)
