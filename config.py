

import datetime


DATABASE = "/home/kees/Data/memo.db"

DARKMODE = 'blue'  # opties: 'dark', 'light', 'blue'

OPSLAGLOCATIE = "/home/kees/Data/"

configuratie = {
    'database': DATABASE,
    'darkmode': DARKMODE,
    'opslaglocatie': OPSLAGLOCATIE,
    'favoriete_font': ("Arial", 12)
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