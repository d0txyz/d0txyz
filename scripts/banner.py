"""Render the profile banner (assets/banner-dark.svg and banner-light.svg).

The look comes from STYLE in theme.py. Run by hand after changing the text
or the style:

    python scripts/banner.py
"""

from pathlib import Path

from theme import MONO, STYLE, frame, inset, palette

W = 1280
SKILLS = ["AI automation", "full-stack web", "mobile"]
LANGUAGES = ["TypeScript", "C#", "Python", "JavaScript", "SQL", "Rust"]
TAGLINE = "  /  ".join(SKILLS)
SUMMARY = f"Builds {', '.join(SKILLS)}. Writes {', '.join(LANGUAGES)}."

PULSE_CSS = """
    .halo { transform-box: fill-box; transform-origin: center; animation: pulse 3.2s ease-out infinite; }
    @keyframes pulse { 0% { transform: scale(1); opacity: .45; } 70%, 100% { transform: scale(3.1); opacity: 0; } }
    @media (prefers-reduced-motion: reduce) { .halo { animation: none; opacity: 0; } }"""

BLINK_CSS = """
    .cursor { animation: blink 1.1s steps(1) infinite; }
    @keyframes blink { 50% { opacity: 0; } }
    @media (prefers-reduced-motion: reduce) { .cursor { animation: none; } }"""

TRAVEL_CSS = """
    .packet { offset-rotate: 0deg; animation: travel 4.5s ease-in-out infinite; }
    @keyframes travel { 0% { offset-distance: 0%; opacity: 0; } 8% { opacity: 1; } 88% { opacity: 1; } 100% { offset-distance: 100%; opacity: 0; } }
    @media (prefers-reduced-motion: reduce) { .packet { animation: none; offset-distance: 50%; } }"""


def wordmark(x, base, t, scale=1.0):
    """The letters d 0 t x y z drawn with strokes, so every device shows the same shapes."""
    ink, accent = t["ink"], t["accent"]
    return f"""<g transform="translate({x} {base}) scale({scale})">
    <g fill="none" stroke="{ink}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="40" cy="-40" r="33"/><path d="M73 -117V-7"/>
      <ellipse cx="135" cy="-62" rx="30" ry="55"/>
      <path d="M218 -110V-29Q218 -7 240 -7H252"/><path d="M197 -73H250"/>
      <path d="M284 -73L342 -7M342 -73L284 -7"/>
      <path d="M374 -73L403 -8M432 -73L386 30"/>
      <path d="M466 -73H520L466 -7H520"/>
    </g>
    <circle cx="135" cy="-62" r="11" fill="{accent}"/>
  </g>"""


def plot_banner(t):
    """A single point plotted on x, y, z axes: the dot in d0t.xyz."""
    ox, oy = 905, 244
    xlen, zlen = 270, 160
    ydx, ydy = -78, 44
    px, py, pz = 0.60, 0.62, 0.70
    fx, fy = ox + px * xlen + py * ydx, oy + py * ydy
    top = fy - pz * zlen
    faint, muted, ink, accent = t["faint"], t["muted"], t["ink"], t["accent"]

    grid = "".join(f'<path d="M{ox + i * xlen / 4:.1f} {oy}l{ydx} {ydy}"/>' for i in range(1, 5))
    grid += "".join(f'<path d="M{ox + i / 3 * ydx:.1f} {oy + i / 3 * ydy:.1f}h{xlen}"/>' for i in range(1, 4))
    body = f"""{wordmark(76, 196, t)}
  <text x="76" y="282" fill="{muted}" font-family="{MONO}" font-size="22" letter-spacing=".4">{TAGLINE}</text>
  <g fill="none" stroke="{faint}" stroke-width="1.5">{grid}</g>
  <g fill="none" stroke="{muted}" stroke-width="2" stroke-linecap="round">
    <path d="M{ox} {oy}H{ox + xlen + 26}"/><path d="M{ox} {oy}V{oy - zlen - 26}"/><path d="M{ox} {oy}l{ydx * 1.22:.1f} {ydy * 1.22:.1f}"/>
  </g>
  <g fill="{muted}" font-family="{MONO}" font-size="21">
    <text x="{ox + xlen + 38}" y="{oy + 7}">x</text>
    <text x="{ox + ydx * 1.22 - 22:.1f}" y="{oy + ydy * 1.22 + 14:.1f}">y</text>
    <text x="{ox - 6}" y="{oy - zlen - 38}">z</text>
  </g>
  <g fill="none" stroke="{accent}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round">
    <path d="M{fx:.1f} {top:.1f}V{fy:.1f}"/>
    <path d="M{fx:.1f} {fy:.1f}L{ox + px * xlen:.1f} {oy}"/>
    <path d="M{fx:.1f} {fy:.1f}L{ox + py * ydx:.1f} {oy + py * ydy:.1f}"/>
  </g>
  <circle cx="{fx:.1f}" cy="{fy:.1f}" r="3.5" fill="{accent}"/>
  <circle class="halo" cx="{fx:.1f}" cy="{top:.1f}" r="13" fill="{accent}"/>
  <circle cx="{fx:.1f}" cy="{top:.1f}" r="13" fill="{accent}"/>
  <text x="{fx + 28:.1f}" y="{top + 8:.1f}" fill="{ink}" font-family="{MONO}" font-size="24" font-weight="700">d0t</text>"""
    return 340, PULSE_CSS, body, "A single dot plotted on x, y and z axes."


def terminal_banner(t):
    """A terminal window answering who this is."""
    ink, muted, faint, accent, line = t["ink"], t["muted"], t["faint"], t["accent"], t["line"]
    x, y, step = 64, 116, 46

    def prompt(row, cmd):
        return (
            f'<text x="{x}" y="{y + row * step}"><tspan fill="{accent}">$</tspan>'
            f'<tspan fill="{ink}"> {cmd}</tspan></text>'
        )

    body = f"""<path d="M2 54H{W - 2}" stroke="{line}" stroke-width="2"/>
  <g fill="{faint}"><circle cx="40" cy="28" r="8"/><circle cx="66" cy="28" r="8"/><circle cx="92" cy="28" r="8"/></g>
  <text x="{W / 2}" y="35" text-anchor="middle" fill="{muted}" font-family="{MONO}" font-size="21">d0txyz: ~</text>
  <g font-family="{MONO}" font-size="28">
    {prompt(0, "whoami")}
    <text x="{x}" y="{y + step}" fill="{ink}" font-weight="700">d0txyz</text>
    {prompt(2, "cat skills.txt")}
    <text x="{x}" y="{y + 3 * step}" fill="{muted}">{", ".join(SKILLS)}</text>
    {prompt(4, "ls languages/")}
    <text x="{x}" y="{y + 5 * step}" fill="{muted}" xml:space="preserve">{"  ".join(lang.lower() for lang in LANGUAGES)}</text>
    <text x="{x}" y="{y + 6 * step}" fill="{accent}">$</text>
  </g>
  <rect class="cursor" x="{x + 34}" y="{y + 6 * step - 25}" width="16" height="31" fill="{accent}"/>"""
    return 440, BLINK_CSS, body, "A terminal window."


def swiss_banner(t):
    """No panel: a large wordmark, two rules and a small index of facts."""
    ink, muted = t["ink"], t["muted"]
    rows = [("BUILDS", "AI automation, web, mobile"), ("LANGUAGES", ", ".join(LANGUAGES[:3]) + ", SQL"), ("SHIPS WITH", "Next.js, .NET, Supabase")]
    index = "".join(
        f'<text x="842" y="{74 + i * 78}" fill="{muted}" font-size="19" letter-spacing="2.5">{label}</text>'
        f'<text x="842" y="{106 + i * 78}" fill="{ink}" font-size="25">{value}</text>'
        for i, (label, value) in enumerate(rows)
    )
    body = f"""{wordmark(4, 200, t, 1.18)}
  <g font-family="{MONO}">{index}</g>"""
    return 300, "", body, "A large wordmark beside a short index."


def flow_banner(t):
    """An automation running: trigger, agent, done."""
    ink, muted, line, accent, surface = t["ink"], t["muted"], t["line"], t["accent"], t["surface"]
    nodes = [(716, 58, "trigger"), (885, 140, "agent"), (1054, 222, "done")]
    route = "M791 122V172H960V254H1054"
    boxes = "".join(
        f'<rect x="{nx}" y="{ny}" width="150" height="64" rx="16" fill="{surface}" stroke="{muted}" stroke-width="2"/>'
        f'<text x="{nx + 75}" y="{ny + 40}" text-anchor="middle" fill="{ink}" font-family="{MONO}" font-size="23">{label}</text>'
        for nx, ny, label in nodes
    )
    body = f"""{wordmark(76, 190, t)}
  <text x="76" y="278" fill="{muted}" font-family="{MONO}" font-size="22" letter-spacing=".4">{TAGLINE}</text>
  <path d="{route}" fill="none" stroke="{line}" stroke-width="3" stroke-linejoin="round"/>
  <path d="{route}" fill="none" stroke="{muted}" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round" stroke-linejoin="round"/>
  <circle class="packet" r="8" fill="{accent}" style="offset-path: path('{route}')"/>
  {boxes}"""
    return 340, TRAVEL_CSS, body, "A small workflow: trigger, agent, done."


BANNERS = {"plot": plot_banner, "terminal": terminal_banner, "swiss": swiss_banner, "flow": flow_banner}


def render(style, mode):
    t = palette(style, mode)
    h, css, body, picture = BANNERS[style](t)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-labelledby="title desc">
  <title id="title">d0txyz</title>
  <desc id="desc">{SUMMARY} {picture}</desc>
  <style>{css}
  </style>
  {frame(style, mode, W, h)}
  {body}
</svg>
"""


if __name__ == "__main__":
    assets = Path(__file__).resolve().parent.parent / "assets"
    assets.mkdir(exist_ok=True)
    for mode in ("dark", "light"):
        (assets / f"banner-{mode}.svg").write_text(render(STYLE, mode), encoding="utf-8", newline="\n")
        print(f"wrote assets/banner-{mode}.svg ({STYLE})")
