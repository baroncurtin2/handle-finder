# standard imports
import re
from abc import ABC


class Extractor(ABC):
    pattern: str

    def extract(self, text: str) -> list[str]:
        results = re.findall(self.pattern, text)
        return list(set(results))


class HrefUrlExtractor(Extractor):
    pattern = r"<a\s+(?:[^>]*?\s+)?href=['\"]([^'\"\s]+)['\"]>"

    def __call__(self, html_text: str) -> list[str]:
        return self.extract(html_text)
