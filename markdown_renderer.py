import markdown

def render_markdown(text: str, color_mode: str = "light") -> str:
    """Convert Markdown text to HTML."""
    html = markdown.markdown(
        text,
        extensions=[
            "fenced_code",
            "tables",
            "toc",
            "footnotes",
            "codehilite",
            "admonition",
            "meta",
        ]
    )

    #print("color-mode: dark;")  # Debugging statement to indicate color mode
    voorgrondkleur = "#FFFFFF" if color_mode == "dark" else "#000000"
    achtergrondkleur = "#000000" if color_mode == "dark" else "#FFFFFF"




    # Eenvoudige HTML template
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                margin: 2rem;
                line-height: 1.6;
                color: {voorgrondkleur};
                background-color: {achtergrondkleur};
            }}
            img {{
                max-width: 100%;
                height: auto;
                border-radius: 5px;
                margin: 1rem 0;
            }}
            pre {{
                background-color: #CCCCCC;
                padding: 1rem;
                border-radius: 5px;
                overflow-x: auto;
            }}
            code {{
                background-color: #CCCCCC;
                padding: 2px 4px;
                border-radius: 3px;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
            }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """

