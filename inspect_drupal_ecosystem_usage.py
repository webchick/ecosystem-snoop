#!/usr/bin/env python3
"""Find a project's position in Drupal.org's public usage listing."""

from pprint import pprint
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from fetch_drupal_project_usage import fetch_project_usage


LISTING_URL = "https://www.drupal.org/project/usage"


def fetch_listing_page(page: int, sort_week: str | None = None) -> dict:
    query = {"page": page}
    if sort_week:
        query["sort_week"] = sort_week
    url = f"{LISTING_URL}?{urlencode(query)}"
    request = Request(url, headers={"User-Agent": "ecosystem-snoop/0.1"})
    with urlopen(request, timeout=30) as response:
        soup = BeautifulSoup(response, "html.parser")

    table = soup.select_one("table")
    headers = [cell.get_text(" ", strip=True) for cell in table.select("thead th")]
    rows = [
        [cell.get_text(" ", strip=True) for cell in row.find_all("td")]
        for row in table.select("tbody tr")
    ]
    current_rows = [row for row in rows if int(row[1]) > 0]

    last_link = soup.select_one(".pager__item--last a")
    last_page = int(parse_qs(urlparse(last_link["href"]).query)["page"][0])
    week_link = soup.select_one(".pager__item.is-active a")
    week = parse_qs(urlparse(week_link["href"]).query)["sort_week"][0]

    return {
        "headers": headers,
        "rows": current_rows,
        "last_page": last_page,
        "sort_week": week,
    }


def inspect_project(machine_name: str, project_name: str) -> dict:
    project_usage = fetch_project_usage(machine_name)
    usage_count = int(project_usage["tables"][0]["rows"][0][-1])

    first_page = fetch_listing_page(0)
    sort_week = first_page["sort_week"]
    page_size = len(first_page["rows"])
    low, high = 0, first_page["last_page"]

    while low <= high:
        page_number = (low + high) // 2
        page = fetch_listing_page(page_number, sort_week)
        highest = int(page["rows"][0][1])
        lowest = int(page["rows"][-1][1])

        if usage_count > highest:
            high = page_number - 1
        elif usage_count < lowest:
            low = page_number + 1
        else:
            break
    else:
        raise ValueError(f"No listing page contains usage count {usage_count}")

    index = next(
        i for i, row in enumerate(page["rows"]) if row[0] == project_name
    )
    start = max(0, index - 3)
    end = min(len(page["rows"]), index + 4)

    return {
        "dataset_url": LISTING_URL,
        "latest_week": page["headers"][1].removesuffix(" ▼"),
        "project": project_name,
        "usage_count": usage_count,
        "listing_position": page_number * page_size + index + 1,
        "columns": page["headers"],
        "surrounding_projects": [
            {
                "position": page_number * page_size + row_index + 1,
                "values": dict(zip(page["headers"], row)),
            }
            for row_index, row in enumerate(page["rows"][start:end], start=start)
        ],
    }


if __name__ == "__main__":
    pprint(
        inspect_project("ultimate_table_field", "Ultimate Table Field"),
        sort_dicts=False,
    )
