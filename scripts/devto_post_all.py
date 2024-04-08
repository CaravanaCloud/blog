# TODO
import requests

# Your Dev.to API key
api_key = 'YOUR_API_KEY'

# The endpoint URL for creating articles
url = 'https://dev.to/api/articles'

# Your article data
article_data = {
    "article": {
        "title": "Your Article Title",
        "published": True,
        "body_markdown": "Your article content in Markdown format",
        "tags": ["tag1", "tag2"],  # Optional
        "series": "Series Name",  # Optional
    }
}

# Headers including your API key for authorization
headers = {
    'Content-Type': 'application/json',
    'api-key': api_key
}

# Sending the POST request to create the article
response = requests.post(url, json=article_data, headers=headers)

# Checking the response
if response.status_code == 201:
    print("Article submitted successfully!")
    print("Article URL:", response.json()['url'])
else:
    print("Failed to submit the article.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
