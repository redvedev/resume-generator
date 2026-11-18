import re
from bs4 import BeautifulSoup, NavigableString

# Etykiety nagłówka w różnych językach -> pole. Dopisuj nowe warianty w razie potrzeby.
LABELS = {
    "sender":  ["From", "Od", "Von", "De", "Da", "Van"],
    "date":    ["Sent", "Date", "Wysłano", "Wysłane", "Data", "Gesendet", "Datum",
                "Envoyé", "Enviado", "Inviato", "Verzonden"],
    "to":      ["To", "Do", "An", "À", "A", "Para", "Aan"],
    "cc":      ["Cc", "DW", "Kopia", "Kopie"],
    "subject": ["Subject", "Temat", "Betreff", "Objet", "Asunto", "Oggetto", "Onderwerp"],
    "_ignore": ["Importance", "Priorytet", "Ważność", "Wichtigkeit", "Attachments", "Załączniki"],
}
LABEL_TO_FIELD = {name.lower(): f for f, names in LABELS.items() for name in names}
LABEL_ALT = "|".join(sorted(map(re.escape, LABEL_TO_FIELD), key=len, reverse=True))
HEADER_LINE_RE = re.compile(rf"^\s*\**\s*({LABEL_ALT})\s*\**\s*:\s*\**\s*(.*?)\s*$", re.I)
EMAIL_RE = re.compile(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+")


def _html_to_lines(html):
    if isinstance(html, bytes):
        html = html.decode("utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["style", "script", "head"]):
        t.decompose()
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for t in soup.find_all(["p", "div", "tr", "li", "table", "blockquote", "hr"]):
        t.insert_after(NavigableString("\n"))
    text = soup.get_text().replace("\xa0", " ").replace("\r", "")
    lines = [re.sub(r"^\s*(>\s?)+", "", l).rstrip() for l in text.split("\n")]
    # zwiń wielokrotne puste linie
    out = []
    for l in lines:
        if l.strip() or (out and out[-1].strip()):
            out.append(l)
    return out


def _header_field(line):
    m = HEADER_LINE_RE.match(line)
    return (LABEL_TO_FIELD[m.group(1).lower()], m.group(2)) if m else None


def _is_header_start(lines, i):
    """Linia 'Od:/From:' + w kolejnych liniach min. 3 różne pola (w tym temat lub data)."""
    h = _header_field(lines[i])
    if not h or h[0] != "sender":
        return False
    seen = {h[0]}
    for l in [l for l in lines[i + 1:i + 15] if l.strip()][:8]:
        f = _header_field(l)
        if f:
            seen.add(f[0])
    seen.discard("_ignore")
    return len(seen) >= 3 and ("subject" in seen or "date" in seen)


def _parse_header(lines, i):
    """Czyta pola nagłówka od linii i. Zwraca (pola, indeks początku treści)."""
    fields, last = {}, None
    while i < len(lines):
        line = lines[i]
        f = _header_field(line) if line.strip() else None
        if f:
            if f[0] in fields and f[0] != "_ignore":
                break
            fields[f[0]], last = f[1], f[0]
        elif not line.strip() and "subject" not in fields:
            pass  # pusta linia w środku nagłówka (artefakt HTML)
        elif line.strip() and last in ("to", "cc") and "subject" not in fields:
            fields[last] += " " + line.strip()  # zawinięta lista odbiorców
        else:
            break
        i += 1
    fields.pop("_ignore", None)
    return fields, i


def split_email_html(html):
    """
    Dzieli htmlBody wątku na wiadomości.
    Zwraca listę słowników od najnowszej do najstarszej:
    sender, sender_email, date, to, cc, subject, body.
    Pierwszy element (najnowsza wiadomość) ma puste pola nagłówka - nie ma ich w treści.
    """
    lines = _html_to_lines(html)

    starts = []
    i = 0
    while i < len(lines):
        if _is_header_start(lines, i):
            starts.append(i)
            i = _parse_header(lines, i)[1]
        else:
            i += 1

    parts = []
    bounds = [0] + starts + [len(lines)]
    for k in range(len(bounds) - 1):
        start, end = bounds[k], bounds[k + 1]
        fields, body_start = _parse_header(lines, start) if k > 0 else ({}, start)
        sender = fields.get("sender", "")
        m = (re.search(r"mailto:([^\]\s>]+)", sender, re.I)
             or re.search(r"<([^>]+@[^>]+)>", sender) or EMAIL_RE.search(sender))
        parts.append({
            "sender": sender,
            "sender_email": (m.group(1) if m and m.groups() else m.group(0)) if m else "",
            "date": fields.get("date", ""),
            "to": fields.get("to", ""),
            "cc": fields.get("cc", ""),
            "subject": fields.get("subject", ""),
            "body": "\n".join(lines[body_start:end]).strip(),
        })
    return parts
