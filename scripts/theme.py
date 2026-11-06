"""Shared look for the profile graphics (banner and activity strip).

Change STYLE to switch the whole profile to another look, then run:

    python scripts/banner.py
    GITHUB_TOKEN=... python scripts/activity.py
"""

STYLE = "swiss"  # plot | terminal | swiss | flow

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# Each style has a dark and a light palette. "surface" None means no panel:
# the graphic sits straight on the GitHub page.
STYLES = {
    "plot": {
        "radius": 20,
        "dark": {"surface": "#0F1216", "line": "#252A31", "ink": "#ECE9E2", "muted": "#8B919A", "faint": "#343A42", "accent": "#FF6A2B"},
        "light": {"surface": "#F7F5F0", "line": "#E2DED5", "ink": "#16181C", "muted": "#5E646D", "faint": "#D3CEC4", "accent": "#E4500F"},
    },
    "terminal": {
        "radius": 14,
        "dark": {"surface": "#0C1110", "line": "#1F2A27", "ink": "#E3EAE6", "muted": "#86958F", "faint": "#2C3A36", "accent": "#4ADE9B"},
        "light": {"surface": "#F3F6F2", "line": "#D9E0DA", "ink": "#121A17", "muted": "#55635D", "faint": "#C5CFC8", "accent": "#0E8A5F"},
    },
    "swiss": {
        "radius": 0,
        "dark": {"surface": None, "line": "#30363D", "ink": "#F0F3F6", "muted": "#8D96A0", "faint": "#30363D", "accent": "#6E8BFF"},
        "light": {"surface": None, "line": "#D0D7DE", "ink": "#111418", "muted": "#59636E", "faint": "#D0D7DE", "accent": "#2447F9"},
    },
    "flow": {
        "radius": 28,
        "dark": {"surface": "#14120E", "line": "#2B2720", "ink": "#F2EEE4", "muted": "#9A9385", "faint": "#3A352B", "accent": "#F5B31B"},
        "light": {"surface": "#FBF8EF", "line": "#E6DFCC", "ink": "#1B1810", "muted": "#665F50", "faint": "#D8D0BA", "accent": "#B87A00"},
    },
}


def palette(style, mode):
    return STYLES[style][mode]


def frame(style, mode, w, h):
    """The background of a graphic: a bordered panel, or two rules for 'swiss'."""
    t = palette(style, mode)
    if t["surface"] is None:
        return (
            f'<path d="M0 2H{w}" stroke="{t["ink"]}" stroke-width="3"/>'
            f'<path d="M0 {h - 1}H{w}" stroke="{t["line"]}" stroke-width="2"/>'
        )
    return (
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{STYLES[style]["radius"]}" '
        f'fill="{t["surface"]}" stroke="{t["line"]}" stroke-width="2"/>'
    )


def inset(style):
    """Left and right padding inside the frame."""
    return 4 if STYLES[style]["dark"]["surface"] is None else 76
