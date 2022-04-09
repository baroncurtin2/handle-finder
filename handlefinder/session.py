# standard imports
import threading

# third party imports
import requests
from attrs import define, field

# local imports
from .helpers import HEADERS

thread_local = threading.local()


@define
class GetterSession:
    session: requests.Session = field(init=False)

    def __attrs_post_init__(self) -> None:
        self._init_session()

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.session.get(url, **kwargs)

    def _init_session(self) -> None:
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
            thread_local.session.headers.update(HEADERS)
        self.session = thread_local.session
