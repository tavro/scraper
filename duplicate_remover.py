from collections import defaultdict
import hashlib
import os


def remove_duplicates(path, hash=hashlib.sha1):
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
