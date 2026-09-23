#!/usr/bin/env python3
"""Fetch Drupal's security RSS feed and print every field on each entry."""

from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


FEED_URL = "https://www.drupal.org/security/all/rss.xml"


def field_name(tag: str) -> str:
    """Make namespaced XML tags readable without hiding the original field."""
    if tag.startswith("{"):
        namespace, name = tag[1:].split("}", 1)
        return f"{name} ({namespace})"
    return tag


def main() -> None:
    request = Request(FEED_URL, headers={"User-Agent": "ecosystem-snoop/0.1"})
    with urlopen(request, timeout=30) as response:
        root = ET.parse(response).getroot()

    entries = root.findall("./channel/item")
    print(f"Feed: {FEED_URL}")
    print(f"Entries: {len(entries)}")

    for number, entry in enumerate(entries, start=1):
        print(f"\n{'=' * 80}\nEntry {number}\n{'=' * 80}")
        for field in entry:
            value = "".join(field.itertext()).strip()
            print(f"{field_name(field.tag)}:")
            print(value or "(empty)")
            if field.attrib:
                print(f"attributes: {field.attrib}")


if __name__ == "__main__":
    main()
