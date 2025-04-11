import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data"

with urllib.request.urlopen(url) as response:
    print(response)
    html = response.read()
    print(html.decode('utf-8'))