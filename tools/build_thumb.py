"""Neon thumbnail featured images for skydesigners.lk articles (approved by Joshuwa, 27 Nov 2026).

Spec (JSON, one per option):
{
  "type": "thumb",
  "layout": "split" | "point" | "versus",
  "character": "sceptical-phone" | "pointing" | "surprised-phone" | "none",   # file in assets/character/
  "tag": "WhatsApp ads",                    # optional small label (split, point)
  "tag_icon": "whatsapp" | "none",          # optional
  "headline": ["Chats"],                    # 1-3 white lines (split, point); versus: one line
  "highlight": "≠ Sales",                   # the yellow-box words
  "bubbles": ["price pls?", "how much?", "delivery to Kandy?"],   # 0-3 floating chat chips
  "card":   {"label": "One campaign · Sept 2026", "badge": "22.0% bought",
             "a": ["6,818", "chats"], "b": ["1,497", "orders"]},             # split
  "rows":   [["WhatsApp chats", "6,818"], ["Actually bought", "1,497"]],     # point (2 rows, 2nd is green)
  "compare": [["WhatsApp chats", 6818], ["Orders", 1497]],  # pop: real numbers drawn as bars
  "notes":  ["price pls?", "how much?", "Booked?", "Paid?"],   # caption: 2-4 arrow labels
  "style":  "neon" | "clean" | "pop" | "caption",   # neon uses layout; clean uses left/right; pop uses hero+card+compare; caption uses notes
  "left":   {"k": "Cost per chat", "v": "LKR 130", "s": "Looks cheap"},      # versus (red)
  "right":  {"k": "Cost per sale", "v": "LKR 592", "s": "What you really pay"},  # versus (green)
  "hero":   {"big": "22%", "label": "of chats bought"}   # used instead of the person when character is "none"
}
Every number must come from the article's Source Log. Size 1200x675, rendered at 2x, saved as JPEG.
"""
import html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = (ROOT / "assets").as_uri()
WA = '<svg viewBox="0 0 24 24" fill="#04210e"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 2.9 2.9 0 0 0-.9 2.2 5 5 0 0 0 1 2.7 11.5 11.5 0 0 0 4.4 3.9c1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2l-.7-.4z"/></svg>'
EXTRA = """
.hero{position:absolute;width:330px;height:470px;border-radius:44px;background:rgba(8,14,34,.9);border:3px solid #3BE8FF;
 box-shadow:0 0 14px #3BE8FF,0 0 50px rgba(59,232,255,.45),inset 0 0 40px rgba(59,232,255,.18);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:30px}
.hero b{font-weight:900;font-size:120px;letter-spacing:-4px;color:#4dff95;line-height:1}
.hero span{font-weight:600;font-size:24px;color:#c9d3ea;margin-top:10px}
.hero .bars{display:flex;gap:10px;align-items:flex-end;height:90px;margin-top:26px}
.hero .bars i{width:22px;border-radius:6px;background:#3BE8FF;box-shadow:0 0 10px #3BE8FF}
"""
e = html.escape

def _tag(s):
    if not s.get("tag"):
        return ""
    icon = WA if s.get("tag_icon", "whatsapp" if "whatsapp" in s["tag"].lower() else "none") == "whatsapp" else ""
    return f'<div class="tag" style="left:60px;top:{s.get("_tagtop",58)}px">{icon}{e(s["tag"])}</div>'

def _bubbles(s, spots, sharp_index):
    out = []
    for i, t in enumerate((s.get("bubbles") or [])[:3]):
        x, y = spots[i]
        cls = "b" if i == sharp_index else "b far"
        out.append((i == sharp_index, f'<div class="{cls}" style="left:{x}px;top:{y}px">{e(t)}<small>{"✓✓ " if i == sharp_index else ""}9:4{i+1}</small></div>'))
    back = "".join(h for front, h in out if not front)
    front = "".join(h for front, h in out if front)
    return back, front

def _person(s, style):
    c = s.get("character", "none")
    if c and c != "none":
        return f'<img class="person" src="{A}/character/{e(c)}.png" style="{style}">'
    h = s.get("hero") or {}
    bars = "".join(f'<i style="height:{v}%"></i>' for v in (35, 55, 45, 70, 90))
    return f'<div class="hero" style="{s.get("_herostyle","")}"><b>{e(h.get("big",""))}</b><span>{e(h.get("label",""))}</span><div class="bars">{bars}</div></div>'

def build(s):
    lay = s.get("layout", "split")
    css = f'<link rel="stylesheet" href="{A}/thumb.css"><style>{EXTRA}{{}}</style>'
    hl = "".join(f'<span style="font-size:{{fs}}px;display:block">{e(l)}</span>' for l in s.get("headline", []))
    if lay == "split":
        card = s.get("card", {})
        a, b = card.get("a", ["", ""]), card.get("b", ["", ""])
        s["_herostyle"] = "right:120px;top:110px"
        back, front = _bubbles(s, [(1010, 70), (560, 330), (600, 165)], 2 if len(s.get("bubbles") or []) >= 3 else 0)
        fs = 126 if len(s.get("headline", [])) <= 1 else 88
        body = f"""
<div class="glow" style="left:640px;top:60px;width:520px;height:520px;background:rgba(46,107,255,.55)"></div>
<div class="glow" style="left:900px;top:300px;width:300px;height:300px;background:rgba(182,92,255,.35)"></div>
<div class="grid"></div><div class="floor"></div>
<div class="ring" style="left:700px;top:40px;width:440px;height:440px"></div>
<div class="ln" style="left:600px;top:96px;width:180px"></div><div class="ln m" style="left:1080px;top:470px;width:140px"></div>
{back}{_person(s, "right:-40px;height:600px")}{front}{_tag(s)}
<h1 style="left:56px;top:124px">{hl.replace('{fs}', str(fs))}<span class="hl" style="font-size:{int(fs*.9)}px;margin-top:12px">{e(s.get("highlight",""))}</span></h1>
<div class="card" style="left:60px;top:442px;width:520px;padding:18px 24px">
 <div class="k">{e(card.get("label",""))}</div>
 {f'<div style="position:absolute;right:20px;top:16px;background:rgba(37,211,102,.15);border:1.5px solid #25D366;color:#4dff95;font-weight:800;font-size:19px;padding:4px 12px;border-radius:9px;box-shadow:0 0 14px rgba(37,211,102,.5)">{e(card["badge"])}</div>' if card.get("badge") else ""}
 <div style="display:flex;align-items:baseline;gap:12px;margin-top:4px"><b style="font-weight:800;font-size:42px;letter-spacing:-1px">{e(a[0])}</b><span style="font-weight:600;font-size:19px;color:#9fb3d9">{e(a[1])}</span><span style="color:#3BE8FF;font-size:28px">→</span><b style="font-weight:800;font-size:42px;letter-spacing:-1px">{e(b[0])}</b><span style="font-weight:600;font-size:19px;color:#9fb3d9">{e(b[1])}</span></div></div>
<div class="brand" style="left:62px">skydesigners.lk/blog</div>"""
    elif lay == "point":
        rows = s.get("rows", [["", ""], ["", ""]])
        s["_tagtop"] = 52; s["_herostyle"] = "right:110px;top:120px"
        back, front = _bubbles(s, [(680, 120), (650, 255), (1000, 380)], 2 if len(s.get("bubbles") or []) >= 3 else 0)
        fs = 76
        body = f"""
<div class="glow" style="left:700px;top:120px;width:520px;height:520px;background:rgba(46,107,255,.5)"></div>
<div class="glow" style="left:40px;top:300px;width:420px;height:380px;background:rgba(182,92,255,.28)"></div>
<div class="grid"></div><div class="floor"></div>
<div class="ln v" style="left:610px;top:40px;height:600px;width:3px"></div><div class="ln m" style="left:610px;top:40px;width:520px"></div>
{back}{_person(s, "right:-70px;height:620px")}{front}{_tag(s)}
<h1 style="left:56px;top:110px">{hl.replace('{fs}', str(fs))}<span class="hl" style="font-size:96px;margin-top:10px">{e(s.get("highlight",""))}</span></h1>
<div class="card" style="left:60px;top:418px;width:500px;padding:12px 26px 12px">
 <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-weight:600;font-size:20px;color:#9fb3d9">{e(rows[0][0])}</span><b style="font-weight:800;font-size:42px">{e(rows[0][1])}</b></div>
 <div style="height:26px;width:3px;margin:6px 0 6px 40px;background:#3BE8FF;box-shadow:0 0 8px #3BE8FF,0 0 22px #3BE8FF"></div>
 <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-weight:600;font-size:20px;color:#9fb3d9">{e(rows[1][0])}</span><b style="font-weight:800;font-size:42px;color:#4dff95;text-shadow:0 0 18px rgba(77,255,149,.6)">{e(rows[1][1])}</b></div></div>
<div class="brand" style="left:62px">skydesigners.lk/blog</div>"""
    else:  # versus
        L, R = s.get("left", {}), s.get("right", {})
        s["_herostyle"] = "left:435px;top:150px"
        back, front = _bubbles(s, [(300, 190), (780, 170), (740, 300)], 2 if len(s.get("bubbles") or []) >= 3 else 0)
        head = " ".join(s.get("headline", []))
        pc = 'position:absolute;width:330px;padding:20px 24px;border-radius:22px;background:rgba(8,14,34,.85)'
        def box(d, col, glow, x, y):
            return (f'<div style="{pc};left:{x}px;top:{y}px;border:2.5px solid {col};box-shadow:0 0 12px {col},0 0 40px {glow},inset 0 0 30px {glow}">'
                    f'<div style="font-weight:600;font-size:18px;color:#c9d3ea">{e(d.get("k",""))}</div>'
                    f'<b style="display:block;font-weight:900;font-size:62px;letter-spacing:-2px;line-height:1.05;margin-top:4px;color:{col}">{e(d.get("v",""))}</b>'
                    f'<span style="font-weight:600;font-size:18px;color:#c9d3ea">{e(d.get("s",""))}</span></div>')
        body = f"""
<div class="glow" style="left:340px;top:120px;width:520px;height:520px;background:rgba(46,107,255,.55)"></div>
<div class="glow" style="left:-60px;top:250px;width:380px;height:380px;background:rgba(255,59,92,.25)"></div>
<div class="glow" style="left:880px;top:250px;width:380px;height:380px;background:rgba(37,211,102,.22)"></div>
<div class="grid"></div><div class="floor"></div>
<div class="ring" style="left:390px;top:150px;width:420px;height:420px"></div>
{back}{_person(s, "left:50%;transform:translateX(-50%);height:540px")}{front}
<h1 style="left:0;right:0;top:34px;text-align:center"><span style="font-size:72px">{e(head)} </span><span class="hl" style="font-size:72px">{e(s.get("highlight",""))}</span></h1>
{box(L, "#ff4d6a", "rgba(255,59,92,.45)", 40, 300)}{box(R, "#4dff95", "rgba(37,211,102,.4)", 830, 410)}
<div class="brand" style="left:42px">skydesigners.lk/blog</div>"""
    return f'<!DOCTYPE html><html><head><meta charset="utf-8">{css}</head><body><div class="c">{body}</div></body></html>'

async def render(page_html, out_path):
    from playwright.async_api import async_playwright
    import tempfile, os
    tmp = pathlib.Path(tempfile.mkdtemp()) / "t.html"
    tmp.write_text(page_html, encoding="utf-8")
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 675}, device_scale_factor=2)
        await pg.goto(tmp.as_uri()); await pg.wait_for_timeout(800)
        png = str(out_path) + ".tmp.png"
        await pg.screenshot(path=png); await b.close()
    from PIL import Image
    Image.open(png).convert("RGB").save(out_path, "JPEG", quality=90, optimize=True)
    os.remove(png)

# ---------------------------------------------------------------------------
# More styles (Joshuwa, 27 Nov 2026: "don't make all three in one style").
# spec["style"]: "neon" (default; layouts split/point/versus above), "clean", "pop", "caption".
STYLE_CSS = """
@font-face{font-family:'Poppins';font-weight:500;src:url(%(A)s/fonts/poppins-latin-500-normal.woff2)}
@font-face{font-family:'Poppins';font-weight:600;src:url(%(A)s/fonts/poppins-latin-600-normal.woff2)}
@font-face{font-family:'Poppins';font-weight:700;src:url(%(A)s/fonts/poppins-latin-700-normal.woff2)}
@font-face{font-family:'Poppins';font-weight:800;src:url(%(A)s/fonts/poppins-latin-800-normal.woff2)}
@font-face{font-family:'Poppins';font-weight:900;src:url(%(A)s/fonts/poppins-latin-900-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:675px;overflow:hidden;font-family:'Poppins'}
.c{position:relative;width:1200px;height:675px;overflow:hidden}
.hl{display:inline-block;background:#FFD43B;color:#0b1020;padding:0 18px 2px 14px;border-radius:6px}
.brand{position:absolute;bottom:20px;font-weight:600;font-size:15px;letter-spacing:.4px}
"""

def _char(s, style):
    c = s.get("character", "none")
    return f'<img src="{A}/character/{e(c)}.png" style="position:absolute;bottom:0;{style}">' if c and c != "none" else ""

def build_clean(s):
    """Light grey grid, dark type, flat yellow box, white floating cards in red/green (refs 1 and 4)."""
    L, R = s.get("left", {}), s.get("right", {})
    has = s.get("character", "none") not in ("", "none")
    def card(d, col, x, y, rot):
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:300px;background:#fff;border-radius:22px;padding:20px 24px;'
                f'box-shadow:0 30px 60px rgba(15,27,45,.18),0 2px 0 rgba(15,27,45,.04);transform:rotate({rot}deg)">'
                f'<div style="font-weight:600;font-size:17px;color:#5b6478">{e(d.get("k",""))}</div>'
                f'<div style="font-weight:900;font-size:56px;letter-spacing:-2px;color:{col};line-height:1.1">{e(d.get("v",""))}</div>'
                f'<div style="height:6px;border-radius:3px;background:{col};opacity:.18;margin:10px 0 8px"></div>'
                f'<div style="font-weight:600;font-size:16px;color:#5b6478">{e(d.get("s",""))}</div></div>')
    head = "".join(f'<div style="font-size:{"64" if has else "84"}px">{e(l)}</div>' for l in s.get("headline", []))
    body = f"""
<div class="c" style="background:#eef1f5">
<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(15,27,45,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(15,27,45,.07) 1px,transparent 1px);background-size:56px 56px"></div>
<div style="position:absolute;inset:0;background:radial-gradient(700px 500px at 70% 60%,rgba(255,255,255,.9),transparent 70%)"></div>
{card(L, "#e5364b", 40 if has else 90, 300, -3)}{card(R, "#16a34a", 860 if has else 810, 330, 3)}
{_char(s, "left:50%;transform:translateX(-50%);height:500px;filter:drop-shadow(0 24px 40px rgba(15,27,45,.35))")}
<div style="position:absolute;left:0;right:0;top:36px;text-align:center;font-weight:900;color:#0b1020;letter-spacing:-2px;line-height:1.02">
 {head}<span class="hl" style="font-size:{"70" if has else "92"}px;margin-top:8px">{e(s.get("highlight",""))}</span></div>
<div class="brand" style="left:40px;color:#5b6478">skydesigners.lk/blog</div></div>"""
    return body

def build_pop(s):
    """Saturated blue, italic heavy headline, big white dashboard card with a number and bars (refs 5, 6, 7)."""
    h = s.get("hero") or {}
    card = s.get("card") or {}
    has = s.get("character", "none") not in ("", "none")
    # bars only from real numbers: spec "compare": [["WhatsApp chats", 6818], ["Orders", 1497]] (2-4 rows, Source Log values)
    cmp_ = s.get("compare") or []
    mx = max([float(v) for _, v in cmp_] or [1])
    cols = ["#1f6bff", "#16a34a", "#f59e0b", "#e5364b"]
    bars = "".join(f'<div style="display:flex;align-items:center;gap:14px;margin-top:14px"><div style="width:170px;font-weight:600;font-size:18px;color:#5b6478">{e(str(k))}</div>'
                   f'<div style="flex:1;height:34px;background:#eef1f6;border-radius:8px;overflow:hidden"><div style="height:100%;width:{max(4,100*float(v)/mx):.1f}%;background:{cols[i%4]};border-radius:8px"></div></div>'
                   f'<div style="width:90px;text-align:right;font-weight:800;font-size:20px;color:#0b1020">{float(v):,.0f}</div></div>' for i, (k, v) in enumerate(cmp_))
    head = " ".join(s.get("headline", []))
    body = f"""
<div class="c" style="background:linear-gradient(135deg,#0a2a8f 0%,#0b47e6 55%,#0a2a8f 100%)">
<div style="position:absolute;left:-200px;top:-300px;width:900px;height:900px;border-radius:50%;background:radial-gradient(rgba(255,255,255,.18),transparent 60%)"></div>
<div style="position:absolute;right:-120px;bottom:-160px;width:620px;height:620px;border-radius:50%;background:radial-gradient(rgba(37,211,102,.35),transparent 65%)"></div>
<div style="position:absolute;left:46px;top:34px;font-weight:900;font-style:italic;color:#fff;font-size:66px;letter-spacing:-2px;line-height:1;transform:skewX(-6deg);text-shadow:0 6px 0 rgba(0,0,0,.18)">
 {e(head)} <span class="hl" style="color:#0b1020;text-shadow:none">{e(s.get("highlight",""))}</span></div>
<div style="position:absolute;left:{60 if has else 250}px;top:150px;width:{560 if has else 700}px;background:#fff;border-radius:26px;padding:28px 32px;box-shadow:0 40px 80px rgba(0,0,30,.45)">
 <div style="font-weight:600;font-size:22px;color:#5b6478">{e(h.get("label") or card.get("label",""))}</div>
 <div style="display:flex;align-items:center;gap:16px"><div style="font-weight:800;font-size:92px;letter-spacing:-3px;color:#0b1020;line-height:1.1">{e(h.get("big",""))}</div>
 {f'<div style="background:#e7f9ee;color:#12924a;font-weight:800;font-size:22px;padding:6px 14px;border-radius:10px">{e(card.get("badge",""))}</div>' if card.get("badge") else ""}</div>
 <div style="font-weight:600;font-size:18px;color:#8a93a6;margin-top:2px">{e(card.get("label","")) if h.get("label") else ""}</div>
 <div style="margin-top:34px">{bars}</div></div>
{_char(s, "right:-30px;height:600px;filter:drop-shadow(0 0 30px rgba(120,255,180,.35))")}
<div class="brand" style="left:46px;color:rgba(255,255,255,.75)">skydesigners.lk/blog</div></div>"""
    return body

def build_caption(s):
    """Dark wall of blurred screens, person in the middle, huge caption at the bottom with a yellow box, hand-drawn style arrows with labels (refs 2 and 3)."""
    import random
    rnd = random.Random(7)
    tiles = []
    for col in range(7):
        for row in range(4):
            x = col * 180 - 30 + rnd.randint(-15, 15); y = row * 175 - 40 + rnd.randint(-15, 15)
            w, hh = rnd.choice([(150, 120), (170, 140), (140, 150)])
            tint = rnd.choice(["#1b2235", "#232c44", "#2a2f3d", "#f2f4f8", "#1d3b2c", "#3a2330"])
            lines = "".join(f'<i style="display:block;height:9px;margin:12px 14px 0;border-radius:5px;width:{rnd.randint(40,90)}%;background:{"rgba(0,0,0,.18)" if tint=="#f2f4f8" else "rgba(255,255,255,.18)"}"></i>' for _ in range(4))
            tiles.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{hh}px;border-radius:14px;background:{tint};transform:rotate({rnd.uniform(-4,4):.1f}deg)">{lines}</div>')
    notes = (s.get("notes") or [])[:4]
    spots = [(70, 150, "M210,215 C260,200 300,230 330,260"), (70, 330, "M200,345 C250,345 300,330 340,320"),
             (930, 170, "M930,190 C880,180 850,210 830,250"), (930, 360, "M930,370 C880,370 850,350 820,330")]
    arrows = ""
    for i, t in enumerate(notes):
        x, y, d = spots[i]
        arrows += (f'<div style="position:absolute;left:{x}px;top:{y}px;font-weight:600;font-size:30px;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.6)">{e(t)}</div>'
                   f'<svg style="position:absolute;left:0;top:0" width="1200" height="675"><path d="{d}" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" marker-end="url(#ah)"/></svg>')
    head = " ".join(s.get("headline", []))
    body = f"""
<div class="c" style="background:#0b0e16">
<div style="position:absolute;inset:-40px;filter:blur(2.5px);opacity:.85">{"".join(tiles)}</div>
<div style="position:absolute;inset:0;background:radial-gradient(520px 520px at 50% 55%,rgba(11,14,22,.35),rgba(11,14,22,.7) 80%)"></div>
<svg width="0" height="0"><defs><marker id="ah" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto"><path d="M0,0 L8,5 L0,10" fill="none" stroke="#fff" stroke-width="2"/></marker></defs></svg>
{_char(s, "left:50%;transform:translateX(-50%);height:600px")}
{arrows}
<div style="position:absolute;left:0;right:0;bottom:44px;text-align:center;font-weight:900;color:#fff;font-size:92px;letter-spacing:-3px;line-height:1;text-shadow:0 8px 30px rgba(0,0,0,.7)">
 {e(head)} <span class="hl" style="text-shadow:none">{e(s.get("highlight",""))}</span></div>
<div class="brand" style="right:30px;top:22px;bottom:auto;color:rgba(255,255,255,.6)">skydesigners.lk/blog</div></div>"""
    return body

_build_neon = build
def build(s):
    st = s.get("style", "neon")
    if st == "neon":
        return _build_neon(s)
    inner = {"clean": build_clean, "pop": build_pop, "caption": build_caption}[st](s)
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{STYLE_CSS % {"A": A}}</style></head><body>{inner}</body></html>'

if __name__ == "__main__":
    import asyncio, json, sys
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
    asyncio.run(render(build(spec), sys.argv[2]))
