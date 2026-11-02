"""Removes the language pie from the generated 3D contribution graphs.

github-profile-3d-contrib always draws the pie; it only counts public repos, so it
misrepresents mostly-private work. The pie is the top-level group the generator
places at translate(40, ...); everything else is left untouched.

    python tools/strip_pie.py [folder]   # default: profile-3d-contrib
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)

folder = Path(sys.argv[1] if len(sys.argv) > 1 else "profile-3d-contrib")
for path in sorted(folder.glob("*.svg")):
    tree = ET.parse(path)
    root = tree.getroot()
    pies = [g for g in root.findall(f"{{{SVG}}}g") if g.get("transform", "").startswith("translate(40,")]
    for g in pies:
        root.remove(g)
    if pies:
        tree.write(path, encoding="unicode")
    print(f"{path}: removed {len(pies)} pie group(s)")
