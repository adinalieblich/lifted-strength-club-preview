# Lifted Strength Club website — read this first

Static website for Dr. Sharon Gam's gym, **Lifted Strength Club** (Longwood, FL). Built and maintained by
Adina Lieblich. Live at https://liftedstrengthclub.com (drsharongam.com 301s to it). Hosted on Netlify,
deployed from `master`.

**Before doing anything, read [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md)** (where things stand, what's
open, who we're waiting on) and [`docs/DECISIONS.md`](docs/DECISIONS.md) (why things are the way they are).
Update both whenever something changes: a request comes in, work ships, a decision is made, Sharon replies.
They are the hand-over record if a chat session is lost.

## Working rules

- **Never push to `master` without Adina's OK.** `master` deploys live. Work on a `claude/...` branch.
- Sharon also edits the site herself through the inline editor (pencil "Edit" button, `edit-mode.js` +
  `netlify/functions`). Those arrive as `Inline edit: <page>` commits on `master`. Don't clobber them: merge
  `master` in before building on a page.
- Keep new elements editable the same way (`data-edit` / `data-edit-global` attributes), so Sharon can change
  wording and prices herself.
- Brand: dark teal `#3E6E73` / `#4D7E83`, blush `#C98D86`, greige `#F4F0EB`, cream `#F4F8F5`, brass `#B78B52`,
  charcoal `#2A2A2A`. Fonts: Cormorant Garamond (display) + Outfit (body).
- Booking: every "book" button goes to Cal.com, `https://cal.com/liftedstrengthclub/free-consultation`
  (Acuity is retired). The home page has the Cal.com inline embed (`flagship.html`).
- `_redirects` holds the legacy-URL 301 map from the Squarespace migration. Keep it intact.
- **This repo is public on GitHub, and every committed file is served by Netlify.** `docs/` and this file are
  blocked from the website by a forced 404 in `_redirects`. They are still readable on GitHub, so never put
  passwords, logins, account IDs, private pricing or email bodies in them.

## Working with Sharon

- Emails come from `sharon@drsharongam.com` (main), sometimes `sharon@liftedstrengthclub.com` or
  `sharongam22@gmail.com`. She's in Orlando (US Eastern) and emails at all hours.
- Replies go from Adina's Gmail, signed **"Claudina"**, warm and plain. **Never send an email without Adina's
  explicit OK.** Draft it, show her, then send.
- Show visual changes as a mockup first. Use a claude.ai Artifact, and remind Adina to turn on link sharing
  before Sharon gets the link, or Sharon can't open it.
- Daily email check: a scheduled task in Adina's Claude Code session runs at 6:40am ET. It finds new emails
  from Sharon, does the work on a branch, drafts the reply and waits for Adina's approval. Handled emails get
  the Gmail label `Claude-Sharon-done`.
