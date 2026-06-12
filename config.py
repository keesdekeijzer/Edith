import datetime


DATABASE = "/home/kees/Data/memo.db"

DARKMODE = 'blue'  # opties: 'dark', 'light', 'blue'

OPSLAGLOCATIE = "/home/kees/Data/"

configuratie = {
    'database': DATABASE,
    'darkmode': DARKMODE,
    'opslaglocatie': OPSLAGLOCATIE,
    'favoriete_font': ("Arial", 12),
    'language': 'en',  # opties: 'nl', 'en', 'de'
}

nu = datetime.datetime.now()
datum_nu = nu.strftime("%Y-%m-%d")

FRONTMATTER_TEXT =f"""---
title: 
hero: images/posts/default.jpg
date: {datum_nu}
tags: [post,]
summary: 
---
"""

font_sizes = {
    "H1": 20,
    "H2": 18,
    "H3": 16
}

VERVANGINGEN = {
        "te": "tot",
        "en": "en",
        "de": "de",
        "het": "het",
        "een": "een",
        "is": "is",
        "zijn": "zijn",
        "was": "was",
        "waren": "waren",
        "wordt": "wordt",
        "worden": "worden",
        "heb": "heb",
        "heeft": "heeft",
        "hebben": "hebben",
        "kan": "kan",
        "kun": "kun",
        "regel": "REGEL",
    }
