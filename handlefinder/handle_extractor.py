# standard imports
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import ClassVar, Type, Callable, Optional
from functools import wraps

# third party imports
from attrs import define

# local imports
from .url_extractor import HrefUrlExtractor
from .html_getter import HtmlGetter
from .helpers import get_specific_url

# instantiate variables
logger = logging.getLogger()
html_getter = HtmlGetter()
extractor = HrefUrlExtractor()


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
            logger.warning(f"HandleExtractor {name} not registered. Returning none...")
            return None

        extractor_cls = cls.registry[name]
        return extractor_cls(**kwargs)


@define
class HandleExtractor(ABC):
    href_url: str

    @abstractmethod
    def extract(self) -> str:
        pass


class SimpleHandleExtractor(HandleExtractor):
    def extract(self) -> str:
        return self.href_url.rsplit("/", 1)[-1]


# ["facebook", "twitter", "ios", "android|google"]
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

    def extract(self) -> str:
        href_url = self.href_url

        if self.handle_url_substring not in href_url:
            href_url = self._get_itunes_url()
        return href_url.rsplit("/", 1)[-1]

    def _get_follow_through_url(self) -> str:
        html = html_getter.get(self.href_url)
        href_urls = extractor(html)
        return get_specific_url(href_urls, self.handle_url_substring)


@HandleExtractorFactory.register("ios")
@define
class IosHandleExtractor(LinkFollowThroughHandleExtractor):
    handle_url_substring: str = "itunes.apple.com"


@HandleExtractorFactory.register("android")
@define
class AndroidHandleExtractor(LinkFollowThroughHandleExtractor):
    handle_url_substring: str = "play.google.com"


@HandleExtractorFactory.register("google")
@define
class GoogleHandleExtractor(LinkFollowThroughHandleExtractor):
    handle_url_substring: str = "play.google.com"
