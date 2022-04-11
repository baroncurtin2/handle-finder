# standard imports
from __future__ import annotations

import logging
import re
from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable, ClassVar, Optional, Type

# third party imports
from attrs import define

# local imports
from .helpers import get_specific_url
from .html_getter import HtmlGetter
from .url_extractor import HrefUrlExtractor

# instantiate variables
logger = logging.getLogger()
html_getter = HtmlGetter()


class HandleExtractorFactory:
    registry: ClassVar[dict[str, Type[HandleExtractor]]] = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        @wraps(cls)
        def wrapper(wrapped_class: HandleExtractor) -> HandleExtractor:
            if name in cls.registry:
                logger.warning(
                    f"HandleExtractor {name} already registered. Overwriting..."
                )
            cls.registry[name] = wrapped_class
            return wrapped_class

        return wrapper

    @classmethod
    def create(cls, name: str, **kwargs) -> Optional[HandleExtractor]:
        if name not in cls.registry:
            name = "custom"

        extractor_cls = cls.registry[name]
        return extractor_cls(**kwargs)


@define
class HandleExtractor(ABC):
    href_url: str

    @abstractmethod
    def extract(self) -> str:
        pass


@define
class SimpleHandleExtractor(HandleExtractor):
    def __init__(self, href_url: str) -> None:
        super().__init__(href_url=href_url)

    def extract(self) -> str:
        href_url = self.href_url

        if href_url.endswith("/"):
            href_url = href_url[:-1]

        return href_url.rsplit("/", 1)[-1]


@HandleExtractorFactory.register("facebook")
@define
class FacebookHandleExtractor(SimpleHandleExtractor):
    pass


@HandleExtractorFactory.register("twitter")
@define
class TwitterHandleExtractor(SimpleHandleExtractor):
    pass


@define
class LinkFollowThroughHandleExtractor(HandleExtractor):
    handle_url_substring: str

    def __init__(self, href_url: str, handle_url_substring: str) -> None:
        super().__init__(href_url=href_url)
        self.handle_url_substring = handle_url_substring

    def extract(self) -> str:
        href_url = self.href_url

        if self.handle_url_substring not in href_url:
            href_url = self._get_follow_through_url()
        return href_url.rsplit("/", 1)[-1]

    def _get_follow_through_url(self) -> str:
        html = html_getter(self.href_url).html_text
        href_urls = HrefUrlExtractor(html).href_urls
        return get_specific_url(href_urls, self.handle_url_substring)


@HandleExtractorFactory.register("ios")
@define
class IosHandleExtractor(LinkFollowThroughHandleExtractor):
    handle_url_substring: str = "itunes.apple.com"

    def extract(self) -> str:
        href_url = self.href_url

        if self.handle_url_substring not in href_url:
            href_url = self._get_follow_through_url()
        split_url = href_url.rsplit("/", 1)[-1]
        return split_url.replace("id", "")


@define
class AndroidFollowThroughHandleExtractor(LinkFollowThroughHandleExtractor):
    handle_url_substring: str = "play.google.com/store/apps"

    def __init__(self, href_url: str, handle_url_substring: str) -> None:
        super().__init__(href_url=href_url, handle_url_substring=handle_url_substring)

    def extract(self) -> str:
        href_url = self.href_url

        if self.handle_url_substring not in href_url:
            href_url = self._get_follow_through_url()
        split_href_url = href_url.rsplit("/", 1)[-1]
        return re.sub(r".*\?id=(.*)", r"\1", split_href_url)


@HandleExtractorFactory.register("android")
@define
class AndroidHandleExtractor(AndroidFollowThroughHandleExtractor):
    pass


@HandleExtractorFactory.register("google")
@define
class GoogleHandleExtractor(AndroidFollowThroughHandleExtractor):
    pass


@HandleExtractorFactory.register("custom")
@define
class CustomHandleExtractor(HandleExtractor):
    def extract(self) -> str:
        return self.href_url.rsplit("/", 1)[-1]
