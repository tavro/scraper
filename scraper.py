from __future__ import print_function
from bs4 import BeautifulSoup
from string import ascii_lowercase
from urllib.request import Request, urlopen
from collections import defaultdict

import lxml
import os
import sys
import string
import random
import hashlib


done = 0
total = 0
counter = 732906715


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
    urls = get_urls(total)

    for url in urls:
        download(url)
    check_for_duplicates(os.getcwd() + "/")

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
        global counter
        counter += 1
        # noise = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        noise = decimal_to_36(counter)
        url = "https://prnt.sc/" + noise.lstrip("0")
        if url not in urls:
            urls.append(url)
        print(url)
    return urls


def encode_36(num):
    """
    Encodes decimal integer number into base 36
    """
    alphabet, base36 = ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', '']

    while num:
        num, i = divmod(num, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]


def decode_36(num_36):
    """
    Decodes base 36 number into decimal integer
    """
    return int(num_36.upper(), 36)


def decimal_to_36(num):
    """
    Formats number to fit prnt.sc url
    """
    return encode_36(num).lower()


def chunk_reader(f, chunk_size=1024):
    """
    Reads a file in chunks of bytes
    """
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    """
    Gets hash of file
    """
    obj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        obj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            obj.update(chunk)
    hashed = obj.digest()

    file_object.close()
    return hashed


def check_for_duplicates(path, hash=hashlib.sha1):
    """
    Check for dublicate files in given path
    """
    hashes_by_size = defaultdict(list)
    hashes_on_1k = defaultdict(list)
    hashes_full = {}

    for dirpath, dirnames, filenames in os.walk(path):
        # find files with same size
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                # target is symlink, dereference it, change value to target file
                full_path = os.path.realpath(full_path)
                file_size = os.path.getsize(full_path)
                hashes_by_size[file_size].append(full_path)
            except (OSError,):
                continue

    # for files with same size, get hash of first 1024 bytes
    for size_in_bytes, files in hashes_by_size.items():
        if len(files) < 2:
            continue

        for filename in files:
            try:
                small_hash = get_hash(filename, first_chunk_only=True)
                # key = hash on first 1024 bytes + size
                hashes_on_1k[(small_hash, size_in_bytes)].append(filename)
            except (OSError,):
                continue

    amount = 0
    duplicates = []

    # for files with hash of first 1024 bytes, get full hash
    for __, files_list in hashes_on_1k.items():
        if len(files_list) < 2:
            continue

        for filename in files_list:
            try:
                full_hash = get_hash(filename, first_chunk_only=False)
                duplicate = hashes_full.get(full_hash)
                if duplicate:
                    if filename not in duplicates:
                        duplicates.append(filename)
                    amount += 1
                else:
                    hashes_full[full_hash] = filename
            except (OSError,):
                continue

    for duplicate in duplicates:
        os.remove(duplicate)
    if amount > 0:
        print(amount, "duplicate(s) found and deleted")


if __name__ == "__main__":
    main()
