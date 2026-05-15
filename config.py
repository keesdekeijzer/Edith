

import datetime


DATABASE = "/home/kees/Data/memo.db"

DARKMODE = 'blue'  # opties: 'dark', 'light', 'blue'

OPSLAGLOCATIE = "/home/kees/Data/"

configuratie = {
    'database': DATABASE,
    'darkmode': DARKMODE,
    'opslaglocatie': OPSLAGLOCATIE
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