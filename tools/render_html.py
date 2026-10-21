"""Render every render/<yyyy>-<mm>-<name>.html to images/<yyyy>/<mm>/<name>.png (1200x675 @2x), then delete the html.
Never overwrites an existing image: if the PNG already exists, the html is left with a .exists marker for a human."""
import asyncio, pathlib, re, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
async def main():
    files = sorted((ROOT / "render").glob("*.html"))
    if not files:
        print("nothing to render"); return
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for f in files:
            m = re.match(r"(\d{4})-(\d{2})-(.+)\.html$", f.name)
            if not m:
                print("skip bad name", f.name); continue
            out = ROOT / "images" / m[1] / m[2] / f"{m[3]}.png"
            if out.exists():
                print("exists, not overwriting", out); f.rename(f.with_suffix(".exists")); continue
            out.parent.mkdir(parents=True, exist_ok=True)
            pg = await b.new_page(viewport={"width": 1200, "height": 675}, device_scale_factor=2)
            await pg.set_content(f.read_text(encoding="utf-8"), wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(out))
            await pg.close()
            f.unlink()
            print("rendered", out)
        await b.close()
asyncio.run(main())
