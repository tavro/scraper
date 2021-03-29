import decimal_to_36
import random
import string


def get_urls(amount, counter):
    """
    Generates a list of random prnt.sc URLs
    """
    urls = []
    for x in range(amount):
        # noise = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        noise = decimal_to_36.decimal_to_36(counter + x)
        url = "https://prnt.sc/" + noise.lstrip("0")
        if url not in urls:
            urls.append(url)
    return urls
