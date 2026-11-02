"""Draws the terminal-style card at the top of the profile README, in light and dark.

    python tools/workshop_card.py

Edit QUAD or INFO, rerun, and commit assets/workshop-light.svg and assets/workshop-dark.svg.
Colours are GitHub's own light and dark palettes so the card sits naturally in either theme.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

QUAD = [
    r" .-''''-.          .-''''-. ",
    r"(   ()   )        (   ()   )",
    r" '-....-'\        /'-....-' ",
    r"          \ .--. /          ",
    r"           \|  |/           ",
    r"            |[]|            ",
    r"           /|  |\           ",
    r"          / '--' \          ",
    r" .-''''-./        \.-''''-. ",
    r"(   ()   )        (   ()   )",
    r" '-....-'          '-....-' ",
]

# None draws a divider between groups.
INFO = [
    ("Builds", "robots, rc trucks, split-flaps"),
    ("Code", "python, typescript, c++, luau"),
    ("Hardware", "raspberry pi, esp32, arduino, qnx"),
    ("Printers", "ender 3 -> bambu p1s"),
    ("Air", "fpv quads"),
    ("Keys", "split, qmk + zmk"),
    ("Since", "2019"),
    None,
    ("Bench", "split-flap display"),
    ("Screen", "roblox fighter, jobapps"),
    ("Won", "best use of qnx, hack the 6ix '26"),
]

PALETTES = {
    "light": dict(bg="#f6f8fa", border="#d0d7de", art="#57606a", key="#953800", value="#0a3069",
                  dim="#8c959f", user="#116329"),
    "dark": dict(bg="#161b22", border="#30363d", art="#8b949e", key="#ffa657", value="#a5d6ff",
                 dim="#6e7681", user="#7ee787"),
}
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SIZE, LINE, CHAR = 14, 20, 8.4          # font size, line height, monospace advance (px)
WIDTH, HEIGHT = 740, 300
ART_X, INFO_X, TOP = 28, 296, 44


def card(mode):
    p = PALETTES[mode]
    out = [f'<rect x=".5" y=".5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="8" '
           f'fill="{p["bg"]}" stroke="{p["border"]}"/>']

    art_top = TOP + (len(INFO) + 1 - len(QUAD)) * LINE / 2
    for i, line in enumerate(QUAD):
        out.append(f'<text x="{ART_X}" y="{art_top + i * LINE}" fill="{p["art"]}" '
                   f'xml:space="preserve">{escape(line)}</text>')

    out.append(f'<text x="{INFO_X}" y="{TOP}"><tspan fill="{p["user"]}">pyturtle</tspan>'
               f'<tspan fill="{p["dim"]}">@</tspan><tspan fill="{p["user"]}">workshop</tspan></text>')

    def rule(baseline):
        y = baseline + 8.5
        return (f'<line x1="{INFO_X}" x2="{INFO_X + 48 * CHAR}" y1="{y}" y2="{y}" '
                f'stroke="{p["dim"]}" stroke-opacity=".6"/>')

    out.append(rule(TOP))
    y = TOP + LINE + 8
    for row in INFO:
        if row is None:
            out.append(rule(y - LINE))
            y += 8
            continue
        key, value = row
        dots = " " + "." * (12 - len(key)) + " "
        out.append(f'<text x="{INFO_X}" y="{y}" xml:space="preserve"><tspan fill="{p["key"]}">{key}</tspan>'
                   f'<tspan fill="{p["dim"]}">{dots}</tspan><tspan fill="{p["value"]}">{escape(value)}</tspan></text>')
        y += LINE

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" '
            f'height="{HEIGHT}" font-family="{MONO}" font-size="{SIZE}">{"".join(out)}</svg>\n')


def main():
    ASSETS.mkdir(exist_ok=True)
    for mode in PALETTES:
        path = ASSETS / f"workshop-{mode}.svg"
        path.write_text(card(mode), encoding="utf-8")
        print(path.relative_to(ASSETS.parent))


if __name__ == "__main__":
    main()
