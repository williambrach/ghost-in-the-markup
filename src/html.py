from typing import Union

from bs4 import BeautifulSoup

from src.models import ContentType
from src.utils import bs2md


def parse_from_file(html_path: str) -> BeautifulSoup:
    with open(html_path, encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    return soup


def transform(
    html: BeautifulSoup, transformation: ContentType
) -> Union[BeautifulSoup, str]:
    if transformation == ContentType.HTML:
        return html
    elif transformation == ContentType.TEXT:
        return html.text
    elif transformation == ContentType.MARKDOWN:
        return bs2md(html)
    else:
        raise ValueError(f"Invalid transformation type: {transformation}")
