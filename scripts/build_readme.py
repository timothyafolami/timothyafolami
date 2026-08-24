#!/usr/bin/env python3
"""Regenerate README.md from README.template.md using live GitHub + PyPI data.

Stdlib only, so CI needs no install step. Everything between a matching pair of
<!--START:key--> / <!--END:key--> markers in the template is replaced, and two
SVGs are rendered into assets/ so the page never depends on a third-party image
host that can disappear.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

USER = "timothyafolami"
PYPI_PACKAGES = ["markitup-py"]
LANG_WINDOW_DAYS = 548  # 18 months: what I write now, not what I wrote in 2023

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "README.template.md"
OUTPUT = ROOT / "README.md"
ASSETS = ROOT / "assets"

HIDE = {USER, "AOC2025"}

# A "recently pushed" feed was cut deliberately: most of the 13,750 annual
# contributions land in private repos, so a public-push feed reads months
# stale and contradicts the activity card directly above it.

# Blue-to-cyan ramp by quantile, with amber reserved for the top 1% of days.
# The amber isn't decoration: those are the handful of 500+ contribution days,
# and a single-hue ramp buries them among the merely-busy ones.
LEVELS = ["#161b22", "#1c3557", "#22558f", "#2f86c9", "#4fc3e8"]
PEAK = "#f0a24e"
BG, BORDER, ACCENT, MUTED, FAINT = "#0d1117", "#21262d", "#58a6ff", "#8b949e", "#484f58"
PAPER, INK = "#e6edf3", "#c9d1d9"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"


def get(url: str, token: str | None = None, raw: bool = False):
    req = urllib.request.Request(url, headers={"User-Agent": f"{USER}-readme-bot"})
    if token and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace") if raw else json.load(r)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
        print(f"  warn: {url} -> {e}", file=sys.stderr)
        return None


# --------------------------------------------------------------------------- data


def fetch_repos(token):
    repos, page = [], 1
    while page <= 5:
        batch = get(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}&sort=pushed", token)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return [r for r in repos if not r["fork"] and not r["archived"] and r["name"] not in HIDE]


def fetch_contributions() -> dict:
    """Scrape the public contribution calendar.

    Deliberately unauthenticated: this returns exactly what an anonymous visitor
    sees, which is the number the README should claim. It also means CI needs no
    user-scoped token, and the default GITHUB_TOKEN would under-report here.
    """
    html = get(f"https://github.com/users/{USER}/contributions", raw=True)
    if not html:
        return {}

    dates = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"', html)
    raw = re.findall(r"(\d[\d,]*|No) contributions? on", html)
    if not dates or len(raw) != len(dates):
        return {}
    counts = [0 if c == "No" else int(c.replace(",", "")) for c in raw]
    total = sum(counts)

    # GitHub buckets days against the single busiest day, so one 1,000-commit
    # outlier flattens the whole year into level 1. Bucket by quantile instead:
    # the graph then shows the shape of a normal week rather than one spike.
    nonzero = sorted(c for c in counts if c)
    if nonzero:
        cuts = [nonzero[int(len(nonzero) * q)] for q in (0.25, 0.50, 0.75)]
    else:
        cuts = [1, 1, 1]

    def level(c: int) -> int:
        if c == 0:
            return 0
        return 1 + sum(c > cut for cut in cuts)

    days = sorted({(d, c, level(c)) for d, c in zip(dates, counts)})

    active = {d for d, _c, lvl in days if lvl > 0}
    longest = run = 0
    for _d, _c, lvl in days:
        run = run + 1 if lvl > 0 else 0
        longest = max(longest, run)

    # Today counts only once there's something on it, so start from yesterday
    # when today is still empty. Otherwise every morning reads as a broken streak.
    cursor = datetime.strptime(days[-1][0], "%Y-%m-%d")
    if cursor.strftime("%Y-%m-%d") not in active:
        cursor -= timedelta(days=1)
    current = 0
    while cursor.strftime("%Y-%m-%d") in active:
        current += 1
        cursor -= timedelta(days=1)

    return {
        "days": days,
        "peak": max(counts) if counts else 0,
        "total": total,
        "active": len(active),
        "span": len(days),
        "longest": longest,
        "current": current,
    }


# --------------------------------------------------------------------------- svg


def svg_text(x, y, s, size, fill, family=SANS, weight="400", anchor="start"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{s}</text>'
    )


def write_hero_svg(repos, user, releases, contrib) -> None:
    """Identity and headline numbers as one composed card, not a row of bars."""
    created = user.get("created_at", "2022-07-13T00:00:00Z")
    years = (datetime.now(timezone.utc) - datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)).days // 365

    stats = [
        (f"{contrib.get('total', 0):,}", "contributions"),
        (f"{contrib.get('active', 0)}", f"of {contrib.get('span', 365)} days active"),
        (f"{contrib.get('longest', 0)}", "day longest streak"),
        (str(len(repos)), "original repos"),
        (str(releases), "PyPI releases"),
        (str(years), "years building"),
    ]

    w, h = 1200, 340
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="Timothy Afolami, Machine Learning Engineer">',
        "<defs>",
        '<radialGradient id="glow" cx="0.18" cy="0.12" r="0.85">'
        f'<stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.22"/>'
        f'<stop offset="45%" stop-color="{ACCENT}" stop-opacity="0.06"/>'
        f'<stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>',
        '<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{LEVELS[4]}"/>'
        f'<stop offset="55%" stop-color="{ACCENT}"/>'
        f'<stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient>',
        '<linearGradient id="spine" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{LEVELS[4]}"/>'
        f'<stop offset="100%" stop-color="{ACCENT}" stop-opacity="0.15"/></linearGradient>',
        '<pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">'
        f'<path d="M34 0 L0 0 0 34" fill="none" stroke="{BORDER}" stroke-opacity="0.5"/></pattern>',
        "</defs>",
        f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>',
        f'<rect width="{w}" height="{h}" rx="14" fill="url(#grid)"/>',
        f'<rect width="{w}" height="{h}" rx="14" fill="url(#glow)"/>',
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{BORDER}"/>',
        # left spine
        '<rect x="64" y="74" width="3" height="132" rx="1.5" fill="url(#spine)"/>',
        svg_text(92, 130, "Timothy Afolami", 58, PAPER, SANS, "700"),
        svg_text(95, 163, "MACHINE LEARNING ENGINEER", 13.5, ACCENT, MONO, "500"),
        svg_text(94, 200, "I build systems meant to scale, and take models the rest of the way:", 16.5, MUTED),
        svg_text(94, 224, "serving, packaging, evaluation, and the parts that break in production.", 16.5, MUTED),
        '<rect x="92" y="252" width="330" height="2.5" rx="1.25" fill="url(#rule)"/>',
        svg_text(92, 288, "@PeepalyticsAIdev   ·   Nigeria, UTC+1   ·   Python · Go · Node · PyTorch · ONNX · FastAPI", 12.5, FAINT, MONO),
    ]

    # stat block, two columns of three, right side
    ox, oy, cw, ch = 706, 74, 218, 62
    for i, (value, label) in enumerate(stats):
        cx, cy = ox + (i % 2) * cw, oy + (i // 2) * ch
        size = 30 if len(value) <= 5 else 25
        out.append(svg_text(cx, cy + 28, value, size, PAPER, MONO, "700"))
        out.append(svg_text(cx, cy + 47, label, 11.5, FAINT, SANS))
    out.append(f'<rect x="{ox + cw - 26}" y="{oy}" width="1" height="{ch*3 - 14}" fill="{BORDER}"/>')
    for r in (1, 2):
        out.append(f'<rect x="{ox}" y="{oy + ch*r - 12}" width="{cw*2 - 26}" height="1" fill="{BORDER}"/>')

    out.append("</svg>")
    (ASSETS / "hero.svg").write_text("\n".join(out), encoding="utf-8")


def write_activity_svg(contrib) -> None:
    """Contribution calendar plus a monthly volume curve.

    The calendar alone is a flat texture; the curve gives the year a shape and
    shows the trajectory a grid of squares cannot.
    """
    days = contrib.get("days")
    if not days:
        return

    cell, gap, pad = 17, 3, 26
    step = cell + gap
    first = datetime.strptime(days[0][0], "%Y-%m-%d")
    origin = first - timedelta(days=(first.weekday() + 1) % 7)
    weeks = ((datetime.strptime(days[-1][0], "%Y-%m-%d") - origin).days // 7) + 1

    chart_h, chart_top = 88, 92
    grid_top = chart_top + chart_h + 48
    w = pad * 2 + weeks * step
    h = grid_top + 7 * step + 40

    peak_cut = sorted((c for _, c, _ in days), reverse=True)[max(0, len(days) // 100)]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="Contribution activity over the past year">',
        "<defs>",
        '<linearGradient id="area" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{LEVELS[4]}" stop-opacity="0.42"/>'
        f'<stop offset="100%" stop-color="{LEVELS[4]}" stop-opacity="0.02"/></linearGradient>',
        "</defs>",
        f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>',
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{BORDER}"/>',
    ]
    # Monospace advance is ~0.6em; measure the headline number so the label
    # that follows it can never collide with it.
    total_str = f"{contrib['total']:,}"
    out.append(svg_text(pad, 40, total_str, 28, PAPER, MONO, "700"))
    out.append(svg_text(pad + len(total_str) * 28 * 0.605 + 14, 40, "contributions in the past year", 15.5, MUTED))
    out.append(svg_text(w - pad, 30, f"{contrib['active']} of {contrib['span']} days active", 12, MUTED, MONO, "400", "end"))
    out.append(svg_text(w - pad, 48, f"{contrib['longest']}-day longest streak", 12, MUTED, MONO, "400", "end"))

    # ---- monthly volume curve
    months: dict[str, int] = {}
    for d, c, _ in days:
        months[d[:7]] = months.get(d[:7], 0) + c
    keys = sorted(months)
    vals = [months[k] for k in keys]
    top = max(vals) or 1
    span = w - pad * 2
    pts = [
        (pad + span * i / max(1, len(vals) - 1), chart_top + chart_h - (v / top) * chart_h)
        for i, v in enumerate(vals)
    ]
    for frac in (0, 0.5, 1):
        y = chart_top + chart_h * frac
        out.append(f'<rect x="{pad}" y="{y:.1f}" width="{span}" height="1" fill="{BORDER}" fill-opacity="0.7"/>')
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(
        f'<polygon points="{pad},{chart_top + chart_h} {line} {pad + span},{chart_top + chart_h}" fill="url(#area)"/>'
    )
    out.append(f'<polyline points="{line}" fill="none" stroke="{LEVELS[4]}" stroke-width="2.5" '
               f'stroke-linejoin="round" stroke-linecap="round"/>')
    hx, hy = pts[vals.index(top)]
    out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="4.5" fill="{PEAK}"/>')
    # Keep the peak label inside the card when the busiest month is the last one.
    label = f"{top:,}"
    half = len(label) * 11.5 * 0.605 / 2
    lx_peak = min(max(hx, pad + half), w - pad - half)
    out.append(svg_text(lx_peak, hy - 13, label, 11.5, PEAK, MONO, "700", "middle"))
    out.append(svg_text(pad, chart_top - 14, "MONTHLY VOLUME  ·  BUSIEST MONTH MARKED", 10, FAINT, MONO, "500"))

    # ---- calendar
    seen = set()
    for date_str, count, level in days:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        x = pad + ((d - origin).days // 7) * step
        y = grid_top + ((d.weekday() + 1) % 7) * step
        fill = PEAK if count >= peak_cut and count > 0 else LEVELS[level]
        out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3.5" fill="{fill}"/>')
        if d.day <= 7 and d.strftime("%Y-%m") not in seen:
            seen.add(d.strftime("%Y-%m"))
            out.append(svg_text(x, grid_top - 10, d.strftime("%b").upper(), 10, FAINT, MONO, "500"))

    ly = grid_top + 7 * step + 14
    out.append(svg_text(pad, ly + 10, f"amber marks the busiest days, {peak_cut:,}+ contributions", 10.5, FAINT, MONO))
    lx = w - pad - 5 * (cell - 3) - 74
    out.append(svg_text(lx - 8, ly + 10, "less", 10, FAINT, MONO, "400", "end"))
    for i, colour in enumerate(LEVELS):
        out.append(f'<rect x="{lx + i*(cell-3)}" y="{ly}" width="{cell-6}" height="{cell-6}" rx="2.5" fill="{colour}"/>')
    out.append(svg_text(lx + 5 * (cell - 3) + 4, ly + 10, "more", 10, FAINT, MONO))
    out.append("</svg>")
    (ASSETS / "activity.svg").write_text("\n".join(out), encoding="utf-8")


# --------------------------------------------------------------------------- blocks


def humanise(dt: str) -> str:
    then = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    days = (datetime.now(timezone.utc) - then).days
    if days <= 0:
        return "today"
    if days == 1:
        return "yesterday"
    if days < 30:
        return f"{days} days ago"
    if days < 365:
        m = days // 30
        return f"{m} month{'s' if m > 1 else ''} ago"
    y = days // 365
    return f"{y} year{'s' if y > 1 else ''} ago"


# Languages I actually write. A whitelist rather than a blocklist, because
# GitHub attributes vendored code to whoever committed it.
WRITTEN = {
    "Python", "Go", "Rust", "Java", "C++", "JavaScript",
    "TypeScript", "Shell", "HTML", "CSS", "SQL", "PLpgSQL",
}
# Tcl and Cython in a Python repo mean a committed virtualenv: the tally would
# then measure someone else's C extensions, not anything written here.
VENDORED_TELLS = {"Tcl", "Cython"}


def block_languages(repos, token) -> str:
    """Bytes written per language across every public repo.

    Two corrections make this honest. Jupyter Notebook is excluded because
    .ipynb bytes are mostly base64-encoded output images, and one repo here scores
    67 MB that way, none of it code. And repos carrying a committed virtualenv
    are skipped outright rather than crediting me with NumPy's C.
    """
    totals: Counter = Counter()
    skipped = 0
    for r in repos:
        data = get(f"https://api.github.com/repos/{USER}/{r['name']}/languages", token)
        if not data:
            continue
        if VENDORED_TELLS & data.keys():
            skipped += 1
            continue
        totals.update({k: v for k, v in data.items() if k in WRITTEN})
    if not totals:
        return "_Language data unavailable at build time._"

    grand = sum(totals.values())
    lines = []
    for lang, n in totals.most_common(6):
        pct = n / grand * 100
        filled = round(pct / 5)
        size = f"{n/1e6:.1f} MB" if n >= 1e6 else f"{n/1e3:.0f} KB"
        lines.append(f"`{lang:<11}` {'█' * filled}{'░' * (20 - filled)} {pct:5.1f}%  <sub>{size}</sub>")
    note = "<sub>By bytes across public repos. Notebooks excluded, since `.ipynb` size is mostly embedded output images rather than code."
    if skipped:
        note += f" {skipped} repo{'s' if skipped > 1 else ''} with a committed virtualenv skipped."
    return "\n".join(lines) + "\n\n" + note + "</sub>"


# --------------------------------------------------------------------------- main


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    print("fetching…")

    user = get(f"https://api.github.com/users/{USER}", token) or {}
    repos = fetch_repos(token)
    if not repos:
        print("error: no repos fetched; refusing to write a hollow README", file=sys.stderr)
        return 1
    contrib = fetch_contributions()
    pypi = get(f"https://pypi.org/pypi/{PYPI_PACKAGES[0]}/json") or {}
    releases = len(pypi.get("releases", {}))

    print(f"  {len(repos)} original repos")
    if contrib:
        print(f"  {contrib['total']:,} contributions · {contrib['active']}/{contrib['span']} active days"
              f" · {contrib['longest']}d longest · {contrib['current']}d current")
    else:
        print("  warn: contribution calendar unavailable; stats will show zeros", file=sys.stderr)

    ASSETS.mkdir(parents=True, exist_ok=True)
    write_hero_svg(repos, user, releases, contrib)
    write_activity_svg(contrib)

    blocks = {
        "languages": block_languages(repos, token),
        "streak": (
            f"<sub>**{contrib['total']:,}** contributions · "
            f"**{contrib['active']}/{contrib['span']}** days active · "
            f"**{contrib['longest']}-day** longest streak</sub>"
            if contrib else "_Contribution data unavailable._"
        ),
        "updated": datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC"),
    }

    text = TEMPLATE.read_text(encoding="utf-8")
    for key, value in blocks.items():
        pattern = re.compile(rf"(<!--START:{key}-->).*?(<!--END:{key}-->)", re.DOTALL)
        if not pattern.search(text):
            print(f"  warn: no marker for '{key}'", file=sys.stderr)
        text = pattern.sub(lambda m: f"{m.group(1)}\n{value}\n{m.group(2)}", text)

    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT.name}, hero.svg, activity.svg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
