"""Generate the fictional sample receipts and the expected extraction CSV.

Needs Pillow (pip install pillow). Every supplier, address and amount
here is invented. The checks at the bottom are the same rules the Make
scenario and the Sheets log apply, so the expected flags come from code,
not from AI.

Usage:
    python make_samples.py
"""

import csv
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "sample" / "receipts"
CSV_PATH = HERE / "sample" / "expected_extraction.csv"

WIDTH = 440
MARGIN = 26
LINE = 22


def font(size, bold=False):
    names = ["consolab.ttf" if bold else "consola.ttf", "courbd.ttf" if bold else "cour.ttf",
             "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"]
    for name in names:
        for folder in ["C:/Windows/Fonts", "/usr/share/fonts/truetype/dejavu", ""]:
            try:
                return ImageFont.truetype(str(Path(folder) / name) if folder else name, size)
            except OSError:
                continue
    return ImageFont.load_default()


F = font(15)
FB = font(17, bold=True)
FS = font(13)

RECEIPTS = [
    {
        "file": "R01-segar-harian.png",
        "supplier": "SEGAR HARIAN PRODUCE",
        "address": ["Gerai 14, Pasar Borong Contoh", "Taman Rekaan, 40000"],
        "date": "2026-10-05", "time": "07:42", "no": "SH-004812",
        "items": [("Tomatoes 5kg", 22.50), ("Onions 10kg", 38.00),
                  ("Cabbage 6kg", 15.60), ("Red chillies 2kg", 24.00)],
        "tax": None, "tax_inclusive": None, "tax_label": None, "rounding": 0.00,
        "printed_total": 100.10, "payment": "CASH", "category": "Ingredients: produce",
        "faded_total": False, "rotate": 0.0,
    },
    {
        "file": "R02-rempah-ratu.png",
        "supplier": "REMPAH RATU SPICE STORE",
        "address": ["No. 3, Lorong Contoh 2", "Bandar Fiksyen, 41000"],
        "date": "2026-10-07", "time": "10:15", "no": "RR-17730",
        "items": [("Turmeric powder 1kg", 18.90), ("Cumin 500g", 14.50),
                  ("Coriander seed 1kg", 16.80), ("Curry powder 2kg", 39.00)],
        "tax": None, "tax_inclusive": None, "tax_label": None, "rounding": 0.00,
        "printed_total": 89.20, "payment": "CASH", "category": "Ingredients: dry goods",
        "faded_total": False, "rotate": 0.6,
    },
    {
        "file": "R03-gas-biru.png",
        "supplier": "GAS BIRU SUPPLY",
        "address": ["Lot 9, Jalan Sampel 5", "Kampung Ilustrasi, 42000"],
        "date": "2026-10-09", "time": "15:03", "no": "GB-2291",
        "items": [("LPG 14kg x3 @26.60", 79.80), ("Delivery", 10.00)],
        "tax": None, "tax_inclusive": None, "tax_label": None, "rounding": 0.00,
        "printed_total": 89.80, "payment": "CASH", "category": "Fuel and gas",
        "faded_total": True, "rotate": -0.8,
    },
    {
        "file": "R04-kotak-hijau.png",
        "supplier": "KOTAK HIJAU PACKAGING",
        "address": ["12A, Jalan Demo 7", "Seksyen Contoh, 43000"],
        "date": "2026-10-12", "time": "11:48", "no": "KH-90514",
        "items": [("Food box 750ml x200", 56.00), ("Paper bag x100", 35.00),
                  ("Cutlery set x200", 30.00)],
        "tax": None, "tax_inclusive": None, "tax_label": None, "rounding": 0.00,
        "printed_total": 131.00, "payment": "DEBIT CARD", "category": "Packaging",
        "faded_total": False, "rotate": 0.4,
    },
    {
        "file": "R05-dapur-kita-hire.png",
        "supplier": "DAPUR KITA EQUIPMENT HIRE",
        "address": ["Unit 2, Jalan Rekaan 11", "Taman Sampel, 44000"],
        "date": "2026-10-14", "time": "09:20", "no": "DK-3318",
        "items": [("Chafing dish hire x6", 90.00)],
        "tax": 7.20, "tax_inclusive": False, "tax_label": "Service Tax 8%", "rounding": 0.00,
        "printed_total": 97.20, "payment": "CREDIT CARD", "category": "Equipment hire",
        "faded_total": False, "rotate": -0.3,
    },
    {
        "file": "R06-segar-harian-again.png",
        "supplier": "SEGAR HARIAN PRODUCE",
        "address": ["Gerai 14, Pasar Borong Contoh", "Taman Rekaan, 40000"],
        "date": "2026-10-05", "time": "07:42", "no": "SH-004812",
        "items": [("Tomatoes 5kg", 22.50), ("Onions 10kg", 38.00),
                  ("Cabbage 6kg", 15.60), ("Red chillies 2kg", 24.00)],
        "tax": None, "tax_inclusive": None, "tax_label": None, "rounding": 0.00,
        "printed_total": 100.10, "payment": "CASH", "category": "Ingredients: produce",
        "faded_total": False, "rotate": 2.2,
    },
]


def centre(draw, y, text, f):
    w = draw.textlength(text, font=f)
    draw.text(((WIDTH - w) / 2, y), text, font=f, fill=(30, 30, 30))


def row(draw, y, left, right, f=F, fill=(30, 30, 30)):
    draw.text((MARGIN, y), left, font=f, fill=fill)
    w = draw.textlength(right, font=f)
    draw.text((WIDTH - MARGIN - w, y), right, font=f, fill=fill)


def dashed(draw, y):
    x = MARGIN
    while x < WIDTH - MARGIN:
        draw.line((x, y, min(x + 6, WIDTH - MARGIN), y), fill=(90, 90, 90), width=1)
        x += 10


def render(r):
    lines = 13 + len(r["items"]) + (1 if r["tax"] else 0)
    height = 40 + lines * LINE + 10
    img = Image.new("RGB", (WIDTH, height), (252, 250, 244))
    d = ImageDraw.Draw(img)
    y = 22
    centre(d, y, r["supplier"], FB); y += LINE + 4
    for a in r["address"]:
        centre(d, y, a, FS); y += LINE - 4
    y += 8
    dashed(d, y); y += 10
    row(d, y, f"Date: {r['date'][8:10]}/{r['date'][5:7]}/{r['date'][0:4]}", f"Time: {r['time']}", FS); y += LINE - 2
    row(d, y, f"Receipt: {r['no']}", "Cashier: 02", FS); y += LINE
    dashed(d, y); y += 10
    for name, amt in r["items"]:
        row(d, y, name, f"{amt:.2f}"); y += LINE
    dashed(d, y); y += 10
    sub = sum(a for _, a in r["items"])
    row(d, y, "Subtotal", f"{sub:.2f}"); y += LINE
    if r["tax"]:
        row(d, y, r["tax_label"], f"{r['tax']:.2f}"); y += LINE
    row(d, y, "Rounding Adj", f"{r['rounding']:.2f}"); y += LINE + 4

    total_y = y
    colour = (205, 203, 196) if r["faded_total"] else (20, 20, 20)
    row(d, y, "TOTAL RM", f"{r['printed_total']:.2f}", FB, colour); y += LINE + 6
    row(d, y, r["payment"], f"{r['printed_total']:.2f}", FS, colour); y += LINE + 4
    dashed(d, y); y += 12
    centre(d, y, "Terima kasih. Thank you.", FS); y += LINE - 4
    centre(d, y, "Goods sold are not returnable", FS)

    if r["faded_total"]:
        # Thermal fade and a smudge over the total and payment lines.
        box = (MARGIN - 6, total_y - 4, WIDTH - MARGIN + 6, total_y + 2 * LINE + 8)
        patch = img.crop(box).filter(ImageFilter.GaussianBlur(3))
        img.paste(patch, box)
        d = ImageDraw.Draw(img)
        d.ellipse((WIDTH - 170, total_y - 8, WIDTH - 40, total_y + 26), fill=(226, 221, 206))

    noise = Image.effect_noise(img.size, 14).convert("RGB")
    img = Image.blend(img, noise, 0.04)
    if r["rotate"]:
        img = img.rotate(r["rotate"], expand=True, fillcolor=(214, 214, 210), resample=Image.BICUBIC)
    canvas = Image.new("RGB", (img.width + 40, img.height + 40), (214, 214, 210))
    canvas.paste(img, (20, 20))
    return canvas


def checks(r):
    """Expected extraction plus the same flag rules the flow applies."""
    total = None if r["faded_total"] else r["printed_total"]
    items_sum = round(sum(a for _, a in r["items"]), 2)
    conf = {"supplier": "high", "date": "high", "total": "low" if r["faded_total"] else "high",
            "tax": "high"}
    unreadable = ["total", "payment_method"] if r["faded_total"] else []
    flags = []
    if total is None:
        flags.append("Missing total")
    for k, v in conf.items():
        if v == "low":
            flags.append(f"Low confidence: {k}")
    if unreadable:
        flags.append("Unreadable: " + ", ".join(unreadable))
    if total is not None:
        tax_extra = (r["tax"] or 0) if r["tax_inclusive"] is False else 0
        expected = items_sum + tax_extra + r["rounding"]
        if abs(total - expected) > 0.01:
            flags.append(f"Total {total:.2f} does not match items {expected:.2f}")
    return {
        "file": r["file"], "supplier": r["supplier"].title(), "date": r["date"], "currency": "MYR",
        "total": "" if total is None else f"{total:.2f}",
        "tax": "" if r["tax"] is None else f"{r['tax']:.2f}",
        "tax_inclusive": "" if r["tax_inclusive"] is None else str(r["tax_inclusive"]).lower(),
        "rounding": f"{r['rounding']:.2f}", "items_sum": f"{items_sum:.2f}",
        "line_items": " | ".join(f"{n} {a:.2f}" for n, a in r["items"]),
        "payment_method": "" if r["faded_total"] else r["payment"].title(), "category": r["category"],
        "conf_supplier": conf["supplier"], "conf_date": conf["date"],
        "conf_total": conf["total"], "conf_tax": conf["tax"],
        "unreadable_fields": ", ".join(unreadable), "flags": "; ".join(flags),
    }


def main():
    random.seed(7)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for r in RECEIPTS:
        render(r).save(OUT_DIR / r["file"])
        rows.append(checks(r))
    # Duplicate rule, same as the Sheets COUNTIFS column: every row that
    # shares supplier + date + total with another row is flagged, so a
    # person decides which copy to keep.
    for out in rows:
        twins = [o["file"] for o in rows if o is not out and o["total"]
                 and (o["supplier"], o["date"], o["total"]) == (out["supplier"], out["date"], out["total"])]
        if twins:
            extra = "Possible duplicate of " + ", ".join(twins)
            out["flags"] = f"{out['flags']}; {extra}" if out["flags"] else extra
        out["status"] = "NEEDS CHECK" if out["flags"] else "OK"
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    for o in rows:
        print(o["file"], o["total"] or "null", o["status"], o["flags"])


if __name__ == "__main__":
    main()
