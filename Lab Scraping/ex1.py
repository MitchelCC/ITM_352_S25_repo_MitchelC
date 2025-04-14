import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data"

try:
    response = urllib.request.urlopen(url)
    print(response)
except Exception as e:
    print(f"An error occurred: {e}")