# Edith

Tekstbewerker met database.

Markdown editor met simpel toevoegen van een frontmatter-blok.

Edith heeft de mogelijkheid om de tekst uit een pdf te importeren.

De inhoud van een pdf kan worden geimporteerd als markdown.

Er is ook een export naar Word-formaat mogelijk.

Export naar epub is ook mogelijk, staat default op lang=nl.

Import van epub bestanden kan ook.

Markdown exporteren als platte tekst kan ook.

Spellingcontrole is op afroep beschikbaar, maar is wel langzaam.

Een favoriet font is in te stellen in het config.py bestand.

Via woorden vervangen kan op basis van een woordenlijst de tekst worden gemoderniseerd.

Configuratie aanpassen via het menupunt onder Extra geeft de mogelijkheid om lichte modus, donkere modus of blauwe modus in te stellen.

Het linkervenster is het edit-venster voor tekst of Markdown.
Het middenvenster is een navigatievenster waar je op hoofdstuktitels kunt klikken om daar in het edit-venster naar toe te gaan.
Het rechtervenster is het preview-venster waar je de HTML rendering ziet van wat er in het edit-venster staat.

Het linker- en rechervenster moeten synchroon scrollen. Dit gaat niet geheel gelijkmatig als er afbeeldingen in de preview staan.

Er zijn ook 2 functies om Romeinse cijfers te vervangen door "normale" cijfers. De eerste functie vervangt alleen geselecteerde Romeinse cijfers en de tweede functie vervangt alle Romeinse cijfers in de tekst indien ze als laatste (of als enige) in een regel staan.

## Paden

Bij import epub: afbeeldingen krijgen volledig lokaal pad: "/home/.../.../epub_files/images/...jpg"

Bij export epub: afbeeldingen komen in "images" in de epub, de verwijzing in de html is naar src="images/...jpg"

Misschien handig om de map images van te voren te legen of the backuppen, want anders komen afbeeldingen van eerdere epubs ook weer mee.
