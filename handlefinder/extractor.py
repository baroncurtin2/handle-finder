# standard imports
import re
from abc import ABC, abstractmethod

# third party imports
from attrs import define


class Extractor(ABC):
    pattern: str

    def extract(self, text: str) -> list[str]:
        return re.findall(self.pattern, text)


class HrefExtractor(Extractor):
    pattern = r""

    def __call__(self, text: str) -> list[str]:
        return self.extract(text)
