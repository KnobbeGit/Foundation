#Pre Reqs
#pip install bcrypt
#pip install requests

import requests
from requests import api
from requests.models import Response
from datetime import datetime
import bcrypt
import urllib3
import json
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#URL of the Http Request
url = "https://knobbe.foundation.litera.com/api/v1/application/metaData" 


#API Key and API Key name loaded from .env file
apiKey = os.getenv("API_KEY")
apiKeyName = os.getenv("API_KEY_NAME")

#AdUserPrincipalName of the user you are impersonating
impersonateUser = ""

timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-1] + "0Z"  # Ensures 7 places after decimal

apiKeyAndTimestamp = apiKey + "|" + timestamp
salt = bcrypt.gensalt()
hash = bcrypt.hashpw(apiKeyAndTimestamp.encode('utf-8'), salt).decode('utf-8')


# Build headers, omitting impersonate if empty
headers = {
    "x-foundation-api-key": apiKeyName,
    "x-foundation-timestamp": timestamp,
    "x-foundation-api-auth": hash,
    "accept": "application/json"
}
if impersonateUser:
    headers["x-foundation-impersonate"] = impersonateUser



r = requests.get(url, headers=headers, verify=False)

requestinfo = {
    "timestamp": timestamp,
    "apiKeyAndTimestamp": apiKeyAndTimestamp,
    "hash": hash,
    "request_url": url,
    "headers": headers,
    "status_code": r.status_code,
}

print(json.dumps(requestinfo, indent=2))


# Combine request info and response content into a single JSON object
try:
    response_json = r.json()
except Exception:
    response_json = r.content.decode("utf-8", errors="replace")

output = {
    "request": requestinfo,
    "response": response_json
}

# Save output to a JSON file in the same directory as this script
output_path = os.path.join(os.path.dirname(__file__), "test.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)


