// Save inline edits -> GitHub -> Netlify rebuild.
//  Per-page: edits (innerHTML of [data-edit]), links (href), images (swap [data-edit-img]).
//  Global (nav/footer): globalEdits / globalLinks applied to EVERY page in one commit so
//  editing once propagates site-wide. Pure Node (crypto + global fetch), no deps.
const crypto = require("crypto");

function b64urlDecode(s) { s = s.replace(/-/g, "+").replace(/_/g, "/"); while (s.length % 4) s += "="; return Buffer.from(s, "base64"); }
function verify(token, secret) {
  if (!token) return null;
  const p = token.split("."); if (p.length !== 3) return null;
  const exp = crypto.createHmac("sha256", secret).update(p[0] + "." + p[1]).digest();
  const got = b64urlDecode(p[2]);
  if (exp.length !== got.length || !crypto.timingSafeEqual(exp, got)) return null;
  let pl; try { pl = JSON.parse(b64urlDecode(p[1]).toString("utf8")); } catch (e) { return null; }
  if (pl.exp && pl.exp < Math.floor(Date.now() / 1000)) return null;
  return pl;
}
function findTag(html, markerAttr, key) {
  const marker = markerAttr + '="' + key + '"';
  const mi = html.indexOf(marker); if (mi === -1) return null;
  const open = /<([a-zA-Z0-9]+)(\s[^<>]*)?$/.exec(html.slice(0, mi + marker.length));
  if (!open) return null;
  const gt = html.indexOf(">", mi); if (gt === -1) return null;
  return { tag: open[1].toLowerCase(), lt: open.index, gt: gt };
}
function setEdit(html, markerAttr, key, value) {
  const t = findTag(html, markerAttr, key); if (!t) return html;
  if (html[t.gt - 1] === "/") return html;
  const lower = html.toLowerCase(); let depth = 1, i = t.gt + 1;
  const oN = "<" + t.tag, cN = "</" + t.tag + ">";
  while (i < html.length) {
    const nO = lower.indexOf(oN, i), nC = lower.indexOf(cN, i);
    if (nC === -1) return html;
    if (nO !== -1 && nO < nC) { const a = html[nO + oN.length]; if (a && /[\s>\/]/.test(a)) depth++; i = nO + oN.length; }
    else { depth--; if (depth === 0) return html.slice(0, t.gt + 1) + value + html.slice(nC); i = nC + cN.length; }
  }
  return html;
}
function setAttr(html, markerAttr, key, attr, value) {
  const t = findTag(html, markerAttr, key); if (!t) return html;
  let tag = html.slice(t.lt, t.gt + 1);
  const safe = String(value).replace(/"/g, "&quot;");
  const re = new RegExp("\\s" + attr + '="[^"]*"');
  if (re.test(tag)) tag = tag.replace(re, " " + attr + '="' + safe + '"');
  else tag = tag.replace(/\/?>$/, ' ' + attr + '="' + safe + '">');
  return html.slice(0, t.lt) + tag + html.slice(t.gt + 1);
}
function applyAll(content, edits, links, images, marker) {
  for (const e of (edits || [])) if (e && e.key) content = setEdit(content, marker, String(e.key), String(e.html == null ? "" : e.html));
  for (const l of (links || [])) if (l && l.key) content = setAttr(content, marker, String(l.key), "href", String(l.href || "#"));
  for (const im of (images || [])) if (im && im._repoPath) content = setAttr(content, "data-edit-img", String(im.key), "src", im._repoPath);
  return content;
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return { statusCode: 405, body: "Method not allowed" };
  const auth = event.headers.authorization || event.headers.Authorization || "";
  const secret = process.env.JWT_SECRET || "";
  if (!secret || !verify(auth.replace(/^Bearer\s+/i, ""), secret))
    return { statusCode: 401, body: JSON.stringify({ error: "Please log in again." }) };
  if ((event.body || "").length > 6 * 1024 * 1024) return { statusCode: 413, body: "Payload too large" };

  let path, edits = [], links = [], images = [], globalEdits = [], globalLinks = [];
  try { ({ path, edits = [], links = [], images = [], globalEdits = [], globalLinks = [] } = JSON.parse(event.body || "{}")); }
  catch (e) { return { statusCode: 400, body: "Bad request" }; }
  if (!path) return { statusCode: 400, body: "Missing page" };
  if (path.includes("..") || path.startsWith("/") || !/^[A-Za-z0-9._\/-]+\.html$/.test(path)) return { statusCode: 400, body: "Bad path" };
  if (images.length > 12) return { statusCode: 400, body: "Too many images at once" };
  const hasLocal = edits.length || links.length || images.length;
  const hasGlobal = globalEdits.length || globalLinks.length;
  if (!hasLocal && !hasGlobal) return { statusCode: 400, body: "Nothing to save" };

  const repo = process.env.GH_REPO || "adinalieblich/lifted-strength-club-preview";
  const branch = process.env.GH_BRANCH || "master";
  const ghToken = process.env.GITHUB_TOKEN;
  if (!ghToken) return { statusCode: 500, body: JSON.stringify({ error: "Saving is not configured yet." }) };
  const ghBase = "https://api.github.com/repos/" + repo;
  const cBase = ghBase + "/contents/";
  const headers = { Authorization: "Bearer " + ghToken, Accept: "application/vnd.github+json", "User-Agent": "lsc-editor" };
  const enc = (p) => p.split("/").map(encodeURIComponent).join("/");
  let count = 0;

  // ---- per-page (proven path: Contents API) ----
  if (hasLocal) {
    for (const im of images) {
      if (!im || !im.key || !im.filename || !im.dataBase64) continue;
      const fn = (String(im.key) + "-" + String(im.filename)).replace(/[^A-Za-z0-9._-]/g, "-").slice(-90);
      const rp = "uploads/" + fn; let sha;
      const ex = await fetch(cBase + enc(rp) + "?ref=" + branch, { headers });
      if (ex.ok) { try { sha = (await ex.json()).sha; } catch (e) {} }
      const b = { message: "Upload image " + fn, content: String(im.dataBase64), branch }; if (sha) b.sha = sha;
      const up = await fetch(cBase + enc(rp), { method: "PUT", headers: { ...headers, "content-type": "application/json" }, body: JSON.stringify(b) });
      if (!up.ok) { const t = await up.text(); return { statusCode: 502, body: JSON.stringify({ error: "Image upload failed.", detail: t.slice(0, 200) }) }; }
      im._repoPath = "/" + rp;
    }
    const gp = await fetch(cBase + enc(path) + "?ref=" + branch, { headers });
    if (!gp.ok) return { statusCode: 502, body: JSON.stringify({ error: "Could not open the page file." }) };
    const file = await gp.json();
    let content = Buffer.from(file.content, "base64").toString("utf8");
    const before = content;
    content = applyAll(content, edits, links, images, "data-edit");
    if (content !== before || images.some((i) => i._repoPath)) {
      const put = await fetch(cBase + enc(path), { method: "PUT", headers: { ...headers, "content-type": "application/json" },
        body: JSON.stringify({ message: "Inline edit: " + path, content: Buffer.from(content, "utf8").toString("base64"), sha: file.sha, branch }) });
      if (!put.ok) { const t = await put.text(); return { statusCode: 502, body: JSON.stringify({ error: "Save failed.", detail: t.slice(0, 200) }) }; }
      count++;
    }
  }

  // ---- global (nav/footer): one commit across every page (Git Data API) ----
  let globalPages = 0, globalError = null;
  if (hasGlobal) {
    try {
      const ref = await (await fetch(ghBase + "/git/ref/heads/" + branch, { headers })).json();
      const baseSha = ref.object.sha;
      const baseCommit = await (await fetch(ghBase + "/git/commits/" + baseSha, { headers })).json();
      const baseTree = baseCommit.tree.sha;
      const tree = await (await fetch(ghBase + "/git/trees/" + baseTree + "?recursive=1", { headers })).json();
      const htmls = tree.tree.filter((t) => t.type === "blob" && /\.html$/.test(t.path));
      const changed = [];
      const batch = async (item) => {
        const blob = await (await fetch(ghBase + "/git/blobs/" + item.sha, { headers })).json();
        let c = Buffer.from(blob.content, "base64").toString("utf8");
        const b = c;
        c = applyAll(c, globalEdits, globalLinks, null, "data-edit-global");
        if (c !== b) changed.push({ path: item.path, mode: "100644", type: "blob", content: c });
      };
      for (let i = 0; i < htmls.length; i += 25) await Promise.all(htmls.slice(i, i + 25).map(batch));
      if (changed.length) {
        const newTree = await (await fetch(ghBase + "/git/trees", { method: "POST", headers: { ...headers, "content-type": "application/json" }, body: JSON.stringify({ base_tree: baseTree, tree: changed }) })).json();
        if (!newTree.sha) throw new Error("tree");
        const commit = await (await fetch(ghBase + "/git/commits", { method: "POST", headers: { ...headers, "content-type": "application/json" }, body: JSON.stringify({ message: "Global edit (" + changed.length + " pages)", tree: newTree.sha, parents: [baseSha] }) })).json();
        if (!commit.sha) throw new Error("commit");
        const upd = await fetch(ghBase + "/git/refs/heads/" + branch, { method: "PATCH", headers: { ...headers, "content-type": "application/json" }, body: JSON.stringify({ sha: commit.sha }) });
        if (!upd.ok) throw new Error("ref");
        globalPages = changed.length; count += changed.length;
      }
    } catch (e) { globalError = String(e && e.message || e); }
  }

  if (globalError) return { statusCode: 207, headers: { "content-type": "application/json" }, body: JSON.stringify({ ok: hasLocal ? true : false, changed: count, globalError: "Site-wide update didn't finish — please try again." }) };
  return { statusCode: 200, headers: { "content-type": "application/json" }, body: JSON.stringify({ ok: true, changed: count, globalPages }) };
};
