from datetime import date
from pathlib import Path
import re, calendar

birth = date(2004, 8, 13)
today = date.today()
years = today.year - birth.year
months = today.month - birth.month
days = today.day - birth.day
if days < 0:
    months -= 1
    pm = 12 if today.month == 1 else today.month - 1
    py = today.year - 1 if today.month == 1 else today.year
    days += calendar.monthrange(py, pm)[1]
if months < 0:
    years -= 1
    months += 12

path = Path(__file__).resolve().parents[1] / "README.md"
text = path.read_text(encoding="utf-8")
age = f"{years} years, {months} months, {days} days"
text, count = re.subn(r"<!-- AGE_START -->.*?<!-- AGE_END -->",
                      f"<!-- AGE_START -->{age}<!-- AGE_END -->", text, count=1)
if count != 1:
    raise RuntimeError("AGE markers not found")
path.write_text(text, encoding="utf-8")
