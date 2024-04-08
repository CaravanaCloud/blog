#!/usr/bin/env python3

import os
import logging
import requests
import frontmatter

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def post_exists(filepath):
    """Check if the post corresponding to the given filepath has already been submitted by looking for a .lock file."""
    lock_file_path = filepath + ".lock"
    try:
        with open(lock_file_path, 'r') as lock_file:
            article_id = lock_file.read().strip()
            # If the file exists and contains a non-empty article ID, we assume the post exists
            if article_id:
                print(f"Post corresponding to '{filepath}' has been submitted. Article ID: {article_id}")
                return True
    except FileNotFoundError:
        # If the .lock file does not exist, the post has not been submitted
        pass
    
    print(f"No submission record found for '{filepath}'.")
    return False

    
def submit_post(filepath):
    # Fetch the API key from the environment variable
    api_key = os.getenv('DEVTO_API_KEY')
    
    if not api_key:
        logging.error("DEVTO_API_KEY environment variable not set.")
        return

    # Read the content of the Markdown file
    with open(filepath, 'r', encoding='utf-8') as file:
        post = frontmatter.load(file)
        content = post.content
        metadata = post.metadata
        canonical_url = metadata.get('canonical_url', None)
        if(post_exists(filepath)):
            logging.info(f"Post already exists on Dev.to: {filepath}")
            return
    
        title = metadata.get('title', 'Untitled Post')
        published = metadata.get('published', False)
        cover_image = metadata.get('cover_image', None)
        tags = metadata.get('tags', [])
        # Prepare the API request
        headers = {
            "api-key": api_key,
            "Content-Type": "application/json",
        }
        data = {
            "article": {
                "title": title,
                "published": published,
                "body_markdown": content,
                "canonical_url": canonical_url,
                "tags": tags,
                "cover_image": cover_image,
            }
        }
        
        # Send the request to Dev.to
        response = requests.post("https://dev.to/api/articles", json=data, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 201:
            logging.info(f"Successfully submitted post: {filepath}")
            article_data = response.json()
            article_id = article_data['id']
            
            with open(filepath + ".lock", 'w') as lockfile:
                lockfile.write(str(article_id))
        else:
            error_body = response.text
            logging.error(f"Failed to submit post: {filepath}. Status code: {response.status_code}")
            logging.error(f"Error response: {error_body}")

def find_posts(directory):
    """Scan the specified directory for .md files and check for corresponding .lock files."""
    for filename in os.listdir(directory):
        # Check if the file is a Markdown file
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            submit_post(filepath)

def main():
    """Main method that calls find_posts with the 'posts/' directory."""
    find_posts("posts/")

if __name__ == "__main__":
    main()

















