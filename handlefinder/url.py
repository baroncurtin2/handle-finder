# standard imports
import re

# third party imports
from attrs import Factory, define, field

# local imports
from .html_getter import HtmlGetter
from .extractor import HrefUrlExtractor

html_getter = HtmlGetter()
extractor = HrefUrlExtractor()


@define
class Url:
    main_url: str
    tokens: str
    html: str = field(init=False)
    href_urls: list[str] = field(init=False)

    def __attrs_post_init__(self):
        self.html = html_getter(self.main_url).html_text
        self.href_urls = extractor(self.html)
        self._filter_href_urls()

    def _fix_href_url(self, href_url: str) -> str:
        if href_url.startswith("/"):
            href_url = self.main_url[:-1] + href_url
        return href_url

    def _filter_href_urls(self) -> None:
        self.href_urls = [
            self._fix_href_url(href_url)
            for href_url in self.href_urls
            if re.match(f".*({self.tokens}).*", href_url)
        ]
