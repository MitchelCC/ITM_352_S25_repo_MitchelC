import urllib.request
import ssl

# Bypass ssl verification
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data"

try:
    with urllib.request.urlopen(url) as response:
        html_lines = response.readlines()
        
        print("Lines containing <title> tags:")
        for line in html_lines:
            decoded_line = line.decode('utf-8')
            if '<title>' in decoded_line.lower():
                print(decoded_line.strip())
                
except Exception as e:
    print(f"Error occurred: {e}")