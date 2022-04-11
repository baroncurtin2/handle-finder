# standard imports
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

# local imports
from handlefinder import Website


def main(*website_urls: str, find_links: list[str] = None) -> list[str]:
    find_links_ = ["facebook", "twitter", "ios", "android|google"]

    if find_links:
        find_links_ += find_links
    find_links_ = "|".join(find_links_)

    websites = download_sites(*website_urls, find_links=find_links_)
    return [site.handles for site in websites]


def download_site(url: str, find_links: str) -> Website:
    return Website(url, find_links)


def download_sites(*urls: str, find_links: str) -> list[Website]:
    download_site_ = partial(download_site, find_links=find_links)

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(download_site_, urls)
    return list(results)


if __name__ == "__main__":
    pprint(
        main("https://www.data.ai/en/", "https://www.zello.com/", "https://zynga.com")
    )
