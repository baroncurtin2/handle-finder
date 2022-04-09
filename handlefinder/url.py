# third party imports
from attrs import Factory, define, field

# local imports
from .url_getter import UrlGetter
from .extractor import HrefUrlExtractor

url_getter = UrlGetter()
extractor = HrefUrlExtractor()


@define
class Url:
    main_url: str
    html: str = field(init=False)
    href_urls: list[str] = field(init=False)

    def __attrs_post_init__(self):
        self.html = url_getter(self.main_url).html
        self.href_urls = extractor(self.html)
