from bs4 import BeautifulSoup
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://shidler.hawaii.edu/itm/people"

try:
    #mimics a real browser request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    #fetching webpage
    response = urllib.request.urlopen(url)
    html_content = response.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    people_sections = soup.find_all('div', class_=['view-content', 'people-listing'])

    people = []
    for section in people_sections:
        items = section.find_all(['div', 'article'], class_=['views-row', 'person-item', 'faculty-member'])
        people.extend(items)
    print ("ITM People Found:")
    for i, person in enumerate(people, 1):
        name_tag = person.select_one('h2.title a, h3.name a, .person-name')
        name = name_tag.get_text(strip=True) if name_tag else "No name found"
        print(f"{i}. {name}")
    print(f"\nTotal number of people found: {len(people)}")
except Exception as e:
    print(f"An error occurred: {e}")