"""Render the neofetch-style profile card (assets/card-dark.svg, assets/card-light.svg).

Usage: python scripts/render.py [avatar.png]
Needs Pillow only when an avatar is given; otherwise reuses assets/avatar.txt.
Edit INFO below and re-run to change the card.
"""
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASCII_FILE = ROOT / "assets" / "avatar.txt"
COLS, ROWS = 62, 31
RAMP = " .:-=+*#%@"

INFO = [
    ("title", "nick@github"),
    ("rule", ""),
    ("Role", "builder of self-hosted tools & AI agents"),
    ("Shell", "TypeScript · Python · SQL · Bash"),
    ("Infra", "Docker · Postgres · Linux · homelab"),
    ("AI", "Claude Code · agents · voice pipelines"),
    ("Now", "FileX · Keel · Agent Office"),
    ("Motto", "own your machine, own your data"),
    ("rule", ""),
    ("Repos", "github.com/niklan1110"),
    ("palette", ""),
]

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", fg="#e6edf3", dim="#7d8590",
                 key="#f0883e", art="#79c0ff", title="#3fb950"),
    "light": dict(bg="#ffffff", border="#d0d7de", fg="#1f2328", dim="#656d76",
                  key="#bc4c00", art="#0969da", title="#1a7f37"),
}
PALETTE = ["#f85149", "#f0883e", "#d29922", "#3fb950", "#58a6ff", "#bc8cff", "#ff7b72", "#8b949e"]


def avatar_to_ascii(path):
    """Map a photo to ASCII; grass-green pixels become background."""
    from PIL import Image

    img = Image.open(path).convert("RGB")
    w, h = img.size
    img = img.crop((int(w * 0.22), int(h * 0.30), int(w * 0.74), int(h * 0.94)))
    # Monospace cells are ~2x taller than wide, so sample half as many rows.
    img = img.resize((COLS, ROWS))
    lines = []
    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            r, g, b = img.getpixel((x, y))
            if g > r + 12 and g > b + 12:
                row += " "
                continue
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            row += RAMP[min(len(RAMP) - 1, int(lum * len(RAMP)))]
        lines.append(row.rstrip())
    return lines


def svg(theme, art):
    t = THEMES[theme]
    lh, pad = 19, 28
    alh, acw = 9, 5.4  # art line height / char width at 9px
    width = 900
    height = pad * 2 + 34 + max(len(art) * alh, len(INFO) * lh)
    info_x = pad + COLS * acw + 32
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="nick@github profile card">',
        "<style>",
        "text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace;"
        "font-size:14px;white-space:pre}",
        ".a{font-size:9px;font-weight:bold}",
        ".cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}",
        "@media (prefers-reduced-motion:reduce){.cur{animation:none}}",
        "</style>",
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="10" '
        f'fill="{t["bg"]}" stroke="{t["border"]}"/>',
    ]
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        out.append(f'<circle cx="{pad + i * 20}" cy="22" r="6" fill="{c}"/>')
    out.append(f'<text x="{width / 2}" y="27" fill="{t["dim"]}" text-anchor="middle">'
               f'nick@github: ~ — neofetch</text>')
    top = pad + 34
    info_top = top + max(0, (len(art) * alh - len(INFO) * lh) // 2)
    for i, line in enumerate(art):
        out.append(f'<text class="a" x="{pad}" '
                   f'y="{top + i * alh}" fill="{t["art"]}">{escape(line)}</text>')
    for i, (k, v) in enumerate(INFO):
        y = info_top + i * lh
        if k == "title":
            out.append(f'<text x="{info_x}" y="{y}" fill="{t["title"]}" '
                       f'font-weight="bold">{escape(v)}</text>')
        elif k == "rule":
            out.append(f'<text x="{info_x}" y="{y}" fill="{t["dim"]}">'
                       f'{"─" * 44}</text>')
        elif k == "palette":
            for j, c in enumerate(PALETTE):
                out.append(f'<rect x="{info_x + j * 26}" y="{y - 12}" '
                           f'width="24" height="14" rx="2" fill="{c}"/>')
            out.append(f'<rect class="cur" x="{info_x + len(PALETTE) * 26 + 6}" y="{y - 12}" '
                       f'width="9" height="16" fill="{t["fg"]}"/>')
        else:
            out.append(f'<text x="{info_x}" y="{y}">'
                       f'<tspan fill="{t["key"]}" font-weight="bold">{escape(k)}</tspan>'
                       f'<tspan fill="{t["fg"]}">: {escape(v)}</tspan></text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    if len(sys.argv) > 1:
        ASCII_FILE.write_text("\n".join(avatar_to_ascii(sys.argv[1])) + "\n")
    art = ASCII_FILE.read_text().splitlines()
    for theme in THEMES:
        (ROOT / "assets" / f"card-{theme}.svg").write_text(svg(theme, art))


if __name__ == "__main__":
    main()
