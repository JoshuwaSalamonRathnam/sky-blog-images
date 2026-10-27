"""Sky Designers featured image (v2, five layouts). Usage: python3 build_post.py spec.json out.png
spec: {"layout","kind","date","title_html","sub","panel_title","rows":[{"label","value","style"}],"note"}
layout: panel (default, title left + panel right) | stat (one big number) | grid (2x2 cards) | split (blue title block + list) | center (centered title + chips)
style: live (green pill) | one (amber pill) | test (grey pill) | num (blue number, no pill)
Title: plain text with the key phrase wrapped in <em>…</em> (shown in blue). 2–4 rows (stat: the first row is the big number)."""
import sys, json, html, asyncio
from playwright.async_api import async_playwright

LAYOUTS = ("panel", "stat", "grid", "split", "center")

CSS = """
:root{--bg:#030713;--card:#0D1424;--card2:#111A2E;--border:#1E2A42;--text:#F2F4F7;--second:#C6CDD8;--muted:#8E98A8;--accent:#5B9BFF;--accent2:#2F6FE0;--green:#3DD68C;--amber:#FFB020;--grey:#8E98A8;--glow:rgba(91,155,255,.22)}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1200px;height:675px;background:var(--bg);font-family:Archivo,Inter,sans-serif;color:var(--text);overflow:hidden;position:relative}
.glow{position:absolute;right:-180px;top:-220px;width:720px;height:720px;border-radius:50%;background:radial-gradient(circle,var(--glow),transparent 65%)}
.glow.l{right:auto;left:-260px;top:auto;bottom:-320px}
.grid-bg{position:absolute;inset:0;background-image:linear-gradient(var(--border) 1px,transparent 1px),linear-gradient(90deg,var(--border) 1px,transparent 1px);background-size:60px 60px;opacity:.35;-webkit-mask-image:radial-gradient(ellipse at 70% 30%,#000 10%,transparent 70%)}
.wrap{position:relative;height:100%;padding:56px 60px 44px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center}
.tag{display:flex;align-items:center;gap:12px;font-size:15px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--second)}
.sq{width:11px;height:11px;background:var(--accent)}
.date{font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
h1{line-height:1.02;font-weight:800;letter-spacing:-.035em}
h1 em{font-style:normal;color:var(--accent)}
.sub{margin-top:22px;font-size:24px;line-height:1.3;color:var(--second);font-weight:500;max-width:560px}
.ph{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:14px}
.f{font-size:18px;font-weight:600;line-height:1.2}
.pill{flex:none;font-size:12.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:6px 10px;border-radius:999px;border:1.5px solid currentColor}
.live{color:var(--green)}.one{color:var(--amber)}.test{color:var(--grey)}
.num{flex:none;font-size:24px;font-weight:800;letter-spacing:-.03em;color:var(--accent);font-variant-numeric:tabular-nums}
.note{margin-top:12px;font-size:12.5px;color:var(--muted)}
.foot{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--border);padding-top:16px}
.brand{font-weight:700;font-size:18px;letter-spacing:.01em}
.dom{font-size:15px;color:var(--muted);letter-spacing:.02em}
/* panel */
.main{flex:1;display:flex;gap:44px;align-items:center}
.left{flex:1}
.panel{width:430px;background:var(--card);border:1px solid var(--border);border-radius:18px;padding:26px 26px 22px}
.row{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:13px 0;border-top:1px solid var(--border)}
.row:first-of-type{border-top:none}
/* stat */
.stat{flex:1;display:flex;flex-direction:column;justify-content:center}
.statrow{display:flex;align-items:flex-end;gap:48px;margin-top:30px}
.big{font-size:132px;font-weight:800;letter-spacing:-.05em;line-height:.9;color:var(--accent);font-variant-numeric:tabular-nums}
.big.live{color:var(--green)}.big.one{color:var(--amber)}.big.test{color:var(--grey)}
.biglabel{font-size:20px;font-weight:600;color:var(--second);margin-top:12px;max-width:560px}
.minis{display:flex;flex-direction:column;gap:10px;padding-left:36px;border-left:2px solid var(--border);margin-bottom:8px}
.mini{display:flex;align-items:baseline;gap:14px}
.mini .num{font-size:28px}
.mini .f{font-size:17px;color:var(--second)}
/* grid */
.gmain{flex:1;display:flex;flex-direction:column;justify-content:center;gap:30px}
.cards{display:grid;gap:16px}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:20px 22px;display:flex;flex-direction:column;gap:10px;min-height:118px}
.card .idx{font-size:13px;font-weight:700;letter-spacing:.14em;color:var(--accent)}
.card .f{font-size:17px;color:var(--second)}
.card .num{font-size:30px}
/* split */
body.split .wrap{padding:0}
.sp{display:flex;height:100%}
.spl{width:560px;background:linear-gradient(160deg,var(--accent2),#173A86 60%,#0E2557);padding:56px 52px 44px;display:flex;flex-direction:column;position:relative;overflow:hidden}
.spl .tag{color:#E6EEFF}.spl .sq{background:#fff}
.spl h1{color:#fff;margin-top:auto}
.spl h1 em{color:#BFD6FF}
.spl .sub{color:#DCE7FF;max-width:460px}
.spl .brand{margin-top:34px;color:#fff;border-top:1px solid rgba(255,255,255,.25);padding-top:16px}
.spl .ring{position:absolute;right:-120px;top:-120px;width:320px;height:320px;border-radius:50%;border:2px solid rgba(255,255,255,.18)}
.spr{flex:1;padding:56px 56px 44px 48px;display:flex;flex-direction:column}
.spr .date{text-align:right}
.items{flex:1;display:flex;flex-direction:column;justify-content:center}
.item{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:18px 0;border-top:1px solid var(--border)}
.item:first-child{border-top:none}
.item .f{font-size:19px}
.item .num{font-size:28px}
.spr .dom{text-align:right;border-top:1px solid var(--border);padding-top:16px}
/* center */
.cmain{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.cmain .sub{margin-left:auto;margin-right:auto;max-width:760px}
.chips{display:flex;gap:14px;margin-top:34px;flex-wrap:wrap;justify-content:center}
.chip{display:flex;align-items:center;gap:12px;background:var(--card);border:1px solid var(--border);border-radius:999px;padding:12px 20px}
.chip .f{font-size:16px;color:var(--second)}
.chip .num{font-size:20px}
.cmain .note{margin-top:18px}
"""

def esc(x):
    return html.escape(x)

def title_of(s, sizes=(62, 54, 46), cuts=(50, 70)):
    plain = s["title_html"].replace("<em>", "").replace("</em>", "")
    n = len(plain)
    size = sizes[0] if n <= cuts[0] else sizes[1] if n <= cuts[1] else sizes[2]
    t = esc(s["title_html"]).replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")
    return t, size

def value(r, cls=""):
    if r["style"] == "num":
        return f'<span class="num {cls}">{esc(r["value"])}</span>'
    return f'<span class="pill {r["style"]}">{esc(r["value"])}</span>'

def top(s):
    return f'<div class="top"><div class="tag"><span class="sq"></span>{esc(s["kind"])}</div><div class="date">{esc(s["date"])}</div></div>'

FOOT = '<div class="foot"><div class="brand">Sky Designers</div><div class="dom">skydesigners.lk/blog</div></div>'

def note(s):
    return f'<div class="note">{esc(s["note"])}</div>' if s.get("note") else ""

def b_panel(s):
    t, size = title_of(s)
    rows = "".join(f'<div class="row"><span class="f">{esc(r["label"])}</span>{value(r)}</div>' for r in s["rows"])
    body = (f'<div class="main"><div class="left"><h1 style="font-size:{size}px">{t}</h1><p class="sub">{esc(s["sub"])}</p></div>'
            f'<div class="panel"><div class="ph">{esc(s["panel_title"])}</div>{rows}{note(s)}</div></div>')
    return "", '<div class="glow"></div>', f'<div class="wrap">{top(s)}{body}{FOOT}</div>'

def b_stat(s):
    t, size = title_of(s, (56, 50, 44), (45, 65))
    r0, rest = s["rows"][0], s["rows"][1:]
    big_cls = "" if r0["style"] == "num" else r0["style"]
    minis = "".join(f'<div class="mini">{value(r)}<span class="f">{esc(r["label"])}</span></div>' for r in rest)
    body = (f'<div class="stat"><h1 style="font-size:{size}px;max-width:1000px">{t}</h1>'
            f'<div class="statrow"><div><div class="big {big_cls}">{esc(r0["value"])}</div><div class="biglabel">{esc(r0["label"])}</div></div>'
            f'{f"<div class=minis>{minis}</div>" if rest else ""}</div>{note(s)}</div>')
    return "", '<div class="grid-bg"></div><div class="glow"></div>', f'<div class="wrap">{top(s)}{body}{FOOT}</div>'

def b_grid(s):
    t, size = title_of(s, (54, 48, 42), (50, 70))
    n = len(s["rows"])
    cols = 4 if n == 4 else n
    cards = "".join(
        f'<div class="card"><span class="idx">{i:02d}</span>{value(r)}<span class="f">{esc(r["label"])}</span></div>'
        for i, r in enumerate(s["rows"], 1))
    body = (f'<div class="gmain"><div><h1 style="font-size:{size}px;max-width:1000px">{t}</h1><p class="sub" style="max-width:900px;margin-top:16px;font-size:22px">{esc(s["sub"])}</p></div>'
            f'<div class="cards" style="grid-template-columns:repeat({cols},1fr)">{cards}</div></div>')
    return "", '<div class="glow l"></div>', f'<div class="wrap">{top(s)}{body}{FOOT}</div>'

def b_split(s):
    t, size = title_of(s, (52, 46, 40), (40, 60))
    items = "".join(f'<div class="item"><span class="f">{esc(r["label"])}</span>{value(r)}</div>' for r in s["rows"])
    left = (f'<div class="spl"><div class="ring"></div><div class="tag"><span class="sq"></span>{esc(s["kind"])}</div>'
            f'<h1 style="font-size:{size}px">{t}</h1><p class="sub" style="font-size:21px">{esc(s["sub"])}</p>'
            f'<div class="brand">Sky Designers</div></div>')
    right = (f'<div class="spr"><div class="date">{esc(s["date"])}</div><div class="items"><div class="ph">{esc(s["panel_title"])}</div>{items}{note(s)}</div>'
             f'<div class="dom">skydesigners.lk/blog</div></div>')
    return "split", "", f'<div class="sp">{left}{right}</div>'

def b_center(s):
    t, size = title_of(s, (64, 56, 48), (45, 65))
    chips = "".join(f'<div class="chip"><span class="f">{esc(r["label"])}</span>{value(r)}</div>' for r in s["rows"])
    body = (f'<div class="cmain"><h1 style="font-size:{size}px;max-width:1000px">{t}</h1><p class="sub">{esc(s["sub"])}</p>'
            f'<div class="chips">{chips}</div>{note(s)}</div>')
    return "", '<div class="grid-bg"></div><div class="glow"></div><div class="glow l"></div>', f'<div class="wrap">{top(s)}{body}{FOOT}</div>'

BUILDERS = {"panel": b_panel, "stat": b_stat, "grid": b_grid, "split": b_split, "center": b_center}

def build(s):
    layout = s.get("layout", "panel")
    assert layout in LAYOUTS, f"layout must be one of {LAYOUTS}"
    body_cls, deco, inner = BUILDERS[layout](s)
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body class="{body_cls}">{deco}{inner}</body></html>'''

async def render(page_html, out):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 675}, device_scale_factor=2)
        await pg.set_content(page_html, wait_until="networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=out)
        await b.close()

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    assert 2 <= len(spec["rows"]) <= 4, "2 to 4 rows"
    asyncio.run(render(build(spec), sys.argv[2]))
    print("ok", sys.argv[2])
