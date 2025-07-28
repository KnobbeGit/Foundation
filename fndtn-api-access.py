import requests
from requests import api
from requests.models import Response
from dotenv import load_dotenv, dotenv_values
import json
import bcrypt
from datetime import datetime, timezone
from pprint import pprint
from tabulate import tabulate
import csv
import os

# Load environment variables from .env file if it exists
load_dotenv()   

# # Define the base URL and API key for the Foundation API
# base_url = 'https://knobbestaging.foundation.litera.com/'
# api_key = 'knobbe-apikey'
# api_key_value = '0f500c90-9df1-4bd4-b789-b89f1a1bcf65'

# # Define the base URL and API key for the Foundation API
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")
api_key_value = os.getenv("API_KEY_VALUE")

# Use bcrypt to hash the API key with a timestamp per Litera documentation
def hash_api_key_with_timestamp():
    #raw_timestamp = datetime.now(timezone.utc)
    #formatted_timestamp = raw_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f0Z")
    instant_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-1] + "0Z"  
    #instant_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-1] + "0Z"  # Ensures 7 places after decimal
    combined = api_key_value + "|" + instant_timestamp
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(combined.encode('utf-8'), salt)
    return hashed, instant_timestamp

hashed_key = hash_api_key_with_timestamp()
headers = {'x-foundation-api-key': api_key, 'x-foundation-timestamp': hashed_key[1], 'x-foundation-api-auth': hashed_key[0], "accept":"application/json"}

# Function to get metadata from the Foundation metadata API endpoint
def get_metadata():
    url = f'{base_url}api/v1/application/metaData/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print({response.status_code})
        #pprint(response.json())
        return response.json()
    else:
        print(f"Error fetching metadata: {response.status_code}")
        return None
    
json_metadata = get_metadata()
data = json.loads(json.dumps(json_metadata, indent=4))

# # Export the full JSON metadata to a file
# json_path = r'C:\Users\jp.laub\Documents\Foundation\API\foundation_metadata_api.json'
# with open(json_path, 'w', encoding='utf-8') as jsonfile:
#     json.dump(data, jsonfile, ensure_ascii=False, indent=4)
# print(f"Metadata JSON exported to {json_path}")

###
# Construct a table listing matter custom fields with their IDs and descriptions
MCFtable = []
# for field in data['matterCustomFieldTypes']:
#     sourceRecordID = field.get('sourceRecordId', '')
#     field_name = field.get('name', '')
#     field_datatype = field.get('dataType', '')
#     field_description = field.get('description', '')
#     MCFtable.append([sourceRecordID, field_datatype, '', field_name, field_description])

# Append the pre-defined matter fields to the table
for field in data['matterFields']:
    field_ID = field.get('name', '')
    field_name = field.get('displayName', '')
    # Check for a match between field_ID and the "id" key in matterObjectTypes
    matched_object = next((obj for obj in data.get('matterObjectTypes', []) if obj.get('id') == field_ID), None)
    if matched_object:
        field_ID = matched_object.get('sourceRecordId', field_ID)
    # Check for a match between field_ID and the "id" key in matterCustomFieldTypes
    matched_object = next((obj for obj in data.get('matterCustomFieldTypes', []) if obj.get('id') == field_ID), None)
    if matched_object:
        field_ID = matched_object.get('sourceRecordId', field_ID)
    field_datatype = field.get('dataTypeName', '')
    field_type = field.get('fieldType', '')
    # If field_ID contains a hyphen, use sourceRecordID instead
    # if '-' in field_ID:
    #     field_name = field.get('displayName', '')
    #     field_ID = field.get('sourceRecordId', field_ID)
    # else:
    #     field_name = field.get('displayName', '')
    field_description = field.get('description', '')
    # Only append if the field_name is not already present in MCFtable (from matterCustomFieldTypes)
    if field_name not in [row[1] for row in MCFtable]:
        MCFtable.append([field_ID, field_datatype, field_type, field_name, field_description])

# Sort the table by sourceRecordID (first column) in ascending order
MCFtable_sorted = sorted(MCFtable, key=lambda x: x[0])
print(tabulate(MCFtable_sorted, headers=["Field ID", "Field Data Type", "Field Type", "Field Name", "Description"], tablefmt="github"))

# Export the sorted table to a CSV file
csv_path = r'\\docs-oc\files\KMOBAPPS\Foundation\MetaData\foundation_matter_custom_fields_api.csv'
with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Field ID", "Field Data Type", "Field Type", "Field Name", "Description"])
    writer.writerows(MCFtable_sorted)
print(f"Matter Custom Field CSV exported to {csv_path}")

###
# Construct a table listing people custom fields with their IDs and descriptions
PCFtable = []
for field in data['personCustomFieldTypes']:
    sourceRecordID = field.get('sourceRecordId', '')
    field_name = field.get('name', '')
    field_description = field.get('description', '')
    PCFtable.append([sourceRecordID, field_name, field_description])

# Append the pre-defined person fields to the table
for field in data['personFields']:
    field_ID = field.get('name', '')
    field_name = field.get('displayName', '')
    field_description = field.get('description', '')
    # Only append if the field_name is not already present in PCFtable (from personCustomFieldTypes)
    if field_name not in [row[1] for row in PCFtable]:
        PCFtable.append([field_ID, field_name, field_description])

# Sort the table by sourceRecordID (first column) in ascending order
PCFtable_sorted = sorted(PCFtable, key=lambda x: x[0])
print(tabulate(PCFtable_sorted, headers=["Field ID", "Field Name", "Description"], tablefmt="github"))

# Export the sorted table to a CSV file
# \\docs-oc\files\KMOBAPPS\Foundation\MetaData
csv_path = r'\\docs-oc\files\KMOBAPPS\Foundation\MetaData\foundation_person_custom_fields_api.csv'
with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Field ID", "Field Name", "Description"])
    writer.writerows(PCFtable_sorted)
print(f"Person Custom Field CSV exported to {csv_path}")
