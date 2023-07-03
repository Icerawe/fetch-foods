import requests
import json


with open('secrets.json', 'r') as f:
    data = json.load(f)



def get_category_id():
    wordpress_site = data['wordpress_site']
    url = f"{wordpress_site}/wp-json/wp/v2/categories"



# Read the HTML file
with open('a.html', 'r') as file:
    html_content = file.read()
# Set up authentication credentials
username = data['username']
password = data['password']


# Prepare the content data
content_data = {
    'title': 'My New Post',
    'content': html_content,
    'status': 'publish',
    'categories': [0],  # IDs of the categories the post belongs to
}

# Convert content data to JSON
json_data = json.dumps(content_data)

# Set the API endpoint
api_endpoint = 'https://fetch-foods.com/wp-json/wp/v2/posts'
headers = {
    'Content-Type': 'application/json'
}

# Send a POST request to create a new post
response = requests.post(
    url=api_endpoint, 
    auth=(username, password), 
    json=content_data,
    headers=headers
)

# Check the response
if response.status_code == 201:
    print('Post created successfully.')
else:
    print('Error creating post:', response.text)