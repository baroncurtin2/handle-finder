# standard imports
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

# local imports
from handlefinder import Url


def main(*urls: str) -> list[str]:
    pass


def download_site(url) -> Url:
    return Url(url)


def download_sites(*urls: str) -> list[Url]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(download_site, urls)
    return list(results)


if __name__ == "__main__":
    pprint(
        main("https://www.data.ai/en/", "https://www.zello.com/", "https://zynga.com")
    )
