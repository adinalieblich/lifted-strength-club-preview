/* Lifted Strength Club — inline Edit Mode (live)
   Sharon logs in (email + password), then edits in place: any text, any link's
   destination, and swaps any photo. "Publish" commits it and the site rebuilds (~1 min).
   - Login: POST /.netlify/functions/login -> JWT in localStorage.
   - Save:  POST /.netlify/functions/save  (Bearer JWT) {path, edits, links, images}.
   Public visitors never see any of this.
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
      var payload = JSON.parse(decodeURIComponent(escape(atob(p[1].replace(/-/g, "+").replace(/_/g, "/")))));
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
    '.lsc-editing [data-edit-img]{outline:2px dashed ' + TEAL + ';outline-offset:3px;cursor:pointer;position:relative}' +
    '.lsc-editing [data-edit-img]:hover{filter:brightness(.85)}' +
    '.lsc-bar{position:fixed;left:50%;transform:translateX(-50%);bottom:22px;z-index:99999;display:flex;align-items:center;gap:11px;background:' + TEAL + ';color:#fff;padding:12px 18px;border-radius:14px;box-shadow:0 10px 34px rgba(0,0,0,.34);font:14px Outfit,system-ui,sans-serif;flex-wrap:wrap;max-width:94vw}' +
    '.lsc-bar .dot{width:8px;height:8px;border-radius:50%;background:' + BRASS + ';animation:lscpulse 1.6s infinite}' +
    '@keyframes lscpulse{0%,100%{opacity:1}50%{opacity:.35}}' +
    '.lsc-bar b{font-weight:600}.lsc-bar button{font:inherit;border:0;border-radius:9px;padding:9px 15px;cursor:pointer;font-weight:600}' +
    '.lsc-save{background:' + BRASS + ';color:#1a1a1a}.lsc-save[disabled]{opacity:.45;cursor:default}' +
    '.lsc-ghost{background:transparent;color:#cfe2e0;padding:9px 8px!important}' +
    '.lsc-link{background:#214e57;color:#cfe2e0}' +
    '.lsc-msg{font-size:12.5px;color:#F7E9CF;flex:1 1 140px}' +
    '.lsc-modal{position:fixed;inset:0;z-index:100000;background:rgba(18,42,47,.55);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center}' +
    '.lsc-card{background:#fff;border-radius:16px;padding:30px;width:340px;max-width:92vw;box-shadow:0 20px 60px rgba(0,0,0,.3);font:14px Outfit,system-ui,sans-serif;color:#2c2924;position:relative}' +
    '.lsc-card h3{font:600 1.5rem "Cormorant Garamond",serif;color:' + TEAL + ';margin:0 0 4px}' +
    '.lsc-card p{margin:0 0 16px;color:#6E6A65;font-size:13px}' +
    '.lsc-card label{display:block;font-size:12px;color:#6E6A65;margin:10px 0 4px}' +
    '.lsc-card input{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid #d8d2c8;border-radius:9px;font:inherit}' +
    '.lsc-card button.go{margin-top:18px;width:100%;background:' + TEAL + ';color:#fff;border:0;border-radius:9px;padding:11px;font:600 14px Outfit,sans-serif;cursor:pointer}' +
    '.lsc-card .err{color:#A8584C;font-size:12.5px;margin-top:10px;min-height:1em}' +
    '.lsc-card .x{position:absolute;top:14px;right:16px;cursor:pointer;color:#999;font-size:20px;background:none;border:0;width:auto;padding:0}';

  function injectCss() { var s = document.createElement("style"); s.textContent = css; document.head.appendChild(s); }

  function showLogin() {
    var m = document.createElement("div");
    m.className = "lsc-modal";
    m.innerHTML =
      '<div class="lsc-card"><button class="x" aria-label="Close">&times;</button>' +
      '<h3>Edit your site</h3><p>Log in to make changes.</p>' +
      '<label>Email</label><input type="email" id="lsc-email" autocomplete="username">' +
      '<label>Password</label><input type="password" id="lsc-pass" autocomplete="current-password">' +
      '<button class="go" id="lsc-login">Log in</button><div class="err" id="lsc-err"></div></div>';
    document.body.appendChild(m);
    var close = function () { m.remove(); };
    m.querySelector(".x").onclick = close;
    m.addEventListener("click", function (e) { if (e.target === m) close(); });
    var doLogin = function () {
      var err = m.querySelector("#lsc-err"); err.textContent = "";
      fetch("/.netlify/functions/login", { method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ email: m.querySelector("#lsc-email").value, password: m.querySelector("#lsc-pass").value }) })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (res.ok && res.j.token) { setToken(res.j.token); close(); mountFab(); enterEdit(); }
          else err.textContent = (res.j && res.j.error) || "Login failed.";
        }).catch(function () { err.textContent = "Network error — try again."; });
    };
    m.querySelector("#lsc-login").onclick = doLogin;
    m.querySelector("#lsc-pass").addEventListener("keydown", function (e) { if (e.key === "Enter") doLogin(); });
    m.querySelector("#lsc-email").focus();
  }

  function mountFab() {
    if (document.getElementById("lsc-fab")) return;
    var b = document.createElement("button");
    b.id = "lsc-fab"; b.innerHTML = '<span class="dot"></span> Edit'; b.onclick = enterEdit;
    document.body.appendChild(b);
  }

  // resize an image file in the browser, return base64 (no data: prefix) + filename
  function processImage(file, cb) {
    var img = new Image();
    img.onload = function () {
      var w = img.width, h = img.height, max = 1600;
      if (Math.max(w, h) > max) { var s = max / Math.max(w, h); w = Math.round(w * s); h = Math.round(h * s); }
      var c = document.createElement("canvas"); c.width = w; c.height = h;
      c.getContext("2d").drawImage(img, 0, 0, w, h);
      var png = /\.png$/i.test(file.name);
      var url = c.toDataURL(png ? "image/png" : "image/jpeg", 0.85);
      var name = file.name.replace(/\.[^.]+$/, "") + (png ? ".png" : ".jpg");
      cb({ dataURL: url, dataBase64: url.split(",")[1], filename: name });
    };
    img.onerror = function () { cb(null); };
    img.src = URL.createObjectURL(file);
  }

  var editing = false;
  function enterEdit() {
    if (editing) return;
    editing = true;
    var fab = document.getElementById("lsc-fab"); if (fab) fab.style.display = "none";
    document.body.classList.add("lsc-editing");

    var els = Array.prototype.slice.call(document.querySelectorAll("[data-edit]"));
    var imgs = Array.prototype.slice.call(document.querySelectorAll("[data-edit-img]"));
    var original = {}, dirty = false, lastLinkEl = null;
    var pendingImages = {}, pendingLinks = {};

    var fileInput = document.createElement("input");
    fileInput.type = "file"; fileInput.accept = "image/*"; fileInput.style.display = "none";
    document.body.appendChild(fileInput);
    var activeImg = null;
    fileInput.addEventListener("change", function () {
      var f = fileInput.files && fileInput.files[0]; fileInput.value = "";
      if (!f || !activeImg) return;
      var imgEl = activeImg;
      processImage(f, function (r) {
        if (!r) { setMsg("Could not read that image"); return; }
        imgEl.src = r.dataURL;
        pendingImages[imgEl.getAttribute("data-edit-img")] = { filename: r.filename, dataBase64: r.dataBase64 };
        markDirty();
      });
    });

    var bar = document.createElement("div");
    bar.className = "lsc-bar";
    bar.innerHTML =
      '<span><span class="dot"></span> <b>Editing</b></span>' +
      '<span class="lsc-msg" id="lsc-msg">Click text to edit · click a photo to swap it</span>' +
      '<button class="lsc-link" id="lsc-linkbtn">🔗 Link</button>' +
      '<button class="lsc-save" id="lsc-savebtn" disabled>Publish changes</button>' +
      '<button class="lsc-ghost" id="lsc-done">Done</button>' +
      '<button class="lsc-ghost" id="lsc-logout">Log out</button>';
    document.body.appendChild(bar);
    var saveBtn = bar.querySelector("#lsc-savebtn"), msgEl = bar.querySelector("#lsc-msg");
    function setMsg(t) { msgEl.textContent = t; }
    function markDirty() { dirty = true; saveBtn.disabled = false; setMsg("Unsaved changes"); }

    function onTextClick(e) {
      var el = e.currentTarget;
      e.preventDefault(); e.stopPropagation();
      if (el.tagName === "A") lastLinkEl = el;
      if (el.getAttribute("contenteditable") === "true") return;
      el.setAttribute("contenteditable", "true"); el.focus();
    }
    els.forEach(function (el) {
      original[el.getAttribute("data-edit")] = el.innerHTML;
      el.addEventListener("click", onTextClick);
      el.addEventListener("input", markDirty);
      el.addEventListener("keydown", function (e) { if (e.key === "Escape") el.blur(); });
    });
    imgs.forEach(function (im) {
      im.addEventListener("click", function (e) {
        e.preventDefault(); e.stopPropagation();
        activeImg = im; fileInput.click();
      });
    });

    bar.querySelector("#lsc-linkbtn").onclick = function () {
      if (!lastLinkEl) { setMsg("Click a link or button first, then set its URL"); return; }
      var cur = lastLinkEl.getAttribute("href") || "";
      var url = window.prompt("Where should this link go? (paste a URL, or use # to do nothing)", cur);
      if (url == null) return;
      pendingLinks[lastLinkEl.getAttribute("data-edit")] = url;
      markDirty(); setMsg("Link set — Publish to apply");
    };

    function cleanup() {
      els.forEach(function (el) {
        el.innerHTML = original[el.getAttribute("data-edit")];
        el.removeEventListener("click", onTextClick);
        el.removeEventListener("input", markDirty);
        el.removeAttribute("contenteditable");
      });
      bar.remove(); fileInput.remove();
      document.body.classList.remove("lsc-editing");
      editing = false; mountFab();
    }

    saveBtn.onclick = function () {
      var edits = [];
      els.forEach(function (el) {
        var k = el.getAttribute("data-edit");
        if (el.innerHTML !== original[k]) edits.push({ key: k, html: el.innerHTML });
      });
      var links = Object.keys(pendingLinks).map(function (k) { return { key: k, href: pendingLinks[k] }; });
      var images = Object.keys(pendingImages).map(function (k) { return { key: k, filename: pendingImages[k].filename, dataBase64: pendingImages[k].dataBase64 }; });
      if (!edits.length && !links.length && !images.length) { setMsg("No changes to publish"); return; }
      saveBtn.disabled = true; setMsg("Publishing…");
      fetch("/.netlify/functions/save", {
        method: "POST", headers: { "content-type": "application/json", Authorization: "Bearer " + getToken() },
        body: JSON.stringify({ path: currentPath(), edits: edits, links: links, images: images }),
      }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, status: r.status, j: j }; }); })
        .then(function (res) {
          if (res.ok && res.j.ok) {
            els.forEach(function (el) { original[el.getAttribute("data-edit")] = el.innerHTML; el.removeAttribute("contenteditable"); });
            pendingImages = {}; pendingLinks = {}; dirty = false;
            setMsg("✓ Published — live in about a minute");
          } else if (res.status === 401) {
            clearToken(); setMsg("Session expired — log in again"); setTimeout(showLogin, 600);
          } else { saveBtn.disabled = false; setMsg((res.j && res.j.error) || "Save failed — try again"); }
        }).catch(function () { saveBtn.disabled = false; setMsg("Network error — try again"); });
    };
    bar.querySelector("#lsc-done").onclick = function () { if (dirty && !confirm("Leave edit mode? Unsaved changes will be dropped.")) return; cleanup(); };
    bar.querySelector("#lsc-logout").onclick = function () {
      if (dirty && !confirm("Log out? Unsaved changes will be dropped.")) return;
      clearToken(); cleanup(); var f = document.getElementById("lsc-fab"); if (f) f.remove();
    };
  }

  function ready(fn) { if (document.readyState !== "loading") fn(); else document.addEventListener("DOMContentLoaded", fn); }
  ready(function () {
    injectCss();
    var params = new URLSearchParams(location.search);
    if (tokenValid(getToken())) { mountFab(); if (params.has("edit")) enterEdit(); }
    else if (params.has("edit") || location.hash === "#login") showLogin();
  });
})();
