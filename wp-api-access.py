import requests
import json
from pprint import pprint

base_url = 'https://www.knobbe.com'
id = 58956
search = 'Hadley'

def get_professional(ID):
    url = f'{base_url}/wp-json/wp/v2/professionals/{id}'

    response = requests.get(url)
    profs_set = response.json()
    return profs_set

def search_professionals(name):
    url = f'{base_url}/wp-json/wp/v2/professionals/?search={search}'

    response = requests.get(url)
    profs_set = response.json()
    return profs_set

#prof_response = get_professional(id)
prof_response = search_professionals(search)
first_response = prof_response[0] if prof_response else None
acf = first_response.get('acf', {}) if first_response else {}
collection_office = acf.get('collection-office', {})
office = collection_office[0].get('office', {})
pprint(f"Collection Office: {collection_office[0].get('office', {}).get('post_title', 'N/A')}")
#print(prof_response)
#print(f"Name: {prof_response[0]["title"]["rendered"]}")
#print(f"Slug: {prof_response[0]["slug"]}")
#print(f"Link: {prof_response[0]["link"]}")
#print(f"First: {prof_response[0]["acf"]["first_name"]}")
#print(f"Office: {prof_response[0]["acf"]["collection-office"]["office"]["post-title"]}")

#if prof_response:
#    print(f"Name: {prof_response["title"]}")
#    print(f"Slug: {prof_response["slug"]}")

#for data in response.json():
    #print(data['title'])
    #print(data['link'])

# Construct the API endpoint URL
#api_url = f"{wordpress_url}/wp-json/wp/v2/{post_type_slug}"

# Add specific post ID if needed
#if post_id:
#    api_url += f"/{post_id}"

# Include ACF fields in the response
#api_url += "?_fields=title,acf" 

#try:
    # Send a GET request to the WordPress REST API
#    response = requests.get(api_url)
#    response.raise_for_status()  # Raise an exception for bad status codes

#    data = response.json()

    # If retrieving all posts, iterate through them
#    if isinstance(data, list):
#        for post in data:
#            print(f"Title: {post['title']['rendered']}")
#            if 'acf' in post:
#                print("ACF Fields:")
#                for field_name, field_value in post['acf'].items():
#                    print(f"  {field_name}: {field_value}")
#    else:  # If retrieving a single post
#        print(f"Title: {data['title']['rendered']}")
#        if 'acf' in data:
#            print("ACF Fields:")
#            for field_name, field_value in data['acf'].items():
#                print(f"  {field_name}: {field_value}")

#except requests.exceptions.RequestException as e:
#    print(f"Error making API request: {e}")