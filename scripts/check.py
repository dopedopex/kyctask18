"""Checks every deliverable before it is pushed. Exits 1 on any problem.

  - no em dashes, en dashes or look-alikes, and no emoji (brand kit rules)
  - no personal credit inside the deliverables
  - every cited source id exists in the source list, and every listed source is cited
  - every in-page link (#id) points at an element that exists
  - pin.txt is identical to the pin block on the page
  - the pin and the guide use the same wording for questions 2, 3 and 4
  - one "last verified" date everywhere
  - the PDF text passes the same character checks and embeds only the brand fonts

  python3 scripts/check.py            offline checks
  python3 scripts/check.py --online   also fetch every external link and the portal files
"""
import hashlib
import os
import html as htmllib
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = [ROOT / "index.html", ROOT / "evidence.html"]
TEXT_FILES = PAGES + [
    ROOT / "pin.txt",
    ROOT / "style.css",
    ROOT / "README.md",
    ROOT / "sources.md",
    *sorted((ROOT / "src").glob("*.html")),
    *sorted((ROOT / "evidence").glob("*")),
    *sorted((ROOT / "scripts").glob("*")),
]
PDF = ROOT / "KYC-and-Wallet-Activation-Explainer.pdf"
DATE_LONG, DATE_SHORT = "22 October 2026", "22 OCT 2026"

DASHES = re.compile("[" + "".join(chr(c) for c in (0x2010, 0x2011, 0x2012, 0x2013, 0x2014, 0x2015, 0x2212, 0xFE58, 0xFE63, 0xFF0D)) + "]")
EMOJI = re.compile("[" + chr(0x1F000) + "-" + chr(0x1FAFF) + chr(0x2600) + "-" + chr(0x27BF) + chr(0x2B00) + "-" + chr(0x2BFF) + chr(0xFE0F) + "]")
# Extra names to ban can be passed as BANNED_NAMES="name1,name2" so they never sit in a published file.
_names = [re.escape(n.strip()) for n in os.environ.get("BANNED_NAMES", "").split(",") if n.strip()]
CREDIT = re.compile("|".join(_names + ["made by", "created by", "written by", "author:"]), re.I)

problems = []


def scan(name, text, credit=True):
    for i, line in enumerate(text.splitlines(), 1):
        if DASHES.search(line):
            problems.append(f"{name}:{i}: dash character: {line.strip()[:80]}")
        if EMOJI.search(line):
            problems.append(f"{name}:{i}: emoji: {line.strip()[:80]}")
        if credit and CREDIT.search(line):
            problems.append(f"{name}:{i}: personal credit: {line.strip()[:80]}")


for f in TEXT_FILES:
    if f.is_file():
        # README may name the repository, and this script names the banned words.
        scan(f.relative_to(ROOT), f.read_text(encoding="utf-8"), credit=f.name not in ("check.py", "README.md"))

page = (ROOT / "index.html").read_text(encoding="utf-8")

defined = set(re.findall(r'<li id="([se]\d+)">', page))
cited = set(re.findall(r'<sup class="c"><a href="#([se]\d+)">', page))
for missing in sorted(cited - defined):
    problems.append(f"index.html: cites #{missing} but the source list has no such entry")
for unused in sorted(defined - cited):
    problems.append(f"index.html: source {unused} is listed but never cited in the text")

for p in PAGES:
    text = p.read_text(encoding="utf-8")
    ids = set(re.findall(r'\bid="([^"]+)"', text))
    for target in sorted(set(re.findall(r'href="#([^"]+)"', text)) - ids):
        problems.append(f"{p.name}: link to #{target} has no target")
    for local in sorted(set(re.findall(r'(?:href|src)="([^"#:]+)(?:#[^"]*)?"', text))):
        if not (ROOT / local).exists():
            problems.append(f"{p.name}: local file {local} does not exist")
    ev_ids = set(re.findall(r'\bid="([^"]+)"', (ROOT / "evidence.html").read_text(encoding="utf-8")))
    for target in sorted(set(re.findall(r'href="evidence\.html#([^"]+)"', text)) - ev_ids):
        problems.append(f"{p.name}: link to evidence.html#{target} has no target")

m = re.search(r'<pre class="pin" id="pin-text">([\s\S]*?)</pre>', page)
pin_page = htmllib.unescape(m.group(1)).strip() if m else ""
pin_file = (ROOT / "pin.txt").read_text(encoding="utf-8").strip()
if pin_page != pin_file:
    problems.append("pin.txt differs from the pin block in index.html: run node scripts/build.mjs")

same_wording = {
    "question 2": "up to 10 wallets per verified identity. At 10 the portal shows \"Account allocation exhausted.\" and stops you adding more.",
    "question 3": "usually a few minutes, in rare cases a few days. That is the portal's own wording while you wait.",
    "question 4 DAO": "5 July 2026",
    "question 4 network": "18 jurisdictions in clause 15.1",
}
page_text = re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", "", page)))
for label, phrase in same_wording.items():
    if phrase.lower() not in pin_file.lower():
        problems.append(f"pin.txt: missing the {label} wording: {phrase}")
    if phrase.lower() not in page_text.lower():
        problems.append(f"index.html: missing the {label} wording: {phrase}")
if "snapshot.box/#/s:rbnt.eth/proposal/0xa57ccc9a6d554c9e5a1b1ca429ad2affc2e9058f12ea50bce999460f2aea4e02" not in pin_file:
    problems.append("pin.txt: does not link the Snapshot vote")

for f in [ROOT / "index.html", ROOT / "evidence.html", ROOT / "pin.txt", *sorted((ROOT / "src").glob("*.html"))]:
    text = f.read_text(encoding="utf-8")
    for d in set(re.findall(r"\b\d{1,2} (?:[A-Z][a-z]+|[A-Z]{3}) 20\d\d\b", text)):
        if ("verified" in text.lower() or "captured" in text.lower()) and d not in (DATE_LONG, DATE_SHORT) and not d.endswith("July 2026") and not d.endswith("June 2026"):
            problems.append(f"{f.name}: date {d} does not match the last verified date {DATE_LONG}")

if PDF.is_file():
    pdf_text = subprocess.run(["pdftotext", str(PDF), "-"], capture_output=True, text=True).stdout
    scan(PDF.name, pdf_text)
    fonts = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True).stdout
    for line in fonts.splitlines()[2:]:
        name = line.split()[0].split("+")[-1] if line.split() else ""
        if name and not name.startswith(("BeVietnamPro", "JetBrainsMono")):
            problems.append(f"PDF uses font {name}: the brand kit allows only Be Vietnam Pro and JetBrains Mono")
    raw = PDF.read_bytes()
    if b"file://" in raw:
        problems.append("PDF contains file:// links (local build paths): run node scripts/build.mjs")
    for leak in [b"/home/", b"/root/"] + [n.encode() for n in os.environ.get("BANNED_NAMES", "").split(",") if n.strip()]:
        if leak in raw:
            problems.append(f"PDF contains {leak.decode()}")
    if "Account allocation exhausted" not in pdf_text:
        problems.append("PDF looks stale: run node scripts/build.mjs")
else:
    problems.append(f"{PDF.name} missing: run node scripts/build.mjs")

if "--online" in sys.argv:
    urls = sorted(set(re.findall(r'href="(https://[^"]+)"', page + (ROOT / "evidence.html").read_text(encoding="utf-8"))))
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 link-check"})
            code = urllib.request.urlopen(req, timeout=30).status
        except Exception as e:  # noqa: BLE001
            code = getattr(e, "code", str(e))
        if code != 200:
            problems.append(f"link {url} returned {code}")
    portal = {
        "https://access.redbelly.network/_next/static/chunks/pages/index-25986869981a8ae9.js": ["Account allocation exhausted.", 'Number("10")', "(0,I.cb)(3e4)", "Enable account", "Begin identity verification", "Continue with Averer", "Link another wallet"],
        "https://access.redbelly.network/_next/static/chunks/pages/_app-cee7356aa3975380.js": ["could take a few days", "MetaMask and Coinbase Wallet", "create a Testnet account"],
    }
    for url, quotes in portal.items():
        try:
            body = urllib.request.urlopen(url, timeout=30).read()
        except Exception as e:  # noqa: BLE001
            problems.append(f"portal file {url} could not be fetched ({e}). The portal may have shipped a new version: re-capture E1 to E5.")
            continue
        print(f"{url.rsplit('/', 1)[1]} sha256 {hashlib.sha256(body).hexdigest()}")
        for q in quotes:
            if q.encode() not in body:
                problems.append(f"portal file {url} no longer contains: {q}")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"OK: {len(TEXT_FILES)} text files and the PDF passed. {len(defined)} sources, all cited. Pin matches the guide.")
