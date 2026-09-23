#!/usr/bin/env python3
"""Fetch Drupal's security RSS feed and print each entry as a dictionary."""

from pprint import pprint
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


FEED_URL = "https://www.drupal.org/security/all/rss.xml"
DC_NAMESPACE = "http://purl.org/dc/elements/1.1/"


def text(entry: ET.Element, field: str) -> str | None:
    element = entry.find(field)
    return element.text.strip() if element is not None and element.text else None


def parse_entry(entry: ET.Element) -> dict[str, str | None]:
    description = text(entry, "description")
    parsed = {
        "title": text(entry, "title"),
        "link": text(entry, "link"),
        "description": description,
        "pubDate": text(entry, "pubDate"),
        "creator": text(entry, f"{{{DC_NAMESPACE}}}creator"),
        "guid": text(entry, "guid"),
    }

    soup = BeautifulSoup(description or "", "html.parser")
    for element in soup.find_all(class_=True):
        field_class = next(
            (name for name in element.get("class", []) if name.startswith("field-name-")),
            None,
        )
        if field_class:
            value_element = element.select_one(".field-items") or element
            parsed[field_class] = value_element.get_text(" ", strip=True)

    return parsed


def main() -> None:
    request = Request(FEED_URL, headers={"User-Agent": "ecosystem-snoop/0.1"})
    with urlopen(request, timeout=30) as response:
        root = ET.parse(response).getroot()

    entries = [parse_entry(entry) for entry in root.findall("./channel/item")]
    pprint(entries, sort_dicts=False)


if __name__ == "__main__":
    main()
