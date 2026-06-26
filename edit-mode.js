/* Lifted Strength Club — inline Edit Mode (live)
   Sharon logs in with email + password, clicks any marked text, edits it in place,
   and Save publishes it live (commits the change; the site rebuilds in ~1 min).
   - Login: POST /.netlify/functions/login -> JWT stored in localStorage.
   - Save:  POST /.netlify/functions/save  (Bearer JWT) -> commits the edited page.
   - Public visitors never see any of this. The editor only appears when logged in,
     or when the page is opened with ?edit (which shows the login box).
*/
(function () {
  var TOKEN_KEY = "lsc_token";
  var BRASS = "#B78B52", TEAL = "#123E47";

  function getToken() { try { return localStorage.getItem(TOKEN_KEY) || ""; } catch (e) { return ""; } }
  function setToken(t) { try { localStorage.setItem(TOKEN_KEY, t); } catch (e) {} }
  function clearToken() { try { localStorage.removeItem(TOKEN_KEY); } catch (e) {} }
  function tokenValid(t) {
    if (!t) return false;
    var p = t.split("."); if (p.length !== 3) return false;
    try {
      var s = p[1].replace(/-/g, "+").replace(/_/g, "/");
      var payload = JSON.parse(decodeURIComponent(escape(atob(s))));
      return !payload.exp || payload.exp > Math.floor(Date.now() / 1000);
    } catch (e) { return false; }
  }
  function currentPath() {
    var p = location.pathname;
    if (p === "/" || p === "") return "flagship.html";
    p = p.replace(/^\//, "");
    if (p.charAt(p.length - 1) === "/") p = p.slice(0, -1);
    if (!/\.html$/.test(p)) p += ".html";
    return p;
  }

  var css =
    '#lsc-fab{position:fixed;right:20px;bottom:20px;z-index:99998;background:' + TEAL + ';color:#fff;border:0;border-radius:40px;padding:12px 20px;font:600 14px Outfit,system-ui,sans-serif;box-shadow:0 8px 26px rgba(0,0,0,.3);cursor:pointer;display:flex;align-items:center;gap:8px}' +
    '#lsc-fab .dot{width:8px;height:8px;border-radius:50%;background:' + BRASS + '}' +
    '.lsc-editing [data-edit]{outline:2px dashed ' + BRASS + ';outline-offset:4px;border-radius:3px;cursor:text;transition:background .15s}' +
    '.lsc-editing [data-edit]:hover{background:rgba(183,139,82,.16)}' +
    '.lsc-editing [data-edit][contenteditable="true"]{background:rgba(183,139,82,.22);outline-style:solid}' +
    '.lsc-bar{position:fixed;left:50%;transform:translateX(-50%);bottom:22px;z-index:99999;display:flex;align-items:center;gap:13px;background:' + TEAL + ';color:#fff;padding:12px 18px;border-radius:14px;box-shadow:0 10px 34px rgba(0,0,0,.34);font:14px Outfit,system-ui,sans-serif}' +
    '.lsc-bar .dot{width:8px;height:8px;border-radius:50%;background:' + BRASS + ';animation:lscpulse 1.6s infinite}' +
    '@keyframes lscpulse{0%,100%{opacity:1}50%{opacity:.35}}' +
    '.lsc-bar b{font-weight:600}.lsc-bar button{font:inherit;border:0;border-radius:9px;padding:9px 16px;cursor:pointer;font-weight:600}' +
    '.lsc-save{background:' + BRASS + ';color:#1a1a1a}.lsc-save[disabled]{opacity:.45;cursor:default}' +
    '.lsc-ghost{background:transparent;color:#cfe2e0;padding:9px 8px!important}' +
    '.lsc-msg{font-size:12.5px;color:#F7E9CF}' +
    '.lsc-modal{position:fixed;inset:0;z-index:100000;background:rgba(18,42,47,.55);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center}' +
    '.lsc-card{background:#fff;border-radius:16px;padding:30px 30px 26px;width:340px;max-width:92vw;box-shadow:0 20px 60px rgba(0,0,0,.3);font:14px Outfit,system-ui,sans-serif;color:#2c2924}' +
    '.lsc-card h3{font:600 1.5rem "Cormorant Garamond",serif;color:' + TEAL + ';margin:0 0 4px}' +
    '.lsc-card p{margin:0 0 16px;color:#6E6A65;font-size:13px}' +
    '.lsc-card label{display:block;font-size:12px;color:#6E6A65;margin:10px 0 4px}' +
    '.lsc-card input{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid #d8d2c8;border-radius:9px;font:inherit}' +
    '.lsc-card button{margin-top:18px;width:100%;background:' + TEAL + ';color:#fff;border:0;border-radius:9px;padding:11px;font:600 14px Outfit,sans-serif;cursor:pointer}' +
    '.lsc-card .err{color:#A8584C;font-size:12.5px;margin-top:10px;min-height:1em}' +
    '.lsc-card .x{position:absolute;top:14px;right:16px;cursor:pointer;color:#999;font-size:20px;background:none;border:0;width:auto;margin:0;padding:0}';

  function injectCss() { var s = document.createElement("style"); s.textContent = css; document.head.appendChild(s); }

  // ---- login modal ----
  function showLogin() {
    var m = document.createElement("div");
    m.className = "lsc-modal";
    m.innerHTML =
      '<div class="lsc-card" style="position:relative">' +
      '<button class="x" aria-label="Close">&times;</button>' +
      '<h3>Edit your site</h3><p>Log in to make changes.</p>' +
      '<label>Email</label><input type="email" id="lsc-email" autocomplete="username">' +
      '<label>Password</label><input type="password" id="lsc-pass" autocomplete="current-password">' +
      '<button id="lsc-login">Log in</button>' +
      '<div class="err" id="lsc-err"></div></div>';
    document.body.appendChild(m);
    var close = function () { m.remove(); };
    m.querySelector(".x").onclick = close;
    m.addEventListener("click", function (e) { if (e.target === m) close(); });
    var doLogin = function () {
      var email = m.querySelector("#lsc-email").value;
      var password = m.querySelector("#lsc-pass").value;
      var err = m.querySelector("#lsc-err");
      err.textContent = "";
      fetch("/.netlify/functions/login", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ email: email, password: password }),
      }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (res.ok && res.j.token) { setToken(res.j.token); close(); mountFab(); enterEdit(); }
          else { err.textContent = (res.j && res.j.error) || "Login failed."; }
        }).catch(function () { err.textContent = "Network error — try again."; });
    };
    m.querySelector("#lsc-login").onclick = doLogin;
    m.querySelector("#lsc-pass").addEventListener("keydown", function (e) { if (e.key === "Enter") doLogin(); });
    m.querySelector("#lsc-email").focus();
  }

  // ---- floating Edit button ----
  function mountFab() {
    if (document.getElementById("lsc-fab")) return;
    var b = document.createElement("button");
    b.id = "lsc-fab";
    b.innerHTML = '<span class="dot"></span> Edit';
    b.onclick = enterEdit;
    document.body.appendChild(b);
  }

  // ---- edit mode ----
  var editing = false;
  function enterEdit() {
    if (editing) return;
    editing = true;
    var fab = document.getElementById("lsc-fab"); if (fab) fab.style.display = "none";
    document.body.classList.add("lsc-editing");
    var els = Array.prototype.slice.call(document.querySelectorAll("[data-edit]"));
    var original = {};
    els.forEach(function (el) {
      original[el.getAttribute("data-edit")] = el.innerHTML;
      el.addEventListener("click", onElClick);
      el.addEventListener("input", markDirty);
      el.addEventListener("keydown", function (e) { if (e.key === "Escape") el.blur(); });
    });

    var bar = document.createElement("div");
    bar.className = "lsc-bar";
    bar.innerHTML =
      '<span><span class="dot"></span> <b>Editing</b></span>' +
      '<span class="lsc-msg" id="lsc-msg">Click any outlined text</span>' +
      '<button class="lsc-save" id="lsc-savebtn" disabled>Publish changes</button>' +
      '<button class="lsc-ghost" id="lsc-done">Done</button>' +
      '<button class="lsc-ghost" id="lsc-logout">Log out</button>';
    document.body.appendChild(bar);

    var saveBtn = bar.querySelector("#lsc-savebtn");
    var msg = bar.querySelector("#lsc-msg");
    var dirty = false;
    function markDirty() { dirty = true; saveBtn.disabled = false; msg.textContent = "Unsaved changes"; }
    function onElClick(e) {
      var el = e.currentTarget;
      if (el.tagName === "A") e.preventDefault();
      if (el.getAttribute("contenteditable") === "true") return;
      el.setAttribute("contenteditable", "true");
      el.focus();
    }
    // expose for cleanup
    enterEdit._cleanup = function () {
      els.forEach(function (el) {
        el.innerHTML = original[el.getAttribute("data-edit")]; // drop any unsaved on-screen edits
        el.removeEventListener("click", onElClick);
        el.removeEventListener("input", markDirty);
        el.removeAttribute("contenteditable");
      });
      bar.remove();
      document.body.classList.remove("lsc-editing");
      editing = false;
      mountFab();
    };

    saveBtn.onclick = function () {
      var edits = [];
      els.forEach(function (el) {
        var k = el.getAttribute("data-edit");
        var html = el.innerHTML;
        if (html !== original[k]) edits.push({ key: k, html: html });
      });
      if (!edits.length) { msg.textContent = "No changes to publish"; return; }
      saveBtn.disabled = true; msg.textContent = "Publishing…";
      fetch("/.netlify/functions/save", {
        method: "POST",
        headers: { "content-type": "application/json", Authorization: "Bearer " + getToken() },
        body: JSON.stringify({ path: currentPath(), edits: edits }),
      }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, status: r.status, j: j }; }); })
        .then(function (res) {
          if (res.ok && res.j.ok) {
            els.forEach(function (el) { original[el.getAttribute("data-edit")] = el.innerHTML; el.removeAttribute("contenteditable"); });
            dirty = false;
            msg.textContent = "✓ Published — live in about a minute";
          } else if (res.status === 401) {
            clearToken(); msg.textContent = "Session expired — log in again"; setTimeout(showLogin, 600);
          } else {
            saveBtn.disabled = false;
            msg.textContent = (res.j && res.j.error) || "Save failed — try again";
          }
        }).catch(function () { saveBtn.disabled = false; msg.textContent = "Network error — try again"; });
    };
    bar.querySelector("#lsc-done").onclick = function () {
      if (dirty && !confirm("You have unsaved changes. Leave edit mode anyway?")) return;
      enterEdit._cleanup();
    };
    bar.querySelector("#lsc-logout").onclick = function () {
      if (dirty && !confirm("You have unsaved changes. Log out anyway?")) return;
      clearToken(); enterEdit._cleanup();
      var fab = document.getElementById("lsc-fab"); if (fab) fab.remove();
    };
  }

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    injectCss();
    var params = new URLSearchParams(location.search);
    if (tokenValid(getToken())) {
      mountFab();
      if (params.has("edit")) enterEdit();
    } else if (params.has("edit") || location.hash === "#login") {
      showLogin();
    }
  });
})();
