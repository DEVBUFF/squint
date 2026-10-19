"""Local tools used by squint.py: image conversion, Chrome screenshots, simulators, folders.

This module has no network code; squint.py has no process launching. Every function raises
RuntimeError with a readable message when the tool is missing or fails.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

READABLE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
IPHONE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")


def convert_to_jpeg(path):
    """HEIC/AVIF -> JPEG with macOS `sips` so Claude can view the file; returns the readable path."""
    path = Path(path)
    if path.suffix.lower() in READABLE_EXT or not shutil.which("sips"):
        return path
    dest = path.with_suffix(".jpg")
    res = subprocess.run(["sips", "-s", "format", "jpeg", str(path), "--out", str(dest)], capture_output=True)
    if res.returncode == 0 and dest.exists():
        path.unlink(missing_ok=True)
        return dest
    return path


def open_folder(path):
    opener = "open" if sys.platform == "darwin" else ("xdg-open" if shutil.which("xdg-open") else None)
    if opener:
        subprocess.run([opener, str(path)], capture_output=True)


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


def chrome_screenshot(target, dest, width=1440, height=900, mobile=False):
    """Viewport screenshot of the user's own page (dev server, file:// concept page) in headless Chrome."""
    chrome = find_chrome()
    if not chrome:
        raise RuntimeError("Chrome/Chromium not found (set CHROME_PATH) - or install the squint-devices companion")
    if mobile:
        width, height = 390, 844
    cmd = [chrome, "--headless=new", "--hide-scrollbars", "--disable-gpu", "--no-first-run",
           "--no-default-browser-check", f"--window-size={width},{height}", "--virtual-time-budget=6000",
           f"--screenshot={dest}"]
    if mobile:
        cmd.append(f"--user-agent={IPHONE_UA}")
    subprocess.run(cmd + [target], capture_output=True, timeout=90)
    if not Path(dest).exists():
        raise RuntimeError("Chrome did not produce a screenshot")
    return Path(dest)


def devices():
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
    return info


def capture_ios(dest, device=None):
    if not shutil.which("xcrun"):
        raise RuntimeError("xcrun not found - Xcode is needed, or use a mobile MCP (squint-devices)")
    r = subprocess.run(["xcrun", "simctl", "io", device or "booted", "screenshot", str(dest)],
                       capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr.strip() or "simctl screenshot failed (is a simulator booted?)")


def capture_android(dest, device=None):
    if not shutil.which("adb"):
        raise RuntimeError("adb not found - Android platform-tools are needed, or use a mobile MCP (squint-devices)")
    cmd = ["adb"] + (["-s", device] if device else []) + ["exec-out", "screencap", "-p"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode or not r.stdout:
        raise RuntimeError(r.stderr.decode(errors="replace").strip() or "screencap failed (is an emulator running?)")
    Path(dest).write_bytes(r.stdout)
