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

if __name__ == "__main__":
    import asyncio, json, sys
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
    asyncio.run(render(build(spec), sys.argv[2]))
