import lxml
import os
import sys


from bs4 import BeautifulSoup
from random import choice
from string import ascii_lowercase
from urllib.request import Request, urlopen


def main():
    """
    Loops through randomly generated urls and saves their content on disk
    """
    amount = int(sys.argv[1])
    urls = get_urls(amount)
    for url in urls:
        download(url)


def download(url):
    """
    Scrapes the given URL
    """
    name = "prnt_" + url[-6:] + ".png"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(urlopen(req).read(), "lxml")
    img = soup.find("img", {"class": "no-click screenshot-image"}).get("src")
    if not img.startswith("https://image.prntscr.com/image/"):
        return download(get_urls(1)[0])
    save_on_disk(img, name, os.getcwd() + "/")


def save_on_disk(img, name, dir):
    """
    Saves image on disk with given name
    """
    print(f"Downloading {name}...")
    req = Request(img, headers={"User-Agent": "Mozilla/5.0"})
    with open(dir + name, "wb") as f:
        f.write(urlopen(req).read())
    print(f"Successfully downloaded {name}!\n")


def get_urls(amount):
    """
    Generates a list of random prnt.sc URLs
    """
    urls = []
    for x in range(amount):
        noise = "".join([choice(ascii_lowercase) for y in range(2)] + [str(choice(range(10))) for z in range(4)])
        url = "https://prnt.sc/" + noise
        if url not in urls:
            urls.append(url)
    return urls


if __name__ == "__main__":
    main()
