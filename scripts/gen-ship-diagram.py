#!/usr/bin/env python3
# Generates two animated "How I ship" pipeline SVGs (dark + light), SMIL-animated,
# transparent background, safe for GitHub <img> rendering.

NODES = [
    ("\U0001F4A1", "Idea"),
    ("\U0001F50D", "Scope"),
    ("\U0001F4D0", "Architect"),
    ("⌨️", "Build"),
    ("✅", "Test"),
    ("\U0001F680", "Ship"),
    ("\U0001F4C8", "Monitor"),
]

THEMES = {
    "dark": dict(
        node_fill="#161b22", node_stroke="#30363d", text="#e6edf3",
        sub="#8b949e", accent="#58a6ff", red="#f85149", green="#3fb950",
        line="#30363d", token="#58a6ff",
    ),
    "light": dict(
        node_fill="#f6f8fa", node_stroke="#d0d7de", text="#1f2328",
        sub="#57606a", accent="#0969da", red="#cf222e", green="#1a7f37",
        line="#d0d7de", token="#0969da",
    ),
}

W, H = 900, 236
Y = 100            # centre line
BW, BH = 104, 46   # node box
centers = [62 + i * 129 for i in range(7)]  # 62 .. 836


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme):
    c = THEMES[theme]
    p = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="-apple-system, BlinkMacSystemFont, '
        f'&apos;Segoe UI&apos;, Helvetica, Arial, sans-serif" role="img" '
        f'aria-label="How I ship: Idea, Scope, Architect, Build, Test, Ship, Monitor, repeat">'
    )
    # glow filter for the moving token
    p.append(
        f'<defs><filter id="g" x="-60%" y="-60%" width="220%" height="220%">'
        f'<feGaussianBlur stdDeviation="3.2" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        f'</filter></defs>'
    )

    # --- straight connectors on the happy path (animated flowing dashes) ---
    for i in range(6):
        x1 = centers[i] + BW / 2
        x2 = centers[i + 1] - BW / 2
        p.append(
            f'<line x1="{x1:.0f}" y1="{Y}" x2="{x2:.0f}" y2="{Y}" stroke="{c["accent"]}" '
            f'stroke-width="2.2" stroke-linecap="round" stroke-dasharray="6 6" opacity="0.9">'
            f'<animate attributeName="stroke-dashoffset" values="24;0" dur="0.9s" '
            f'repeatCount="indefinite"/></line>'
        )

    # --- loop-back: Test (idx4) -> Build (idx2 line, i.e. back to Build idx3) ---
    # Build is index 3, Test index 4. red retry arc below.
    bx, tx = centers[3], centers[4]
    p.append(
        f'<path d="M {tx} {Y+BH/2} C {tx} {Y+54}, {bx} {Y+54}, {bx} {Y+BH/2}" '
        f'fill="none" stroke="{c["red"]}" stroke-width="2" stroke-dasharray="5 5" opacity="0.85">'
        f'<animate attributeName="stroke-dashoffset" values="0;20" dur="0.8s" repeatCount="indefinite"/></path>'
    )
    p.append(
        f'<text x="{(bx+tx)/2:.0f}" y="{Y+42}" fill="{c["red"]}" font-size="11.5" '
        f'font-weight="600" text-anchor="middle">tests red</text>'
    )

    # --- loop-back: Monitor (idx6) -> Idea (idx0), big green arc below, "ship & repeat" ---
    mx, ix = centers[6], centers[0]
    p.append(
        f'<path d="M {mx} {Y+BH/2} C {mx} {Y+104}, {ix} {Y+104}, {ix} {Y+BH/2}" '
        f'fill="none" stroke="{c["green"]}" stroke-width="2" stroke-dasharray="6 6" opacity="0.8">'
        f'<animate attributeName="stroke-dashoffset" values="0;24" dur="1.1s" repeatCount="indefinite"/></path>'
    )
    p.append(
        f'<text x="{(mx+ix)/2:.0f}" y="{Y+124}" fill="{c["green"]}" font-size="11.5" '
        f'font-weight="600" text-anchor="middle">green: ship, sleep, repeat</text>'
    )

    # --- loop above: Scope (idx1) "too big -> cut" small arc ---
    sx = centers[1]
    p.append(
        f'<path d="M {sx-14} {Y-BH/2} C {sx-42} {Y-46}, {sx+42} {Y-46}, {sx+14} {Y-BH/2}" '
        f'fill="none" stroke="{c["sub"]}" stroke-width="1.8" stroke-dasharray="4 4" opacity="0.8">'
        f'<animate attributeName="stroke-dashoffset" values="0;16" dur="0.9s" repeatCount="indefinite"/></path>'
    )
    p.append(
        f'<text x="{sx}" y="{Y-52}" fill="{c["sub"]}" font-size="11" '
        f'text-anchor="middle">too big? cut it</text>'
    )

    # --- nodes ---
    for (emoji, label), cx in zip(NODES, centers):
        x = cx - BW / 2
        y = Y - BH / 2
        p.append(
            f'<g><rect x="{x:.0f}" y="{y:.0f}" width="{BW}" height="{BH}" rx="10" '
            f'fill="{c["node_fill"]}" stroke="{c["node_stroke"]}" stroke-width="1.4"/>'
            f'<rect x="{x:.0f}" y="{y:.0f}" width="{BW}" height="{BH}" rx="10" fill="none" '
            f'stroke="{c["accent"]}" stroke-width="1.6" opacity="0">'
            # pulse ring cycles across nodes
            f'<animate attributeName="opacity" values="0;0.9;0" dur="4.2s" '
            f'begin="{centers.index(cx)*0.6:.1f}s" repeatCount="indefinite"/></rect>'
            f'<text x="{cx}" y="{Y-3}" fill="{c["text"]}" font-size="15" '
            f'text-anchor="middle">{esc(emoji)}</text>'
            f'<text x="{cx}" y="{Y+15}" fill="{c["text"]}" font-size="12.5" '
            f'font-weight="600" text-anchor="middle">{esc(label)}</text></g>'
        )

    # --- travelling token along the happy path ---
    x_start = centers[0] + BW / 2
    x_end = centers[6] - BW / 2
    p.append(
        f'<circle r="5" fill="{c["token"]}" filter="url(#g)">'
        f'<animate attributeName="cx" values="{x_start:.0f};{x_end:.0f}" dur="4.8s" '
        f'keyTimes="0;1" repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="{Y};{Y}" dur="4.8s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.06;0.5;0.94;1" '
        f'dur="4.8s" repeatCount="indefinite"/></circle>'
    )

    p.append("</svg>")
    return "".join(p)


import os
# repo-relative: scripts/ -> ../assets
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(out, exist_ok=True)
for theme in ("dark", "light"):
    fn = f"{out}/how-i-ship-{theme}.svg"
    with open(fn, "w") as f:
        f.write(build(theme))
    print("wrote", fn, os.path.getsize(fn), "bytes")
