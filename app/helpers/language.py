LANGUAGES = {
    'bg': {'name': 'Bulgarian', 'tesseract': 'bul',
           'hints': 'и/н, ш/щ, ъ/ь, and Bulgarian italic letterforms'},
    'ru': {'name': 'Russian',   'tesseract': 'rus',
           'hints': 'и/н, ш/щ, ъ/ь, ь/ъ'},
    'en': {'name': 'English',   'tesseract': 'eng',
           'hints': 'common cursive ambiguities like a/o, n/u, cl/d'},
    'uk': {'name': 'Ukrainian', 'tesseract': 'ukr',
           'hints': 'і/ї, и/н, г/ґ'},
    'sr': {'name': 'Serbian',   'tesseract': 'srp',
           'hints': 'ш/щ, similar Cyrillic forms'},
    'de': {'name': 'German',    'tesseract': 'deu',
           'hints': 'umlauts ä/ö/ü and ß'},
}

DEFAULT_LANG = 'en'

def resolve(code: str) -> dict:
    code = (code or DEFAULT_LANG).lower().strip()

    if code not in LANGUAGES:
        supported = ', '.join(LANGUAGES.keys())

        raise ValueError(f"Unsupported language '{code}'. Supported: {supported}")

    return LANGUAGES[code]
