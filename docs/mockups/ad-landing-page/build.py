"""Builds the two landing-page mockups for Sharon: A (exactly as requested) and B (recommended)."""
import pathlib, sys

HERE = pathlib.Path(__file__).parent
CAL = "https://cal.com/liftedstrengthclub/free-consultation"
LINK_A = sys.argv[1] if len(sys.argv) > 1 else "#"
LINK_B = sys.argv[2] if len(sys.argv) > 2 else "#"

CSS = r"""
:root{
  /* Lifted brand: dark teal, blush, cream/white; Cormorant Garamond display + Outfit body. Single light look on purpose (it mirrors the live site). */
  --teal:#3E6E73;--teal-2:#4D7E83;--teal-deep:#24474B;--blush:#C98D86;--blush-soft:#F3E3E0;
  --cream:#F4F8F5;--greige:#F4F0EB;--white:#fff;--ink:#2A2A2A;--muted:#5F5B57;--rule:rgba(42,42,42,.13);
  --chrome:#1E2324;--chrome-2:#2C3436;--tag:#E2B13C;
  --display:'Cormorant Garamond',Georgia,'Times New Roman',serif;--body:'Outfit',system-ui,-apple-system,'Segoe UI',sans-serif;
  color-scheme:light;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{background:var(--chrome)}
body{margin:0;font-family:var(--body);color:var(--ink);-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}
a{color:inherit}
button{font:inherit;cursor:pointer}
:focus-visible{outline:3px solid var(--tag);outline-offset:2px}

/* ---------- mockup chrome (not part of the page) ---------- */
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:40;background:var(--chrome);color:#E9EEEC;border-bottom:1px solid rgba(255,255,255,.08);
  padding-block:10px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:41;background:var(--chrome)}
.bar-in{max-width:1180px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px}
.bar .tagline{font-size:.86rem;line-height:1.35;min-width:0;flex:1 1 260px}
.bar .tagline b{font-weight:600;color:#fff}
.bar .tagline span{color:#AEB9B6}
.seg{display:inline-flex;background:var(--chrome-2);border-radius:999px;padding:3px}
.seg button{border:0;background:none;color:#C9D2CF;padding:6px 13px;border-radius:999px;font-size:.8rem}
.seg button[aria-pressed="true"]{background:#fff;color:var(--chrome)}
.switch{display:inline-flex;align-items:center;gap:8px;font-size:.82rem;color:#E9EEEC;background:none;border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:6px 13px}
.switch[aria-pressed="true"]{background:var(--tag);border-color:var(--tag);color:#1E1E1E}
.otherlink{font-size:.82rem;color:#fff;text-decoration:underline;text-underline-offset:3px}
.stage{padding-block:24px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;justify-content:center}
.device{position:relative;width:100%;max-width:1180px;background:var(--white);border-radius:14px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.screen{container-type:inline-size;background:var(--white)}
body.phone .device{max-width:400px;border-radius:44px;border:11px solid #0C0F10}
body.phone .screen{height:min(820px,calc(100vh - 150px));overflow-y:auto;overscroll-behavior:contain}
@media (max-width:560px){.seg{display:none}.stage{padding-left:0;padding-right:0;padding-block:0}.device,body.phone .device{border-radius:0;border:0;max-width:none}body.phone .screen{height:auto;overflow:visible}}

/* ---------- the landing page ---------- */
.lp{font-size:17px;line-height:1.65}
.in{max-width:1080px;margin:0 auto;padding-left:22px;padding-right:22px}
@container (min-width:760px){.in{padding-left:48px;padding-right:48px}}
.lp h1,.lp h2,.lp h3,.thanks h3,.summary h2{font-family:var(--display);font-weight:600;line-height:1.08;text-wrap:balance;margin:0}
.lp h2{font-size:clamp(2rem,6cqi,2.9rem);color:var(--teal-deep)}
.lp p{margin:0}
.eyebrow{font-size:.74rem;letter-spacing:.2em;text-transform:uppercase;font-weight:500;color:var(--blush)}
section{padding-block:64px}
@container (min-width:760px){section{padding-block:92px}}

.top{background:var(--teal-deep);padding-block:14px}
.top .in{display:flex;align-items:center;justify-content:space-between;gap:12px}
.top img{height:54px;width:auto}
.top .phone-link{font-size:.82rem;color:#D9E6E3;letter-spacing:.04em}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:56px;padding:0 30px;border-radius:999px;border:0;
  background:var(--blush);color:#fff;font-weight:600;font-size:.95rem;letter-spacing:.09em;text-transform:uppercase;text-decoration:none;text-align:center;
  box-shadow:0 8px 22px rgba(201,141,134,.35);transition:transform .15s ease,background .15s ease}
.btn:hover{background:#B9786F;transform:translateY(-1px)}
.btn.block{width:100%}
@container (min-width:760px){.btn.block{width:auto}}
.btn-row{display:flex;flex-direction:column;align-items:center;gap:10px;margin-top:34px;text-align:center}
.btn-row .sub{font-size:.92rem;color:var(--muted)}

/* hero */
.hero{background:var(--teal-deep);color:#fff;padding-block:36px 56px}
.hero .grid{display:grid;gap:30px;align-items:center}
@container (min-width:760px){.hero .grid{grid-template-columns:1.05fr 1fr;gap:56px}.hero{padding-block:64px 88px}}
.hero h1{font-size:clamp(2.45rem,8.4cqi,4.1rem);font-weight:500;color:#fff}
.hero .sub{font-size:1.06rem;color:#DCE7E4;margin-top:16px;max-width:34em}
.hero .loc{display:inline-block;margin-bottom:14px;font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:#F1CFCA;font-weight:500}
.hero .cta{margin-top:26px;display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.hero .cta .note{font-size:.92rem;color:#C9D9D5}
.hero .cta .btn{width:100%}
@container (min-width:760px){.hero .cta .btn{width:auto}}
.hero .photo{border-radius:20px;overflow:hidden;aspect-ratio:4/3}
.hero .photo img{width:100%;height:100%;object-fit:cover}
.trust{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:4px;font-size:.86rem;color:#DCE7E4}
.trust span::before{content:"✓";color:var(--blush);margin-right:6px;font-weight:700}

/* proof strip (B) */
.proof{background:var(--blush-soft);padding-block:26px}
.proof blockquote{margin:0;display:flex;flex-direction:column;gap:6px;align-items:center;text-align:center}
.proof q{font-family:var(--display);font-size:1.5rem;line-height:1.25;font-style:italic;color:var(--teal-deep);quotes:"“" "”"}
.proof cite{font-style:normal;font-size:.85rem;letter-spacing:.08em;color:var(--muted)}

/* who */
.who{background:var(--cream)}
.who .copy{max-width:40rem;margin:0 auto;display:flex;flex-direction:column;gap:18px;font-size:1.08rem;color:#3B3836}
.who .copy h2{margin-bottom:6px}
.who .hl{font-family:var(--display);font-size:1.6rem;line-height:1.3;color:var(--teal);border-left:3px solid var(--blush);padding-left:18px;margin-top:8px}

/* different */
.diff h2{text-align:center;max-width:22ch;margin:0 auto}
.diff .lead{max-width:38rem;margin:18px auto 0;text-align:center;color:var(--muted)}
.cards{display:grid;gap:22px;margin-top:40px}
@container (min-width:760px){.cards{grid-template-columns:repeat(3,1fr)}}
.card{background:var(--greige);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;min-width:0}
.card img{aspect-ratio:3/2;object-fit:cover;width:100%}
.card .t{padding:20px 22px 24px;display:flex;flex-direction:column;gap:8px}
.card h3{font-size:1.55rem;color:var(--teal-deep)}
.card p{font-size:.98rem;color:#45413E}
.card.key{outline:2px solid var(--blush)}

/* sharon */
.sharon{background:var(--greige)}
.sharon .grid{display:grid;gap:30px;align-items:center}
@container (min-width:760px){.sharon .grid{grid-template-columns:.8fr 1.2fr;gap:56px}}
.sharon .portrait{border-radius:20px;overflow:hidden;aspect-ratio:4/5;max-width:420px}
.sharon .portrait img{width:100%;height:100%;object-fit:cover;object-position:50% 20%}
.sharon .creds{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 22px}
.sharon .creds span{font-size:.8rem;letter-spacing:.04em;background:#fff;border:1px solid var(--rule);border-radius:999px;padding:6px 12px;color:var(--teal-deep)}
.sharon .copy{display:flex;flex-direction:column;gap:14px;color:#3B3836}

/* consult */
.consult{background:var(--teal-deep);color:#fff}
.consult h2{color:#fff}
.consult .grid{display:grid;gap:34px}
@container (min-width:860px){.consult .grid{grid-template-columns:.9fr 1.1fr;gap:56px;align-items:start}}
.consult .intro{color:#DCE7E4;margin-top:16px}
.consult ul{list-style:none;padding:0;margin:18px 0 0;display:flex;flex-direction:column;gap:12px}
.consult li{display:flex;gap:12px;color:#EEF4F2}
.consult li::before{content:"";flex:none;width:9px;height:9px;border-radius:50%;background:var(--blush);margin-top:.62em}
.consult .reassure{margin-top:20px;font-family:var(--display);font-size:1.45rem;font-style:italic;color:#F1CFCA}

/* cal mock */
.cal{background:#fff;color:var(--ink);border-radius:18px;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.25)}
.cal-head{display:flex;align-items:center;gap:12px;padding:16px 18px;border-bottom:1px solid var(--rule)}
.cal-head img{width:38px;height:38px;border-radius:50%;object-fit:cover;object-position:50% 15%}
.cal-head b{display:block;font-size:.98rem}
.cal-head small{color:var(--muted);font-size:.8rem}
.cal-body{display:grid;gap:0}
@container (min-width:620px){.cal-body{grid-template-columns:1.25fr 1fr}}
.month{padding:16px 18px}
.month .mh{display:flex;justify-content:space-between;font-weight:600;font-size:.95rem;margin-bottom:10px}
.month .mh span{color:var(--muted);font-weight:400}
.days{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;text-align:center;font-size:.82rem;font-variant-numeric:tabular-nums}
.days .dow{font-size:.68rem;letter-spacing:.06em;color:var(--muted);padding-bottom:4px}
.days button{border:0;background:none;aspect-ratio:1;border-radius:9px;color:#B5B1AD;font-size:.85rem;padding:0;cursor:default}
.days button.av{background:#E8F0EE;color:var(--teal-deep);font-weight:600;cursor:pointer}
.days button.sel{background:var(--teal-deep);color:#fff}
.slots{padding:16px 18px;border-top:1px solid var(--rule);display:flex;flex-direction:column;gap:8px}
@container (min-width:620px){.slots{border-top:0;border-left:1px solid var(--rule)}}
.slots .sh{font-size:.85rem;font-weight:600}
.slots button{border:1px solid var(--rule);background:#fff;border-radius:10px;padding:10px;font-size:.88rem;color:var(--teal-deep);font-variant-numeric:tabular-nums}
.slots button:hover{border-color:var(--teal-2)}
.cal-foot{font-size:.76rem;color:var(--muted);padding:10px 18px;border-top:1px dashed var(--rule);background:#FAFAF8}
.cal-foot a{color:var(--teal)}
.thanks{padding:34px 24px;text-align:center;display:flex;flex-direction:column;gap:12px;align-items:center}
.thanks .tick{width:56px;height:56px;border-radius:50%;background:var(--blush-soft);color:var(--blush);display:grid;place-items:center;font-size:1.6rem;font-weight:700}
.thanks h3{font-size:1.9rem;color:var(--teal-deep)}
.thanks p{color:var(--muted);font-size:.95rem;max-width:30em}
.thanks .url{font-family:ui-monospace,Menlo,monospace;font-size:.78rem;background:var(--greige);border-radius:6px;padding:3px 8px;color:var(--teal-deep)}

/* testimonials */
.voices h2{text-align:center}
.quotes{display:grid;gap:20px;margin-top:38px}
@container (min-width:760px){.quotes{grid-template-columns:repeat(3,1fr)}}
.quote{margin:0;background:var(--cream);border-radius:18px;padding:26px 24px;display:flex;flex-direction:column;gap:14px;min-width:0}
.quote .mark{font-family:var(--display);font-size:3.4rem;line-height:.6;color:var(--blush);height:.45em}
.quote p{font-family:var(--display);font-size:1.32rem;line-height:1.35;color:var(--teal-deep)}
.quote cite{font-style:normal;font-size:.85rem;letter-spacing:.06em;color:var(--muted);margin-top:auto}

/* faq (B) */
.faq{background:var(--cream)}
.faq h2{text-align:center}
.qa{max-width:44rem;margin:34px auto 0;display:flex;flex-direction:column;gap:10px}
.qa details{background:#fff;border:1px solid var(--rule);border-radius:14px}
.qa summary{list-style:none;cursor:pointer;padding:18px 20px;font-weight:600;display:flex;justify-content:space-between;gap:16px;align-items:center}
.qa summary::-webkit-details-marker{display:none}
.qa summary::after{content:"+";font-size:1.4rem;color:var(--blush);line-height:1}
.qa details[open] summary::after{content:"–"}
.qa .ans{padding:0 20px 18px;color:#45413E}
.fill{background:#FFF1C9;border-radius:4px;padding:0 4px;color:#6A4E00;font-size:.92em}

/* final */
.final{background:var(--greige);text-align:center}
.final h2{max-width:20ch;margin:0 auto}
.final .lead{color:var(--muted);margin-top:14px}
.addr{margin-top:26px;display:inline-flex;flex-direction:column;gap:2px;font-size:.98rem}
.addr b{font-weight:600}
.addr small{color:var(--muted);margin-top:8px;font-size:.9rem}
footer{background:var(--ink);color:#BDB8B3;font-size:.82rem;padding-block:26px 30px}
footer .in{display:flex;flex-wrap:wrap;gap:8px 22px;justify-content:space-between}
footer a{color:#E2DDD8}

/* sticky mobile CTA */
.stick{position:sticky;bottom:0;z-index:5;padding:10px 14px calc(10px + env(safe-area-inset-bottom,0px));background:rgba(255,255,255,.96);border-top:1px solid var(--rule);box-shadow:0 -6px 20px rgba(0,0,0,.08)}
.stick .btn{width:100%;min-height:52px;box-shadow:none}
@container (min-width:760px){.stick{display:none}}

/* pop-up (B) */
.modal{position:fixed;inset:0;z-index:60;background:rgba(18,30,32,.62);display:flex;align-items:flex-end;justify-content:center;padding:16px}
body.phone .modal{position:absolute}
@media (max-width:560px){body.phone .modal{position:fixed}}
.modal .sheet{width:100%;max-width:720px;max-height:92%;overflow:auto;border-radius:18px;background:#fff;container-type:inline-size}
@media (min-width:560px){.modal{align-items:center}}
.modal .x{position:sticky;top:0;display:flex;justify-content:flex-end;background:#fff;padding:8px 10px 0;z-index:2}
.modal .x button{border:0;background:var(--greige);border-radius:999px;width:36px;height:36px;font-size:1.2rem}

/* change tags (B) */
.chg{display:none}
body.show .chg{display:flex}
.chg{gap:10px;align-items:flex-start;background:#FFF6DA;border:1.5px solid var(--tag);color:#3A2E05;border-radius:12px;padding:10px 12px;font-size:.85rem;line-height:1.45;margin:14px 0;text-align:left;font-family:var(--body);font-style:normal;letter-spacing:0;text-transform:none;font-weight:400}
.chg b.n{flex:none;width:24px;height:24px;border-radius:50%;background:var(--tag);color:#1E1E1E;display:grid;place-items:center;font-size:.78rem}
.chg strong{font-weight:600}
.hero .chg,.consult .chg{background:#FFF6DA}
.summary{background:#FFFBEA;border-top:3px solid var(--tag);padding-block:40px}
.summary h2{font-size:2rem;color:#3A2E05}
.summary ol{margin:18px 0 0;padding-left:22px;display:flex;flex-direction:column;gap:10px;max-width:46rem}
.summary li{color:#3A2E05}
.summary .keep{margin-top:20px;color:#5A4B14;max-width:46rem}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""


def chg(n, text, b):
    return f'<div class="chg" role="note"><b class="n">{n}</b><span>{text}</span></div>' if b else ""


def cal_mock(b, uid):
    days = ['<div class="dow">S</div>', '<div class="dow">M</div>', '<div class="dow">T</div>', '<div class="dow">W</div>',
            '<div class="dow">T</div>', '<div class="dow">F</div>', '<div class="dow">S</div>']
    # November 2026 starts on a Sunday; example availability only.
    for d in range(1, 31):
        wd = (d - 1) % 7
        av = wd in (1, 2, 3, 4) and d >= 3
        cls = "av" + (" sel" if d == 5 else "") if av else ""
        days.append(f'<button type="button" class="{cls}" {"" if av else "disabled"} aria-label="November {d}">{d}</button>')
    slots = "".join(f'<button type="button" data-slot="{t}">{t}</button>' for t in ["9:00am", "11:30am", "4:00pm", "6:30pm"])
    after = ("Picking a time here walks through the booking, then lands on your thank-you page." if b
             else "On the real page this is your live Cal.com calendar, and visitors book without leaving the page.")
    return f'''<div class="cal" id="cal-{uid}">
  <div class="cal-head"><img src="img/sharon.jpg" alt=""/><div><b>Free Consultation</b><small>Lifted Strength Club · Longwood, FL</small></div></div>
  <div class="cal-step">
  <div class="cal-body">
    <div class="month"><div class="mh">November 2026 <span>Example times</span></div><div class="days">{"".join(days)}</div></div>
    <div class="slots"><div class="sh">Thu, Nov 5</div>{slots}</div>
  </div>
  </div>
  <div class="cal-foot">Preview of your Cal.com calendar. {after} <a href="{CAL}" target="_blank" rel="noopener">Open the real booking page ↗</a></div>
</div>'''


def page(b):
    btn_attr = 'data-book' if b else 'href="#book"'
    tag = "button type=\"button\"" if b else "a"
    endtag = "button" if b else "a"

    def button(label="Book your free consultation", extra=""):
        return f'<{tag} class="btn {extra}" {btn_attr}>{label}</{endtag}>'

    if b:
        hero_h = "Personalized strength training, in a small group."
        hero_loc = "Small-group personal training · Longwood, FL"
        hero_img = '<div class="photo"><img src="img/t3.jpg" alt="Dr. Sharon Gam coaching a member through a cable exercise at Lifted"/></div>'
        hero_note = '<div class="trust"><span>Free</span><span>No workout required</span><span>No experience needed</span></div>'
    else:
        hero_h = "A Different Kind Of Strength Training Studio"
        hero_loc = "Small-Group Personal Training in Longwood, FL"
        hero_img = '<div class="photo"><img src="img/studio.jpg" alt="Inside the Lifted Strength Club studio"/></div>'
        hero_note = ""

    hero = f'''<section class="hero"><div class="in"><div class="grid">
  <div>
    <span class="loc">{hero_loc}</span>
    <h1>{hero_h}</h1>
    {chg(1, "<strong>Headline leads with what you get.</strong> Personalized training and small groups are what set you apart, so they go first. We'd match the final wording to your ads, so people see the same promise they clicked on. Your original headline is a good one to test against it.", b)}
    <p class="sub">Personalized strength training in a small, supportive environment where you can build strength, confidence, and resilience, at your own pace.</p>
    <div class="cta">{button(extra="block")}<span class="note">Come see the studio and learn how Lifted works.</span>{hero_note}</div>
    {chg(4, "<strong>Every booking button opens your calendar in a pop-up</strong>, wherever the visitor is on the page. Try it. No scrolling, and nobody leaves the page.", b)}
  </div>
  <div>{hero_img}{chg(2, "<strong>A photo of real coaching</strong> instead of the empty studio, so people picture themselves training here before they scroll.", b)}</div>
</div></div></section>'''

    proof = f'''<div class="proof"><div class="in"><blockquote><q>Judgement-free zone, super motivational crew. I truly look forward to my twice weekly sessions.</q><cite>LISA R. · MEMBER</cite></blockquote>
  {chg(3, "<strong>A member review straight after the top section.</strong> People who click an ad don't know you yet, and reviews reassure them most. Most of them won't scroll down to a testimonials section near the bottom. We also moved the full testimonials higher.", b)}</div></div>''' if b else ""

    who = '''<section class="who"><div class="in"><div class="copy">
  <h2>Strength Training That Meets You Where You Are</h2>
  <p>Maybe you want to get stronger, but traditional gyms feel overwhelming. Maybe you've tried group fitness classes but struggled to keep up, or felt like the workouts weren't designed for you.</p>
  <p>At Lifted Strength Club, we do things differently.</p>
  <p class="hl">You don't need to be fit, strong, or experienced before you start. You just need a place where you feel comfortable showing up and giving it a try.</p>
</div></div></section>'''

    diff = f'''<section class="diff"><div class="in">
  <h2>Personalized Training. Small Groups. Individual Support.</h2>
  {'<p class="lead">Everyone trains together, but every member follows their own personalized program.</p>' if b else ''}
  <div class="cards">
    <article class="card{' key' if b else ''}"><img src="img/t2.jpg" alt="A member doing a seated press while Sharon coaches"/><div class="t"><h3>Your Own Personalized Program</h3><p>We don't do one-size-fits-all workouts. Your exercises are selected for your goals, abilities, and needs.</p></div></article>
    <article class="card"><img src="img/t6.jpg" alt="Sharon coaching a member through a deadlift"/><div class="t"><h3>Expert Coaching In Small Groups</h3><p>Train alongside a small group of up to five people, with a qualified coach there to guide, support, and challenge you.</p></div></article>
    <article class="card"><img src="img/t5.jpg" alt="Sharon and a member squatting together"/><div class="t"><h3>More Than Physical Strength</h3><p>Build confidence, resilience, and a sense of accomplishment as you discover what you're capable of.</p></div></article>
  </div>
  <div class="btn-row">{button()}</div>
</div></section>'''

    quotes = '''<section class="voices"><div class="in">
  <h2>What Our Members Are Saying</h2>
  <div class="quotes">
    <figure class="quote"><span class="mark" aria-hidden="true">“</span><p>I love the small-group setting, the friendly atmosphere, and the way the coaches offer just the right amount of encouragement and challenge.</p><cite>RINA A.</cite></figure>
    <figure class="quote"><span class="mark" aria-hidden="true">“</span><p>I love the way my workout is customized to ME. It's been a very balanced experience having personalized training within a group setting.</p><cite>LISA R.</cite></figure>
    <figure class="quote"><span class="mark" aria-hidden="true">“</span><p>I knew nothing about exercising or strength training. Three months later I now feel confident enough to continue on my journey for years to come.</p><cite>HALEY D.</cite></figure>
  </div>
</div></section>'''

    sharon = '''<section class="sharon"><div class="in"><div class="grid">
  <div class="portrait"><img src="img/sharon.jpg" alt="Dr. Sharon Gam"/></div>
  <div>
    <span class="eyebrow">Meet your coach</span>
    <h2 style="margin-top:10px">Hi, I'm Dr. Sharon Gam.</h2>
    <div class="creds"><span>PhD Exercise Physiology</span><span>Certified Strength and Conditioning Specialist</span><span>Certified Health Coach</span></div>
    <div class="copy">
      <p>I've spent 20 years helping people use strength training to improve their physical and mental well-being.</p>
      <p>I created Lifted Strength Club because I believe everyone deserves a place where they feel safe, supported, and capable of getting stronger.</p>
      <p>My approach isn't about changing how your body looks. It's about changing what your body can do, and how you feel about yourself.</p>
    </div>
  </div>
</div></div></section>'''

    faq = f'''<section class="faq"><div class="in">
  <h2>Questions people ask before they book</h2>
  {chg(5, "<strong>New: a short FAQ.</strong> These are the questions that stop people booking, and price is the big one. Even \"memberships start at $X\" stops people leaving the page to go find out. <strong>We need your answers for the highlighted parts.</strong>", b)}
  <div class="qa">
    <details open><summary>How much does membership cost?</summary><div class="ans">Memberships start at <span class="fill">$___ / month</span>. We'll go over the options at your consultation and help you pick the one that fits. There's no obligation to sign up.</div></details>
    <details><summary>I'm a complete beginner. Is that OK?</summary><div class="ans">Yes. You don't need to be fit, strong, or experienced before you start. Your program is built around where you are right now.</div></details>
    <details><summary>Will I be pressured to join?</summary><div class="ans">No. The consultation is relaxed and no-pressure: a tour, a conversation about your goals, and a chance to ask questions.</div></details>
    <details><summary>Do I need to work out at the consultation?</summary><div class="ans">No workout required. Come as you are.</div></details>
    <details><summary>When are classes, and where do I park?</summary><div class="ans">Sessions run <span class="fill">days / times</span>. Parking: <span class="fill">where to park</span>.</div></details>
  </div>
</div></section>''' if b else ""

    consult_list = '''<ul><li>Tour our welcoming studio.</li><li>Tell us about your goals and what you're looking for.</li><li>Learn how our personalized small-group training works.</li><li>Ask questions and see whether Lifted is a good fit for you.</li></ul>'''
    consult = f'''<section class="consult" id="book"><div class="in"><div class="grid">
  <div>
    <span class="eyebrow">Free consultation</span>
    <h2 style="margin-top:10px">Curious About Lifted? Come See for Yourself.</h2>
    <p class="intro">Your free consultation is a relaxed, no-pressure opportunity to:</p>
    {consult_list}
    <p class="reassure">No workout required and no fitness experience needed.</p>
    {chg(6, "<strong>Booking ends on a thank-you page.</strong> Pick a time in the calendar to see it. That page is how Google Analytics and your Meta ads count a real booking, separately from someone who only clicked the button.", b)}
  </div>
  <div>{cal_mock(b, "inline")}</div>
</div></div></section>'''

    final = f'''<section class="final"><div class="in">
  <h2>Ready to Get Stronger? We'd Love to Meet You.</h2>
  <p class="lead">Come discover a different kind of strength training at Lifted Strength Club.</p>
  <div class="addr"><b>Lifted Strength Club</b><span>2100 N Ronald Reagan Blvd, Suite 1012</span><span>Longwood, FL 32750</span><small>Conveniently located for Longwood, Lake Mary, and surrounding communities.</small></div>
  <div class="btn-row">{button()}</div>
  {chg(7, "<strong>No menu anywhere on the page</strong>, as you asked. It ends on one booking button, and the page stays out of Google search results so your ad numbers stay clean.", b)}
</div></section>'''

    footer = '''<footer><div class="in"><span>© 2026 Lifted Strength Club · Dr. Sharon Gam, PhD · Longwood, FL</span><span>sharon@drsharongam.com · <a href="#" onclick="return false">Privacy policy</a></span></div></footer>'''

    stick = f'<div class="stick">{button()}</div>'

    if b:
        order = [hero, proof, who, diff, quotes, sharon, faq, consult, final, footer]
    else:
        order = [hero, who, diff, sharon, consult, quotes, final, footer]
    return '<div class="lp"><div class="top"><div class="in"><img src="img/logo-white.png" alt="Lifted Strength Club"/></div></div>' + "".join(order) + stick + "</div>"


def summary():
    items = [
        "Headline leads with what you get (personalized program, small group, Longwood). The final wording would match your ads.",
        "A photo of real coaching at the top instead of the empty studio.",
        "A member review right after the top section, and the testimonials moved higher.",
        "Booking buttons open the calendar in a pop-up from anywhere on the page.",
        "A short FAQ before the calendar: cost, beginners, no pressure, schedule and parking.",
        "Booking ends on a thank-you page, which is how real bookings get counted for Google Analytics and Meta.",
        "No menu, one booking button to finish, and the page kept out of Google search so your ad numbers stay clean.",
    ]
    lis = "".join(f"<li>{t}</li>" for t in items)
    return f'''<div class="summary"><div class="in"><h2>What's different from Mockup A</h2><ol>{lis}</ol>
<p class="keep">Everything else is your copy, word for word, and your layout: no menu, a booking button that stays at the bottom on phones, your Cal.com calendar on the page, and three cards that stack on mobile.</p></div></div>'''


JS_COMMON = r"""
(function(){
  const body=document.body;
  const store={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
  const segBtns=document.querySelectorAll('.seg button');
  function setMode(m){body.classList.toggle('phone',m==='phone');segBtns.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===m)));store.set('lp-mode',m)}
  segBtns.forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.mode)));
  setMode(store.get('lp-mode')||'phone');
  const sw=document.getElementById('showchg');
  if(sw){const on=v=>{body.classList.toggle('show',v);sw.setAttribute('aria-pressed',String(v))};sw.addEventListener('click',()=>on(!body.classList.contains('show')));}
  // anchor buttons scroll inside the phone frame too
  document.querySelectorAll('a[href="#book"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();document.getElementById('book').scrollIntoView({behavior:'smooth',block:'start'})}));
  // calendar date picking (example only)
  document.querySelectorAll('.cal').forEach(cal=>{
    cal.addEventListener('click',e=>{
      const d=e.target.closest('.days button.av');
      if(d){cal.querySelectorAll('.days .sel').forEach(x=>x.classList.remove('sel'));d.classList.add('sel');
        const n=+d.textContent, wd=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][(n-1)%7];cal.querySelector('.slots .sh').textContent=wd+', Nov '+n;}
      const s=e.target.closest('.slots button[data-slot]');
      if(s && window.LP_BOOK){window.LP_BOOK(cal,s.dataset.slot,cal.querySelector('.slots .sh').textContent)}
    });
  });
})();
"""

JS_B = r"""
(function(){
  const modal=document.getElementById('modal'), sheet=modal.querySelector('.sheet');
  let last=null;
  function open(){last=document.activeElement;modal.hidden=false;modal.querySelector('.x button').focus()}
  function close(){modal.hidden=true;resetAll();if(last)last.focus()}
  document.querySelectorAll('[data-book]').forEach(b=>b.addEventListener('click',open));
  modal.addEventListener('click',e=>{if(e.target===modal)close()});
  modal.querySelector('.x button').addEventListener('click',close);
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!modal.hidden)close()});
  const originals=new Map();
  document.querySelectorAll('.cal').forEach(c=>originals.set(c,c.querySelector('.cal-step').innerHTML));
  function resetAll(){originals.forEach((html,c)=>{c.querySelector('.cal-step').innerHTML=html})}
  window.LP_BOOK=function(cal,slot,day){
    cal.querySelector('.cal-step').innerHTML='<div class="thanks"><div class="tick">✓</div><h3>You\'re booked, see you soon!</h3><p>'+day+' at '+slot+'. A confirmation email is on its way with the address and what to expect.</p><span class="url">liftedstrengthclub.com/consultation-booked</span><p style="font-size:.82rem">This thank-you page is where a completed booking gets counted for Google Analytics and Meta.</p><button type="button" class="btn" style="min-height:44px;font-size:.8rem">Back</button></div>';
    cal.querySelector('.thanks .btn').addEventListener('click',()=>{cal.querySelector('.cal-step').innerHTML=originals.get(cal)});
  };
})();
"""


def doc(b):
    title = "Lifted Ad Page · Mockup B" if b else "Lifted Ad Page · Mockup A"
    if b:
        bar = f'''<div class="bar"><div class="bar-in"><div class="tagline"><b>Mockup B · Recommended</b> <span>Your plan plus our suggested changes.</span> <a class="otherlink" href="{LINK_A}" target="_blank" rel="noopener">See Mockup A</a></div>
<div class="seg" role="group" aria-label="Preview size"><button type="button" data-mode="phone">Phone</button><button type="button" data-mode="desktop">Desktop</button></div>
<button type="button" class="switch" id="showchg" aria-pressed="false">Show what changed</button></div></div>'''
    else:
        bar = f'''<div class="bar"><div class="bar-in"><div class="tagline"><b>Mockup A · Exactly as requested</b> <span>Your sections, your copy, your order.</span> <a class="otherlink" href="{LINK_B}" target="_blank" rel="noopener">See Mockup B (recommended)</a></div>
<div class="seg" role="group" aria-label="Preview size"><button type="button" data-mode="phone">Phone</button><button type="button" data-mode="desktop">Desktop</button></div></div></div>'''
    modal = f'''<div class="modal" id="modal" hidden role="dialog" aria-modal="true" aria-label="Book your free consultation"><div class="sheet"><div class="x"><button type="button" aria-label="Close">×</button></div><div style="padding:0 14px 14px">{cal_mock(True, "pop")}</div></div></div>''' if b else ""
    tail = summary() if b else ""
    return f'''<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
{bar}
<div class="stage"><div class="device"><div class="screen">{page(b)}{tail}</div>{modal}</div></div>
<script>{JS_COMMON}</script>
{"<script>" + JS_B + "</script>" if b else ""}
'''


(HERE / "lifted-ad-page-a.html").write_text(doc(False))
(HERE / "lifted-ad-page-b.html").write_text(doc(True))
print("ok")
