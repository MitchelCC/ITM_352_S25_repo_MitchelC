from bs4 import BeautifulSoup
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://shidler.hawaii.edu/itm/people"


try: 
#fetching webpage
    response = urllib.request.urlopen(url)
    html_content = response.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    print(f"Type of object returned: {type(soup)}")
    print("\nFirst few lines of prettified HTML:")
    print(soup.prettify()[:500])  # Print the first 500 characters of prettified HTML

except Exception as e:
    print(f"An error occurred: {e}")
