# ecosystem-snoop

The script fetches Drupal's security RSS feed and prints each entry as a Python
dictionary. Alongside the generic RSS fields, it dynamically extracts Drupal
fields marked with a `field-name-*` CSS class in the entry's HTML description.

Each entry is marked `NEW`, `UNCHANGED`, or `UPDATED` by comparing a stable hash
of its parsed data with the previous run. The local `rss_state.json` file stores
each GUID's hash plus its `first_seen_at` and `last_seen_at` timestamps. This
runtime state is ignored by Git.

Install the small HTML parsing dependency, then run the script:

```sh
python3 -m pip install -r requirements.txt
python3 fetch_drupal_security_rss.py
```

Inspect the public Drupal.org usage data for the M0.3 test project:

```sh
python3 fetch_drupal_project_usage.py
```

Inspect that project's position and nearby projects in Drupal.org's public
cross-project usage listing:

```sh
python3 inspect_drupal_ecosystem_usage.py
```
