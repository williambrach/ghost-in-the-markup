from bs4 import BeautifulSoup
from markdownify import MarkdownConverter


def bs2md(soup: BeautifulSoup, **options) -> str:
    """
    Convert a BeautifulSoup object to Markdown formatted text.
    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing HTML/XML to convert
        **options: Additional conversion options to pass to the MarkdownConverter
    Returns:
        str: The converted text in Markdown format
    Example:
        >>> html = '<h1>Title</h1><p>Some <b>bold</b> text</p>'
        >>> soup = BeautifulSoup(html, 'html.parser')
        >>> bs2md(soup)
        '# Title\\n\\nSome **bold** text'
    """
    return MarkdownConverter(**options).convert_soup(soup)
