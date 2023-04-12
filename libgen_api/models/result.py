from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup

import requests

MIRROR_SOURCES = [
    "GET",
    "Cloudflare",
    "IPFS.io",
    "Pinata",
]


@dataclass
class Result:
    id: str
    author: str
    title: str
    publisher: str
    year: str
    pages: str
    language: str
    size: str
    extension: str
    mirror_1: str
    mirror_2: str
    mirror_3: str

    @property
    def download_links(self) -> dict[str, str]:
        mirror_1 = self.mirror_1

        response = requests.get(mirror_1)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", string=MIRROR_SOURCES)
        download_links = {link.string: link["href"] for link in links}
        return download_links

    asdict = asdict
