import requests
import sys

url = f"http://localhost:8080/inspect/{sys.argv[1]}"

payload = {}
headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
