import requests
import os
import glob
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import simplejson as js

# Parameters
url = "https://www.bing.com/images/search"
search = input("What are u looking for? ")
params = {"q": search}

# If your search request is denied, use headers parameter
# In my case, I need headers
headers = {"User-agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/60.0.3112.90 Safari/537.36'}

# Send the request and get the response in r
r = requests.get(url, params, headers=headers)

# Create a nested/tree structure of the HTML data, so we can extract data through string processing
soup = BeautifulSoup(r.text, "html.parser")
# print(soup.prettify())

links = soup.findAll("a", {"class": "iusc"})
print("Results:", len(links))

# The folder containing the pictures.
# If it doesn't exist, it is created. If it exists, I delete all files in it before I get the new pics.
mydir = "images"
if not os.path.exists(mydir):
    os.mkdir(mydir)
else:
    file_list = glob.glob(os.path.join(mydir, "*"))
    for f in file_list:
        os.remove(f)

for link in links:
    # Convert from string to json
    m = js.loads(link.attrs['m'])
    # Now, you can access the value through the key
    murl = m['murl']
    name = murl.split('/')[-1]
    r = requests.get(url=murl, headers=headers)
    img = Image.open(BytesIO(r.content))
    img.save("./" + mydir + "/" + name, img.format.lower())
    print("Image:", murl)

