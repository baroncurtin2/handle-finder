# standard imports
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

from handlefinder import Url


# local imports


def main(*urls: str, tokens: list[str] = None) -> list[list[str]]:
    tokens_ = ["facebook", "twitter", "ios", "android|google"]

    if tokens:
        tokens_ += tokens
    tokens_ = "|".join(tokens_)

    websites = download_sites(*urls, tokens=tokens_)
    return [site.href_urls for site in websites]


def download_site(url: str, tokens: str) -> Url:
    return Url(url, tokens)


def download_sites(*urls: str, tokens: str) -> list[Url]:
    download_site_ = partial(download_site, tokens=tokens)

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(download_site_, urls)
    return list(results)


if __name__ == "__main__":
    pprint(
        main("https://www.data.ai/en/", "https://www.zello.com/", "https://zynga.com")
    )
