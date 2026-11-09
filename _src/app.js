/* riddleverse.com — client. Global daily reset at 00:00 UTC. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var LS = { g: function (k) { try { return JSON.parse(localStorage.getItem('rv_' + k)); } catch (e) { return null; } }, s: function (k, v) { try { localStorage.setItem('rv_' + k, JSON.stringify(v)); } catch (e) {} } };
  var GAMES = ['riddle', 'rebus', 'chain'];
  var ICON = { riddle: '🧩', rebus: '🖼️', chain: '⛓️' };
  var LABEL = { riddle: 'Riddle', rebus: 'Rebus', chain: 'Chain' };

  function utcDate(d) { d = d || new Date(); return d.toISOString().slice(0, 10); }
  function nextDrop() { var n = new Date(); return Date.UTC(n.getUTCFullYear(), n.getUTCMonth(), n.getUTCDate() + 1); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function fmt(ms) { var s = Math.round(ms / 1000); return Math.floor(s / 60) + ':' + pad(s % 60); }
  function norm(s) { return (s || '').toLowerCase().replace(/[’'"`.,!?;:()\-]/g, ' ').replace(/\s+/g, ' ').trim().replace(/^(a|an|the|it is|its|it's) /, '').replace(/^(a|an|the) /, '').trim(); }
  function sha(s) { var b = new TextEncoder().encode(s); return crypto.subtle.digest('SHA-256', b).then(function (h) { return [].map.call(new Uint8Array(h), function (x) { return ('0' + x.toString(16)).slice(-2); }).join(''); }); }
  function dels(s) { var o = [s]; for (var i = 0; i < s.length; i++) o.push(s.slice(0, i) + s.slice(i + 1)); return o; }
  function deob(s) { try { return decodeURIComponent(escape(atob(s))).split('').reverse().join(''); } catch (e) { return ''; } }
  function vid() { var v = LS.g('vid'); if (!v) { v = ''; var a = new Uint8Array(12); crypto.getRandomValues(a); a.forEach(function (x) { v += ('0' + x.toString(16)).slice(-2); }); LS.s('vid', v); } return v; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  var root = $('#app'); if (!root) return;
  var DATE = root.getAttribute('data-date') || utcDate();
  var ARCHIVE = root.getAttribute('data-archive') === '1';
  var IS_TODAY = DATE === utcDate();
  var P = null, STATE = LS.g('day_' + DATE) || {}, STATS = null;
  var NAME = LS.g('name') || '';

  function save() { LS.s('day_' + DATE, STATE); }
  function gs(g) { if (!STATE[g]) STATE[g] = { status: 'new', ms: 0, hints: 0, guesses: 0, start: 0, step: 0, done: [] }; return STATE[g]; }

  // ---------- countdown ----------
  function tick() { var el = $('#countdown'); if (!el) return; var ms = nextDrop() - Date.now(); if (ms <= 0) { el.textContent = 'New puzzles are live — refresh'; return; } var h = Math.floor(ms / 3.6e6), m = Math.floor(ms % 3.6e6 / 6e4), s = Math.floor(ms % 6e4 / 1000); el.textContent = pad(h) + ':' + pad(m) + ':' + pad(s); }
  setInterval(tick, 1000); tick();

  // ---------- load puzzle ----------
  fetch('/p/' + DATE + '.json', { cache: 'no-store' }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (p) { P = p; render(); loadStats(); }).catch(function () { root.innerHTML = '<div class="card"><h2>No puzzle for ' + esc(DATE) + '</h2><p>Puzzles drop daily at 00:00 UTC. <a href="/">Play today\'s</a>.</p></div>'; });

  function loadStats() { if (ARCHIVE && !IS_TODAY) return; fetch('/api/?stats=' + DATE, { cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (s) { STATS = s; renderStats(); }).catch(function () {}); }
  function post(g) { if (!IS_TODAY) return; var st = gs(g); fetch('/api/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ date: DATE, game: g, solved: st.status === 'solved', ms: st.ms, hints: st.hints, name: NAME, vid: vid() }) }).then(function () { loadStats(); }).catch(function () {}); }

  // ---------- render ----------
  function render() {
    var tabs = GAMES.map(function (g) { var st = gs(g); var mark = st.status === 'solved' ? ' ✓' : st.status === 'gaveup' ? ' ✕' : ''; return '<button class="tab' + (g === cur ? ' on' : '') + '" data-g="' + g + '">' + ICON[g] + ' ' + LABEL[g] + mark + '</button>'; }).join('');
    root.innerHTML = '<div class="tabs">' + tabs + '</div><div id="game"></div><div id="stats"></div>';
    $$('.tab', root).forEach(function (b) { b.onclick = function () { cur = b.getAttribute('data-g'); render(); renderStats(); }; });
    renderGame();
  }
  var cur = (location.hash || '').replace('#', '') || 'riddle'; if (GAMES.indexOf(cur) < 0) cur = 'riddle';

  function hintsHtml(g, hints, st) {
    var out = '';
    for (var i = 0; i < hints.length; i++) {
      if (i < st.hints) out += '<div class="hint on">💡 ' + esc(hints[i]) + '</div>';
      else if (i === st.hints && st.status === 'new') out += '<button class="hint btn-hint" data-g="' + g + '">💡 Reveal hint ' + (i + 1) + ' of ' + hints.length + ' <small>(costs a star)</small></button>';
    }
    return out;
  }
  function stars(st) { var n = Math.max(0, 3 - st.hints); return '⭐'.repeat(n) + '☆'.repeat(3 - n); }

  function renderGame() {
    var el = $('#game'), g = cur, st = gs(g), pz = P[g], h = '';
    var head = '<div class="phead"><span class="pill">' + ICON[g] + ' ' + LABEL[g] + ' #' + P.n + '</span><span class="pill">' + esc(DATE) + ' UTC</span>' + (pz.difficulty ? '<span class="pill">' + '🔥'.repeat(pz.difficulty) + '</span>' : '') + '</div>';
    if (g === 'chain') {
      var i = st.step, clues = pz.clues;
      h = head + '<p class="lede">Five clues. Each answer is one word. The first letters of your five answers spell the final word.</p><ol class="chain">';
      clues.forEach(function (c, k) { var done = st.done && st.done[k]; h += '<li class="' + (done ? 'done' : k === i && st.status === 'new' ? 'cur' : '') + '"><span class="cq">' + esc(c.q) + '</span>' + (done ? ' <b class="ca">' + esc(done) + '</b>' : '') + '</li>'; });
      h += '</ol>';
      if (st.status === 'new') {
        if (i < clues.length) h += form('Clue ' + (i + 1) + ' answer…');
        else h += '<p class="lede">Now the final word, spelled by your first letters: <b>' + (st.done.map(function (w) { return w[0].toUpperCase(); }).join(' ')) + '</b></p>' + form('Final word…');
      }
    } else {
      h = head + '<div class="q">' + esc(pz.q) + '</div>' + hintsHtml(g, pz.hints, st);
      if (st.status === 'new') h += form('Your answer…');
    }
    if (st.status !== 'new') h += result(g);
    el.innerHTML = h;
    var f = $('form', el); if (f) { f.onsubmit = onSubmit; var inp = $('input', f); inp.focus(); inp.oninput = function () { if (!st.start) { st.start = Date.now(); save(); } }; }
    $$('.btn-hint', el).forEach(function (b) { b.onclick = function () { st.hints++; if (!st.start) st.start = Date.now(); save(); renderGame(); }; });
    var gu = $('.giveup', el); if (gu) gu.onclick = function () { if (confirm('Reveal the answer and end today\'s ' + LABEL[g] + '?')) { st.status = 'gaveup'; st.ms = st.start ? Date.now() - st.start : 0; save(); post(g); render(); } };
    $$('[data-share]', el).forEach(function (b) { b.onclick = share; });
    var nm = $('#nameIn', el); if (nm) nm.onchange = function () { NAME = nm.value.trim().slice(0, 16); LS.s('name', NAME); GAMES.forEach(function (x) { if (gs(x).status !== 'new') post(x); }); };
    var ch = $('[data-challenge]', el); if (ch) ch.onclick = challenge;
  }
  function form(ph) { return '<form class="ans" autocomplete="off"><input type="text" placeholder="' + ph + '" aria-label="Answer" maxlength="40" autocapitalize="off" spellcheck="false"><button class="btn" type="submit">Check</button></form><div class="fb" id="fb"></div><button class="giveup">Give up & reveal</button>'; }
  function result(g) {
    var st = gs(g), pz = P[g], solved = st.status === 'solved';
    var answer = g === 'chain' ? (pz.final_plain || deob(pz.final_ob)) : deob(pz.a_ob);
    var why = deob(pz.why_ob || ''), trivia = pz.trivia_ob ? deob(pz.trivia_ob) : '';
    var h = '<div class="res ' + (solved ? 'ok' : 'no') + '"><div class="big">' + (solved ? '🎉 Solved' : '😮 The answer') + '</div><div class="answer">' + esc(answer) + '</div>' +
      (solved ? '<div class="meta">' + stars(st) + ' · ⏱ ' + fmt(st.ms) + ' · ' + st.hints + ' hint' + (st.hints === 1 ? '' : 's') + ' · ' + st.guesses + ' guess' + (st.guesses === 1 ? '' : 'es') + '</div>' : '') +
      (why ? '<p class="why"><b>Why:</b> ' + esc(why) + '</p>' : '') + (trivia ? '<p class="why"><b>Did you know?</b> ' + esc(trivia) + '</p>' : '') +
      '<div class="row"><button class="btn" data-share>Share result</button>' + (IS_TODAY ? '<button class="btn ghost" data-challenge>Challenge a friend</button>' : '') + '</div>' +
      (IS_TODAY ? '<label class="namelab">Name on today\'s leaderboard <input id="nameIn" maxlength="16" value="' + esc(NAME) + '" placeholder="optional"></label>' : '') + '</div>';
    var left = GAMES.filter(function (x) { return gs(x).status === 'new'; });
    if (left.length) h += '<p class="nextup">Next up: ' + left.map(function (x) { return '<a href="#' + x + '" data-go="' + x + '">' + ICON[x] + ' ' + LABEL[x] + '</a>'; }).join(' · ') + '</p>';
    else h += '<p class="nextup">That\'s all three. New puzzles for the whole world in <b id="countdown2"></b>. <a href="/archive/">Play the archive</a>.</p>';
    setTimeout(function () { $$('[data-go]').forEach(function (a) { a.onclick = function (e) { e.preventDefault(); cur = a.getAttribute('data-go'); render(); renderStats(); }; }); var c2 = $('#countdown2'); if (c2) setInterval(function () { c2.textContent = $('#countdown') ? $('#countdown').textContent : ''; }, 1000); }, 0);
    return h;
  }

  function onSubmit(e) {
    e.preventDefault();
    var g = cur, st = gs(g), pz = P[g], inp = $('input', e.target), raw = inp.value, v = norm(raw), fb = $('#fb');
    if (!v) return;
    if (!st.start) st.start = Date.now();
    st.guesses++; save();
    var targets, closeSet;
    if (g === 'chain') { if (st.step < pz.clues.length) { targets = pz.clues[st.step].h; closeSet = pz.clues[st.step].c || []; } else { targets = pz.final_h; closeSet = pz.final_c || []; } }
    else { targets = pz.h; closeSet = pz.c || []; }
    Promise.all(dels(v).map(sha)).then(function (hs) {
      var exact = hs[0] && targets.indexOf(hs[0]) >= 0;
      var close = !exact && hs.some(function (x) { return closeSet.indexOf(x) >= 0; });
      if (exact) {
        if (g === 'chain' && st.step < pz.clues.length) { st.done[st.step] = raw.trim().toLowerCase(); st.step++; save(); renderGame(); return; }
        st.status = 'solved'; st.ms = Date.now() - st.start; save(); post(g); confetti(); render(); renderStats(); return;
      }
      inp.value = ''; inp.focus();
      fb.textContent = close ? 'So close — check your spelling.' : ['Nope.', 'Not that.', 'Keep thinking…', 'Hmm, no.', 'Try again.'][st.guesses % 5];
      fb.className = 'fb ' + (close ? 'close' : 'no'); inp.classList.add('shake'); setTimeout(function () { inp.classList.remove('shake'); }, 400);
    });
  }

  // ---------- stats / leaderboard ----------
  function renderStats() {
    var el = $('#stats'); if (!el) return;
    if (!STATS || !STATS[cur]) { el.innerHTML = ''; return; }
    var s = STATS[cur], pct = s.played ? Math.round(100 * s.solved / s.played) : 0;
    var h = '<div class="card stats"><div class="srow"><div><b>' + s.played.toLocaleString() + '</b><small>played today</small></div><div><b>' + pct + '%</b><small>solved it</small></div><div><b>' + (s.avg_ms ? fmt(s.avg_ms) : '—') + '</b><small>average time</small></div><div><b>' + (s.hints_avg !== null ? s.hints_avg : '—') + '</b><small>hints on average</small></div></div>';
    if (s.top && s.top.length) h += '<h3>Today\'s leaderboard (fewest hints, then fastest)</h3><ol class="lb">' + s.top.map(function (t) { return '<li><span>' + esc(t.name) + '</span><span>' + '⭐'.repeat(Math.max(0, 3 - t.hints)) + ' ' + fmt(t.ms) + '</span></li>'; }).join('') + '</ol>';
    else h += '<h3>Today\'s leaderboard</h3><p class="meta">🏆 Nobody on it yet. Solve the ' + LABEL[cur] + ' and add your name to claim the top spot for the whole world.</p>';
    h += '<p class="meta">' + (STATS.players_total || 0).toLocaleString() + (STATS.players_total === 1 ? ' person has' : ' people have') + ' played Riddleverse. New puzzles for everyone in <b id="cd3"></b>.</p></div>';
    el.innerHTML = h; setInterval(function () { var c = $('#cd3'); if (c && $('#countdown')) c.textContent = $('#countdown').textContent; }, 1000);
  }

  // ---------- streak ----------
  (function streak() { var sk = LS.g('streak') || { last: null, n: 0, best: 0 }; var el = $('#streak'); if (el) el.textContent = sk.n + ' day' + (sk.n === 1 ? '' : 's'); window.__bumpStreak = function () { if (sk.last === DATE) return; var y = new Date(Date.parse(DATE) - 864e5).toISOString().slice(0, 10); sk.n = sk.last === y ? sk.n + 1 : 1; sk.best = Math.max(sk.best, sk.n); sk.last = DATE; LS.s('streak', sk); if (el) el.textContent = sk.n + ' day' + (sk.n === 1 ? '' : 's'); }; })();
  var _post = post; post = function (g) { if (gs(g).status === 'solved' && IS_TODAY) window.__bumpStreak(); _post(g); };

  // ---------- share / challenge ----------
  function shareText() {
    var lines = GAMES.map(function (g) { var st = gs(g); if (st.status === 'new') return ICON[g] + ' ' + LABEL[g] + ' ⬜ not yet'; if (st.status === 'gaveup') return ICON[g] + ' ' + LABEL[g] + ' 🟥 gave up'; return ICON[g] + ' ' + LABEL[g] + ' 🟩 ' + stars(st) + ' ⏱' + fmt(st.ms); });
    return 'Riddleverse #' + P.n + '\n' + lines.join('\n') + '\nriddleverse.com';
  }
  function share() { var t = shareText(); if (navigator.share) navigator.share({ text: t }).catch(function () {}); else { navigator.clipboard && navigator.clipboard.writeText(t); toast('Copied to clipboard'); } }
  function challenge() { var st = gs(cur); var u = location.origin + '/?c=' + encodeURIComponent([DATE, cur, st.ms, st.hints, NAME || 'A friend'].join('|')) + '#' + cur; var t = (NAME || 'I') + ' solved today\'s Riddleverse ' + LABEL[cur] + ' in ' + fmt(st.ms) + ' with ' + st.hints + ' hints. Beat it: ' + u; if (navigator.share) navigator.share({ text: t }).catch(function () {}); else { navigator.clipboard && navigator.clipboard.writeText(t); toast('Challenge link copied'); } }
  (function () { var c = new URLSearchParams(location.search).get('c'); if (!c) return; var p = c.split('|'); if (p[0] !== DATE) return; var b = document.createElement('div'); b.className = 'card chal'; b.innerHTML = '⚔️ <b>' + esc(p[4]) + '</b> solved the ' + esc(LABEL[p[1]] || p[1]) + ' in <b>' + fmt(+p[2]) + '</b> with ' + esc(p[3]) + ' hints. Beat it?'; root.parentNode.insertBefore(b, root); if (GAMES.indexOf(p[1]) >= 0) cur = p[1]; })();

  function toast(m) { var t = document.createElement('div'); t.className = 'toast'; t.textContent = m; document.body.appendChild(t); setTimeout(function () { t.remove(); }, 1800); }
  function confetti() { var c = document.createElement('canvas'); c.className = 'confetti'; document.body.appendChild(c); var x = c.getContext('2d'); c.width = innerWidth; c.height = innerHeight; var ps = []; for (var i = 0; i < 120; i++) ps.push({ x: Math.random() * c.width, y: -20 - Math.random() * 200, v: 2 + Math.random() * 4, r: 4 + Math.random() * 6, h: Math.random() * 360, a: Math.random() * 6 }); var t0 = Date.now(); (function f() { x.clearRect(0, 0, c.width, c.height); ps.forEach(function (p) { p.y += p.v; p.a += .1; x.fillStyle = 'hsl(' + p.h + ',90%,60%)'; x.save(); x.translate(p.x, p.y); x.rotate(p.a); x.fillRect(-p.r / 2, -p.r / 2, p.r, p.r * .6); x.restore(); }); if (Date.now() - t0 < 2200) requestAnimationFrame(f); else c.remove(); })(); }
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js').catch(function () {});
})();
