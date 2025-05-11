#COPYRIGHT Zylto11 | 2025 | Liscence under LISCENCE File.
import os
import re
import json

# ————— Config —————
IN_PATH   = r"DataCollection/Data/imported/Raw/dan_remixed_cleaned copy.json" #replace with desired input path
OUT_PATH  = r"DataCollection/Data/imported/Raw/dan_remixed_cleaned.json" #replace with desired output path

IN_Q      = "question" #given key value for the question key value
IN_A      = "answer"  #given value pair for the answer value `value
OUT_Q     = "question" #desired output key value
OUT_A     = "answer" #desired output value `value

# ————— One-time setup —————
# Single-char removals/translations
_translate_table = str.maketrans({
    "\\": None, "/": None,
    "!": " ", "@": " ", "#": " ",
    "^": " ", "`": " ",
})

# Unicode-escape sequences (must run before translate)
_unicode_map = {
    r"\u2014": "_", r"\u2019": "'", r"\u00e9": "e", r"\u0142": "t",
    r"\u0144": "n", r"\u00f2": "o", r"\u00e0": "a", r"\u00f3": "o",
    r"\u00e7": "c", r"\u00f9": "u", r"\u00e6": "ae", r"\u00f8": "o",
    r"\u00fc": "u", r"\u00e1": "a", r"\u00ed": "i", r"\u00f1": "n",
}
_unicode_re = re.compile("|".join(map(re.escape, _unicode_map)))
def _replace_unicode(m): return _unicode_map[m.group(0)]

# Strip HTML entities
_html_re = re.compile(r"&amp;|&#57361;|&#8220;|&#8221;")

# Patterns to **remove** (not drop) emojis and links
_emoji_re = re.compile(
    "[" 
    "\U0001F600-\U0001FAFF"  # emoticons & symbols
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+", flags=re.UNICODE
)
_link_re = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)

def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    # 1) unicode-escape replaces
    s = _unicode_re.sub(_replace_unicode, s)
    # 2) remove emojis & URLs
    s = _emoji_re.sub("", s)
    s = _link_re.sub("", s)
    # 3) single-char translate (slashes, punctuation cleanup)
    s = s.translate(_translate_table)
    # 4) strip HTML entities
    s = _html_re.sub("", s)
    # 5) collapse whitespace
    s = " ".join(s.split())
    # 6) drop any remaining non-ASCII
    s = s.encode("ascii", errors="ignore").decode()
    return s

# ————— Load, clean, and save —————
with open(IN_PATH, "r", encoding="utf-8") as f:
    raw = json.load(f)

cleaned = []

for entry in raw:
    q = entry.get(IN_Q, "")
    a = entry.get(IN_A, "")

    # unwrap singleton lists
    if isinstance(q, list) and len(q) == 1: q = q[0]
    if isinstance(a, list) and len(a) == 1: a = a[0]

    q_clean = clean_text(q)
    a_clean = clean_text(a)

    # Skip only if empty after cleaning
    if not q_clean or not a_clean:
        continue

    cleaned.append({OUT_Q: q_clean, OUT_A: a_clean})

header = {
    "count[remove before merge]": len(cleaned),
    }

cleaned.insert(0, header)

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"Cleaned {len(cleaned)} entries → saved to {OUT_PATH}")
