import requests

url = "https://bet365-futebol-virtual.p.rapidapi.com/last/league/2"

headers = {
	"X-RapidAPI-Key": "558ae27720msh716e7500a9515a7p1b4072jsn50f47b5b2b17",
	"X-RapidAPI-Host": "bet365-futebol-virtual.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())