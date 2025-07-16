#Pre Reqs
#pip install bcrypt
#pip install requests

import requests
from requests import api
from requests.models import Response
from datetime import datetime

import bcrypt


#URL of the Http Request
url = "https://cs5.foundationsg.com/api/metadata" 

#API Key found under Admin > Integration > Foundation API Keys
apiKey = ""

#API Key name found uder Admin > Integrations > Foundation API Keys
apiKeyName = ""

#AdUserPrincipalName of the user you are impersonating
impersonateUser = ""

timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ") #2023-05-26T15:16:21.1055946Z
print(timestamp) 

apiKeyAndTimestamp = apiKey + "|" + timestamp
print(apiKeyAndTimestamp)

salt = bcrypt.gensalt()
hash = bcrypt.hashpw(apiKeyAndTimestamp.encode('utf-8'), salt)

print(hash)

headers = {"x-foundation-api-auth":hash, "x-foundation-timestamp":timestamp, "x-foundation-api-key":apiKeyName, "x-foundation-impersonate":impersonateUser, "accept":"application/json"}

r = requests.get(url, headers=headers)
print(r.content)


