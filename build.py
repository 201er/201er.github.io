#!/usr/bin/env python3
"""
Generate one static page per PDF in invites/ so WhatsApp shows the guest's
name as the link preview title.

Repo layout:
    index.html              <- generic page, also used as the template
    build.py
    invites/Col_LV_Raju.pdf
    ...

Run:    python build.py
Result: Col_LV_Raju/index.html  ->  https://201er.github.io/Col_LV_Raju/

WhatsApp preview: title = guest name only (from the PDF filename,
Col_LV_Raju.pdf -> "Col LV Raju"); description = whatever og:description
says in index.html (Erunootru Onne Eppothum Munne).
"""
import html
import pathlib
import sys

SITE = "https://201er.github.io"
ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = ROOT / "index.html"
INVITES = ROOT / "invites"

# Exact strings in index.html that get replaced for each guest.
HTML_TAG = '<html lang="en" data-guest="">'
TITLE = "<title>Diamond Jubilee Celebrations | 201 Engineer Regiment</title>"
OG_TYPE = '<meta property="og:type" content="website">'
OG_TITLE = '<meta property="og:title" content="Diamond Jubilee Celebrations">'

def name_from_id(gid):
    name = " ".join(gid.replace("_", " ").replace("-", " ").split())
    if name.endswith(" Retd"):
        name = name[:-5] + " (Retd)"
    return name

def main():
    if not TEMPLATE.exists():
        sys.exit("index.html not found next to build.py")
    if not INVITES.is_dir():
        sys.exit("invites/ folder not found")

    tpl = TEMPLATE.read_text(encoding="utf-8")
    for needle in (HTML_TAG, TITLE, OG_TYPE, OG_TITLE):
        if needle not in tpl:
            sys.exit(f"index.html no longer contains this line, update build.py:\n  {needle}")

    count = 0
    for pdf in sorted(INVITES.glob("*.pdf")):
        gid = pdf.stem
        if not all(c.isalnum() or c in "_-" for c in gid):
            print(f"SKIPPED (use only letters, digits, _ and -): {pdf.name}")
            continue

        name = name_from_id(gid)
        n = html.escape(name, quote=True)

        page = (
            tpl.replace(HTML_TAG, f'<html lang="en" data-guest="{gid}">')
               .replace(TITLE, f"<title>{n} | Diamond Jubilee Celebrations</title>")
               .replace(OG_TYPE, f'{OG_TYPE}\n  <meta property="og:url" content="{SITE}/{gid}/">')
               .replace(OG_TITLE, f'<meta property="og:title" content="{n}">')
        )

        out = ROOT / gid
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(page, encoding="utf-8")
        print(f"{SITE}/{gid}/   ->   {name}")
        count += 1

    print(f"\nDone: {count} guest page(s) generated.")


if __name__ == "__main__":
    main()