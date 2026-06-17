import urllib.request
import urllib.parse
import json

def search_wikipedia_image(query):
    try:
        # Step 1: Search for the page
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        if not data['query']['search']:
            return None
            
        page_id = data['query']['search'][0]['pageid']
        
        # Step 2: Get the image for the page
        image_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&pageids={page_id}"
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            image_data = json.loads(response.read().decode())
            
        pages = image_data['query']['pages']
        page = pages[str(page_id)]
        
        if 'original' in page:
            return page['original']['source']
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

queries = ["iPhone 15 Pro", "Puzzle Set", "Mechanical Keyboard", "Treadmill"]
for q in queries:
    img = search_wikipedia_image(q)
    print(f"{q}: {img}")
