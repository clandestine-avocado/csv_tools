import requests
import json

def get_repo_urls(username):
    # GitHub API endpoint for user repositories
    url = f"https://api.github.com/users/{username}/repos"
    
    # Send GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        repos = json.loads(response.text)
        
        # Extract and return the URLs
        return [repo['html_url'] for repo in repos]
    else:
        print(f"Error: Unable to fetch repositories. Status code: {response.status_code}")
        return []

# Replace 'your_username' with your actual GitHub username
username = 'clandestine-avocado'

repo_urls = get_repo_urls(username)

# Print the URLs
for url in repo_urls:
    print(url)