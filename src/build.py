"""Build the Lifelike Color Grid Press site.

    python src/build.py                 # live site: index.html, answers/, bonus-birds/, free-page/, 404.html
    python src/build.py --preview OUT   # one self-contained preview page (the claude.ai artifact)

Sources live in src/: template.html (the home page), plates.json (plate pictures and grids),
photo.txt and free_page.txt (embedded images). Downloads live in files/, small images in img/.
"""
import argparse, json, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DOMAIN = "https://lifelikecolorgridpress.com"

# Kit form IDs (also set in CONFIG inside template.html)
FORM_BONUS_BOOK = "10059985"

# What the free-page and download pages offer right now
FREE_PAGE = {"month": "November 2026", "species": "Black-billed Magpie",
             "pdf": "files/free-page-2026-11.pdf", "img": "img/free-page-2026-11.png"}
BONUS = {"pdf": "files/bonus-birds.pdf",
         "birds": [("Painted Bunting", "img/bonus-1.png"), ("Yellow Warbler", "img/bonus-2.png"),
                   ("Pileated Woodpecker", "img/bonus-3.png")]}
ANSWERS = {"pdf": "files/backyard-birds-answer-keys.pdf", "book": "Backyard Birds"}

LIVE_BANNER = "Book 1, <em>Backyard Birds</em>, is coming in December 2026. Get 3 free pages while you wait."
PREVIEW_BANNER = "Site preview. Prices and plates are working versions until Book 1 is final."

DESCRIPTION = ("Color-by-number books made from real wildlife photos. One 24-pencil set, "
               "true-to-life colors, full-color answer keys online. Birds first.")


def head(title, desc=DESCRIPTION, path=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/{path}">
<link rel="canonical" href="{DOMAIN}/{path}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 6 6'%3E%3Crect width='6' height='6' fill='%23f7f8f8'/%3E%3Cg fill='%23b4471a'%3E%3Crect x='1' y='1' width='2' height='1'/%3E%3Crect x='0' y='2' width='4' height='2'/%3E%3Crect x='1' y='4' width='2' height='1'/%3E%3C/g%3E%3Crect x='3' y='2' width='2' height='1' fill='%231f292e'/%3E%3Crect x='4' y='0' width='1' height='1' fill='%234f7563'/%3E%3C/svg%3E">"""


def home(preview):
    t = (SRC / "template.html").read_text()
    t = t.replace("__DATA__", (SRC / "plates.json").read_text().strip())
    t = t.replace("__PHOTO__", (SRC / "photo.txt").read_text().strip())
    t = t.replace("__FREEIMG__", (SRC / "free_page.txt").read_text().strip())
    t = t.replace("__BANNER__", PREVIEW_BANNER if preview else LIVE_BANNER)
    t = t.replace("__ANSWERSPDF__", "" if preview else ANSWERS["pdf"])
    if preview:
        return t.replace("__HEADMETA__", '<meta name="claude:viewport-fit-sides" content="cover">')
    t = t.replace("__HEADMETA__\n", "")
    t = re.sub(r"^<title>.*?</title>\n", "", t, count=1)
    body_start = t.index("</style>") + len("</style>")
    return head("Lifelike Color Grid Press: wildlife color by number") + "\n" + t[:body_start] + \
        "\n</head>\n<body>" + t[body_start:] + "\n</body>\n</html>\n"


def style():
    t = (SRC / "template.html").read_text()
    return t[t.index("<style>"):t.index("</style>") + len("</style>")]


FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,600&family=Public+Sans:wght@400;600;700&display=swap">"""

SUB_CSS = """<style>
main.sub{padding-block:56px 72px}
main.sub .wrap{display:grid;gap:28px;max-width:760px}
.sub h1{font-size:var(--step-3)}
.sub .lead{color:var(--muted);font-size:var(--step-0);max-width:60ch}
.thumbs3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.thumbs3 figure{margin:0;display:grid;gap:6px;font-size:var(--step--1);color:var(--muted)}
.thumbs3 img,.one img{width:100%;height:auto;border:1px solid var(--line);border-radius:var(--radius);image-rendering:pixelated;background:var(--sheet)}
.one{max-width:280px}
.steps{margin:0;padding-left:1.2em;display:grid;gap:6px;color:var(--ink)}
.dl{display:grid;gap:8px;justify-items:start}
.dl .fine,.fine{font-size:var(--step--1);color:var(--muted)}
footer.mini{padding-block:28px 40px;border-top:1px solid var(--line);font-size:var(--step--1);color:var(--muted)}
footer.mini .wrap{display:flex;flex-wrap:wrap;gap:8px 20px;justify-content:space-between}
</style>"""


def subpage(title, path, body, depth=1, script=""):
    up = "../" * depth
    brand = re.search(r'<a class="brand".*?</a>', (SRC / "template.html").read_text(), re.S).group(0)
    brand = brand.replace('href="#top"', f'href="{up or "./"}"')
    return f"""{head(title, path=path)}
{FONTS}
{style()}
{SUB_CSS}
</head>
<body>
<header class="top"><div class="wrap">{brand}<a class="btn small" href="{up or './'}" style="margin-left:auto">Home</a></div></header>
<main class="sub"><div class="wrap">
{body}
</div></main>
<footer class="mini"><div class="wrap"><span>&copy; 2026 Lifelike Color Grid Press</span><span>Questions: <a href="mailto:admin@lifelikecolorgridpress.com">admin@lifelikecolorgridpress.com</a></span></div></footer>
{script}
</body>
</html>
"""


FORM_JS = """<script>
document.querySelectorAll("form[data-kit]").forEach(f => f.addEventListener("submit", e => {
  e.preventDefault();
  const input = f.querySelector('input[type=email]'), out = f.querySelector(".done"), btn = f.querySelector("button");
  out.hidden = false; out.style.color = "";
  if (!input.value || !input.checkValidity()) { out.style.color = "var(--accent)"; out.textContent = "Enter an email address like name@example.com."; input.focus(); return; }
  if (location.protocol === "file:") { out.textContent = "Preview only: nothing was sent."; return; }
  btn.disabled = true; out.textContent = "Sending\\u2026";
  const body = new FormData(); body.append("email_address", input.value.trim());
  fetch(`https://app.kit.com/forms/${f.dataset.kit}/subscriptions`, { method: "POST", body, headers: { Accept: "application/json" } })
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(() => { out.textContent = "Almost done: check your inbox and tap the confirm button. (Look in Promotions or spam if it isn't there in a few minutes.)"; input.value = ""; })
    .catch(() => { out.style.color = "var(--accent)"; out.textContent = "That didn't go through. Please try again in a minute, or email admin@lifelikecolorgridpress.com."; })
    .finally(() => { btn.disabled = false; });
}));
</script>"""


def wh(img):
    w, h = Image.open(ROOT / img).size
    return f'width="{w}" height="{h}"'


def answers_page():
    body = f"""<span class="label">Answer keys</span>
<h1>{ANSWERS['book']}: full-color answer keys</h1>
<p class="lead">Your book prints in black ink to keep the price down. Here is every finished picture in full color, four to a page, numbered and named to match the puzzles. Free, no sign-up.</p>
<div class="dl">
  <a class="btn primary" href="../{ANSWERS['pdf']}" download>Download the answer keys (PDF)</a>
  <p class="fine">Letter size, prints at home. Large Print Color Edition: your keys are at the back of the book.</p>
</div>
<ol class="steps"><li>Color a page using the pencil names in its color key.</li><li>Stuck on a cell, or curious how it should look? Check the matching key.</li><li>Print a key in color, or keep it open on a phone or tablet beside you.</li></ol>
<div class="panel answers">
  <form class="signup" data-kit="{FORM_BONUS_BOOK}" novalidate>
    <label class="label" for="email-bonus">Bonus: 3 color-by-number pages that aren't in the book, free</label>
    <div class="row"><input id="email-bonus" type="email" placeholder="you@example.com" autocomplete="email" required><button class="btn" type="submit">Send my bonus pages</button></div>
    <p class="fine">You'll also get <em>Field Notes</em> monthly, with a new free page. One click unsubscribes. Your email is never sold or shared.</p>
    <p class="done" role="status" hidden></p>
  </form>
</div>"""
    return subpage("Backyard Birds answer keys | Lifelike Color Grid Press", "answers/", body, script=FORM_JS)


def bonus_page():
    figs = "".join(f'<figure><img src="../{img}" alt="Finished picture of a {name}" {wh(img)}><figcaption>{name}</figcaption></figure>'
                   for name, img in BONUS["birds"])
    body = f"""<span class="label">You're confirmed</span>
<h1>Here are your 3 bonus pages</h1>
<p class="lead">Thanks for joining. Print the pages on letter paper and color with any 24-count set of colored pencils. Each picture has its color key underneath, and the finished pictures are at the back.</p>
<div class="thumbs3">{figs}</div>
<div class="dl"><a class="btn primary" href="../{BONUS['pdf']}" download>Download the bonus pages (PDF)</a>
<p class="fine">Personal use: print as many copies as you like for yourself, your family or your classroom.</p></div>
<p class="fine"><em>Field Notes</em> arrives once a month with a new free page. Reply to any email to say hello or send a finished page.</p>"""
    return subpage("Your bonus pages | Lifelike Color Grid Press", "bonus-birds/", body)


def free_page():
    body = f"""<span class="label">You're confirmed · Free page for {FREE_PAGE['month']}</span>
<h1>This month's free page: {FREE_PAGE['species']}</h1>
<p class="lead">Thanks for joining. Print it on letter paper; the color key is under the picture and the finished picture is on page 2.</p>
<div class="one"><img src="../{FREE_PAGE['img']}" alt="Finished picture of a {FREE_PAGE['species']}" {wh(FREE_PAGE['img'])}></div>
<div class="dl"><a class="btn primary" href="../{FREE_PAGE['pdf']}" download>Download the free page (PDF)</a>
<p class="fine">Personal use: print as many copies as you like for yourself, your family or your classroom.</p></div>
<p class="fine">Next month's page arrives in <em>Field Notes</em>.</p>"""
    return subpage("This month's free page | Lifelike Color Grid Press", "free-page/", body)


def not_found():
    body = """<span class="label">Page not found</span>
<h1>That page flew off</h1>
<p class="lead">The link may be old or mistyped. Looking for your book's answer keys? <a href="/answers/">They're here</a>.</p>
<div class="dl"><a class="btn primary" href="/">Go to the home page</a></div>"""
    return subpage("Page not found | Lifelike Color Grid Press", "404.html", body, depth=0).replace('href="./"', 'href="/"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", help="write the single-page preview here instead of the live site")
    a = ap.parse_args()
    if a.preview:
        Path(a.preview).write_text(home(True)); print("preview:", a.preview); return
    (ROOT / "index.html").write_text(home(False))
    for d, html in [("answers", answers_page()), ("bonus-birds", bonus_page()), ("free-page", free_page())]:
        (ROOT / d).mkdir(exist_ok=True); (ROOT / d / "index.html").write_text(html)
    (ROOT / "404.html").write_text(not_found())
    print("built index.html, answers/, bonus-birds/, free-page/, 404.html")


if __name__ == "__main__":
    main()
