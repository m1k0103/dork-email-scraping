import requests


search_query = "coding books"

api_key = ""
search_engine_id = ""

url = "https://www.googleapis.com/customsearch/v1"
params = {
    "q": search_query,
    "key": api_key,
    "cx":search_engine_id
}


response = requests.get(url, params=params)


results = response.json()
#print(results)

links = []
for item in results["items"]:
    links.append(item["link"])

print(links)