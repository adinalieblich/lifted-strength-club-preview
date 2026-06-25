/* Lifted Strength Club — inline Edit Mode (PROTOTYPE)
   - Applies saved text overrides to any [data-edit] element on load.
   - When the page is opened with ?edit=1, shows an editing toolbar so any
     marked text can be clicked and edited in place.
   - PROTOTYPE: "Save" stores changes in this browser (localStorage) so you can
     feel the experience. The production version will publish live + require login.
*/
(function () {
  var KEY = 'lsc_edits_v1';
  var BRASS = '#B78B52';

  function loadOverrides() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}'); }
    catch (e) { return {}; }
  }
  function saveOverrides(obj) {
    localStorage.setItem(KEY, JSON.stringify(obj));
  }

  // 1) Apply any saved edits to the live page (runs for everyone).
  function applyOverrides() {
    var ov = loadOverrides();
    document.querySelectorAll('[data-edit]').forEach(function (el) {
      var k = el.getAttribute('data-edit');
      if (ov[k] != null) el.innerHTML = ov[k];
    });
  }

  // 2) Edit UI (only with ?edit=1).
  function initEditor() {
    var els = Array.prototype.slice.call(document.querySelectorAll('[data-edit]'));
    if (!els.length) return;
    document.body.classList.add('lsc-editing');

    var style = document.createElement('style');
    style.textContent =
      '.lsc-editing [data-edit]{outline:2px dashed ' + BRASS + ';outline-offset:4px;border-radius:3px;cursor:text;transition:background .15s}' +
      '.lsc-editing [data-edit]:hover{background:rgba(183,139,82,.16)}' +
      '.lsc-editing [data-edit][contenteditable="true"]{background:rgba(183,139,82,.22);outline-style:solid}' +
      '.lsc-bar{position:fixed;left:50%;transform:translateX(-50%);bottom:22px;z-index:99999;display:flex;align-items:center;gap:14px;' +
      'background:#123E47;color:#fff;padding:12px 18px;border-radius:14px;box-shadow:0 10px 34px rgba(0,0,0,.32);font-family:Outfit,system-ui,sans-serif;font-size:14px}' +
      '.lsc-bar .dot{width:8px;height:8px;border-radius:50%;background:' + BRASS + ';display:inline-block;margin-right:8px;animation:lscpulse 1.6s infinite}' +
      '@keyframes lscpulse{0%,100%{opacity:1}50%{opacity:.35}}' +
      '.lsc-bar b{font-weight:600}' +
      '.lsc-bar button{font:inherit;border:0;border-radius:9px;padding:8px 16px;cursor:pointer;font-weight:600}' +
      '.lsc-save{background:' + BRASS + ';color:#1a1a1a}.lsc-save[disabled]{opacity:.45;cursor:default}' +
      '.lsc-discard{background:transparent;color:#cfe2e0;padding:8px 6px!important}' +
      '.lsc-note{background:#F7E9CF;color:#6b5424;font-size:12px;padding:3px 9px;border-radius:20px}';
    document.head.appendChild(style);

    var dirty = false;
    function markDirty() { dirty = true; saveBtn.disabled = false; }

    els.forEach(function (el) {
      el.addEventListener('click', function (e) {
        if (el.tagName === 'A') e.preventDefault(); // don't navigate links while editing
        if (el.getAttribute('contenteditable') === 'true') return;
        el.setAttribute('contenteditable', 'true');
        el.focus();
      });
      el.addEventListener('input', markDirty);
      el.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { el.blur(); }
      });
    });

    var bar = document.createElement('div');
    bar.className = 'lsc-bar';
    bar.innerHTML =
      '<span><span class="dot"></span><b>Edit mode</b></span>' +
      '<span class="lsc-note">preview only — won’t publish yet</span>' +
      '<button class="lsc-save" disabled>Save changes</button>' +
      '<button class="lsc-discard">Discard</button>';
    document.body.appendChild(bar);

    var saveBtn = bar.querySelector('.lsc-save');
    saveBtn.addEventListener('click', function () {
      var ov = loadOverrides();
      els.forEach(function (el) {
        ov[el.getAttribute('data-edit')] = el.innerHTML.trim();
        el.removeAttribute('contenteditable');
      });
      saveOverrides(ov);
      dirty = false; saveBtn.disabled = true;
      saveBtn.textContent = 'Saved ✓';
      setTimeout(function () { saveBtn.textContent = 'Save changes'; }, 1600);
    });
    bar.querySelector('.lsc-discard').addEventListener('click', function () {
      if (dirty && !confirm('Discard your unsaved changes?')) return;
      location.reload();
    });
    window.addEventListener('beforeunload', function (e) {
      if (dirty) { e.preventDefault(); e.returnValue = ''; }
    });
  }

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }
  ready(function () {
    applyOverrides();
    if (new URLSearchParams(location.search).get('edit') === '1') initEditor();
  });
})();
