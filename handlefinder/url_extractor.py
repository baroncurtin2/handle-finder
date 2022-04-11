# standard imports
import re
from abc import ABC, abstractmethod

# third party imports
from attrs import define, field


@define
class ATagExtractor:
    html_text: str
    pattern = r"<a.*?>"
    a_tags: list[str] = field(init=False, factory=list)

    def __attrs_post_init__(self):
        self.a_tags = re.findall(self.pattern, self.html_text)


@define
class HrefUrlExtractor:
    html_text: str
    pattern = r"href=['\"]([^'\"\s]+?)['\"]"
    href_urls: list[str] = field(init=False, factory=list)

    def __attrs_post_init__(self):
        self.href_urls = re.findall(self.pattern, self.html_text)
