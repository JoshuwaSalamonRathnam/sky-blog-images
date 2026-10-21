"""Render every render/<yyyy>-<mm>-<name>.json spec (sky-article-post format) with tools/build_post.py
to images/<yyyy>/<mm>/<name>.png (1200x675 @2x), then delete the spec.
Never overwrites an existing image: the spec is renamed to .exists instead. Bad specs are renamed to .error."""
import asyncio, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from build_post import build, render
async def main():
    files = sorted((ROOT / "render").glob("*.json"))
    if not files:
        print("nothing to render"); return
    for f in files:
        m = re.match(r"(\d{4})-(\d{2})-([a-z0-9-]+-v\d+)\.json$", f.name)
        if not m:
            print("bad name", f.name); f.rename(f.with_suffix(".error")); continue
        out = ROOT / "images" / m[1] / m[2] / f"{m[3]}.png"
        if out.exists():
            print("exists, not overwriting", out); f.rename(f.with_suffix(".exists")); continue
        try:
            spec = json.loads(f.read_text(encoding="utf-8"))
            assert 2 <= len(spec["rows"]) <= 4, "2 to 4 rows"
            out.parent.mkdir(parents=True, exist_ok=True)
            await render(build(spec), str(out))
            f.unlink()
            print("rendered", out)
        except Exception as e:
            print("error", f.name, e); f.rename(f.with_suffix(".error"))
asyncio.run(main())
