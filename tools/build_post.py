"""Sky Designers featured image. Usage: python3 build_post.py spec.json out.png
spec: {"kind","date","title_html","sub","panel_title","rows":[{"label","value","style"}],"note"}
style: live (green pill) | one (amber pill) | test (grey pill) | num (blue number, no pill)
Title: plain text with the key phrase wrapped in <em>…</em> (shown in blue). 2–4 rows."""
import sys, json, html, asyncio
from playwright.async_api import async_playwright
CSS = """
:root{--bg:#030713;--card:#0D1424;--border:#1E2A42;--text:#F2F4F7;--second:#C6CDD8;--muted:#8E98A8;--accent:#5B9BFF;--green:#3DD68C;--amber:#FFB020;--grey:#8E98A8;--glow:rgba(91,155,255,.22)}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1200px;height:675px;background:var(--bg);font-family:Archivo,Inter,sans-serif;color:var(--text);overflow:hidden;position:relative}
.glow{position:absolute;right:-180px;top:-220px;width:720px;height:720px;border-radius:50%;background:radial-gradient(circle,var(--glow),transparent 65%)}
.wrap{position:relative;height:100%;padding:56px 60px 44px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center}
.tag{display:flex;align-items:center;gap:12px;font-size:15px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--second)}
.sq{width:11px;height:11px;background:var(--accent)}
.date{font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.main{flex:1;display:flex;gap:44px;align-items:center}
.left{flex:1}
h1{line-height:1.02;font-weight:800;letter-spacing:-.035em}
h1 em{font-style:normal;color:var(--accent)}
.sub{margin-top:22px;font-size:24px;line-height:1.3;color:var(--second);font-weight:500;max-width:560px}
.panel{width:430px;background:var(--card);border:1px solid var(--border);border-radius:18px;padding:26px 26px 22px}
.ph{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:14px}
.row{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:13px 0;border-top:1px solid var(--border)}
.row:first-of-type{border-top:none}
.f{font-size:18px;font-weight:600;line-height:1.2}
.pill{flex:none;font-size:12.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:6px 10px;border-radius:999px;border:1.5px solid currentColor}
.live{color:var(--green)}.one{color:var(--amber)}.test{color:var(--grey)}
.num{flex:none;font-size:24px;font-weight:800;letter-spacing:-.03em;color:var(--accent);font-variant-numeric:tabular-nums}
.note{margin-top:12px;font-size:12.5px;color:var(--muted)}
.foot{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--border);padding-top:16px}
.brand{font-weight:700;font-size:18px;letter-spacing:.01em}
.dom{font-size:15px;color:var(--muted);letter-spacing:.02em}
"""
def build(s):
    e = html.escape
    plain = s["title_html"].replace("<em>", "").replace("</em>", "")
    size = 62 if len(plain) <= 50 else 54 if len(plain) <= 70 else 46
    title = e(s["title_html"]).replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")
    rows = "".join(
        f'<div class="row"><span class="f">{e(r["label"])}</span>'
        + (f'<span class="num">{e(r["value"])}</span>' if r["style"] == "num" else f'<span class="pill {r["style"]}">{e(r["value"])}</span>')
        + "</div>" for r in s["rows"])
    note = f'<div class="note">{e(s["note"])}</div>' if s.get("note") else ""
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="glow"></div><div class="wrap">
<div class="top"><div class="tag"><span class="sq"></span>{e(s["kind"])}</div><div class="date">{e(s["date"])}</div></div>
<div class="main"><div class="left"><h1 style="font-size:{size}px">{title}</h1><p class="sub">{e(s["sub"])}</p></div>
<div class="panel"><div class="ph">{e(s["panel_title"])}</div>{rows}{note}</div></div>
<div class="foot"><div class="brand">Sky Designers</div><div class="dom">skydesigners.lk/blog</div></div>
</div></body></html>'''
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
