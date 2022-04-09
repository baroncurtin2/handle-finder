# standard imports
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor

# local imports
from handlefinder import URLGetter, HrefUrlExtractor


def main(*urls: str) -> list[str]:
    extractor = HrefUrlExtractor()

    websites = download_sites(*urls)
    return [extractor(site.html) for site in websites]


def download_site(url):
    getter = URLGetter()
    return getter(url)


def download_sites(*urls: str) -> list[URLGetter]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(download_site, urls)
    return list(results)


if __name__ == "__main__":
    pprint(
        main("https://www.data.ai/en/", "https://www.zello.com/", "https://zynga.com")[
            0
        ]
    )
