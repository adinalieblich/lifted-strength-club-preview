# Make the WHOLE site editable: strip old data-edit, re-tag every customer page cleanly,
# and ensure each page loads the editor. Skips nav/footer/animations/compound nav rows.
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
BLOCKCAND = {"h1","h2","h3","h4","h5","h6","p","li","blockquote","figcaption"}
EXCL_TAGS = {"header","footer","nav","script","style","iframe","svg","noscript","head","title","button"}
EXCL_CLASS = {"lm-rotate","lm-stack","lm-line","scrollcue","slide","hero-media","press","herotop",
              "live","count","sched","grain","progress","burger","menu","forwho","ix","pcard","im"}

def pagekey(f):
    base = os.path.basename(f)[:-5]
    if base == "flagship": return "home"
    return re.sub(r"[^a-z0-9]+","-", base.lower())[:18]

def excluded(el):
    for anc in el.parents:
        if anc.name in EXCL_TAGS: return True
        if any(c in EXCL_CLASS for c in (anc.get("class") or [])): return True
    if any(c in EXCL_CLASS for c in (el.get("class") or [])): return True
    return False

def has_text(el):
    t = el.get_text(strip=True)
    return bool(t) and len(t) >= 2

def is_pure_inline(el):
    return all(c.name in INLINE for c in el.find_all(True, recursive=True))

def has_block_desc(el):
    return any(c.name in BLOCKCAND for c in el.find_all(True, recursive=True))

total_tags = 0
for f in pages:
    html = open(f, encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    if not soup.body:
        print("skip (no body):", f); continue
    pk = pagekey(f)
    # 1) strip old data-edit
    for el in soup.find_all(attrs={"data-edit": True}):
        del el["data-edit"]
    # 2) choose targets
    targets = []
    for el in soup.find_all(True):
        if el.name in EXCL_TAGS: continue
        if excluded(el): continue
        if not has_text(el): continue
        if el.name in BLOCKCAND:
            if has_block_desc(el): continue          # innermost block
            targets.append(el)
        elif el.name in {"div","span","a"}:
            if not is_pure_inline(el): continue       # pure text leaf only
            targets.append(el)
    tset = set(id(t) for t in targets)
    used = set(); added = 0
    def keyfor(tag, text):
        h = hashlib.md5(re.sub(r"\s+"," ",text).strip().encode("utf-8")).hexdigest()[:6]
        k = f"{pk}.{tag}-{h}"; n = 2
        while k in used: k = f"{pk}.{tag}-{h}-{n}"; n += 1
        used.add(k); return k
    for t in targets:
        if any(id(a) in tset for a in t.parents): continue   # outermost only
        t["data-edit"] = keyfor(t.name, t.get_text())
        added += 1
    # 3) ensure the editor script loads (absolute path so /articles/ works), no dupes
    for s in soup.find_all("script", src=re.compile(r"edit-mode\.js")):
        s.decompose()
    tag = soup.new_tag("script", src="/edit-mode.js")
    soup.body.append(tag)
    open(f, "w", encoding="utf-8").write(str(soup))
    total_tags += added
print(f"pages tagged: {len(pages)} | total editable spots added: {total_tags}")
