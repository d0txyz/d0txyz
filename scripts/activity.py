"""Render the activity strip (assets/activity-dark.svg and activity-light.svg).

Reads the contribution calendar from the GitHub API and draws the last 30 days
as two numbers plus the last 12 weeks as bars. A workflow runs this every day.

    GITHUB_TOKEN=... python scripts/activity.py [login]
"""

import json
import os
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

from theme import MONO, STYLE, frame, inset, palette

W, H = 1280, 220
WEEKS = 12
QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch(login, token):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"Bearer {token}", "User-Agent": "profile-activity"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        payload = json.load(res)
    if payload.get("errors"):
        raise SystemExit(f"GitHub API error: {payload['errors']}")
    weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [
        [(date.fromisoformat(d["date"]), d["contributionCount"]) for d in w["contributionDays"]]
        for w in weeks
    ]


def summarize(weeks):
    days = [d for w in weeks for d in w]
    today = max(d for d, _ in days)
    recent = [(d, n) for d, n in days if d > today - timedelta(days=30)]
    return {
        "total": sum(n for _, n in recent),
        "active": sum(1 for _, n in recent if n),
        "bars": [(w[0][0], sum(n for _, n in w)) for w in weeks[-WEEKS:]],
    }


def bar(x, base, w, h, fill):
    r = min(4, h)
    return (
        f'<path d="M{x} {base}V{base - h + r}Q{x} {base - h} {x + r} {base - h}'
        f'H{x + w - r}Q{x + w} {base - h} {x + w} {base - h + r}V{base}Z" fill="{fill}"/>'
    )


def render(stats, style, mode):
    t = palette(style, mode)
    pad = inset(style)
    ink, muted, faint, accent = t["ink"], t["muted"], t["faint"], t["accent"]
    bars = stats["bars"]
    peak = max((n for _, n in bars), default=0) or 1

    bw, gap, base, tall = 26, 16, 160, 84
    x0 = W - pad - (len(bars) * bw + (len(bars) - 1) * gap)
    marks, labels = [], []
    last_month = None
    for i, (start, n) in enumerate(bars):
        x = x0 + i * (bw + gap)
        current = i == len(bars) - 1
        if n:
            h = max(6, round(tall * n / peak))
            marks.append(bar(x, base, bw, h, accent if current else muted))
            # label only the peak week and the current week
            if current or n == peak:
                labels.append(
                    f'<text x="{x + bw / 2}" y="{base - h - 10}" text-anchor="middle" fill="{ink}">{n}</text>'
                )
        else:
            marks.append(f'<rect x="{x}" y="{base - 3}" width="{bw}" height="3" rx="1.5" fill="{faint}"/>')
        month = start.strftime("%b")
        if month != last_month and (i == 0 or start.day <= 7):
            # keep the last label inside the frame
            at, anchor = (x + bw, "end") if x + 44 > W - pad else (x, "start")
            labels.append(f'<text x="{at}" y="{base + 32}" text-anchor="{anchor}" fill="{muted}">{month}</text>')
            last_month = month

    total, active = stats["total"], stats["active"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">
  <title id="title">Recent activity</title>
  <desc id="desc">{total} contributions on {active} active days in the last 30 days. Bars show contributions per week for the last {len(bars)} weeks.</desc>
  {frame(style, mode, W, H)}
  <g font-family="{MONO}">
    <text x="{pad}" y="118" fill="{ink}" font-size="68" font-weight="700">{total}</text>
    <text x="{pad}" y="160" fill="{muted}" font-size="22">contributions, last 30 days</text>
    <text x="{pad + 384}" y="118" fill="{ink}" font-size="68" font-weight="700">{active}</text>
    <text x="{pad + 384}" y="160" fill="{muted}" font-size="22">active days</text>
    <text x="{x0}" y="50" fill="{muted}" font-size="21">per week, last {len(bars)} weeks</text>
    <path d="M{x0} {base + 1}H{W - pad}" stroke="{t['line']}" stroke-width="2"/>
    {"".join(marks)}
    <g font-size="21">{"".join(labels)}</g>
  </g>
</svg>
"""


if __name__ == "__main__":
    login = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REPOSITORY_OWNER", "d0txyz")
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("Set GITHUB_TOKEN first.")
    stats = summarize(fetch(login, token))
    assets = Path(__file__).resolve().parent.parent / "assets"
    assets.mkdir(exist_ok=True)
    for mode in ("dark", "light"):
        (assets / f"activity-{mode}.svg").write_text(render(stats, STYLE, mode), encoding="utf-8", newline="\n")
    print(f"{login}: {stats['total']} contributions on {stats['active']} days (last 30 days)")
