from queue import Queue
from bs4 import BeautifulSoup
import requests
import colorama
from termcolor import colored


# Function to retrieve links on a Wikipedia page
def get_links(page_url, links_dict={}):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('/wiki/') and ':' not in link['href'] and '.' not in link['href'][5:] and '/wiki' in link['href'] and 'Main_Page' not in link['href']:
            url = "https://en.wikipedia.org" + link['href']
            if url not in links_dict:
                links_dict[url] = None
                print(link.get('title', ''))
                yield url


# Function to perform Breadth-First Search
def bfs(start_page, dest_page):
    start_url = "https://en.wikipedia.org/wiki/" + start_page
    dest_url = "https://en.wikipedia.org/wiki/" + dest_page
    visited = {start_url}
    q = Queue()
    q.put([start_url])

    while not q.empty():
        path = q.get()
        node = path[-1]
        print(f"Visiting {node}...")

        if node.lower() == dest_url.lower():
            print(f"Destination page {dest_url} found!")
            return path

        for link in get_links(node):
            if link not in visited:
                visited.add(link)
                new_path = path + [link]
                q.put(new_path)

                if link.lower() == dest_url.lower():
                    print(f"Destination page {dest_url} found!")
                    return new_path

    print(f"Destination page {dest_url} not found.")
    return None


# Prompt the user to enter the start and destination page URLs
start_page = input("Enter the start page name: ").lower().replace(" ", "_")
dest_page = input("Enter the destination page name: ").lower().replace(" ", "_")

# Call the BFS function and print the shortest path
path = bfs(start_page, dest_page)
if path:
    print("The shortest path between", start_page, "and", dest_page, "is:")
    for page in path:
        print(page[30:] + "> ", end='')

else:
    print("No path found between", start_page, "and", dest_page)
