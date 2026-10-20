"""Monthly Shariah ratio screen for a share watchlist.

Pure Python standard library. No API calls, no AI. The numbers in the
monthly report come from this file (or from the Sheets formulas that
mirror it), never from a language model.

Thresholds follow AAOIFI Shari'ah Standard No. 21, Financial Paper
(Shares and Bonds), clause 3/4:
  3/4/1  the company's stated objects must not include dealing in
         interest or prohibited goods (business-activity screen)
  3/4/2  interest-bearing borrowing must not exceed 30% of market
         capitalisation
  3/4/3  interest-taking deposits must not exceed 30% of market
         capitalisation
  3/4/4  income from prohibited components must not exceed 5% of
         total income
  3/4/6/4 purification per share = total prohibited income divided by
         the number of shares

Other standard setters and index providers use different denominators
and limits. Change the constants below if your adviser uses another
methodology. This is an educational tool, not a fatwa or investment
advice.

Usage:
    python screen.py
    python screen.py path/to/input.csv path/to/output.csv
"""

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_IN = HERE / "sample" / "watchlist_financials.csv"
DEFAULT_OUT = HERE / "sample" / "screening_output.csv"

# Thresholds (AAOIFI SS 21, clauses 3/4/2, 3/4/3, 3/4/4). "Does not
# exceed" means a ratio exactly at the limit passes.
MAX_DEBT_TO_MCAP = 0.30
MAX_DEPOSITS_TO_MCAP = 0.30
MAX_NONPERMISSIBLE_TO_REVENUE = 0.05

PASS, FAIL, REVIEW, MISSING = "PASS", "FAIL", "REVIEW", "DATA MISSING"

NUMERIC_FIELDS = [
    "market_cap_myr_m",
    "interest_bearing_debt_myr_m",
    "interest_bearing_deposits_myr_m",
    "total_revenue_myr_m",
    "non_permissible_income_myr_m",
    "shares_outstanding_m",
]


def to_number(value):
    """Return a float, or None if the cell is blank or not a number."""
    try:
        text = str(value).replace(",", "").strip()
        return float(text) if text else None
    except ValueError:
        return None


def ratio_screen(ratio, limit):
    if ratio is None:
        return MISSING
    return PASS if ratio <= limit else FAIL


def business_screen(flag):
    flag = (flag or "").strip().lower()
    if flag == "permissible":
        return PASS
    if flag == "prohibited":
        return FAIL
    return REVIEW  # "review" or anything unexpected goes to a person


def safe_div(a, b):
    if a is None or b is None or b <= 0:
        return None
    return a / b


def screen_row(row):
    n = {f: to_number(row.get(f)) for f in NUMERIC_FIELDS}

    debt_ratio = safe_div(n["interest_bearing_debt_myr_m"], n["market_cap_myr_m"])
    deposits_ratio = safe_div(n["interest_bearing_deposits_myr_m"], n["market_cap_myr_m"])
    income_ratio = safe_div(n["non_permissible_income_myr_m"], n["total_revenue_myr_m"])

    screens = {
        "business_screen": business_screen(row.get("business_activity")),
        "debt_screen": ratio_screen(debt_ratio, MAX_DEBT_TO_MCAP),
        "deposits_screen": ratio_screen(deposits_ratio, MAX_DEPOSITS_TO_MCAP),
        "income_screen": ratio_screen(income_ratio, MAX_NONPERMISSIBLE_TO_REVENUE),
    }
    values = list(screens.values())

    if FAIL in values:
        overall = FAIL
    elif MISSING in values:
        overall = MISSING
    elif REVIEW in values:
        overall = REVIEW
    else:
        overall = PASS

    notes = []
    failed = [k.replace("_screen", "") for k, v in screens.items() if v == FAIL]
    if failed:
        notes.append("fails: " + ", ".join(failed))
    if MISSING in values:
        notes.append("missing figures, check source data")
    if screens["business_screen"] == REVIEW:
        notes.append("business activity needs a Shariah adviser's view")

    # Purification (SS 21, 3/4/6/4): prohibited income / number of shares.
    # Not shown where the core business itself fails, because the screen
    # result there is to exit rather than purify and hold.
    purification = ""
    if screens["business_screen"] != FAIL:
        per_share = safe_div(n["non_permissible_income_myr_m"], n["shares_outstanding_m"])
        if per_share is not None and per_share > 0:
            purification = f"{per_share:.4f}"
    else:
        notes.append("purification not applicable: core business fails")

    prev = (row.get("prev_status") or "").strip().upper()
    changed = "YES" if prev and prev != overall else "NO"

    def fmt(r):
        return "" if r is None else f"{r:.4f}"

    return {
        "ticker": row.get("ticker", "").strip(),
        "company": row.get("company", "").strip(),
        "debt_ratio": fmt(debt_ratio),
        "deposits_ratio": fmt(deposits_ratio),
        "income_ratio": fmt(income_ratio),
        "prev_debt_ratio": row.get("prev_debt_ratio", "").strip(),
        "prev_deposits_ratio": row.get("prev_deposits_ratio", "").strip(),
        "prev_income_ratio": row.get("prev_income_ratio", "").strip(),
        **screens,
        "overall_status": overall,
        "prev_status": prev,
        "status_changed": changed,
        "purification_per_share_myr": purification,
        "notes": "; ".join(notes),
    }


def main(argv):
    src = Path(argv[1]) if len(argv) > 1 else DEFAULT_IN
    dst = Path(argv[2]) if len(argv) > 2 else DEFAULT_OUT

    with src.open(newline="", encoding="utf-8") as f:
        rows = [screen_row(r) for r in csv.DictReader(f)]

    with dst.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"{'Ticker':<6} {'Debt':>7} {'Dep.':>7} {'Income':>7}  {'Status':<7} {'Prev':<7} Changed  Purif/share")
    for r in rows:
        def pct(x):
            return f"{float(x) * 100:6.2f}%" if x else "    n/a"
        print(
            f"{r['ticker']:<6} {pct(r['debt_ratio'])} {pct(r['deposits_ratio'])} "
            f"{pct(r['income_ratio'])}  {r['overall_status']:<7} {r['prev_status']:<7} "
            f"{r['status_changed']:<8} {r['purification_per_share_myr'] or '-'}"
        )
    print(f"\nWrote {len(rows)} rows to {dst}")


if __name__ == "__main__":
    main(sys.argv)
