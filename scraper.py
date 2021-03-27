import lxml
import os
import sys
import string
import random

from bs4 import BeautifulSoup
from string import ascii_lowercase
from urllib.request import Request, urlopen

done = 0
total = 0


def main():
    """
    Loops through randomly generated urls and saves their content on disk
    """
    global total
    total = int(sys.argv[1])
    urls = get_urls(total)
    for url in urls:
        download(url)


def download(url):
    """
    Scrapes the given URL
    """
    name = "prnt_" + url[-6:] + ".png"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(urlopen(req).read(), "lxml")
    img = soup.find("img", {"class": "no-click screenshot-image"})
    if img is None:
        return download(get_urls(1)[0])
    src = img.get("src")
    if not src.startswith("https://image.prntscr.com/image/"):
        return download(get_urls(1)[0])
    save_on_disk(src, name, os.getcwd() + "/")


def save_on_disk(img, name, dir):
    """
    Saves image on disk with given name
    """
    global done
    done += 1
    print(f"Downloading {name}...  ({done}/{total})")
    req = Request(img, headers={"User-Agent": "Mozilla/5.0"})
    with open(dir + name, "wb") as f:
        f.write(urlopen(req).read())
    print(f"Successfully downloaded {name}! ({done}/{total})\n")


def get_urls(amount):
    """
    Generates a list of random prnt.sc URLs
    """
    urls = []
    for _ in range(amount):
        noise = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        url = "https://prnt.sc/" + noise
        if url not in urls:
            urls.append(url)
    return urls


if __name__ == "__main__":
    main()
