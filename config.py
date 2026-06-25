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
    'font_path' : "/home/kees/Data/FreeSerif.ttf",
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

FRONTMATTER_TEXT_EPUB = """---
title: 
subtitle:
author: 
language: nl
identifier: 
cover_file: assets/cover.jpg
---
"""

font_sizes = {
    "H1": 20,
    "H2": 18,
    "H3": 16
}
