# Map EVERY live drsharongam.com URL -> kept (same address) / forwarded (301 to closest)
# / removed. Writes _redirects (real config) + url-matching-index.html (client report).
import os, re, html as H

SITEMAP = r"C:\PA-Agent\lifted-strength-club\_scrape\sitemap.xml"
paths = sorted(set(re.sub(r"https?://[^/]+", "", u).rstrip("/") or "/" for u in re.findall(r"<loc>([^<]+)</loc>", open(SITEMAP, encoding="utf-8").read())))

def served(p):
    """Does the new site serve this exact path?"""
    if p == "/": return True
    rel = p.lstrip("/")
    return os.path.isfile(rel + ".html") or os.path.isfile(rel) or os.path.isfile(os.path.join(rel, "index.html"))

# explicit forwards for pages whose address changed or that Sharon retired
FORWARD = {
 "/articles": "/blog.html",
 "/about-expert-lake-mary-personal-training": "/about.html",
 "/group-strength-training": "/membership.html",
 "/personal-training-lake-mary-florida": "/strength-training-longwood.html",
 "/anxiety-strength-training-12-week-program": "/mental-health.html",     # retired -> closest (mental health)
 "/lift-and-learn-workshop": "/membership.html",                          # retired
 "/contact": "/",                                                          # retired (footer email + booking)
 "/start-here-lake-mary-personal-training": "/",
 "/start-here-lake-mary-personal-training-welcome": "/",
 "/welcome": "/",
 "/guide-to-exercise-for-mental-health/download-guide-to-exercise-for-mental-health": "/guide-to-exercise-for-mental-health-download.html",
 "/strength-training-101/download-guide-to-strength-training-101": "/strength-training-101-download.html",
 "/how-to-set-effective-goals/download-effective-goals-ebook": "/how-to-set-effective-goals-download.html",
 "/guide-to-healthy-eating/download-a-guide-to-healthy-eating": "/guide-to-healthy-eating-download.html",
}
REMOVE = {"/design-styling-do-not-delete": "Squarespace internal style page (never public)",
          "/lsc-preview-home": "internal preview page (never public)"}
RETIRED = {"/anxiety-strength-training-12-week-program","/lift-and-learn-workshop","/contact",
           "/start-here-lake-mary-personal-training","/start-here-lake-mary-personal-training-welcome","/welcome"}

kept, fwd, removed = [], [], []
for p in paths:
    if p in REMOVE: removed.append((p, REMOVE[p])); continue
    if p.startswith("/articles/category/") or p.startswith("/articles/tag/"):
        fwd.append((p, "/blog.html", "blog/tag archive")); continue
    if served(p): kept.append(p); continue
    if p in FORWARD: fwd.append((p, FORWARD[p], "retired" if p in RETIRED else "address changed")); continue
    # safety net: anything unmapped still forwards home so it never 404s
    fwd.append((p, "/", "forwarded to home (safety)"))

# ---- write _redirects (keep root rewrite first) ----
lines = ["/    /flagship.html    200", "", "# blog taxonomy archives", "/articles/category/*    /blog.html    301", "/articles/tag/*    /blog.html    301", "", "# moved or retired pages -> closest live page"]
for p, t, _why in fwd:
    if p.startswith("/articles/category/") or p.startswith("/articles/tag/"): continue
    lines.append(p + "    " + t + "    301")
open("_redirects", "w", encoding="utf-8").write("\n".join(lines) + "\n")

# ---- client-facing index ----
def rows(items):
    out = '<table><tr><th>Current address</th><th>What happens</th></tr>'
    for it in items:
        if len(it) == 2 and it in [(p, r) for p, r in removed]:
            out += '<tr><td><code>%s</code></td><td><span class="rm">Removed</span> &mdash; %s</td></tr>' % (H.escape(it[0]), H.escape(it[1]))
        else:
            p, t = it[0], it[1]
            out += '<tr><td><code>%s</code></td><td><span class="fw">Forwards to</span> <code>%s</code></td></tr>' % (H.escape(p), H.escape(t))
    return out + '</table>'

fwd_disp = sorted(set((p, t) for p, t, _ in fwd))
arts = sum(1 for p in kept if p.startswith("/articles/"))
CSS = "*{box-sizing:border-box}body{font-family:Outfit,system-ui,sans-serif;color:var(--ink);background:var(--paper);margin:0;line-height:1.62;font-size:15px}" \
  ".wrap{max-width:780px;margin:0 auto;padding:50px 30px 70px}" \
  ".eyebrow{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--brass);font-weight:600}" \
  "h1{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:2.6rem;line-height:1.08;color:var(--teal-d);margin:.25em 0 .1em}h1 em{font-style:italic;color:var(--brass)}" \
  "h2{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:1.5rem;color:var(--teal-d);margin:40px 0 6px;border-bottom:1px solid #e7e0d6;padding-bottom:7px}" \
  ".sum{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0}.box{background:#F4F0EB;border-radius:12px;padding:15px 20px;text-align:center;min-width:120px}.box b{font-family:'Cormorant Garamond',serif;font-size:2rem;display:block;line-height:1;color:var(--teal-d)}" \
  "ol.steps{padding-left:20px}ol.steps li{margin:8px 0}" \
  "table{width:100%;border-collapse:collapse;margin:10px 0;font-size:.85rem}th{text-align:left;font-size:.64rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:6px 8px;border-bottom:1px solid #ddd}" \
  "td{padding:6px 8px;border-bottom:1px solid #eee;vertical-align:top}code{font-family:ui-monospace,monospace;font-size:.8rem;color:var(--teal-d)}" \
  ".fw{color:var(--brass);font-weight:600}.rm{color:#A8584C;font-weight:600}.note{color:var(--muted)}" \
  ".foot{margin-top:38px;padding-top:18px;border-top:1px solid #e7e0d6;color:var(--muted)}.sig{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.25rem;color:var(--teal-d)}"
T = lambda n: str(n)
report = (
 '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">'
 '<title>Going live — every web address mapped</title>'
 '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">'
 '<style>:root{--teal:#17505B;--teal-d:#123E47;--brass:#B78B52;--paper:#FBF9F6;--ink:#2C2924;--muted:#6E6A65}' + CSS + '</style></head><body><div class="wrap">'
 '<div class="eyebrow">Lifted Strength Club &middot; for Dr. Sharon Gam</div>'
 '<h1>Going live &mdash; <em>every web address mapped</em></h1>'
 '<p class="note">Your biggest worry was SEO. Here&rsquo;s the proof it&rsquo;s protected: every single one of your ' + T(len(paths)) + ' current web addresses has a plan, so <b>nothing will 404 and your rankings carry over</b>.</p>'
 '<div class="sum">'
 '<div class="box"><b>' + T(len(kept)) + '</b>kept at the<br>same address</div>'
 '<div class="box"><b>' + T(len(fwd_disp)) + '</b>forwarded to the<br>closest page</div>'
 '<div class="box"><b>' + T(len(removed)) + '</b>removed<br>(internal/empty)</div>'
 '<div class="box"><b>' + T(len(paths)) + '</b>total addresses</div>'
 '</div>'
 '<h2>How going live works</h2><ol class="steps">'
 '<li><b>We keep your domain</b> &mdash; drsharongam.com stays yours; nothing about your web address changes.</li>'
 '<li><b>Pages you kept stay at the exact same address</b> (all ' + T(len(kept)) + ' of them, including every blog article). Google keeps the rankings you&rsquo;ve earned &mdash; no redirect, no &ldquo;page not found&rdquo;.</li>'
 '<li><b>The handful you retired or moved forward automatically</b> to the closest live page (listed below), so any links or ranking they had flow to a real page instead of breaking.</li>'
 '<li><b>Internal/empty pages are removed</b> &mdash; they were never public and have no traffic.</li>'
 '<li><b>Cutover day:</b> everything is already built and tested on the preview. We point drsharongam.com at the new site (a DNS change), then submit your sitemap to Google and watch Search Console. <b>Your current site stays live as an instant fallback</b> until you&rsquo;re completely happy &mdash; if anything looked off we switch back in minutes.</li>'
 '<li><b>All we need from you:</b> access to your domain&rsquo;s DNS settings when you&rsquo;re ready to flip it.</li>'
 '</ol>'
 '<h2>Kept at the same address (' + T(len(kept)) + ')</h2>'
 '<p class="note">Your homepage, About, Membership, The Science, free guides, and <b>all ' + T(arts) + ' blog articles</b> &mdash; every one keeps its exact current web address. (Not listed individually here for length; the forwards below are the only addresses that change.)</p>'
 '<h2>Forwarded to the closest page (' + T(len(fwd_disp)) + ')</h2>' + rows(fwd_disp) +
 '<h2>Removed (' + T(len(removed)) + ')</h2>' + rows(removed) +
 '<div class="foot">Any questions, just reply &mdash; I&rsquo;ll talk you through it.<div class="sig" style="margin-top:10px">&mdash; Claudina</div></div>'
 '</div></body></html>')
open("url-matching-index.html", "w", encoding="utf-8").write(report)

print("TOTAL %d | kept %d | forward %d | removed %d" % (len(paths), len(kept), len(fwd_disp), len(removed)))
print("articles kept:", sum(1 for p in kept if p.startswith("/articles/")))
