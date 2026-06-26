// Editor login: email + password -> signed JWT (30 days). No GitHub needed for the editor.
const crypto = require("crypto");

function b64url(buf) {
  return Buffer.from(buf).toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
function sign(payload, secret) {
  const header = b64url(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const body = b64url(JSON.stringify(payload));
  const data = header + "." + body;
  const sig = b64url(crypto.createHmac("sha256", secret).update(data).digest());
  return data + "." + sig;
}
function safeEq(a, b) {
  const ab = Buffer.from(String(a)); const bb = Buffer.from(String(b));
  if (ab.length !== bb.length) return false;
  return crypto.timingSafeEqual(ab, bb);
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return { statusCode: 405, body: "Method not allowed" };
  let email = "", password = "";
  try { ({ email = "", password = "" } = JSON.parse(event.body || "{}")); }
  catch (e) { return { statusCode: 400, body: "Bad request" }; }

  const okEmail = (process.env.EDITOR_EMAIL || "").toLowerCase().trim();
  const okPass = process.env.EDITOR_PASSWORD || "";
  const secret = process.env.JWT_SECRET || "";
  if (!okEmail || !okPass || !secret) {
    return { statusCode: 500, body: JSON.stringify({ error: "Editor login is not configured yet." }) };
  }
  const emailOk = safeEq(email.toLowerCase().trim(), okEmail);
  const passOk = safeEq(password, okPass);
  if (!emailOk || !passOk) {
    return { statusCode: 401, body: JSON.stringify({ error: "Wrong email or password." }) };
  }
  const exp = Math.floor(Date.now() / 1000) + 60 * 60 * 24 * 30;
  const token = sign({ sub: okEmail, exp }, secret);
  return { statusCode: 200, headers: { "content-type": "application/json" }, body: JSON.stringify({ token }) };
};
