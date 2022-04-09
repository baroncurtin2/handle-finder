# third party imports
from attrs import Factory, define

# local imports
from .session import GetterSession


@define
class UrlGetter:
    html: str = ""
    session: GetterSession = Factory(GetterSession)

    def __call__(self, url: str) -> "UrlGetter":
        self._get_html(url)
        return self

    def _get_html(self, url: str) -> None:
        response = self.session.get(url)
        self.html = response.text
