#Pre Reqs
#pip install bcrypt
#pip install requests


import requests
from requests import api
from requests.models import Response
from datetime import datetime
import bcrypt
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#URL of the Http Request
url = "https://knobbe.foundation.litera.com/api/v1/application/metaData" 

#API Key found under Admin > Integration > Foundation API Keys
apiKey = "0f500c90-9df1-4bd4-b789-b89f1a1bcf65"

#API Key name found uder Admin > Integrations > Foundation API Keys
apiKeyName = "knobbe-apikey"

#AdUserPrincipalName of the user you are impersonating
impersonateUser = ""

timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ") #2023-05-26T15:16:21.1055946Z
print(timestamp) 

apiKeyAndTimestamp = apiKey + "|" + timestamp
print(apiKeyAndTimestamp)

salt = bcrypt.gensalt()
hash = bcrypt.hashpw(apiKeyAndTimestamp.encode('utf-8'), salt).decode('utf-8')

print(hash)


# Build headers, omitting impersonate if empty
headers = {
    "x-foundation-api-key": apiKeyName,
    "x-foundation-timestamp": timestamp,
    "x-foundation-api-auth": hash,
    "accept": "application/json"
}
if impersonateUser:
    headers["x-foundation-impersonate"] = impersonateUser


# Debug: print request details
print("Request URL:", url)
print("Request Headers:", headers)

r = requests.get(url, headers=headers, verify=False)

# Debug: print response details
print("Status Code:", r.status_code)
print("Response Content:", r.content)


