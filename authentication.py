import requests

# Get Authentication Token from Elrond Explorer
url = "https://internal-api.elrond.com/access"

payload={}
headers = {
  'Origin': 'https://explorer.elrond.com',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
}

response = requests.request("POST", url, headers=headers, data=payload)
act = response.headers.get('x-access')

headers = {'x-access': act}
