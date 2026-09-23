#!/usr/bin/env python3
"""Fetch and print Drupal.org's public usage data for a project."""

from pprint import pprint
from urllib.parse import quote
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


def fetch_project_usage(machine_name: str) -> dict:
    url = f"https://www.drupal.org/project/usage/{quote(machine_name, safe='')}"
    request = Request(url, headers={"User-Agent": "ecosystem-snoop/0.1"})
    with urlopen(request, timeout=30) as response:
        soup = BeautifulSoup(response, "html.parser")

    tables = []
    for table in soup.select("div.usage table"):
        tables.append(
            {
                "headers": [
                    cell.get_text(" ", strip=True) for cell in table.select("thead th")
                ],
                "rows": [
                    [cell.get_text(" ", strip=True) for cell in row.find_all("td")]
                    for row in table.select("tbody tr")
                ],
            }
        )

    title = soup.select_one("h1")
    return {
        "machine_name": machine_name,
        "url": url,
        "title": title.get_text(" ", strip=True) if title else None,
        "tables": tables,
    }


if __name__ == "__main__":
    pprint(fetch_project_usage("ultimate_table_field"), sort_dicts=False)
