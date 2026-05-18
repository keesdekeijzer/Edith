import pdfplumber
from collections import Counter, defaultdict

def fontsize_counts(pdf_path):
    counts_by_page = []
    total_counter = Counter()
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_counter = Counter()
            # page.chars bevat per teken o.a. 'size' en 'fontname'
            for ch in page.chars:
                # formaat afronden als je variaties wilt samenvoegen, bv. 11.999 -> 12.0
                size = round(ch.get("size", 0), 2)
                page_counter[size] += 1
                total_counter[size] += 1
            counts_by_page.append((i, dict(page_counter)))
    return counts_by_page, dict(total_counter)

# Voorbeeld gebruik
if __name__ == "__main__":
    pdf_path = "voorbeeld.pdf"
    per_page, totaal = fontsize_counts(pdf_path)

    print("Per pagina (pagina, {fontsize: count}):")
    for pnum, ctr in per_page:
        print(f"Pagina {pnum}: {ctr}")

    print("\nTotaal over hele document (fontsize: count):")
    # Sorteer op fontsize oplopend
    grootste_font_aantal = 0
    grootste_font_size = 0
    for size in sorted(totaal):
        print(f"{size}: {totaal[size]}")
        if totaal[size] > grootste_font_aantal:
            grootste_font_aantal = totaal[size]
            grootste_font_size = size
    print("grootste font: ", grootste_font_size)

    

"""
Opmerkingen:
- pdfplumber vult page.chars met items die keys 'text', 'fontname', 'size', 'adv' e.d. kunnen bevatten.
- Ronding: PDF-fontsizes kunnen lichtjes variëren (bijv. 11.9999). Pas round(..., 1 of 2) aan om samenvoegen te reguleren.
- Als je liever telt per woord/tekstobject i.p.v. per teken, kun je page.extract_words() gebruiken (maar dat bevat meestal geen size per woord). De char-methode is betrouwbaarder voor fontsizes.
- Voor grote pdf's kun je memory/performance optimaliseren door niet alles in geheugen te houden; het bovenstaande verwerkt pagina-voor-pagina.
"""