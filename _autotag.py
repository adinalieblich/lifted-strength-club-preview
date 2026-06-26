# Auto-add data-edit="KEY" to editable text across the main marketing pages so the
# inline editor covers far more of each page. Safe: skips nav/footer/animation/scripts,
# skips already-tagged elements, tags outermost text-leaves only.
import hashlib, re
from bs4 import BeautifulSoup

PAGES = {
 "flagship.html": "home", "about.html": "about", "membership.html": "memb",
 "founding-members.html": "found", "mental-health.html": "science",
 "strength-training-neurological-symptoms.html": "neural", "guides.html": "guides",
 "reviews.html": "reviews", "strength-training-longwood.html": "local",
 "guide-to-exercise-for-mental-health.html": "ebk1", "strength-training-101.html": "ebk2",
 "how-to-set-effective-goals.html": "ebk3", "guide-to-healthy-eating.html": "ebk4",
}

INLINE = {"a","em","strong","b","i","span","small","br","s","sup","sub","mark","u","time","code","abbr","wbr"}
BLOCKCAND = {"h1","h2","h3","h4","h5","h6","p","li","blockquote","figcaption"}
EXCL_TAGS = {"header","footer","nav","script","style","iframe","svg","noscript","head","title","button"}
EXCL_CLASS = {"lm-rotate","lm-stack","scrollcue","slide","hero-media","press","herotop","live",
              "count","sched","grain","progress","burger","menu","forwho"}

def excluded(el):
    for anc in el.parents:
        if anc.name in EXCL_TAGS: return True
        cls = anc.get("class") or []
        if any(c in EXCL_CLASS for c in cls): return True
    cls = el.get("class") or []
    if any(c in EXCL_CLASS for c in cls): return True
    return False

def has_text(el):
    return bool(el.get_text(strip=True)) and len(el.get_text(strip=True)) >= 2

def child_elems(el):
    return [c for c in el.find_all(True, recursive=True)]

def is_pure_inline_leaf(el):
    return all(c.name in INLINE for c in el.find_all(True, recursive=True))

def has_block_cand_desc(el):
    return any(c.name in BLOCKCAND for c in el.find_all(True, recursive=True))

for fname, pk in PAGES.items():
    try:
        html = open(fname, encoding="utf-8").read()
    except FileNotFoundError:
        print("skip (missing):", fname); continue
    soup = BeautifulSoup(html, "html.parser")
    used = set()
    def keyfor(tag, text):
        h = hashlib.md5(re.sub(r"\s+"," ",text).strip().encode("utf-8")).hexdigest()[:6]
        k = f"{pk}.{tag}-{h}"; n = 2
        while k in used: k = f"{pk}.{tag}-{h}-{n}"; n += 1
        used.add(k); return k
    # record existing keys to avoid clashes
    for el in soup.find_all(attrs={"data-edit": True}): used.add(el["data-edit"])

    targets = []
    for el in soup.find_all(True):
        if el.name in EXCL_TAGS: continue
        if el.has_attr("data-edit"): continue
        if excluded(el): continue
        if not has_text(el): continue
        # already inside an element we will tag? handled later via outermost/innermost rules
        if el.name in BLOCKCAND:
            if has_block_cand_desc(el): continue          # innermost block only
            targets.append(el)
        elif el.name in {"div","span","a"}:
            if not is_pure_inline_leaf(el): continue        # only pure text leaves
            targets.append(el)

    # drop any target that has an ancestor also in targets (keep outermost)
    tset = set(id(t) for t in targets)
    final = []
    for t in targets:
        if any(id(a) in tset for a in t.parents): continue
        final.append(t)

    added = 0
    for el in final:
        if el.has_attr("data-edit"): continue
        el["data-edit"] = keyfor(el.name, el.get_text())
        added += 1

    out = str(soup)
    open(fname, "w", encoding="utf-8").write(out)
    total = out.count("data-edit=")
    print(f"{fname:48s} +{added:3d} new  ({total} total)")
print("done")
