from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import lxml
import os
import sys

import url_generator
import duplicate_remover


done = 0
total = 0
counter = 0


def main():
    """
    Loops through randomly generated urls and saves their content on disk
    Also removes found duplicate(s)
    """
    global counter
    file1 = open("counter.txt", "r")
    counter = int(file1.readline())
    file1.close()

    global total
    total = int(sys.argv[1])
    urls = url_generator.get_urls(total, counter)

    for url in urls:
        download(url)
    counter += total
    duplicate_remover.remove_duplicates(os.getcwd() + "/")

    file1 = open("counter.txt", "w")
    file1.write(str(counter))
    file1.close()

    file1 = open("counter.txt", "r")
    print("updated counter.txt:", file1.readline())
    file1.close()


def download(url):
    """
    Scrapes the given URL
    """
    global counter
    name = "prnt_" + url[-6:] + ".png"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(urlopen(req).read(), "lxml")
    img = soup.find("img", {"class": "no-click screenshot-image"})
    if img is None:
        counter += 1
        return download(url_generator.get_urls(1, counter)[0])
    src = img.get("src")
    if not src.startswith("https://image.prntscr.com/image/"):
        counter += 1
        return download(url_generator.get_urls(1, counter)[0])
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


if __name__ == "__main__":
    main()
