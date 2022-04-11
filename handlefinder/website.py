# standard imports
import json
import re

# third party imports
from attrs import define, field

# local imports
from .handle_extractor import HandleExtractorFactory
from .helpers import get_specific_url
from .html_getter import HtmlGetter
from .url_extractor import HrefUrlExtractor

html_getter = HtmlGetter()


@define
class Website:
    main_url: str
    find_handles: str
    html: str = field(init=False)
    href_urls: list[str] = field(init=False)
    handles: str = field(init=False)

    def __attrs_post_init__(self):
        self.html = html_getter(self.main_url).html_text
        self.href_urls = HrefUrlExtractor(self.html).href_urls
        self._filter_href_urls()
        self._extract_handles()

    def _fix_href_url(self, href_url: str) -> str:
        if href_url.startswith("/"):
            href_url = self.main_url[:-1] + href_url
        return href_url

    def _filter_href_urls(self) -> None:
        self.href_urls = [
            self._fix_href_url(href_url)
            for href_url in self.href_urls
            if re.match(f".*({self.find_handles}).*", href_url)
        ]

    def _extract_handles(self) -> None:
        handles = {}

        for handle in self.find_handles.split("|"):
            if href_url := get_specific_url(self.href_urls, handle):
                handle_extractor = HandleExtractorFactory.create(
                    handle, href_url=href_url
                )
                extracted_handle = handle_extractor.extract()
                handles[handle] = extracted_handle

        self.handles = json.dumps(handles)
