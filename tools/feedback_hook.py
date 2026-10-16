"""Adauga la fiecare pagina o legatura catre formularul public Tally.

Linkul foloseste campul ascuns 'page' pentru a identifica pagina din wiki.
Ruleaza la randarea MkDocs; nu modifica sursele Markdown si nici PDF-ul.
"""
from urllib.parse import urlencode, urljoin

FORM_URL = "https://tally.so/r/rDyV1M"


def feedback_url(page_url):
    """Construieste URL-ul cu parametrul Tally 'page', codificat corect."""
    return FORM_URL + "?" + urlencode({"page": page_url})


def on_page_markdown(markdown, page, config, files):
    """Afiseaza legatura pentru toate paginile, in afara paginii Contribuie."""
    if page.file.src_uri == "contribuie.md":
        return markdown

    site_url = config["site_url"]
    if not site_url:
        raise ValueError("site_url este necesar pentru contextul paginii Tally")

    public_page_url = urljoin(site_url.rstrip("/") + "/", page.url.lstrip("/"))
    link = feedback_url(public_page_url)
    return (
        markdown.rstrip()
        + "\n\n---\n\n"
        + "**Ai o sugestie pentru aceasta pagina?** "
        + f'[Trimite o corectura sau o propunere]({link})'
        + '{: target="_blank" rel="noopener noreferrer" }'
        + "\n\n"
        + "Nu este necesar un cont GitHub. Sugestiile sunt verificate inainte de publicare.\n"
    )
