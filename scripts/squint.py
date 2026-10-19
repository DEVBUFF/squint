#!/usr/bin/env python3
"""squint helper: moodboard ingest, taste stats, platform detection, captures, state.

Stdlib only; Pillow is used by `palette` when it is installed. Output is plain text or
JSON so Claude can read it directly. `python3 squint.py -h` lists the commands.

Data lives in two stores with the same layout:
  global   ~/.squint (override: SQUINT_HOME) - your taste; follows you across projects
  project  <project>/.squint                       - brief, audits, decisions, project moodboard
"""
import argparse
import colorsys
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = PLUGIN_ROOT / "knowledge"
# `research --repo` updates the shipped base. In CI the plugin is loaded from a copy (Claude Code
# protects a loaded plugin's own files), so SQUINT_REPO_DIR points at the checkout to update.
REPO_KNOWLEDGE = Path(os.environ["SQUINT_REPO_DIR"]) / "knowledge" if os.environ.get("SQUINT_REPO_DIR") else KNOWLEDGE
TEMPLATES = PLUGIN_ROOT / "templates"
GLOBAL_HOME = Path(os.environ.get("SQUINT_HOME", "~/.squint")).expanduser()
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic", ".heif", ".avif"}
READABLE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
PLATFORMS = ("web", "ios", "android", "branding")
STALE_DAYS = 35
NUDGE_HOURS = 20
SKIP_DIRS = {".git", "node_modules", "Pods", "DerivedData", "build", "dist", ".next", ".nuxt",
             ".svelte-kit", ".gradle", ".idea", ".vscode", "vendor", ".squint", ".expo",
             "coverage", ".turbo", ".cache", "out", "target", "venv", ".venv", "__pycache__"}


# ---------------------------------------------------------------- utilities

def today():
    return dt.date.today().isoformat()


def now_iso():
    return dt.datetime.now().replace(microsecond=0).isoformat()


def out(obj):
    if isinstance(obj, (dict, list)):
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        print(obj)


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def sha(text, n=10):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]


def slugify(text, n=48):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return s[:n] or "item"


def ssl_context():
    """Default trust store, or certifi's when Python's own store is missing (python.org macOS builds)."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def http_get(url, limit=20_000_000, timeout=25):
    """Return (bytes, content_type, final_url)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context()) as r:
            data = r.read(limit + 1)
            if len(data) > limit:
                raise ValueError(f"response larger than {limit} bytes")
            return data, r.headers.get("Content-Type", ""), r.geturl()
    except urllib.error.URLError as e:
        if "CERTIFICATE" in str(e).upper():
            raise RuntimeError("Python cannot verify HTTPS certificates. Add the certifi package to this Python, or "
                               "use the certificate installer that ships with python.org builds.") from e
        raise


def frontmatter(path):
    meta = {}
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return meta
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.split("#")[0].strip()
    return meta


# ---------------------------------------------------------------- stores

def find_project_root(start=None):
    start = Path(start or os.getcwd()).resolve()
    for d in [start, *start.parents]:
        if (d / ".squint").is_dir():
            return d
    for d in [start, *start.parents]:
        if (d / ".git").exists():
            return d
    return start


class Store:
    def __init__(self, root, scope):
        self.root, self.scope = Path(root), scope

    def p(self, *parts):
        return self.root.joinpath(*parts)

    def ensure(self):
        dirs = ["inbox", "references/files"]
        dirs += ["taste", "trends", "logs"] if self.scope == "global" else ["audits"]
        for d in dirs:
            self.p(d).mkdir(parents=True, exist_ok=True)
        return self

    @property
    def index_path(self):
        return self.p("references", "index.json")

    def index(self):
        return read_json(self.index_path, {})

    def save_index(self, idx):
        write_json(self.index_path, idx)

    def sources(self):
        return read_json(self.p("sources.json"), [])

    def save_sources(self, items):
        write_json(self.p("sources.json"), items)


def global_store():
    return Store(GLOBAL_HOME, "global")


def project_store(project_dir=None):
    return Store(find_project_root(project_dir) / ".squint", "project")


def pick_store(args):
    return project_store(args.project_dir) if getattr(args, "project", False) else global_store()


def state():
    return read_json(GLOBAL_HOME / "state.json", {})


def save_state(st):
    write_json(GLOBAL_HOME / "state.json", st)


# ---------------------------------------------------------------- trends

def trend_files():
    """All trend files: {platform: [(period, researched_at, path, origin)]}, newest first."""
    found = {p: [] for p in PLATFORMS}
    for origin, base in (("shipped", KNOWLEDGE / "trends"), ("personal", GLOBAL_HOME / "trends")):
        if not base.is_dir():
            continue
        for period_dir in base.iterdir():
            if not re.fullmatch(r"\d{4}-\d{2}", period_dir.name):
                continue
            for plat in PLATFORMS:
                f = period_dir / f"{plat}.md"
                if f.is_file():
                    meta = frontmatter(f)
                    found[plat].append((period_dir.name, meta.get("researched_at", period_dir.name + "-01"),
                                        str(f), origin))
    for plat in found:
        found[plat].sort(key=lambda t: (t[0], t[1], t[3] == "personal"), reverse=True)
    return found


def trend_age_days():
    newest = None
    for items in trend_files().values():
        for _, researched, _, _ in items:
            try:
                d = dt.date.fromisoformat(researched[:10])
            except ValueError:
                continue
            newest = d if newest is None or d > newest else newest
    return (dt.date.today() - newest).days if newest else None, newest


def cmd_trends(args):
    files = trend_files()
    plats = [p.strip() for p in args.platform.split(",")] if args.platform else list(PLATFORMS)
    result = {}
    for plat in plats:
        if plat not in files:
            die(f"unknown platform {plat!r}; use {', '.join(PLATFORMS)}")
        items = files[plat][: (args.history or 1)]
        result[plat] = [{"period": p, "researched_at": r, "path": f, "origin": o} for p, r, f, o in items]
    age, newest = trend_age_days()
    result["_freshness"] = {"newest": newest.isoformat() if newest else None, "age_days": age,
                            "stale": age is None or age > STALE_DAYS}
    summary = None
    for origin_base in (GLOBAL_HOME / "trends", KNOWLEDGE / "trends"):
        cands = sorted(origin_base.glob("*/summary.md"), reverse=True) if origin_base.is_dir() else []
        if cands and (summary is None or cands[0].parent.name > Path(summary).parent.name):
            summary = str(cands[0])
    result["_summary"] = summary
    out(result)


def cmd_research(args):
    period = args.period or dt.date.today().strftime("%Y-%m")
    base = (REPO_KNOWLEDGE / "trends") if args.repo else (GLOBAL_HOME / "trends")
    if args.done:
        st = state()
        st["last_research"] = {"date": today(), "period": period, "target": str(base / period)}
        save_state(st)
        if args.repo:
            idx_path = REPO_KNOWLEDGE / "trends" / "index.json"
            idx = read_json(idx_path, {"periods": []})
            periods = sorted(set(idx.get("periods", [])) | {period}, reverse=True)
            write_json(idx_path, {"latest": periods[0], "periods": periods})
        out(f"recorded research for {period} -> {base / period}")
        return
    target = base / period
    target.mkdir(parents=True, exist_ok=True)
    prev, in_place = {}, []
    for plat, items in trend_files().items():
        own = target / f"{plat}.md"
        if own.exists():  # re-run within the same period: refresh the file in place
            prev[plat] = str(own)
            in_place.append(plat)
            continue
        cands = [i for i in items if i[0] <= period]  # newest first: same period elsewhere, then older
        prev[plat] = cands[0][2] if cands else None
    out({"period": period, "target_dir": str(target), "format": str(KNOWLEDGE / "trends" / "FORMAT.md"),
         "sources": str(KNOWLEDGE / "sources.md"), "previous": prev, "update_in_place": in_place,
         "files_to_write": [str(target / f"{p}.md") for p in PLATFORMS] + [str(target / "summary.md")]})


TREND_PREFIX = {"web": "web-", "ios": "ios-", "android": "and-", "branding": "brand-"}
TREND_STATUS = {"emerging", "rising", "mainstream", "peaking", "fading"}


def check_trend_file(path):
    errors, text = [], Path(path).read_text(encoding="utf-8")
    meta = frontmatter(path)
    for key in ("platform", "period", "researched_at", "sources"):
        if not meta.get(key):
            errors.append(f"front matter: missing {key}")
    prefix = TREND_PREFIX.get(meta.get("platform", ""))
    if not prefix:
        errors.append(f"front matter: platform must be one of {', '.join(TREND_PREFIX)}")
    for head in ("## TL;DR", "## Trends", "## Fading", "## Watchlist", "## Sources"):
        if head not in text:
            errors.append(f"missing section {head!r}")
    if "## Platform baseline" not in text and "## Baseline" not in text:
        errors.append("missing baseline section")
    blocks = re.split(r"^### ", text.split("## Trends", 1)[-1].split("\n## ", 1)[0], flags=re.M)[1:]
    if len(blocks) < 6:
        errors.append(f"only {len(blocks)} trends (expected 8+)")
    ids = []
    for b in blocks:
        tid = re.split(r"\s+[—–-]\s+", b.splitlines()[0], maxsplit=1)[0].strip()
        ids.append(tid)
        if prefix and not tid.startswith(prefix):
            errors.append(f"{tid}: id should start with {prefix}")
        status = re.search(r"\*\*Status:\*\*\s*([a-z]+)", b)
        if not status or status.group(1) not in TREND_STATUS:
            errors.append(f"{tid}: missing/invalid Status")
        for field in ("Momentum", "What", "Avoid when", "Implement", "Sources"):
            if f"**{field}:**" not in b:
                errors.append(f"{tid}: missing {field}")
    if len(ids) != len(set(ids)):
        errors.append("duplicate trend ids")
    sources = re.findall(r"^\d+\.\s+\[", text.split("## Sources", 1)[-1], re.M) if "## Sources" in text else []
    if len(sources) < 8:
        errors.append(f"only {len(sources)} numbered sources (expected 12+)")
    return {"file": str(path), "trends": len(blocks), "sources": len(sources), "errors": errors}


def cmd_check_trends(args):
    paths = args.paths or [f for items in trend_files().values() for _, _, f, _ in items]
    results = [check_trend_file(p) for p in paths]
    out(results)
    if any(r["errors"] for r in results):
        sys.exit(1)


# ---------------------------------------------------------------- sources

PIN_HOST = re.compile(r"^(?:[a-z]{2,3}\.)?pinterest\.[a-z.]+$", re.I)
PIN_RESERVED = {"pin", "search", "ideas", "today", "_", "explore", "business", "settings", "categories"}


def classify(url):
    u = urllib.parse.urlparse(url.strip())
    host = (u.netloc or "").lower()
    parts = [p for p in u.path.split("/") if p]
    if host == "pin.it":
        try:
            _, _, url = http_get(url, limit=2_000_000)
        except Exception as e:  # noqa: BLE001
            die(f"could not resolve {url}: {e}")
        return classify(url)
    if PIN_HOST.match(host):
        if parts and parts[0] in PIN_RESERVED:
            if parts[0] == "pin":
                return {"type": "image-page", "url": url}
            die("this Pinterest URL is not a board or profile; open the board and copy its URL")
        if len(parts) >= 2:
            user, board = parts[0], parts[1]
            return {"type": "pinterest-board", "id": f"pinterest-{slugify(user)}-{slugify(board)}",
                    "url": f"https://www.pinterest.com/{user}/{board}/",
                    "feed": f"https://www.pinterest.com/{user}/{board}.rss", "name": f"{user}/{board}"}
        if len(parts) == 1:
            user = parts[0]
            return {"type": "pinterest-profile", "id": f"pinterest-{slugify(user)}",
                    "url": f"https://www.pinterest.com/{user}/",
                    "feed": f"https://www.pinterest.com/{user}/feed.rss", "name": user}
    if host.endswith("are.na"):
        return {"type": "arena", "url": url}
    ext = Path(u.path).suffix.lower()
    if ext in IMG_EXT or host.startswith("i.pinimg.com"):
        return {"type": "image", "id": f"image-{sha(url)}", "url": url, "name": Path(u.path).name}
    return {"type": "page", "id": f"page-{slugify(host + '-' + '-'.join(parts[:3]))}", "url": url,
            "name": host + ("/" + "/".join(parts) if parts else "")}


def cmd_source(args):
    store = pick_store(args).ensure()
    items = store.sources()
    if args.action == "list":
        out(items or "no sources yet - add one with: squint.py source add <pinterest/are.na/url>")
        return
    if args.action == "remove":
        keep = [s for s in items if s["id"] != args.value]
        if len(keep) == len(items):
            die(f"no source with id {args.value}")
        store.save_sources(keep)
        out(f"removed {args.value} (downloaded references are kept)")
        return
    if not args.value:
        die("source add needs a URL")
    src = classify(args.value)
    if src["type"] == "arena":
        die(ARENA_HELP)
    if any(s["id"] == src["id"] for s in items):
        out(f"already registered: {src['id']}")
        return
    src.update({"tags": [t for t in (args.tags or "").split(",") if t], "note": args.note or "",
                "added": today(), "last_sync": None, "count": 0})
    if args.name:
        src["name"] = args.name
    items.append(src)
    store.save_sources(items)
    out({"added": src, "next": "run: squint.py sync" + (" --project" if store.scope == "project" else "")})


# ---------------------------------------------------------------- ingest

def ext_from(ctype, url):
    ctype = (ctype or "").split(";")[0].strip().lower()
    by_type = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif",
               "image/avif": ".avif", "image/heic": ".heic"}
    if ctype in by_type:
        return by_type[ctype]
    ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
    return ext if ext in IMG_EXT else ".jpg"


def make_readable(path):
    """Convert HEIC/AVIF to JPEG with macOS `sips` so Claude can view the file."""
    path = Path(path)
    if path.suffix.lower() in READABLE_EXT or not shutil.which("sips"):
        return path
    dest = path.with_suffix(".jpg")
    res = subprocess.run(["sips", "-s", "format", "jpeg", str(path), "--out", str(dest)], capture_output=True)
    if res.returncode == 0 and dest.exists():
        path.unlink(missing_ok=True)
        return dest
    return path


def add_record(store, idx, *, key, source, kind, data=None, src_path=None, ext=".jpg", url=None,
               page=None, title="", tags=None, note=""):
    rid = "r_" + sha(key)
    if rid in idx:
        return None
    folder = store.p("references", "files", slugify(source, 60))
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / f"{rid}{ext}"
    if data is not None:
        dest.write_bytes(data)
    else:
        shutil.copy2(src_path, dest)
    dest = make_readable(dest)
    idx[rid] = {"id": rid, "source": source, "kind": kind, "url": url, "page": page,
                "title": (title or "")[:200], "file": str(dest.relative_to(store.root)),
                "tags": tags or [], "note": note, "added": today(), "status": "new"}
    return rid


def download_image(url):
    data, ctype, final = http_get(url)
    if not (ctype.startswith("image/") or Path(urllib.parse.urlparse(final).path).suffix.lower() in IMG_EXT):
        raise ValueError(f"not an image ({ctype or 'unknown type'})")
    return data, ext_from(ctype, final)


def pin_big(url):
    """i.pinimg.com size segment -> 1200x (capped at the original width); ingest falls back to 736x."""
    return re.sub(r"(i\.pinimg\.com)/(?:\d+x\d*|originals)/", r"\1/1200x/", url)


def pinterest_items(src, limit):
    """Public board/profile RSS: the newest 25 pins."""
    data, _, _ = http_get(src["feed"], limit=5_000_000)
    items = []
    try:
        root = ET.fromstring(data)
        nodes = root.iter("item")
        for it in nodes:
            desc = it.findtext("description") or ""
            m = re.search(r'<img[^>]+src="([^"]+)"', desc)
            if m:
                items.append({"img": pin_big(html.unescape(m.group(1))), "page": it.findtext("link"),
                              "title": (it.findtext("title") or "").strip()})
    except ET.ParseError:
        text = html.unescape(data.decode("utf-8", "replace"))
        for m in re.finditer(r'src="(https://i\.pinimg\.com/[^"]+)"', text):
            items.append({"img": pin_big(m.group(1)), "page": None, "title": ""})
    return items[:limit]


ARENA_HELP = ("Are.na does not permit automated access to its site or API, so it is not synced by this script. "
              "Options: (1) connect Are.na's official MCP with your own account "
              "(`claude mcp add --transport http arena https://mcp.are.na/mcp`, then /mcp -> Authenticate) and ask "
              "Claude to list your channel's images, then `squint.py add <image urls>`; (2) save the images you like "
              "and drop them into the inbox folder (`squint.py inbox --open`).")


def find_chrome():
    env = os.environ.get("CHROME_PATH")
    cands = [env] if env else []
    cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
              "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"]
    cands += [shutil.which(n) for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                                        "microsoft-edge", "chrome")]
    return next((c for c in cands if c and Path(c).exists()), None)


def chrome_screenshot(url, dest, width=1440, height=900, mobile=False):
    chrome = find_chrome()
    if not chrome:
        raise RuntimeError("Chrome/Chromium not found (set CHROME_PATH) - or install the squint-devices companion")
    if mobile:
        width, height = 390, 844
    cmd = [chrome, "--headless=new", "--hide-scrollbars", "--disable-gpu", "--no-first-run",
           "--no-default-browser-check", f"--window-size={width},{height}", "--virtual-time-budget=6000",
           f"--screenshot={dest}", url]
    if mobile:
        cmd.insert(-1, "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
                       "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")
    subprocess.run(cmd, capture_output=True, timeout=90)
    if not Path(dest).exists():
        raise RuntimeError("Chrome did not produce a screenshot")
    return Path(dest)


def page_items(src):
    """A web page source: og:image (if any) + a viewport screenshot when Chrome is available."""
    items = []
    try:
        data, ctype, final = http_get(src["url"], limit=5_000_000)
        if ctype.startswith("image/"):
            return [{"img": src["url"], "page": src["url"], "title": src.get("name", "")}]
        text = data.decode("utf-8", "replace")
        title = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
        title = html.unescape(title.group(1).strip()) if title else src.get("name", "")
        for pat in (r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
                    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image'):
            m = re.search(pat, text, re.I)
            if m:
                items.append({"img": urllib.parse.urljoin(final, html.unescape(m.group(1))),
                              "page": src["url"], "title": title})
                break
    except Exception as e:  # noqa: BLE001
        title = src.get("name", "")
        print(f"  could not fetch page ({e})", file=sys.stderr)
    items.append({"screenshot": True, "page": src["url"], "title": title})
    return items


def ingest(store, idx, src, item, tags):
    if item.get("screenshot"):
        tmp = store.p("references", "files", "_tmp.png")
        tmp.parent.mkdir(parents=True, exist_ok=True)
        try:
            chrome_screenshot(item["page"], tmp)
        except Exception as e:  # noqa: BLE001
            print(f"  skip screenshot: {e}", file=sys.stderr)
            return None
        rid = add_record(store, idx, key="shot:" + item["page"], source=src["id"], kind="page-screenshot",
                         src_path=tmp, ext=".png", page=item["page"], title=item.get("title"), tags=tags)
        tmp.unlink(missing_ok=True)
        return rid
    key = re.sub(r"/\d+x\d*/", "/", item["img"])
    if "r_" + sha(key) in idx:
        return None
    candidates = [item["img"]] + ([item["img"].replace("/1200x/", "/736x/")] if "/1200x/" in item["img"] else [])
    for i, url in enumerate(candidates):
        try:
            data, ext = download_image(url)
            break
        except Exception as e:  # noqa: BLE001
            if i == len(candidates) - 1:
                print(f"  skip {item['img']}: {e}", file=sys.stderr)
                return None
    return add_record(store, idx, key=key, source=src["id"], kind="image", data=data, ext=ext, url=item["img"],
                      page=item.get("page"), title=item.get("title"), tags=tags)


def cmd_sync(args):
    store = pick_store(args).ensure()
    sources = store.sources()
    if args.source:
        sources = [s for s in sources if s["id"] == args.source]
        if not sources:
            die(f"no source {args.source}")
    idx = store.index()
    report = []
    for src in sources:
        tags = src.get("tags", [])
        try:
            if src["type"].startswith("pinterest"):
                items = pinterest_items(src, args.limit)
            elif src["type"].startswith("arena"):
                report.append({"source": src["id"], "error": ARENA_HELP})
                continue
            elif src["type"] in ("page", "image-page"):
                items = page_items(src)
            else:
                items = [{"img": src["url"], "page": None, "title": src.get("name", "")}]
        except Exception as e:  # noqa: BLE001
            report.append({"source": src["id"], "error": str(e)})
            continue
        added = [rid for item in items if (rid := ingest(store, idx, src, item, tags))]
        src["last_sync"], src["count"] = now_iso(), src.get("count", 0) + len(added)
        report.append({"source": src["id"], "found": len(items), "new": len(added)})
        store.save_index(idx)
    synced = {s["id"]: s for s in sources}
    store.save_sources([synced.get(s["id"], s) for s in store.sources()])
    st = state()
    st["last_sync"] = now_iso()
    save_state(st)
    pending = sum(1 for r in idx.values() if r["status"] == "new")
    out({"store": str(store.root), "sync": report, "pending_analysis": pending})


def cmd_add(args):
    store = pick_store(args).ensure()
    idx = store.index()
    tags = [t for t in (args.tags or "").split(",") if t]
    added, skipped = [], []
    paths = []
    for item in args.items:
        if re.match(r"https?://", item):
            src = classify(item)
            if src["type"] == "arena":
                skipped.append(f"{item}: {ARENA_HELP}")
                continue
            if src["type"] in ("image",):
                rid = ingest(store, idx, {"id": "manual-urls"}, {"img": item, "page": None, "title": ""}, tags)
            elif src["type"] in ("page", "image-page"):
                rids = [ingest(store, idx, {"id": "manual-pages"}, it, tags) for it in page_items(src)]
                rid = next((r for r in rids if r), None)
            else:
                skipped.append(f"{item}: this is a {src['type']} - register it with `source add` instead")
                continue
            (added if rid else skipped).append(rid or f"{item}: duplicate or failed")
            continue
        p = Path(item).expanduser()
        if p.is_dir():
            paths += [f for f in sorted(p.rglob("*")) if f.suffix.lower() in IMG_EXT]
        elif p.is_file():
            paths.append(p)
        else:
            skipped.append(f"{item}: not found")
    for p in paths:
        if p.suffix.lower() not in IMG_EXT:
            skipped.append(f"{p}: not an image")
            continue
        key = "file:" + hashlib.sha1(p.read_bytes()).hexdigest()
        rid = add_record(store, idx, key=key, source=args.source or "manual", kind="screenshot", src_path=p,
                         ext=p.suffix.lower(), title=p.stem, tags=tags, note=args.note or "")
        (added if rid else skipped).append(rid or f"{p.name}: duplicate")
    store.save_index(idx)
    out({"store": str(store.root), "added": added, "skipped": skipped})


def cmd_inbox(args):
    store = pick_store(args).ensure()
    inbox = store.p("inbox")
    if args.open:
        opener = "open" if sys.platform == "darwin" else "xdg-open" if shutil.which("xdg-open") else None
        if opener:
            subprocess.run([opener, str(inbox)], capture_output=True)
        out(f"inbox folder: {inbox}\ndrop screenshots there (subfolders become tags), then run: squint.py inbox"
            + (" --project" if store.scope == "project" else ""))
        return
    files = [f for f in sorted(inbox.rglob("*")) if f.is_file() and f.suffix.lower() in IMG_EXT]
    if not files:
        out(f"inbox is empty: {inbox}")
        return
    idx = store.index()
    added = []
    for f in files:
        key = "file:" + hashlib.sha1(f.read_bytes()).hexdigest()
        tags = [f.parent.name] if f.parent != inbox else []
        rid = add_record(store, idx, key=key, source="inbox", kind="screenshot", src_path=f, ext=f.suffix.lower(),
                         title=f.stem, tags=tags)
        if rid:
            added.append(rid)
        f.unlink()
    store.save_index(idx)
    out({"store": str(store.root), "imported": len(added), "ids": added,
         "hint": "subfolders of inbox/ become tags (e.g. inbox/fintech/shot.png -> tag fintech)"})


# ---------------------------------------------------------------- learning

def cmd_pending(args):
    store = pick_store(args)
    idx = store.index()
    items = [r for r in idx.values() if r["status"] == "new"][: args.limit]
    out({"store": str(store.root), "total_pending": sum(1 for r in idx.values() if r["status"] == "new"),
         "items": [{"id": r["id"], "file": str(store.p(r["file"])), "source": r["source"], "title": r["title"],
                    "tags": r["tags"], "page": r.get("page")} for r in items],
         "schema": str(TEMPLATES / "reference-analysis.json")})


def cmd_annotate(args):
    store = pick_store(args)
    idx = store.index()
    if args.file:
        batch = read_json(args.file, None)
        if batch is None:
            die(f"cannot read JSON from {args.file}")
    elif args.id and args.json:
        batch = {args.id: json.loads(args.json)}
    else:
        die("use --file batch.json or <id> '<json>'")
    if isinstance(batch, list):
        batch = {b["id"]: b.get("analysis", b) for b in batch}
    done, missing = [], []
    for rid, analysis in batch.items():
        if rid not in idx:
            missing.append(rid)
            continue
        if analysis in ("skip", None) or (isinstance(analysis, dict) and analysis.get("skip")):
            idx[rid]["status"] = "skipped"
        else:
            idx[rid]["analysis"] = analysis
            idx[rid]["status"] = "analyzed"
            idx[rid]["analyzed"] = today()
        done.append(rid)
    store.save_index(idx)
    out({"updated": len(done), "missing": missing,
         "pending_left": sum(1 for r in idx.values() if r["status"] == "new")})


def color_family(hexv):
    try:
        r, g, b = (int(hexv.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except (ValueError, IndexError):
        return None
    h, light, s = colorsys.rgb_to_hls(r, g, b)
    deg = h * 360
    if light < 0.12:
        return "near-black"
    if light > 0.93:
        return "near-white"
    if s < 0.12:
        return "gray"
    if s < 0.45 and 20 <= deg <= 60 and light > 0.6:
        return "warm-neutral"
    if s < 0.6 and 10 <= deg <= 50 and light < 0.5:
        return "brown"
    for limit, name in ((15, "red"), (40, "orange"), (65, "yellow"), (160, "green"), (195, "teal"),
                        (255, "blue"), (290, "purple"), (335, "pink"), (361, "red")):
        if deg < limit:
            return name
    return None


def norm_hex(v):
    v = str(v).strip().lstrip("#")
    if re.fullmatch(r"[0-9a-fA-F]{3}", v):
        v = "".join(c * 2 for c in v)
    return "#" + v.upper() if re.fullmatch(r"[0-9a-fA-F]{6}", v) else None


def bucket_hex(hexv):
    r, g, b = (int(hexv[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % tuple(min(255, (c // 24) * 24 + 12) for c in (r, g, b))


def collect(analyses, field):
    c = Counter()
    for a in analyses:
        cur = a
        for part in field.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
        if isinstance(cur, list):
            c.update(str(x).lower().strip() for x in cur if x)
        elif cur:
            c[str(cur).lower().strip()] += 1
    return c


def fmt_counter(c, n=12):
    total = sum(c.values()) or 1
    return " · ".join(f"{k} {v} ({round(100 * v / total)}%)" for k, v in c.most_common(n)) or "-"


def cmd_stats(args):
    stores = [global_store()]
    if args.project:
        stores = [project_store(args.project_dir)]
    if args.with_project:
        stores = [global_store(), project_store(args.project_dir)]
    refs = []
    for s in stores:
        refs += [r for r in s.index().values()]
    analyzed = [r for r in refs if r["status"] == "analyzed" and isinstance(r.get("analysis"), dict)]
    an = [r["analysis"] for r in analyzed]
    fb = []
    fb_path = GLOBAL_HOME / "taste" / "feedback.jsonl"
    if fb_path.exists():
        for line in fb_path.read_text(encoding="utf-8").splitlines():
            try:
                fb.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    fam, hexes, themes = Counter(), Counter(), Counter()
    for a in an:
        for v in a.get("palette") or []:
            h = norm_hex(v)
            if h:
                hexes[bucket_hex(h)] += 1
                f = color_family(h)
                if f:
                    fam[f] += 1
        if a.get("theme"):
            themes[str(a["theme"]).lower()] += 1
    lines = [f"# Taste stats — {', '.join(s.scope for s in stores)}",
             f"references: {len(refs)} total · {len(analyzed)} analyzed · "
             f"{sum(1 for r in refs if r['status'] == 'new')} pending · feedback events: {len(fb)}",
             "", "## Platform", fmt_counter(collect(an, "platform")),
             "## Type", fmt_counter(collect(an, "type")),
             "## Mood", fmt_counter(collect(an, "mood"), 20),
             "## Theme (light/dark)", fmt_counter(themes),
             "## Typography style", fmt_counter(collect(an, "typography.style")),
             "## Layout density", fmt_counter(collect(an, "layout.density")),
             "## Layout grid", fmt_counter(collect(an, "layout.grid")),
             "## Corner radius", fmt_counter(collect(an, "shape.radius")),
             "## Depth", fmt_counter(collect(an, "shape.depth")),
             "## Imagery", fmt_counter(collect(an, "imagery")),
             "## Palette families (share of swatches)", fmt_counter(fam, 14),
             "## Most frequent colours (bucketed)", " ".join(f"{h}×{n}" for h, n in hexes.most_common(16)) or "-",
             "## Tags", fmt_counter(collect(an, "tags") + Counter(t.lower() for r in analyzed for t in r["tags"]), 20),
             "", "## Signature moves (most recent 40)"]
    moves = [m for r in sorted(analyzed, key=lambda r: r.get("analyzed", ""), reverse=True)
             for m in (r["analysis"].get("signature_moves") or [])]
    lines += [f"- {m}" for m in moves[:40]] or ["-"]
    lines += ["", "## Why it was liked (sample of 20)"]
    lines += [f"- {r['analysis'].get('like_why')}" for r in analyzed[-20:] if r["analysis"].get("like_why")] or ["-"]
    if fb:
        acc = Counter(t for e in fb if e.get("verdict") == "accepted" for t in e.get("tags", []))
        rej = Counter(t for e in fb if e.get("verdict") == "rejected" for t in e.get("tags", []))
        lines += ["", "## Feedback from audits", f"accepted tags: {fmt_counter(acc, 15)}",
                  f"rejected tags: {fmt_counter(rej, 15)}", "recent:"]
        lines += [f"- [{e.get('verdict')}] {e.get('item')}" + (f" — {e['reason']}" if e.get("reason") else "")
                  for e in fb[-15:]]
    out("\n".join(lines))


def cmd_palette(args):
    try:
        from PIL import Image
    except ImportError:
        die("Pillow is not available, so exact colours are off - estimate the palette visually instead")
    res = {}
    for f in args.files:
        img = Image.open(f).convert("RGB")
        img.thumbnail((256, 256))
        q = img.quantize(colors=args.k, method=Image.Quantize.MEDIANCUT)
        pal = q.getpalette()[: args.k * 3]
        counts = sorted(q.getcolors(), reverse=True)
        total = sum(c for c, _ in counts) or 1
        res[f] = [{"hex": "#%02X%02X%02X" % tuple(pal[i * 3:i * 3 + 3]), "share": round(c / total, 3),
                   "family": color_family("#%02X%02X%02X" % tuple(pal[i * 3:i * 3 + 3]))} for c, i in counts]
    out(res)


def cmd_feedback(args):
    entry = {"ts": now_iso(), "verdict": args.verdict, "item": args.item,
             "tags": [t for t in (args.tags or "").split(",") if t], "reason": args.reason or "",
             "project": args.project_name or find_project_root(args.project_dir).name}
    path = GLOBAL_HOME / "taste" / "feedback.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    out(f"logged {args.verdict}: {args.item}")


# ---------------------------------------------------------------- project

def list_files(root, max_files=20000):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")
                       and not d.endswith((".imageset", ".appiconset", ".launchimage", ".symbolset"))]
        for fn in filenames:
            files.append(Path(dirpath) / fn)
            if len(files) >= max_files:
                return files
    return files


def detect(root):
    root = Path(root).resolve()
    files = list_files(root)
    rel = lambda p: str(p.relative_to(root))  # noqa: E731
    names = {f.name for f in files}
    platforms, stack, evidence = set(), [], []
    deps = {}
    for pj in [f for f in files if f.name == "package.json"][:10]:
        data = read_json(pj, {})
        deps.update(data.get("dependencies", {}) or {})
        deps.update(data.get("devDependencies", {}) or {})
    web_fw = [n for n in ("next", "nuxt", "@remix-run/react", "astro", "@sveltejs/kit", "svelte", "vue", "react",
                          "@angular/core", "solid-js", "vite", "gatsby", "@builder.io/qwik") if n in deps]
    if "react-native" in deps or "expo" in deps:
        platforms |= {"ios", "android"}
        stack.append("expo" if "expo" in deps else "react-native")
        evidence.append("package.json: react-native/expo")
        if "react-native-web" in deps:
            platforms.add("web")
    elif web_fw:
        platforms.add("web")
        stack += web_fw[:3]
        evidence.append(f"package.json: {', '.join(web_fw[:3])}")
    for f in files:
        if f.name == "pubspec.yaml" and "flutter" in f.read_text(errors="ignore"):
            platforms |= {"ios", "android"}
            stack.append("flutter")
            evidence.append(rel(f))
            if (f.parent / "web").is_dir():
                platforms.add("web")
            break
    xc = [f for f in files if f.suffix == ".pbxproj"]
    swift =[f for f in files if f.suffix == ".swift"]
    if swift or xc:
        sample = "".join(f.read_text(errors="ignore")[:4000] for f in swift[:60])
        is_flutter_or_rn = any(s in stack for s in ("flutter", "expo", "react-native"))
        if not is_flutter_or_rn:
            platforms.add("ios")
            ui = [k for k, v in (("swiftui", "import SwiftUI"), ("uikit", "import UIKit")) if v in sample]
            stack += ui or ["swift"]
            evidence.append(f"{len(swift)} .swift files" + (", Xcode project" if xc else ""))
    gradle = [f for f in files if f.name in ("build.gradle", "build.gradle.kts")]
    gtext = "".join(f.read_text(errors="ignore") for f in gradle[:12])
    if "com.android.application" in gtext or "com.android.library" in gtext or "android {" in gtext:
        if not any(s in stack for s in ("flutter", "expo", "react-native")):
            platforms.add("android")
            kt = [f for f in files if f.suffix == ".kt"]
            compose = "compose" in gtext.lower() or any("@Composable" in f.read_text(errors="ignore")[:6000]
                                                         for f in kt[:80])
            stack.append("jetpack-compose" if compose else "android-views")
            evidence.append(f"gradle android plugin, {len(kt)} .kt files")
        if "org.jetbrains.compose" in gtext:
            stack.append("compose-multiplatform")
    if not platforms and ("index.html" in names or any(f.suffix in (".html", ".css") for f in files[:3000])):
        platforms.add("web")
        stack.append("static-html")
        evidence.append("html/css files")

    token_pat = re.compile(r"(tailwind\.config\.|theme\.|tokens?\.|colors?\.|typography\.|Type\.kt$|Color\.kt$|"
                           r"Theme\.kt$|themes?\.xml$|colors\.xml$|styles\.xml$|globals?\.css$|variables\.(s?css|less)$|"
                           r"design-tokens|\.colorset$|Colors\.swift$|Theme\.swift$|Font.*\.swift$|app_theme\.dart$|"
                           r"theme\.dart$)", re.I)
    code_ext = SCAN_EXT | {".json", ".mjs", ".cjs", ".yaml", ".yml", ".toml"}
    tokens = [rel(f) for f in files if f.suffix in code_ext and token_pat.search(f.name)
              and ".colorset" not in str(f) and f.name != "package.json"][:40]
    colorsets = Counter(str(f.parent.parent.relative_to(root)) for f in files if f.parent.suffix == ".colorset")
    tokens += [f"{d} ({n} colorsets)" for d, n in colorsets.items()]
    if not tokens:
        tokens = [rel(f) for f in files if f.suffix == ".css"][:10]
    pos_pat = re.compile(r"^(README(\.\w+)?|index\.html|page\.(t|j)sx?|index\.(t|j)sx?|Home.*\.(t|j)sx|"
                         r"Landing.*|Hero.*|App\.(t|j)sx?|ContentView\.swift|MainActivity\.kt|"
                         r"Onboarding.*|Paywall.*)$", re.I)
    positioning = [rel(f) for f in files if pos_pat.match(f.name) and "test" not in str(f).lower()][:25]
    store_meta = [rel(f) for f in files if "fastlane/metadata" in str(f) or "store_listing" in str(f).lower()][:20]
    screens_pat = re.compile(r"(Screen|View|Page|Activity|Fragment)\.(swift|kt|tsx|jsx|vue|svelte|dart)$")
    screens = [rel(f) for f in files if screens_pat.search(f.name) or "/app/" in rel(f) and f.name.startswith("page.")]
    scripts = read_json(root / "package.json", {}).get("scripts", {})
    return {"root": str(root), "platforms": sorted(platforms) or ["unknown"], "stack": stack, "evidence": evidence,
            "token_files": tokens, "positioning_files": positioning, "store_metadata": store_meta,
            "screen_files": screens[:60], "screen_count": len(screens),
            "run_hints": {k: v for k, v in scripts.items() if k in ("dev", "start", "storybook", "preview", "ios",
                                                                   "android", "web")},
            "file_count": len(files)}


def cmd_detect(args):
    out(detect(args.path or find_project_root(args.project_dir)))


SCAN_EXT = {".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", ".html", ".astro",
            ".swift", ".kt", ".xml", ".dart"}
SCAN_PATTERNS = {
    "colors": [r"(?<![\w&/=\"'])#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", r"\b0x[fF]{2}([0-9a-fA-F]{6})\b",
               r"\brgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+[^)]*\)"],
    "font_sizes": [r"font-size:\s*([\d.]+(?:px|rem|em))", r"\btext-\[([\d.]+(?:px|rem))\]",
                   r"\btext-(xs|sm|base|lg|xl|[2-9]xl)\b", r"fontSize\s*[:=]\s*([\d.]+)(?:\.sp)?",
                   r"\.system\(size:\s*([\d.]+)", r"textSize=\"([\d.]+)sp\"", r"\.custom\([^)]*size:\s*([\d.]+)"],
    "radii": [r"border-radius:\s*([\d.]+(?:px|rem|%))", r"\brounded(?:-[trblse]{1,2})?-(none|sm|md|lg|xl|2xl|3xl|full|\[[^\]]+\])",
              r"borderRadius\s*[:=]\s*([\d.]+)", r"cornerRadius[:(]\s*([\d.]+)", r"RoundedCornerShape\(([\d.]+)\.dp",
              r"BorderRadius\.circular\(([\d.]+)"],
    "shadows": [r"box-shadow:\s*([^;}\n]+)",r"\b(shadow(?:-(?:sm|md|lg|xl|2xl|inner|none))?)\b(?=[\s\"'`])",
                r"\.shadow\(([^)]*)\)", r"elevation\s*[:=]\s*([\d.]+)"],
    "font_families": [r"font-family:\s*([^;}\n]+)",r"Font\.custom\(\s*\"([^\"]+)\"", r"fontFamily\s*[:=]\s*['\"]?([\w\s-]+)"],
}


def cmd_scan(args):
    root = Path(args.path or find_project_root(args.project_dir)).resolve()
    compiled = {k: [re.compile(p) for p in v] for k, v in SCAN_PATTERNS.items()}
    counts = {k: Counter() for k in compiled}
    hex_by_file = Counter()
    scanned = 0
    for f in list_files(root):
        if f.suffix not in SCAN_EXT or f.stat().st_size > 400_000 or ".min." in f.name:
            continue
        try:
            text = f.read_text(errors="ignore")
        except OSError:
            continue
        scanned += 1
        for kind, pats in compiled.items():
            for pat in pats:
                for m in pat.finditer(text):
                    val = (m.group(1) if m.groups() else m.group(0)).strip().lower()
                    if kind == "colors" and not val.startswith("rgb"):
                        val = "#" + (val * 2 if len(val) == 3 else val)[:6]
                        hex_by_file[str(f.relative_to(root))] += 1
                    counts[kind][val[:60]] += 1
    res = {"root": str(root), "files_scanned": scanned}
    for kind, c in counts.items():
        res[kind] = {"unique": len(c), "top": [f"{k} ×{v}" for k, v in c.most_common(args.top)]}
    res["files_with_most_hardcoded_colors"] = [f"{k} ×{v}" for k, v in hex_by_file.most_common(10)]
    res["read_me"] = ("Rough regex counts. Many unique values per role = design-system debt "
                      "(e.g. 40 colours for ~10 roles, 14 font sizes for a 7-step scale). "
                      "Token files naturally list many colours - judge the files outside them.")
    out(res)


def next_audit_dir(store):
    base = store.p("audits")
    base.mkdir(parents=True, exist_ok=True)
    name, n = today(), 2
    while (base / name).exists():
        name, n = f"{today()}-{n}", n + 1
    return base / name


def cmd_new_audit(args):
    store = project_store(args.project_dir).ensure()
    d = next_audit_dir(store)
    for sub in ("screens/before", "screens/after", "concepts"):
        (d / sub).mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMPLATES / "report.md", d / "report.md")
    shutil.copy2(TEMPLATES / "concepts.html", d / "concepts.html")
    brief = store.p("brief.md")
    if not brief.exists():
        shutil.copy2(TEMPLATES / "brief.md", brief)
    decisions = store.p("decisions.md")
    if not decisions.exists():
        decisions.write_text("# Design decisions\n\nAppend-only log: what was proposed, decided and why.\n",
                             encoding="utf-8")
    gi = store.root / ".gitignore"
    if not gi.exists():
        gi.write_text("# moodboard images can be large; commit them only if you want to share\nreferences/files/\n"
                      "inbox/\n", encoding="utf-8")
    out({"audit_dir": str(d), "report": str(d / "report.md"), "concepts": str(d / "concepts.html"),
         "before_screens": str(d / "screens" / "before"), "after_screens": str(d / "screens" / "after"),
         "brief": str(brief), "brief_is_new": "status: draft" in brief.read_text(encoding="utf-8"),
         "decisions": str(decisions)})


def cmd_latest_audit(args):
    store = project_store(args.project_dir)
    base = store.p("audits")
    dirs = sorted([d for d in base.iterdir() if d.is_dir()], key=lambda d: d.stat().st_mtime) if base.is_dir() else []
    if not dirs:
        die("no audits yet - run /squint:audit first")
    d = dirs[-1]
    out({"audit_dir": str(d), "report": str(d / "report.md"), "concepts": str(d / "concepts.html"),
         "after_screens": str(d / "screens" / "after"), "decisions": str(store.p("decisions.md"))})


# ---------------------------------------------------------------- capture

def cmd_capture(args):
    dest = Path(args.out).expanduser() if args.out else None
    if args.target == "devices":
        info = {}
        if shutil.which("xcrun"):
            r = subprocess.run(["xcrun", "simctl", "list", "devices", "booted"], capture_output=True, text=True)
            info["ios_booted"] = [ln.strip() for ln in r.stdout.splitlines() if "Booted" in ln]
        else:
            info["ios_booted"] = "xcrun not available (Xcode not installed)"
        if shutil.which("adb"):
            r = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            info["android"] = [ln for ln in r.stdout.splitlines()[1:] if ln.strip()]
        else:
            info["android"] = "adb not on PATH (Android platform-tools not installed)"
        info["chrome"] = find_chrome() or "not found"
        out(info)
        return
    if not dest:
        die("--out is required")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if args.target == "url":
        if not args.url:
            die("capture url needs --url")
        chrome_screenshot(args.url, dest, args.width, args.height, args.mobile)
    elif args.target == "ios":
        if not shutil.which("xcrun"):
            die("xcrun not found - install Xcode, or use a mobile MCP (squint-devices)")
        r = subprocess.run(["xcrun", "simctl", "io", args.device or "booted", "screenshot", str(dest)],
                           capture_output=True, text=True)
        if r.returncode:
            die(r.stderr.strip() or "simctl screenshot failed (is a simulator booted?)")
    elif args.target == "android":
        if not shutil.which("adb"):
            die("adb not found - install Android platform-tools, or use a mobile MCP (squint-devices)")
        cmd = ["adb"] + (["-s", args.device] if args.device else []) + ["exec-out", "screencap", "-p"]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode or not r.stdout:
            die(r.stderr.decode(errors="replace").strip() or "screencap failed (is an emulator running?)")
        dest.write_bytes(r.stdout)
    out(f"saved {dest}")


# ---------------------------------------------------------------- status / setup / hook

def cmd_init(args):
    g = global_store().ensure()
    st = state()
    st.setdefault("installed", today())
    save_state(st)
    if not g.p("taste", "profile.md").exists():
        shutil.copy2(TEMPLATES / "taste-profile.md", g.p("taste", "profile.md"))
    res = {"global": str(g.root), "inbox": str(g.p("inbox"))}
    if args.project:
        p = project_store(args.project_dir).ensure()
        res["project"] = str(p.root)
    out(res)


def store_summary(store):
    idx = store.index()
    c = Counter(r["status"] for r in idx.values())
    inbox = store.p("inbox")
    return {"root": str(store.root), "exists": store.root.is_dir(), "sources": len(store.sources()),
            "references": len(idx), "analyzed": c.get("analyzed", 0), "pending": c.get("new", 0),
            "inbox": sum(1 for f in inbox.rglob("*") if f.suffix.lower() in IMG_EXT) if inbox.is_dir() else 0}


def cmd_status(args):
    g = global_store()
    age, newest = trend_age_days()
    files = trend_files()
    prof = g.p("taste", "profile.md")
    prof_meta = frontmatter(prof) if prof.exists() else {}
    proj_root = find_project_root(args.project_dir)
    proj = Store(proj_root / ".squint", "project")
    audits = sorted(p.name for p in proj.p("audits").iterdir()) if proj.p("audits").is_dir() else []
    res = {
        "plugin_root": str(PLUGIN_ROOT),
        "trends": {"newest": newest.isoformat() if newest else None, "age_days": age,
                   "stale": age is None or age > STALE_DAYS,
                   "latest_by_platform": {p: (v[0][0] + f" ({v[0][3]})" if v else None) for p, v in files.items()}},
        "global": store_summary(g),
        "taste_profile": {"path": str(prof), "exists": prof.exists(),
                          "updated": prof_meta.get("updated"), "based_on": prof_meta.get("based_on")},
        "feedback_events": len(g.p("taste", "feedback.jsonl").read_text(encoding="utf-8").splitlines())
        if g.p("taste", "feedback.jsonl").exists() else 0,
        "project": {**store_summary(proj), "brief": proj.p("brief.md").exists(), "audits": audits[-5:],
                    "name": proj_root.name},
        "last_research": state().get("last_research"),
    }
    if args.json:
        out(res)
        return
    t = res["trends"]
    lines = [f"squint · plugin {PLUGIN_ROOT}",
             f"trends: newest {t['newest']} ({t['age_days']} days old){'  ⚠ stale' if t['stale'] else ''} · "
             + ", ".join(f"{p}: {v}" for p, v in t["latest_by_platform"].items()),
             f"global moodboard {g.root}: {res['global']['sources']} sources, {res['global']['references']} refs "
             f"({res['global']['analyzed']} learned, {res['global']['pending']} pending), inbox {res['global']['inbox']}",
             f"taste profile: {'updated ' + str(res['taste_profile']['updated']) if res['taste_profile']['exists'] else 'not built yet'}"
             f" · feedback events: {res['feedback_events']}",
             f"project {proj_root.name}: brief {'yes' if res['project']['brief'] else 'no'}, "
             f"audits {len(audits)}, project refs {res['project']['references']} "
             f"({res['project']['pending']} pending), inbox {res['project']['inbox']}"]
    out("\n".join(lines))


def cmd_hook(args):
    """SessionStart hook: emit at most a couple of short reminders, rate-limited."""
    try:
        GLOBAL_HOME.mkdir(parents=True, exist_ok=True)
        st = state()
        nudges = st.setdefault("nudges", {})
        now = dt.datetime.now()
        msgs = []

        def due(kind):
            last = nudges.get(kind)
            try:
                return last is None or (now - dt.datetime.fromisoformat(last)).total_seconds() > NUDGE_HOURS * 3600
            except ValueError:
                return True

        age, newest = trend_age_days()
        if (age is None or age > STALE_DAYS) and due("trends"):
            msgs.append(f"squint: the trend base is {age if age is not None else '?'} days old "
                        f"(newest {newest}). If the user is doing design work, offer /squint:research "
                        f"(monthly refresh).")
            nudges["trends"] = now.isoformat()
        g = store_summary(global_store())
        proj = store_summary(project_store())
        waiting = g["pending"] + g["inbox"] + proj["pending"] + proj["inbox"]
        if waiting and due("learn"):
            msgs.append(f"squint: {waiting} new moodboard references are waiting to be learned "
                        f"(inbox + synced). Offer /squint:learn when relevant.")
            nudges["learn"] = now.isoformat()
        if msgs:
            save_state(st)
            print("\n".join(msgs))
    except Exception:  # noqa: BLE001 - a hook must never break the session
        pass


# ---------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(prog="squint.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project-dir", help="project root (default: nearest .squint/.git above cwd)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def scoped(p):
        p.add_argument("--project", action="store_true", help="use the project store instead of the global one")
        return p

    s = sub.add_parser("init", help="create the global store (and --project store)")
    s.add_argument("--project", action="store_true")
    s.set_defaults(fn=cmd_init)
    s = sub.add_parser("status", help="trend freshness, moodboard and project state")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_status)
    s = sub.add_parser("detect", help="detect platforms, stack, token/theme and positioning files")
    s.add_argument("path", nargs="?")
    s.set_defaults(fn=cmd_detect)
    s = sub.add_parser("scan", help="count hard-coded colours, font sizes, radii, shadows (design-system debt)")
    s.add_argument("path", nargs="?")
    s.add_argument("--top", type=int, default=15)
    s.set_defaults(fn=cmd_scan)
    s = sub.add_parser("trends", help="paths of the newest trend files")
    s.add_argument("--platform", help="comma list: web,ios,android,branding")
    s.add_argument("--history", type=int, help="how many periods per platform (default 1)")
    s.set_defaults(fn=cmd_trends)
    s = sub.add_parser("research", help="where to write this month's research / record completion")
    s.add_argument("--period", help="YYYY-MM (default: current month)")
    s.add_argument("--repo", action="store_true", help="write into the plugin's shipped knowledge/ (maintainers, CI)")
    s.add_argument("--done", action="store_true", help="record that research for the period is complete")
    s.set_defaults(fn=cmd_research)
    s = sub.add_parser("check-trends", help="validate trend files against knowledge/trends/FORMAT.md")
    s.add_argument("paths", nargs="*")
    s.set_defaults(fn=cmd_check_trends)
    s = scoped(sub.add_parser("source", help="manage moodboard sources: add|list|remove"))
    s.add_argument("action", choices=["add", "list", "remove"])
    s.add_argument("value", nargs="?", help="URL (add) or source id (remove)")
    s.add_argument("--tags")
    s.add_argument("--name")
    s.add_argument("--note")
    s.set_defaults(fn=cmd_source)
    s = scoped(sub.add_parser("sync", help="download new images from registered sources"))
    s.add_argument("--source", help="only this source id")
    s.add_argument("--limit", type=int, default=60, help="max items per source (default 60)")
    s.set_defaults(fn=cmd_sync)
    s = scoped(sub.add_parser("add", help="add local images/folders or image/page URLs as references"))
    s.add_argument("items", nargs="+")
    s.add_argument("--tags")
    s.add_argument("--note")
    s.add_argument("--source", help="label for local files (default: manual)")
    s.set_defaults(fn=cmd_add)
    s = scoped(sub.add_parser("inbox", help="import images dropped into the inbox folder (--open shows it)"))
    s.add_argument("--open", action="store_true", help="open the inbox folder in Finder / file manager")
    s.set_defaults(fn=cmd_inbox)
    s = scoped(sub.add_parser("pending", help="references not analyzed yet"))
    s.add_argument("--limit", type=int, default=24)
    s.set_defaults(fn=cmd_pending)
    s = scoped(sub.add_parser("annotate", help="save analyses: --file batch.json | <id> '<json>'"))
    s.add_argument("id", nargs="?")
    s.add_argument("json", nargs="?")
    s.add_argument("--file")
    s.set_defaults(fn=cmd_annotate)
    s = scoped(sub.add_parser("stats", help="aggregate analyzed references + feedback for the taste profile"))
    s.add_argument("--with-project", action="store_true", help="global + project together")
    s.set_defaults(fn=cmd_stats)
    s = sub.add_parser("palette", help="dominant colours of images (needs Pillow)")
    s.add_argument("files", nargs="+")
    s.add_argument("--k", type=int, default=6)
    s.set_defaults(fn=cmd_palette)
    s = sub.add_parser("feedback", help="log an accepted/rejected recommendation (teaches the taste profile)")
    s.add_argument("--verdict", required=True, choices=["accepted", "rejected", "modified"])
    s.add_argument("--item", required=True)
    s.add_argument("--tags")
    s.add_argument("--reason")
    s.add_argument("--project-name")
    s.set_defaults(fn=cmd_feedback)
    s = sub.add_parser("new-audit", help="create .squint/audits/<date>/ from templates")
    s.set_defaults(fn=cmd_new_audit)
    s = sub.add_parser("latest-audit", help="paths of the most recent audit")
    s.set_defaults(fn=cmd_latest_audit)
    s = sub.add_parser("capture", help="screenshots: url | ios | android | devices")
    s.add_argument("target", choices=["url", "ios", "android", "devices"])
    s.add_argument("--url")
    s.add_argument("--out")
    s.add_argument("--width", type=int, default=1440)
    s.add_argument("--height", type=int, default=900)
    s.add_argument("--mobile", action="store_true", help="390x844 with an iPhone user agent")
    s.add_argument("--device", help="simulator UDID / adb serial")
    s.set_defaults(fn=cmd_capture)
    s = sub.add_parser("hook", help="SessionStart reminder (used by hooks/hooks.json)")
    s.set_defaults(fn=cmd_hook)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
