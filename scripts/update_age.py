from datetime import date
from pathlib import Path
import re

BIRTH_DATE = date(2004, 8, 13)
README_PATH = Path(__file__).resolve().parents[1] / "README.md"

AGE_PATTERN = re.compile(
    r"<!-- AGE_START -->.*?<!-- AGE_END -->",
    flags=re.DOTALL,
)


def calculate_age(birth_date: date, today: date) -> tuple[int, int, int]:
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    if days < 0:
        months -= 1
        previous_month = today.month - 1 or 12
        previous_month_year = today.year if today.month > 1 else today.year - 1

        if previous_month == 12:
            next_month = date(previous_month_year + 1, 1, 1)
        else:
            next_month = date(previous_month_year, previous_month + 1, 1)

        current_month = date(previous_month_year, previous_month, 1)
        days += (next_month - current_month).days

    if months < 0:
        years -= 1
        months += 12

    return years, months, days


def main() -> None:
    today = date.today()
    years, months, days = calculate_age(BIRTH_DATE, today)
    age = f"{years} years, {months} months, {days} days"

    readme = README_PATH.read_text(encoding="utf-8")
    updated_readme, replacements = AGE_PATTERN.subn(
        f"<!-- AGE_START -->{age}<!-- AGE_END -->",
        readme,
        count=1,
    )

    if replacements != 1:
        raise RuntimeError("AGE markers were not found exactly once in README.md")

    README_PATH.write_text(updated_readme, encoding="utf-8")
    print(f"Age updated: {age}")


if __name__ == "__main__":
    main()
