HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 "
        "Safari/537.36 "
    ),
}


def get_specific_url(urls: list[str], get: str) -> str:
    """
    Gets a specific url from a list of urls
    :param urls: list of urls
    :param get: the url to get
    :return: the url
    """
    return next((url for url in urls if get in url), "")
