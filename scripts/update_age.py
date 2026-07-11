from datetime import date
from pathlib import Path
import calendar
import re

BIRTH_DATE = date(2004, 8, 13)
README = Path(__file__).resolve().parents[1] / "README.md"

today = date.today()
years = today.year - BIRTH_DATE.year
months = today.month - BIRTH_DATE.month
days = today.day - BIRTH_DATE.day

if days < 0:
    months -= 1
    previous_month = 12 if today.month == 1 else today.month - 1
    previous_year = today.year - 1 if today.month == 1 else today.year
    days += calendar.monthrange(previous_year, previous_month)[1]

if months < 0:
    years -= 1
    months += 12

age = f"{years} years, {months} months, {days} days"
text = README.read_text(encoding="utf-8")
text, count = re.subn(
    r"(?m)^(\s*age:).*?$",
    lambda m: f"{m.group(1)}{age.rjust(41)}",
    text,
    count=1,
)
if count != 1:
    raise RuntimeError("Age line not found")
README.write_text(text, encoding="utf-8")
