#!/usr/bin/env python3
"""Fetch Drupal's security RSS feed and print each entry as a dictionary."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from pprint import pprint
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


FEED_URL = "https://www.drupal.org/security/all/rss.xml"
DC_NAMESPACE = "http://purl.org/dc/elements/1.1/"
STATE_FILE = Path(__file__).with_name("rss_state.json")


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


def entry_hash(entry: dict[str, str | None]) -> str:
    normalized = json.dumps(
        entry, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def load_state() -> dict[str, dict[str, str]]:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def classify_entries(
    entries: list[dict[str, str | None]], state: dict[str, dict[str, str]]
) -> list[dict[str, str | None]]:
    now = datetime.now(timezone.utc).isoformat()
    results = []

    for entry in entries:
        guid = entry["guid"]
        if not guid:
            raise ValueError("RSS entry is missing its guid")

        digest = entry_hash(entry)
        previous = state.get(guid)
        if previous is None:
            status = "NEW"
            first_seen_at = now
        elif previous["hash"] == digest:
            status = "UNCHANGED"
            first_seen_at = previous["first_seen_at"]
        else:
            status = "UPDATED"
            first_seen_at = previous["first_seen_at"]

        state[guid] = {
            "hash": digest,
            "first_seen_at": first_seen_at,
            "last_seen_at": now,
        }
        results.append({"status": status, **entry})

    return results


def main() -> None:
    request = Request(FEED_URL, headers={"User-Agent": "ecosystem-snoop/0.1"})
    with urlopen(request, timeout=30) as response:
        root = ET.parse(response).getroot()

    entries = [parse_entry(entry) for entry in root.findall("./channel/item")]
    state = load_state()
    results = classify_entries(entries, state)
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    pprint(results, sort_dicts=False)


if __name__ == "__main__":
    main()
