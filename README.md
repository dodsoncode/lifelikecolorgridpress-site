# lifelikecolorgridpress.com

Website for Lifelike Color Grid Press: wildlife color-by-number books made from real photos. Hosted on GitHub Pages.

| Path | What it is |
|---|---|
| `/` | Home page (built from `src/template.html`) |
| `/answers/` | Book answer keys, open download (the QR code in each book points here) |
| `/bonus-birds/` | Thank-you page after confirming a bonus-birds signup (Kit forms 10059973, 10059985) |
| `/free-page/` | Thank-you page after confirming the monthly free page signup (Kit form 10060011) |
| `files/` | PDFs: answer keys, bonus birds, free page |
| `img/` | Small images for the thank-you pages |

## Update the site

Edit files in `src/` (and `FREE_PAGE`, `BONUS`, `ANSWERS` at the top of `src/build.py`), then:

```
python src/build.py          # rebuilds index.html and the subpages (needs Pillow)
```

The PDFs come from the book generator (dodsoncode/color-by-number-generator): `books/backyard-birds/bonus_pack.json`, `free_page_YYYY_MM.json`, and the Book 1 answer keys.

Sign-ups post straight to Kit; nothing is stored on this site.
