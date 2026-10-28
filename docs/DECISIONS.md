# Decision log

Newest first. Record what was decided, why, and who decided.

## 2026-10-28 — Project docs live in the repo
- `CLAUDE.md`, `docs/PROJECT-STATUS.md` and `docs/DECISIONS.md` are now committed, so work can resume if a
  chat session is lost. They used to be git-ignored and local-only, which meant they disappeared with each
  session.
- Netlify serves every committed file, so `_redirects` forces a 404 for `/docs/*` and `/CLAUDE.md`. The repo
  is **public** on GitHub, so these files must never hold credentials, account IDs or private details.
  Making the repo private would be safer (Adina to decide).

## 2026-10-28 — Daily email automation (Adina)
- Check once a day at 6:40am Orlando time. Sharon's emails over June to October are spread evenly across
  mornings, afternoons and late evenings (latest about 11pm ET), so early morning catches everything from the
  previous day.
- Scope: do the work and draft the reply, but **send nothing without Adina's approval**. Anything involving
  passwords, payments, account access, deletion or third parties gets flagged, not actioned.
- Set up as a scheduled task bound to Adina's session. A stand-alone routine created from the session could
  not be given the Gmail connector, and it didn't appear on the Routines page.
- Instructions to reuse if it ever has to be recreated as a routine:
  1. Search Gmail: `from:(sharon@drsharongam.com OR sharon@liftedstrengthclub.com OR sharongam22@gmail.com OR hello@liftedstrengthclub.com) after:2026/10/27 -label:Claude-Sharon-done`.
     Skip automated mail. Read whole threads.
  2. List everything she asks for. 3. Do the work on branch `claude/sharon-YYYY-MM-DD`, never on master;
     mockups as Artifacts where useful; recommend better approaches. 4. Gmail draft reply in the same
     thread, signed "Claudina", not sent. 5. Label handled emails `Claude-Sharon-done`. 6. Summarize for Adina
     and wait for approval before sending.

## 2026-10-27 — Ad landing page: two mockups, recommend B
Sharon's brief (written with AI help) was sound: a page with no menu and one call to action, built for
phones, is best practice for paid social. We built it exactly as asked (A) and with these changes (B):
1. **Headline leads with what you get** ("Personalized strength training, in a small group."), because her
   differentiator is a personal program inside a small group. Final wording should match the ad copy. Her
   headline is a good A/B test.
2. **Hero photo of real coaching**, not the empty studio.
3. **Social proof right after the top section** (Lisa R. quote), and testimonials moved above "Meet Sharon".
   Visitors from ads don't know her yet, and many won't scroll to section 6.
4. **Booking buttons open the Cal.com calendar in a pop-up**, instead of scrolling down the page.
5. **FAQ before the calendar** (price, beginners, no pressure, schedule, parking). Not knowing the price is a
   main reason people leave without booking. Whether to show a price is Sharon's call.
6. **Thank-you page after booking** (`/consultation-booked`), so GA4 and Meta count real bookings
   separately from button clicks.
7. **Address `/free-consultation`**, kept out of Google and out of the nav, to keep ad data clean.
Also: tag ad links with UTMs. The Oct 7 duplicate membership page wasn't strictly needed for tracking, since
UTMs on the normal page do the same job; going forward this landing page is the main ad destination.

## 2026-10-27 — Analytics status
Checked the code: no GA4, no Meta Pixel and no consent banner anywhere on the site. Sitewide install planned
alongside the landing page. Cookie banner probably not legally required for a small Florida business, but
Sharon should confirm. A privacy policy that mentions the pixel is required by Meta.

## 2026-10-15 — Membership page hero photo
Recommended "Lifted Strength Club 17.jpg" (centre-aisle studio shot) from the event photos Sharon sent, with
13.jpg as runner-up. Not yet confirmed whether the live page uses it (it currently shows
`images/Lifted-Strength-Club-Studio.jpg`).

## 2026-10 — Booking platform
Sharon moved free-consultation booking from Acuity to Cal.com. All buttons now use
`cal.com/liftedstrengthclub/free-consultation`.

## 2026-07-11 — Domain
liftedstrengthclub.com is the canonical site; drsharongam.com 301s to it, preserving paths.
