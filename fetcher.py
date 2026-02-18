"""
Fetches grades from Pronote for all children linked to a parent account.
"""

import datetime
import pronotepy
from dataclasses import dataclass


@dataclass
class GradeEntry:
    child_name: str
    subject: str
    grade: str
    out_of: str
    coefficient: str
    comment: str
    date: datetime.date
    period: str
    is_bonus: bool
    average: str = ""
    max: str = ""
    min: str = ""


def fetch_grades(
    pronote_url: str,
    username: str,
    password: str,
    days: int = 14,
) -> dict[str, list[GradeEntry]]:
    """
    Log in as a parent and return grades per child for the last `days` days.

    Args:
        pronote_url: Full URL to the Pronote parent page
                     e.g. "https://YOUR_SCHOOL.index-education.net/pronote/parent.html"
        username: Pronote username
        password: Pronote password
        days: How many days back to look (default: 14)

    Returns:
        dict mapping child full name -> list of GradeEntry sorted by date desc
    """
    client = pronotepy.ParentClient(pronote_url, username=username, password=password)
    if not client.logged_in:
        raise RuntimeError("Pronote login failed — check URL, username, and password")

    cutoff = datetime.date.today() - datetime.timedelta(days=days)
    results: dict[str, list[GradeEntry]] = {}

    for child in client.children:
        client.set_child(child)
        child_name = child.name

        grades: list[GradeEntry] = []
        for period in client.periods:
            for g in period.grades:
                if g.date < cutoff:
                    continue
                grades.append(
                    GradeEntry(
                        child_name=child_name,
                        subject=g.subject.name if g.subject else "—",
                        grade=g.grade,
                        out_of=g.out_of,
                        coefficient=g.coefficient,
                        comment=g.comment or "",
                        date=g.date,
                        period=period.name,
                        is_bonus=g.is_bonus,
                        average=g.average,
                        max=g.max,
                        min=g.min,
                    )
                )

        grades.sort(key=lambda x: x.date, reverse=True)
        results[child_name] = grades

    return results
