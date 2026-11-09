#!/usr/bin/env python3
"""riddleverse.com generator. Run: cd _src && python3 build.py  → writes site to repo root (../)."""
import json, os, re, html, datetime, shutil, hashlib, base64, glob
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "data"); OUT = os.path.abspath(os.path.join(HERE, ".."))
ROOT = "https://riddleverse.com"; BRAND = "Riddleverse"
TODAY = datetime.datetime.now(datetime.timezone.utc).date()
PUZ = json.load(open(os.path.join(DATA, "puzzles.json"), encoding="utf-8"))
LIB = json.load(open(os.path.join(DATA, "library.json"), encoding="utf-8"))
CFG = json.load(open(os.path.join(DATA, "config.json"), encoding="utf-8")) if os.path.exists(os.path.join(DATA, "config.json")) else {}

def esc(s): return html.escape(str(s), quote=True)
def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:70]
def norm(s):
    s = re.sub(r"[’'\"`.,!?;:()\-]", " ", s.lower()); s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^(a|an|the|it is|its|it's) ", "", s); s = re.sub(r"^(a|an|the) ", "", s); return s.strip()
def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def hashes(answers): return sorted({sha(norm(a)) for a in answers})
def close(answers):
    out = set()
    for a in answers:
        n = norm(a); out.add(sha(n))
        for i in range(len(n)): out.add(sha(n[:i] + n[i + 1:]))
    return sorted(out)
def ob(s): return base64.b64encode(s[::-1].encode("utf-8")).decode("ascii")
def write(path, content):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f: f.write(content)
def fmt_date(iso): return datetime.date.fromisoformat(iso).strftime("%A, %B %-d, %Y")

CSS = r"""
:root{--bg:#14122b;--bg2:#1d1a3a;--bg3:#272352;--ink:#f6f3ff;--ink2:#c9c3e6;--mute:#8d86b8;--line:#332e5e;--acc:#ffb703;--acc2:#2ec4b6;--bad:#ff5d73;--max:720px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:radial-gradient(1200px 600px at 50% -200px,#2a2560,var(--bg));color:var(--ink);font:17px/1.55 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;min-height:100vh}
a{color:var(--acc2);text-decoration:none}a:hover{text-decoration:underline}
h1,h2,h3,.disp{font-family:Fraunces,Georgia,serif;font-weight:700;letter-spacing:-.01em;line-height:1.1}
h1{font-size:clamp(30px,6vw,48px);margin:.2em 0 .3em}h2{font-size:clamp(22px,4vw,30px);margin:1.2em 0 .4em}
.wrap{max-width:var(--max);margin:0 auto;padding:0 18px}
header{padding:14px 0 6px}header .wrap{display:flex;align-items:center;justify-content:space-between;gap:10px}
.logo{font-family:Fraunces,Georgia,serif;font-weight:800;font-size:26px;color:var(--ink);letter-spacing:-.02em}.logo b{color:var(--acc)}
nav{white-space:nowrap}nav a{color:var(--ink2);font-size:14px;margin-left:12px;font-weight:500}
.topbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;justify-content:space-between;margin:6px 0 16px;font-size:14px;color:var(--ink2)}.topbar b{color:var(--acc)}
.chip{background:var(--bg2);border:1px solid var(--line);border-radius:999px;padding:5px 11px}button.namechip{color:var(--acc);cursor:pointer;font:inherit;font-size:14px}
.nameform{display:flex;gap:8px;margin:-6px 0 14px}.nameform input{flex:1;padding:11px 14px;font-size:16px;border-radius:12px;border:2px solid var(--line);background:#0f0d22;color:var(--ink)}
.tabs{display:flex;gap:6px;margin:0 0 14px}.tab{flex:1;background:var(--bg2);border:1px solid var(--line);color:var(--ink2);padding:12px 8px;border-radius:12px;font-size:15px;font-weight:600;cursor:pointer}.tab.on{background:var(--acc);color:#1a1400;border-color:var(--acc)}
.card{background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:20px}
#game{background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:22px 20px}
.phead{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}.pill{font-size:12px;color:var(--mute);border:1px solid var(--line);border-radius:999px;padding:3px 9px}
.q{font-family:Fraunces,Georgia,serif;font-size:clamp(24px,5vw,34px);line-height:1.25;font-weight:600;margin:4px 0 18px}
.lede{color:var(--ink2);font-size:17px}
.hint{display:block;width:100%;text-align:left;background:var(--bg3);border:1px dashed var(--line);color:var(--ink2);padding:11px 13px;border-radius:12px;margin:8px 0;font-size:15px}button.hint{cursor:pointer;color:var(--acc)}button.hint:hover{border-style:solid}.hint.on{border-style:solid;color:var(--ink)}.hint small{color:var(--mute)}
form.ans{display:flex;gap:8px;margin:16px 0 6px}form.ans input{flex:1;padding:14px 16px;font-size:18px;border-radius:12px;border:2px solid var(--line);background:#0f0d22;color:var(--ink);outline:none}form.ans input:focus{border-color:var(--acc2)}
.btn{background:var(--acc);color:#1a1400;border:0;border-radius:12px;padding:14px 18px;font-size:16px;font-weight:700;cursor:pointer}.btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--line)}
.giveup{background:none;border:0;color:var(--mute);font-size:13px;cursor:pointer;padding:6px 0;text-decoration:underline}
.fb{min-height:22px;font-size:15px;color:var(--mute)}.fb.close{color:var(--acc)}.fb.no{color:var(--bad)}
.shake{animation:sh .35s}@keyframes sh{20%{transform:translateX(-6px)}60%{transform:translateX(6px)}}
.res{border-radius:14px;padding:18px;margin-top:10px;border:1px solid var(--line);background:var(--bg3)}.res.ok{border-color:var(--acc2)}.res .big{font-size:14px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}.res .answer{font-family:Fraunces,Georgia,serif;font-size:34px;font-weight:700;margin:4px 0 6px;color:var(--acc)}.res .meta{color:var(--ink2);font-size:15px}.res .why{color:var(--ink2);font-size:15px;margin:10px 0 0}.res .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.namelab{display:block;margin-top:12px;font-size:13px;color:var(--mute)}.namelab input{margin-left:8px;padding:7px 10px;border-radius:8px;border:1px solid var(--line);background:#0f0d22;color:var(--ink);width:140px}
.nextup{margin:16px 0 0;color:var(--ink2)}
.chain{padding-left:22px;margin:0 0 10px}.chain li{padding:8px 0;color:var(--mute);border-bottom:1px solid var(--line)}.chain li.cur{color:var(--ink);font-weight:600}.chain li.done{color:var(--ink2)}.chain .ca{color:var(--acc2);margin-left:8px}
.stats{margin-top:16px}.srow{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.srow div{text-align:center}.srow b{display:block;font-size:22px;font-family:Fraunces,Georgia,serif}.srow small{color:var(--mute);font-size:12px}
@media(max-width:480px){.srow{grid-template-columns:repeat(2,1fr)}}
.lb{list-style:none;padding:0;margin:0}.lb li{display:flex;justify-content:space-between;padding:7px 0;border-top:1px solid var(--line);font-size:15px}.lb li:nth-child(1) span:first-child:before{content:"🥇 "}.lb li:nth-child(2) span:first-child:before{content:"🥈 "}.lb li:nth-child(3) span:first-child:before{content:"🥉 "}
.meta{color:var(--mute);font-size:13px}
.chal{border-color:var(--acc);margin-bottom:12px}
.toast{position:fixed;left:50%;bottom:30px;transform:translateX(-50%);background:var(--acc);color:#1a1400;padding:10px 16px;border-radius:10px;font-weight:600;z-index:9}
.confetti{position:fixed;inset:0;pointer-events:none;z-index:8}
footer{margin:40px 0 50px;color:var(--mute);font-size:13px}footer a{color:var(--ink2);margin-right:14px}
.list a{display:block;padding:12px 0;border-bottom:1px solid var(--line);color:var(--ink)}.list a:hover{color:var(--acc);text-decoration:none}.list small{display:block;color:var(--mute)}
details{border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:10px 0;background:var(--bg2)}summary{cursor:pointer;font-weight:600;color:var(--acc)}
.rq{font-family:Fraunces,Georgia,serif;font-size:21px;line-height:1.3;margin:0 0 6px}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}.tile{background:var(--bg2);border:1px solid var(--line);border-radius:14px;padding:16px;color:var(--ink)}.tile:hover{border-color:var(--acc);text-decoration:none}.tile h3{margin:0 0 4px;font-size:19px}.tile p{margin:0;color:var(--mute);font-size:14px}
.article{max-width:620px}.article p,.article li{color:var(--ink2);font-size:17px}
"""

SW = "const C='rv-v1';self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(['/','/assets/app.js','/assets/site.css'])).then(()=>self.skipWaiting()))});self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||!r.url.startsWith(self.location.origin)||r.url.indexOf('/api/')>=0||r.url.indexOf('/p/')>=0)return;e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(C).then(c=>c.put(r,cp));return res}).catch(()=>caches.match(r)))});"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
V = hashlib.md5((CSS + open(os.path.join(HERE, "app.js")).read()).encode()).hexdigest()[:8]

def layout(title, desc, path, body, jsonld=None, noindex=False, og_type="website"):
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": ROOT + "/"}] + (jsonld if isinstance(jsonld, list) else [jsonld] if jsonld else [])
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{ROOT}{path}">
<meta name="robots" content="{'noindex' if noindex else 'index,follow,max-image-preview:large'}"><meta name="theme-color" content="#14122b">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{ROOT}{path}"><meta property="og:image" content="{ROOT}/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/icon-192.png"><link rel="manifest" href="/manifest.webmanifest">{FONTS}
<link rel="stylesheet" href="/assets/site.css?v={V}">{"".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)}{CFG.get("analytics_html", "")}</head>
<body><header><div class="wrap"><a class="logo" href="/">Riddle<b>verse</b></a><nav><a href="/archive/">Archive</a><a href="/riddles/">Riddles</a><a href="/how-to-play/">Help</a></nav></div></header>
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap"><a href="/">Today</a><a href="/archive/">Archive</a><a href="/riddles/">Riddle collections</a><a href="/how-to-play/">How to play</a><a href="/about/">About</a><a href="/privacy/">Privacy</a><a href="/feed.xml">RSS</a><div style="margin-top:10px">One world, one puzzle. New riddles for everyone at 00:00 UTC. &copy; {TODAY.year} riddleverse.com</div></div></footer>
<script src="/assets/app.js?v={V}" defer></script></body></html>"""

def play_body(date=None, archive=False):
    attrs = (f' data-date="{date}"' if date else "") + (' data-archive="1"' if archive else "")
    top = '<div class="topbar"><span class="chip">🌍 Same puzzles for the whole world · new drop in <b id="countdown">—</b></span><span class="chip">🔥 Streak: <b id="streak">0 days</b></span><button class="chip namechip" id="nameChip" type="button">👤 Set your name</button></div><form id="nameForm" class="nameform" style="display:none"><input id="nameTop" maxlength="16" placeholder="Name for the leaderboard (optional)" aria-label="Your name"><button class="btn" type="submit">Save</button></form>'
    return top + f'<div id="app"{attrs}><div class="card">Loading today\'s puzzles…</div></div>'

def puzzle_json(d):
    p = PUZ[d]; r, b, c = p["riddle"], p["rebus"], p["chain"]
    return {"n": p["n"], "date": d,
            "riddle": {"q": r["q"], "hints": r["hints"], "difficulty": r["difficulty"], "h": hashes(r["a"]), "c": close(r["a"]), "a_ob": ob(r.get("display", r["a"][0])), "why_ob": ob(r["why"]), "trivia_ob": ob(r["trivia"])},
            "rebus": {"q": b["q"], "hints": b["hints"], "difficulty": b["difficulty"], "h": hashes(b["a"]), "c": close(b["a"]), "a_ob": ob(b.get("display", b["a"][0])), "why_ob": ob(b["why"])},
            "chain": {"clues": [{"q": x["q"], "h": hashes(x["a"]), "c": close(x["a"])} for x in c["clues"]], "final_h": hashes(c["final"]), "final_c": close(c["final"]), "final_ob": ob(c["final"][0]), "why_ob": ob(c["why"])}}

def riddle_page(d):
    p = PUZ[d]; r = p["riddle"]; slug = f"{slugify(r['q'])}"; path = f"/riddle/{slug}/"
    body = (f'<p class="meta">Daily riddle #{p["n"]} · {fmt_date(d)}</p><h1 class="rq" style="font-size:clamp(24px,5vw,36px)">{esc(r["q"])}</h1>'
            f'<details><summary>Show the answer</summary><p><b>{esc(r.get("display", r["a"][0]).capitalize())}.</b> {esc(r["why"])}</p><p class="meta">{esc(r["trivia"])}</p></details>'
            f'<p><a class="btn" href="/play/{d}/">Play this day\'s three puzzles</a></p><h2>More riddles</h2><p><a href="/riddles/{r["category"]}/">{esc(r["category"].title())} riddles</a> · <a href="/">Today\'s riddle</a> · <a href="/archive/">Archive</a></p>')
    ld = {"@context": "https://schema.org", "@type": "Question", "name": r["q"], "text": r["q"], "dateCreated": d, "answerCount": 1, "acceptedAnswer": {"@type": "Answer", "text": r["a"][0], "dateCreated": d}}
    return path, layout(f'Riddle: {r["q"][:70]} — answer | Riddleverse', f'Riddle: {r["q"]} Answer and explanation, plus the daily riddle game.', path, body, ld)

def collection(cat, title, desc, items):
    path = f"/riddles/{cat}/"
    body = f'<h1>{esc(title)}</h1><p class="lede">{esc(desc)} Tap to reveal each answer.</p>' + "".join(f'<details><summary class="rq">{esc(q)}</summary><p><b>{esc(a[0].title())}.</b></p></details>' for q, a in items) + '<p style="margin-top:18px"><a class="btn" href="/">Play today\'s riddle</a></p>'
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a[0]}} for q, a in items]}
    return path, layout(f"{title} with answers ({len(items)}) | Riddleverse", desc[:155], path, body, ld)

HOW = """
## Three puzzles, one world
Every day at 00:00 UTC, three new puzzles go live for everyone on Earth at the same moment. Same puzzles, same clock, one global leaderboard.

- **Riddle.** A classic or original riddle. Type your answer; spelling is forgiving and we accept sensible variants. Three hints are available; each one you use costs a star.
- **Rebus.** A picture puzzle in emoji. Say the pictures out loud and the phrase appears.
- **Chain.** Five short clues. The first letters of your five answers spell a final word.

## Scoring
Three stars for a solve with no hints, two with one hint, one with two. The leaderboard ranks by fewest hints, then fastest time. Your streak counts consecutive days with at least one solve.

## Sharing
After each puzzle, **Share** copies a spoiler-free result card. **Challenge a friend** sends a link with your time, so they play the same puzzle against your clock.

## Fair play
Answers are stored as one-way hashes, so the page source can't spoil you. Names on the leaderboard are optional and anything goes within 16 characters; be nice.
"""
ABOUT = """
Riddleverse is a daily puzzle ritual: three small, satisfying puzzles that the whole world plays together, with a shared leaderboard and a new drop every day at 00:00 UTC.

It is free, has no account, and asks for nothing except your best guess. Classic riddles are drawn from the public domain; originals are written and tested in-house. Every past day stays playable in the archive.

Questions or a riddle you think we should run: hello@riddleverse.com.
"""
PRIV = """
Riddleverse stores your progress, streak and chosen name in your own browser (localStorage). When you finish a puzzle, your result (solved or not, time, hints, optional name, and a random anonymous id) is sent to our server to compute the day's statistics and leaderboard. No email, no account, no advertising trackers, no cookies. Analytics, if present, are cookie-free page counts.
"""
def md(text):
    out = []
    for blk in text.strip().split("\n\n"):
        if blk.startswith("## "): out.append(f"<h2>{esc(blk[3:])}</h2>")
        elif blk.startswith("- "): out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in blk.split("\n")) + "</ul>")
        else: out.append(f"<p>{inline(blk)}</p>")
    return "".join(out)
def inline(s): return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(s))

HTACCESS = r"""RewriteEngine On
# canonical host only (https is enforced by Hostinger's Force HTTPS once SSL is active); never touch preview hosts
RewriteCond %{HTTP_HOST} !hostingersite[.]com$ [NC]
RewriteCond %{HTTP_HOST} !^(localhost|127[.]0[.]0[.]1)
RewriteCond %{HTTP_HOST} !^riddleverse[.]com$ [NC]
RewriteRule ^ http://riddleverse.com%{REQUEST_URI} [R=301,L]
RedirectMatch 404 ^/_src(/|$)
RedirectMatch 404 ^/[.]git
RedirectMatch 404 ^/README[.]md$
RedirectMatch 404 ^/api/data(/|$)
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8
AddType application/manifest+json .webmanifest
<IfModule mod_headers.c>
Header set X-Content-Type-Options "nosniff"
Header set Referrer-Policy "strict-origin-when-cross-origin"
<FilesMatch "\.(html)$">
Header set Cache-Control "public, max-age=300"
</FilesMatch>
<FilesMatch "\.(json)$">
Header set Cache-Control "no-cache"
</FilesMatch>
<FilesMatch "\.(css|js|png|svg|webmanifest)$">
Header set Cache-Control "public, max-age=86400"
</FilesMatch>
<FilesMatch "sw\.js$">
Header set Cache-Control "no-cache"
</FilesMatch>
</IfModule>
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml
</IfModule>
"""
FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#14122b"/><text x="32" y="46" text-anchor="middle" font-family="Georgia,serif" font-weight="800" font-size="40" fill="#ffb703">?</text></svg>'

def og_image():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError: return
    W, H = 1200, 630; img = Image.new("RGB", (W, H), (20, 18, 43)); d = ImageDraw.Draw(img)
    def f(p, s):
        try: return ImageFont.truetype(p, s)
        except Exception: return ImageFont.load_default()
    serif = f("/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf", 110); sans = f("/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf", 30)
    d.text((80, 150), "Riddle", font=serif, fill=(246, 243, 255)); w = d.textlength("Riddle", font=serif); d.text((80 + w, 150), "verse", font=serif, fill=(255, 183, 3))
    d.text((82, 310), "Three daily puzzles. One world. One clock.", font=sans, fill=(201, 195, 230))
    d.text((82, 360), "Riddle · Rebus · Chain   ·   new drop at 00:00 UTC", font=f("/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf", 24), fill=(141, 134, 184))
    d.rectangle([80, 520, 1120, 524], fill=(46, 196, 182)); d.text((82, 545), "riddleverse.com", font=sans, fill=(246, 243, 255))
    img.save(os.path.join(OUT, "og.png"), optimize=True)
    for s in (192, 512):
        ic = Image.new("RGB", (s, s), (20, 18, 43)); dd = ImageDraw.Draw(ic); dd.text((s / 2, s * .55), "?", font=f("/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf", int(s * .7)), fill=(255, 183, 3), anchor="mm"); ic.save(os.path.join(OUT, f"icon-{s}.png"))

def main():
    for name in os.listdir(OUT):
        if name in ("_src", ".git", "README.md", ".gitignore"): continue
        p = os.path.join(OUT, name); shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    pages = {}
    dates = sorted(PUZ)
    horizon = (TODAY + datetime.timedelta(days=2)).isoformat()
    for d in dates:
        if d <= horizon: write(f"p/{d}.json", json.dumps(puzzle_json(d), ensure_ascii=False))
    past = [d for d in dates if d < TODAY.isoformat()]
    # home
    body = play_body() + '<section style="margin-top:28px"><h2>How Riddleverse works</h2><p class="lede">Three small puzzles a day, the same for everyone on Earth, with a shared leaderboard. No account, no ads, just your best guess. <a href="/how-to-play/">How to play →</a></p></section>'
    pages["/"] = layout("Riddleverse — three daily puzzles the whole world plays together", "A daily riddle, rebus and chain puzzle, the same for everyone on Earth, with a global leaderboard. New drop at 00:00 UTC. Free, no account.", "/", body, {"@context": "https://schema.org", "@type": "WebApplication", "name": BRAND, "url": ROOT + "/", "applicationCategory": "GameApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}})
    # archive play pages + riddle pages
    for d in past:
        p = PUZ[d]; r = p["riddle"]
        body = f'<p class="meta"><a href="/archive/">Archive</a> · Day #{p["n"]} · {fmt_date(d)}</p>' + play_body(d, archive=True)
        pages[f"/play/{d}/"] = layout(f"Riddleverse #{p['n']} — {fmt_date(d)}", f"Play the three puzzles from {fmt_date(d)}: riddle, rebus and chain.", f"/play/{d}/", body)
        path, h = riddle_page(d); pages[path] = h
    arch = "".join(f'<a href="/play/{d}/"><strong>#{PUZ[d]["n"]} · {fmt_date(d)}</strong><small>{esc(PUZ[d]["riddle"]["q"][:90])}</small></a>' for d in reversed(past)) or "<p>The archive fills up from tomorrow. Today's puzzles are on the <a href='/'>home page</a>.</p>"
    pages["/archive/"] = layout("Archive — every past Riddleverse day | Riddleverse", "Play every past day's riddle, rebus and chain puzzle.", "/archive/", f'<h1>Archive</h1><p class="lede">Every past day stays playable. Archive results don\'t count toward the global leaderboard.</p><div class="list">{arch}</div>')
    # collections
    pool = [(x["q"], x["a"], x["category"], x["difficulty"]) for x in LIB] + [(PUZ[d]["riddle"]["q"], PUZ[d]["riddle"]["a"], PUZ[d]["riddle"]["category"], PUZ[d]["riddle"]["difficulty"]) for d in past]
    cols = [("kids", "Riddles for kids", "Easy, fun riddles with answers for children and families.", [(q, a) for q, a, c, dd in pool if c == "kids" or dd == 1]),
            ("hard", "Hard riddles", "The toughest riddles with answers: the ones that make clever people groan.", [(q, a) for q, a, c, dd in pool if dd >= 4]),
            ("math", "Math riddles", "Number and logic riddles with answers.", [(q, a) for q, a, c, dd in pool if c == "math"]),
            ("logic", "Logic riddles", "Lateral-thinking and logic puzzles with answers.", [(q, a) for q, a, c, dd in pool if c == "logic"]),
            ("wordplay", "Wordplay riddles", "Riddles that hinge on letters, spelling and double meanings.", [(q, a) for q, a, c, dd in pool if c == "wordplay"]),
            ("what-am-i", "What am I? riddles", "Classic 'what am I' riddles with answers.", [(q, a) for q, a, c, dd in pool if "what am i" in q.lower()]),
            ("classic", "Classic riddles", "The all-time classic riddles with answers.", [(q, a) for q, a, c, dd in pool if c == "classic"])]
    tiles = ""
    for cat, title, desc, items in cols:
        if not items: continue
        path, h = collection(cat, title, desc, items); pages[path] = h
        tiles += f'<a class="tile" href="{path}"><h3>{esc(title)}</h3><p>{len(items)} riddles with answers</p></a>'
    pages["/riddles/"] = layout("Riddle collections with answers | Riddleverse", "Riddles for kids, hard riddles, math, logic, wordplay and what-am-I riddles, all with answers.", "/riddles/", f'<h1>Riddle collections</h1><p class="lede">Hundreds of riddles with answers, sorted by kind. Or play <a href="/">today\'s</a>.</p><div class="grid">{tiles}</div>')
    pages["/how-to-play/"] = layout("How to play Riddleverse", "How the daily riddle, rebus and chain puzzles work, how scoring and streaks work, and how to challenge a friend.", "/how-to-play/", f'<h1>How to play</h1><div class="article">{md(HOW)}</div><p><a class="btn" href="/">Play today</a></p>')
    pages["/about/"] = layout("About Riddleverse", "What Riddleverse is and who makes it.", "/about/", f'<h1>About</h1><div class="article">{md(ABOUT)}</div>')
    pages["/privacy/"] = layout("Privacy | Riddleverse", "What Riddleverse stores and why.", "/privacy/", f'<h1>Privacy</h1><div class="article">{md(PRIV)}</div>')
    for path, h in pages.items(): write(path.lstrip("/") + "index.html", h)
    write("404.html", layout("Not found | Riddleverse", "That page is a riddle we can't solve.", "/404.html", '<h1>Not found</h1><p class="lede">That page doesn\'t exist. <a href="/">Play today\'s puzzles</a> or browse the <a href="/archive/">archive</a>.</p>', noindex=True))
    write("assets/site.css", CSS); shutil.copy(os.path.join(HERE, "app.js"), os.path.join(OUT, "assets", "app.js")); write("sw.js", SW)
    write("manifest.webmanifest", json.dumps({"name": "Riddleverse", "short_name": "Riddleverse", "start_url": "/", "display": "standalone", "background_color": "#14122b", "theme_color": "#14122b", "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}))
    os.makedirs(os.path.join(OUT, "api"), exist_ok=True); shutil.copy(os.path.join(HERE, "api.php"), os.path.join(OUT, "api", "index.php"))
    write("api/.htaccess", "DirectoryIndex index.php\n<FilesMatch \"\\.(sqlite|db)$\">\nRequire all denied\n</FilesMatch>\n")
    # feed of past riddles (spoiler-free)
    items = "".join(f'<item><title>Riddleverse #{PUZ[d]["n"]}: {esc(PUZ[d]["riddle"]["q"])}</title><link>{ROOT}/play/{d}/</link><guid isPermaLink="true">{ROOT}/play/{d}/</guid><pubDate>{datetime.datetime.fromisoformat(d + "T00:00:00+00:00").strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate><description>{esc(PUZ[d]["riddle"]["q"])} Play all three puzzles.</description></item>' for d in reversed(past[-20:]))
    write("feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Riddleverse</title><link>{ROOT}/</link><description>Three daily puzzles for the whole world.</description><atom:link href="{ROOT}/feed.xml" rel="self" type="application/rss+xml"/>{items}</channel></rss>')
    urls = "".join(f"<url><loc>{ROOT}{p}</loc><lastmod>{TODAY.isoformat()}</lastmod><priority>{'1.0' if p == '/' else '0.8' if p.startswith('/riddles/') else '0.6'}</priority></url>" for p in pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /p/\nSitemap: {ROOT}/sitemap.xml\n")
    write(".htaccess", HTACCESS); write("favicon.svg", FAVICON); og_image()
    print(f"built {len(pages)} pages, puzzles through {horizon}")

if __name__ == "__main__": main()
