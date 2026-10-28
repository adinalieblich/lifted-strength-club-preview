# Project status

_Last updated: 2026-10-28. Update this file whenever something changes._

## Right now

**Waiting on Sharon** to choose a version of the ad landing page and send what we asked for (emailed Oct 27,
"Website" thread). Nothing is being built until she replies.

- Oct 27, 3:46pm ET: Sharon said the mockup links asked her to sign in. Adina turned on link sharing and
  replied Oct 27 evening asking her to try again. No reply from Sharon yet (checked Oct 28, 6:45am ET).

## Open work

### 1. Ad landing page: free-consultation page for Facebook/Instagram ads
- **Request (Sharon, Oct 22):** a focused page for paid ads whose job is to get visitors to book a free
  consultation, with tracking so she can see how the ads perform. She sent a 7-section brief with copy.
- **Our recommendation:** the dedicated page is the right approach. We suggested seven changes; see
  `DECISIONS.md` (2026-10-27).
- **Mockups sent Oct 27** (link sharing turned on Oct 28):
  - A, exactly as she asked: https://claude.ai/artifact/THpuENYgk8cm67HrxbWE2g
  - B, with our recommendations and a "Show what changed" toggle: https://claude.ai/artifact/AEMpbsN8XvPHzcDgkxLbxM
  - Source: `docs/mockups/ad-landing-page/` (see its README to rebuild).
- **Asked Sharon for:**
  - [ ] Which version (A, B or a mix)
  - [ ] Google Analytics admin access, or OK to create GA4 under her Google account
  - [ ] Meta Pixel ID or Meta Business access (her VA may have it)
  - [ ] Cal.com access (to redirect to a thank-you page after booking)
  - [ ] Studio photo of her (otherwise use the current headshot)
  - [ ] FAQ answers: starting price (only if she wants it shown), class days/times, parking
  - [ ] Her VA's ad copy, so the headline matches the ads
- **Build plan once she replies:**
  1. Install GA4 + Meta Pixel sitewide.
  2. Build `/free-consultation`: noindex, no menu, booking button that stays at the bottom on phones,
     Cal.com pop-up + inline embed.
  3. Add a `/consultation-booked` thank-you page as the conversion event (GA4 key event + Meta `Schedule`/`Lead`).
  4. Add or update the privacy policy to mention analytics and the pixel (Meta requires it).
  5. Make a test booking on a phone, then send Sharon a short guide to reading GA4, plus tagged ad links for her VA.

### 2. Analytics and tracking (part of 1, but sitewide)
- As of Oct 27 the site has **no Google Analytics and no Meta Pixel**, and no cookie banner. We told Sharon.
- Privacy policy: check whether one exists on the site; none was found in the file list.

### 3. Professional email `hello@liftedstrengthclub.com`
- Sharon asked for it (Oct 13 email), as one inbox alongside her current one (Adina's "Option A").
- Adina told her (Oct 2) she may need to set it up herself because of a small monthly fee.
- **Status unclear from the repo.** Confirm with Adina.

## Done (most recent first)

| Date | What | Where |
|---|---|---|
| 2026-10-15 | Acuity replaced with Cal.com on every page; home page Cal.com inline embed; Membership page redesign (Sharon's Oct 13 list: hero consult button, pricing simplified, one-on-one packages in a dropdown, etc.) | `a19536d` on master |
| 2026-10-07 | Ad-tracking copy of the Membership page (`membership-ad.html`, noindex) | `9852eff` |
| 2026-10-07 | Schedule page: sunburst removed per Sharon's feedback; she can mark classes full and add/remove time slots herself | `e8e8127` |
| 2026-09-16 | New Class Schedule page, matched to Sharon's example and added to the nav and footer | `dc94d72`, `a89ff26`, `6af02ad` |
| 2026-07-15 | Domain swap: liftedstrengthclub.com is the site, drsharongam.com 301s to it, all images hosted locally | `fe2c716` |
| 2026-06/07 | Squarespace migration, go-live URL mapping (all 193 old URLs resolve), SEO audits, inline editor for Sharon | see `git log` |

## Automation

- **Daily Sharon email check**, 6:40am America/New_York. It runs as a scheduled task bound to Adina's Claude
  Code session (trigger `trig_01SD43A3U8DqVBhRZ3vcwa1q`). It finds new emails from Sharon, does the work on a
  `claude/sharon-YYYY-MM-DD` branch, drafts a Gmail reply and waits for Adina's OK. It labels handled emails
  `Claude-Sharon-done`.
- If that session is lost, recreate the check as a routine in claude.ai, with the Gmail connector and this
  repo attached. The instructions are in `docs/DECISIONS.md` (2026-10-28).
