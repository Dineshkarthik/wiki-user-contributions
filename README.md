# wiki-user-contributions
Generate a table of the user's contributions on Wikimedia's projects.

The generated table can be exported as a CSV file as well.

Inspired from - https://github.com/tshrinivasan/wiki_user_contributions_report

## Installation

```sh
$ pip install -r requirements.txt
```

## Execution

```sh
$ python app.py
```

> For production deployment use any wsgi server. Ex: `gunicorn app:app.server`.
