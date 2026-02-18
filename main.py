"""
Entry point. Run directly or via GitHub Actions.

Usage:
    python main.py

Required env vars (set in .env locally, or GitHub Actions secrets in CI):
    PRONOTE_URL        — e.g. https://YOUR_SCHOOL.index-education.net/pronote/parent.html
    PRONOTE_USERNAME   — your Pronote login
    PRONOTE_PASSWORD   — your Pronote password
    GMAIL_ADDRESS      — your Gmail address
    GMAIL_APP_PASSWORD — 16-char app password from Google
    EMAIL_TO           — recipient email address
"""

import datetime
import os
import sys

from dotenv import load_dotenv

from fetcher import fetch_grades
from mailer import send_report
from report import build_html_report, build_text_report

DAYS = 14


def main() -> None:
    load_dotenv()

    pronote_url = os.environ["PRONOTE_URL"]
    username = os.environ["PRONOTE_USERNAME"]
    password = os.environ["PRONOTE_PASSWORD"]

    print("Connecting to Pronote…")
    try:
        grades_by_child = fetch_grades(pronote_url, username, password, days=DAYS)
    except Exception as exc:
        print(f"ERROR: could not fetch grades — {exc}", file=sys.stderr)
        sys.exit(1)

    total = sum(len(g) for g in grades_by_child.values())
    print(f"Fetched {total} grade(s) across {len(grades_by_child)} child(ren).")

    text_body = build_text_report(grades_by_child, days=DAYS)
    html_body = build_html_report(grades_by_child, days=DAYS)

    today = datetime.date.today()
    subject = f"Notes Pronote — semaine du {(today - datetime.timedelta(days=DAYS)).strftime('%d/%m')} au {today.strftime('%d/%m/%Y')}"

    print("Sending email…")
    try:
        send_report(subject=subject, text_body=text_body, html_body=html_body)
    except Exception as exc:
        print(f"ERROR: could not send email — {exc}", file=sys.stderr)
        sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    main()
