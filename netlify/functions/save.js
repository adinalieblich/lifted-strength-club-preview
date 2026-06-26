// Save inline edits to the repo (GitHub) -> Netlify rebuilds -> live.
// Handles: text edits (innerHTML of [data-edit]), link URLs (href of [data-edit]),
// and image swaps (upload file + set src of [data-edit-img]). Pure Node, no deps.
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

// Find the opening tag that carries markerAttr="key" (robust against "<" in earlier attrs).
function findTag(html, markerAttr, key) {
  const marker = markerAttr + '="' + key + '"';
  const mi = html.indexOf(marker);
  if (mi === -1) return null;
  const open = /<([a-zA-Z0-9]+)(\s[^<>]*)?$/.exec(html.slice(0, mi + marker.length));
  if (!open) return null;
  const lt = open.index;
  const gt = html.indexOf(">", mi);
  if (gt === -1) return null;
  return { tag: open[1].toLowerCase(), lt: lt, gt: gt };
}

// Replace innerHTML of [data-edit="key"].
function setEdit(html, key, value) {
  const t = findTag(html, "data-edit", key);
  if (!t) return html;
  if (html[t.gt - 1] === "/") return html; // void/self-closing
  const lower = html.toLowerCase();
  let depth = 1, i = t.gt + 1;
  const openNeedle = "<" + t.tag, closeNeedle = "</" + t.tag + ">";
  while (i < html.length) {
    const nO = lower.indexOf(openNeedle, i), nC = lower.indexOf(closeNeedle, i);
    if (nC === -1) return html;
    if (nO !== -1 && nO < nC) {
      const a = html[nO + openNeedle.length];
      if (a && /[\s>\/]/.test(a)) depth++;
      i = nO + openNeedle.length;
    } else {
      depth--;
      if (depth === 0) return html.slice(0, t.gt + 1) + value + html.slice(nC);
      i = nC + closeNeedle.length;
    }
  }
  return html;
}

// Set/replace an attribute (e.g. href, src) on the element carrying markerAttr="key".
function setAttr(html, markerAttr, key, attr, value) {
  const t = findTag(html, markerAttr, key);
  if (!t) return html;
  let tag = html.slice(t.lt, t.gt + 1);
  const safe = String(value).replace(/"/g, "&quot;");
  const re = new RegExp("\\s" + attr + '="[^"]*"');
  if (re.test(tag)) tag = tag.replace(re, " " + attr + '="' + safe + '"');
  else tag = tag.replace(/\/?>$/, ' ' + attr + '="' + safe + '">');
  return html.slice(0, t.lt) + tag + html.slice(t.gt + 1);
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return { statusCode: 405, body: "Method not allowed" };
  const auth = event.headers.authorization || event.headers.Authorization || "";
  const token = auth.replace(/^Bearer\s+/i, "");
  const secret = process.env.JWT_SECRET || "";
  const payload = secret ? verify(token, secret) : null;
  if (!payload) return { statusCode: 401, body: JSON.stringify({ error: "Please log in again." }) };
  if ((event.body || "").length > 6 * 1024 * 1024) return { statusCode: 413, body: "Payload too large" };

  let path, edits = [], links = [], images = [];
  try { ({ path, edits = [], links = [], images = [] } = JSON.parse(event.body || "{}")); }
  catch (e) { return { statusCode: 400, body: "Bad request" }; }
  if (!path || (!edits.length && !links.length && !images.length))
    return { statusCode: 400, body: "Nothing to save" };
  if (path.includes("..") || path.startsWith("/") || !/^[A-Za-z0-9._\/-]+\.html$/.test(path))
    return { statusCode: 400, body: "Bad path" };
  if (images.length > 12) return { statusCode: 400, body: "Too many images at once" };

  const repo = process.env.GH_REPO || "adinalieblich/lifted-strength-club-preview";
  const branch = process.env.GH_BRANCH || "master";
  const ghToken = process.env.GITHUB_TOKEN;
  if (!ghToken) return { statusCode: 500, body: JSON.stringify({ error: "Saving is not configured yet." }) };
  const base = "https://api.github.com/repos/" + repo + "/contents/";
  const headers = { Authorization: "Bearer " + ghToken, Accept: "application/vnd.github+json", "User-Agent": "lsc-editor" };
  const enc = (p) => p.split("/").map(encodeURIComponent).join("/");

  // 1) Upload any images first, then point their src at the uploaded file.
  let imgChanges = 0;
  for (const im of images) {
    if (!im || !im.key || !im.filename || !im.dataBase64) continue;
    let fn = (String(im.key) + "-" + String(im.filename)).replace(/[^A-Za-z0-9._-]/g, "-").slice(-90);
    const repoPath = "uploads/" + fn;
    // overwrite-safe: get existing sha if present
    let sha;
    const ex = await fetch(base + enc(repoPath) + "?ref=" + branch, { headers });
    if (ex.ok) { try { sha = (await ex.json()).sha; } catch (e) {} }
    const body = { message: "Upload image " + fn, content: String(im.dataBase64), branch };
    if (sha) body.sha = sha;
    const up = await fetch(base + enc(repoPath), { method: "PUT", headers: { ...headers, "content-type": "application/json" }, body: JSON.stringify(body) });
    if (!up.ok) { const t = await up.text(); return { statusCode: 502, body: JSON.stringify({ error: "Image upload failed.", detail: t.slice(0, 200) }) }; }
    im._repoPath = "/" + repoPath; imgChanges++;
  }

  // 2) Get the page, apply text + link + image-src changes.
  const getRes = await fetch(base + enc(path) + "?ref=" + branch, { headers });
  if (!getRes.ok) return { statusCode: 502, body: JSON.stringify({ error: "Could not open the page file." }) };
  const file = await getRes.json();
  let content = Buffer.from(file.content, "base64").toString("utf8");
  let changed = 0;
  for (const e of edits) {
    if (!e || !e.key) continue;
    const b = content; content = setEdit(content, String(e.key), String(e.html == null ? "" : e.html));
    if (content !== b) changed++;
  }
  for (const l of links) {
    if (!l || !l.key) continue;
    const b = content; content = setAttr(content, "data-edit", String(l.key), "href", String(l.href || "#"));
    if (content !== b) changed++;
  }
  for (const im of images) {
    if (!im || !im._repoPath) continue;
    content = setAttr(content, "data-edit-img", String(im.key), "src", im._repoPath);
  }
  if (!changed && !imgChanges) return { statusCode: 200, body: JSON.stringify({ ok: true, changed: 0 }) };

  const n = changed + imgChanges;
  const put = await fetch(base + enc(path), {
    method: "PUT",
    headers: { ...headers, "content-type": "application/json" },
    body: JSON.stringify({
      message: "Inline edit: " + path + " (" + n + " change" + (n > 1 ? "s" : "") + ")",
      content: Buffer.from(content, "utf8").toString("base64"),
      sha: file.sha, branch,
    }),
  });
  if (!put.ok) { const t = await put.text(); return { statusCode: 502, body: JSON.stringify({ error: "Save failed.", detail: t.slice(0, 200) }) }; }
  return { statusCode: 200, headers: { "content-type": "application/json" }, body: JSON.stringify({ ok: true, changed: n }) };
};
