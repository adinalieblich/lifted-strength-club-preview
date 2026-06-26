// Save inline edits: verify JWT, replace [data-edit="KEY"] inner HTML in the page file,
// commit to GitHub -> Netlify rebuilds -> live. Pure Node (crypto + global fetch), no deps.
const crypto = require("crypto");

function b64urlDecode(s) {
  s = s.replace(/-/g, "+").replace(/_/g, "/");
  while (s.length % 4) s += "=";
  return Buffer.from(s, "base64");
}
function verify(token, secret) {
  if (!token) return null;
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  const data = parts[0] + "." + parts[1];
  const expected = crypto.createHmac("sha256", secret).update(data).digest();
  const got = b64urlDecode(parts[2]);
  if (expected.length !== got.length || !crypto.timingSafeEqual(expected, got)) return null;
  let payload;
  try { payload = JSON.parse(b64urlDecode(parts[1]).toString("utf8")); } catch (e) { return null; }
  if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) return null;
  return payload;
}

// Replace the inner HTML of the element carrying data-edit="key". Handles nested tags
// by counting opens/closes of the same tag name. Returns the (possibly) updated html.
function setEdit(html, key, value) {
  const marker = 'data-edit="' + key + '"';
  const mi = html.indexOf(marker);
  if (mi === -1) return html;
  // Derive the tag from the REAL opening tag: walk back to a "<tag ...attrs" that ends at
  // the marker, forbidding any "<" in between — so a "<" inside an earlier attribute value
  // can't be mistaken for the tag start (would otherwise corrupt the doc). No match => no-op.
  const open = /<([a-zA-Z0-9]+)(\s[^<>]*)?$/.exec(html.slice(0, mi + marker.length));
  if (!open) return html;
  const tag = open[1].toLowerCase();
  const gt = html.indexOf(">", mi);
  if (gt === -1) return html;
  if (html[gt - 1] === "/") return html; // self-closing, nothing to edit
  const lower = html.toLowerCase();
  let depth = 1, i = gt + 1;
  const openNeedle = "<" + tag;
  const closeNeedle = "</" + tag + ">";
  while (i < html.length) {
    const nextOpen = lower.indexOf(openNeedle, i);
    const nextClose = lower.indexOf(closeNeedle, i);
    if (nextClose === -1) return html; // malformed; bail
    if (nextOpen !== -1 && nextOpen < nextClose) {
      const after = html[nextOpen + openNeedle.length];
      if (after && /[\s>\/]/.test(after)) depth++;
      i = nextOpen + openNeedle.length;
    } else {
      depth--;
      if (depth === 0) {
        return html.slice(0, gt + 1) + value + html.slice(nextClose);
      }
      i = nextClose + closeNeedle.length;
    }
  }
  return html;
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return { statusCode: 405, body: "Method not allowed" };
  const auth = event.headers.authorization || event.headers.Authorization || "";
  const token = auth.replace(/^Bearer\s+/i, "");
  const secret = process.env.JWT_SECRET || "";
  const payload = secret ? verify(token, secret) : null;
  if (!payload) return { statusCode: 401, body: JSON.stringify({ error: "Please log in again." }) };
  if ((event.body || "").length > 512 * 1024) return { statusCode: 413, body: "Payload too large" };

  let path, edits;
  try { ({ path, edits } = JSON.parse(event.body || "{}")); }
  catch (e) { return { statusCode: 400, body: "Bad request" }; }
  if (!path || !Array.isArray(edits) || !edits.length) return { statusCode: 400, body: "Nothing to save" };
  if (path.includes("..") || path.startsWith("/") || !/^[A-Za-z0-9._\/-]+\.html$/.test(path))
    return { statusCode: 400, body: "Bad path" };

  const repo = process.env.GH_REPO || "adinalieblich/lifted-strength-club-preview";
  const branch = process.env.GH_BRANCH || "master";
  const ghToken = process.env.GITHUB_TOKEN;
  if (!ghToken) return { statusCode: 500, body: JSON.stringify({ error: "Saving is not configured yet." }) };

  const api = "https://api.github.com/repos/" + repo + "/contents/" + path.split("/").map(encodeURIComponent).join("/");
  const headers = { Authorization: "Bearer " + ghToken, Accept: "application/vnd.github+json", "User-Agent": "lsc-editor" };

  const getRes = await fetch(api + "?ref=" + branch, { headers });
  if (!getRes.ok) return { statusCode: 502, body: JSON.stringify({ error: "Could not open the page file." }) };
  const file = await getRes.json();
  let content = Buffer.from(file.content, "base64").toString("utf8");
  let changed = 0;
  for (const e of edits) {
    if (!e || !e.key) continue;
    const before = content;
    content = setEdit(content, String(e.key), String(e.html == null ? "" : e.html));
    if (content !== before) changed++;
  }
  if (!changed) return { statusCode: 200, body: JSON.stringify({ ok: true, changed: 0 }) };

  const put = await fetch(api, {
    method: "PUT",
    headers: { ...headers, "content-type": "application/json" },
    body: JSON.stringify({
      message: "Inline edit: " + path + " (" + changed + " change" + (changed > 1 ? "s" : "") + ")",
      content: Buffer.from(content, "utf8").toString("base64"),
      sha: file.sha,
      branch,
    }),
  });
  if (!put.ok) {
    const t = await put.text();
    return { statusCode: 502, body: JSON.stringify({ error: "Save failed.", detail: t.slice(0, 200) }) };
  }
  return { statusCode: 200, headers: { "content-type": "application/json" }, body: JSON.stringify({ ok: true, changed }) };
};
