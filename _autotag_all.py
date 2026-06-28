# Make the WHOLE site editable. Body content -> data-edit (per page). Nav + footer text ->
# data-edit-global (same key across all pages, so editing once can propagate everywhere).
# Strips old tags first (idempotent). Skips animations/decoration/structural controls.
import os, glob, hashlib, re
from bs4 import BeautifulSoup

ROOT_EXCLUDE = {
 "preview.html","mockups.html","style-guide.html","logo-compare.html","logo-rebuild.html",
 "font-options.html","seo-audit.html","webflow-for-sharon.html","launch-plan.html",
 "url-matching-index.html","option-1-warm-editorial.html","option-2-bold-modern.html",
 "option-3-community-wellness.html",
}
pages = [f for f in glob.glob("*.html") if f not in ROOT_EXCLUDE and not f.startswith("_")]
pages += sorted(glob.glob("articles/*.html"))

INLINE = {"a","em","strong","b","i","span","small","br","s","sup","sub","mark","u","time","code","abbr","wbr"}
BLOCKCAND = {"h1","h2","h3","h4","h5","h6","p","li","blockquote","figcaption","cite"}
EXCL_TAGS = {"script","style","iframe","svg","noscript","head","title"}
# decoration / animation / structural controls we never tag
EXCL_CLASS = {"lm-rotate","lm-stack","slide","hero-media","count","sched","grain","progress",
              "burger","scrollcue","im","press","herotop"}

def pagekey(f):
    b = os.path.basename(f)[:-5]
    return "home" if b == "flagship" else re.sub(r"[^a-z0-9]+","-", b.lower())[:18]

def in_global(el):
    return any(a.name in ("header","footer") for a in el.parents)

def excluded(el):
    for a in el.parents:
        if a.name in EXCL_TAGS: return True
        if any(c in EXCL_CLASS for c in (a.get("class") or [])): return True
    if any(c in EXCL_CLASS for c in (el.get("class") or [])): return True
    return False

def has_text(el):
    t = el.get_text(strip=True); return bool(t) and (len(t) >= 2 or t.isalnum())

def is_pure_inline(el):
    return all(c.name in INLINE for c in el.find_all(True, recursive=True))

def has_block_desc(el):
    return any(c.name in BLOCKCAND for c in el.find_all(True, recursive=True))

def is_logo(src):
    return bool(re.search(r"lifted-(badge|logo|favicon|emblem|lockup)", src or ""))

total_local = total_global = total_img = 0
for f in pages:
    soup = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser")
    if not soup.body: continue
    pk = pagekey(f)
    for attr in ("data-edit","data-edit-global","data-edit-img","data-edit-img-global"):
        for el in soup.find_all(attrs={attr: True}): del el[attr]
    used = set()
    def keyfor(prefix, tag, text):
        h = hashlib.md5(re.sub(r"\s+"," ",text).strip().encode()).hexdigest()[:6]
        k = f"{prefix}.{tag}-{h}"; n = 2
        while k in used: k = f"{prefix}.{tag}-{h}-{n}"; n += 1
        used.add(k); return k

    # text targets
    targets = []
    for el in soup.find_all(True):
        if el.name in EXCL_TAGS or el.name in ("header","footer","nav"):
            if el.name in EXCL_TAGS: continue
        if excluded(el): continue
        if not has_text(el): continue
        if el.name in BLOCKCAND:
            if has_block_desc(el): continue
            targets.append(el)
        elif el.name in ("div","span","a","button"):
            if not is_pure_inline(el): continue
            targets.append(el)
    tset = set(id(t) for t in targets)
    for t in targets:
        if any(id(a) in tset for a in t.parents): continue   # outermost
        if in_global(t):
            t["data-edit-global"] = keyfor("g", t.name, t.get_text()); total_global += 1
        else:
            t["data-edit"] = keyfor(pk, t.name, t.get_text()); total_local += 1

    # images (content imgs editable per page; skip logos/badges)
    for img in soup.find_all("img"):
        if excluded(img): continue
        if is_logo(img.get("src","")): continue
        if in_global(img): continue
        h = hashlib.md5((img.get("src","") or "x").encode()).hexdigest()[:6]
        key = f"{pk}.img-{h}"; n = 2
        while key in used: key = f"{pk}.img-{h}-{n}"; n += 1
        used.add(key); img["data-edit-img"] = key; total_img += 1

    # ensure editor script (absolute path; one only)
    for s in soup.find_all("script", src=re.compile(r"edit-mode\.js")): s.decompose()
    soup.body.append(soup.new_tag("script", src="/edit-mode.js"))
    open(f, "w", encoding="utf-8").write(str(soup))

print(f"pages {len(pages)} | local text {total_local} | GLOBAL text {total_global} | images {total_img}")
