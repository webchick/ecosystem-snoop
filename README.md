# ecosystem-snoop

The current milestone fetches Drupal's security RSS feed and prints each entry
as a Python dictionary. Alongside the generic RSS fields, it dynamically
extracts Drupal fields marked with a `field-name-*` CSS class in the entry's
HTML description.

Install the small HTML parsing dependency, then run the script:

```sh
python3 -m pip install -r requirements.txt
python3 fetch_drupal_security_rss.py
```
