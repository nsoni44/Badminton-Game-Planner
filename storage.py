# storage.py
import json
from pathlib import Path
from datetime import datetime, time
from zoneinfo import ZoneInfo

DATA_DIR = Path("JSON")
DATA_DIR.mkdir(exist_ok=True)
TIMEZONE = ZoneInfo("Europe/Tallinn")

def week_name_for_date(dt: datetime):
    iso = dt.isocalendar()  # (year, week, weekday)
    year = dt.year
    weeknum = iso.week
    return f"{year} - WK {weeknum}"

def week_filepath_for_date(dt: datetime):
    name = week_name_for_date(dt)
    return DATA_DIR / f"{name}.json"

def create_week_if_missing(dt: datetime | None = None):
    dt = dt or datetime.now(TIMEZONE)
    fp = week_filepath_for_date(dt)
    if not fp.exists():
        initial = {
            "week": week_name_for_date(dt),
            "created_at": dt.isoformat(),
            "locked": False,
            "players": [],
            "matches": []
        }
        fp.write_text(json.dumps(initial, indent=2))
    return fp

def read_week(dt: datetime | None = None):
    fp = week_filepath_for_date(dt or datetime.now(TIMEZONE))
    if not fp.exists():
        fp = create_week_if_missing(dt)
    return json.loads(fp.read_text()), fp

def save_week(data: dict, dt: datetime | None = None):
    _, fp = read_week(dt or datetime.now(TIMEZONE))
    fp.write_text(json.dumps(data, indent=2))
    return fp

def lock_week(dt: datetime | None = None):
    data, fp = read_week(dt)
    data["locked"] = True
    data["locked_at"] = datetime.now(TIMEZONE).isoformat()
    save_week(data, dt)
    # optionally make file read-only at filesystem level:
    # try:
    #     fp.chmod(0o444)  # read-only for owner/group/others (POSIX)
    # except Exception:
    #     pass
    return data

def is_entry_window_open(dt: datetime | None = None):
    "Return True if today/time is Mon-Thu (inclusive)."
    dt = dt or datetime.now(TIMEZONE)
    # Python weekday(): Monday=0 ... Sunday=6
    wd = dt.weekday()
    return wd in (0,1,2,3)  # Mon(0) Tue Wed Thu(3)

def now_is_past_thursday_end(dt: datetime | None = None):
    dt = dt or datetime.now(TIMEZONE)
    # If current weekday > 3 then past Thu
    return dt.weekday() > 3
