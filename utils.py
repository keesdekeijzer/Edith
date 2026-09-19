import hashlib
import re


def slugify(text):
    # Unieke maar stabiele ID
    base = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    h = hashlib.md5(text.encode()).hexdigest()[:6]
    return f"{base}-{h}"