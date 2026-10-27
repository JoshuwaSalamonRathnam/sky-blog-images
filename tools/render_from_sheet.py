"""Render image specs listed in the published 'Image Specs' tab of the Sky Web Articles Engine sheet.
The tab's CSV URL (File > Share > Publish to web, that tab only, CSV) lives in tools/specs_url.txt.
Column A = <yyyy>-<mm>-<slug>-v<n>, column B = spec JSON. Renders only images that do not exist yet; never overwrites."""
import asyncio, csv, io, json, pathlib, re, sys, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from build_post import build, render
url = (ROOT / "tools" / "specs_url.txt").read_text().strip() if (ROOT / "tools" / "specs_url.txt").exists() else ""
async def main():
    if not url.startswith("https://"):
        print("no published specs URL yet"); return
    data = urllib.request.urlopen(url, timeout=30).read().decode("utf-8")
    rows = list(csv.reader(io.StringIO(data)))[1:]
    for r in rows:
        if len(r) < 2 or not r[0].strip():
            continue
        m = re.match(r"(\d{4})-(\d{2})-([a-z0-9-]+-v\d+)$", r[0].strip())
        if not m:
            print("bad name", r[0]); continue
        out = ROOT / "images" / m[1] / m[2] / f"{m[3]}.png"
        if out.exists():
            continue
        try:
            spec = json.loads(r[1])
            assert 2 <= len(spec["rows"]) <= 4, "2 to 4 rows"
            out.parent.mkdir(parents=True, exist_ok=True)
            await render(build(spec), str(out))
            print("rendered", out)
        except Exception as e:
            print("error", r[0], e)
asyncio.run(main())
