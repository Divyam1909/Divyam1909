"""Generates assets/banner.svg (particle name) and assets/typing.svg (typing header).

Self-contained SVG + SMIL, no fonts or external services, so GitHub renders them as-is.
Run: python tools/make_svgs.py
"""
import html
import math
import os
import random

random.seed(7)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(ROOT, exist_ok=True)

# 5x7 pixel glyphs
FONT = {
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "V": ["10001", "10001", "10001", "10001", "01010", "01010", "00100"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10101", "10011", "10001", "10001"],
    " ": ["00000"] * 7,
}


def banner():
    W, H, CELL = 1200, 280, 13
    text = "DIVYAM NAVIN"
    cols = len(text) * 6 - 1
    ox, oy = (W - cols * CELL) / 2, (H - 7 * CELL) / 2 - 10
    targets = []
    for li, ch in enumerate(text):
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    x, y = ox + (li * 6 + c) * CELL + CELL / 2, oy + r * CELL + CELL / 2
                    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
                        q = CELL / 4
                        targets.append((x + dx * q + random.uniform(-0.8, 0.8), y + dy * q + random.uniform(-0.8, 0.8)))
    T = 9  # seconds per loop: drift in, hold, burst out
    kt = "0;0.28;0.66;0.8;1"
    spline = ";".join(["0.2 0.8 0.2 1"] * 4)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Divyam Navin">',
           '<defs><radialGradient id="bg" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#141a3a"/><stop offset="1" stop-color="#05060f"/></radialGradient>',
           '<linearGradient id="ink" x1="0" x2="1"><stop offset="0" stop-color="#60a5fa"/><stop offset="0.5" stop-color="#a78bfa"/><stop offset="1" stop-color="#22d3ee"/></linearGradient>',
           '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
           f'<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>']
    # twinkling background stars
    for _ in range(90):
        x, y, r = random.uniform(0, W), random.uniform(0, H), random.uniform(0.4, 1.3)
        d, b = random.uniform(2, 6), random.uniform(0, 5)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#cbd5ff" opacity="0.2"><animate attributeName="opacity" values="0.15;0.8;0.15" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')
    out.append('<g filter="url(#glow)">')
    for tx, ty in targets:
        a = random.uniform(0, 2 * math.pi)
        sx, sy = W / 2 + math.cos(a) * random.uniform(300, 700), H / 2 + math.sin(a) * random.uniform(120, 400)
        a2 = math.atan2(ty - H / 2, tx - W / 2) + random.uniform(-0.6, 0.6)
        ex, ey = tx + math.cos(a2) * random.uniform(150, 500), ty + math.sin(a2) * random.uniform(80, 300)
        hue = 210 + (tx / W) * 90
        r = random.uniform(1.5, 2.1)
        out.append(
            f'<circle r="{r:.1f}" fill="hsl({hue:.0f},90%,72%)">'
            f'<animate attributeName="cx" values="{sx:.0f};{tx:.1f};{tx:.1f};{ex:.0f};{sx:.0f}" keyTimes="{kt}" calcMode="spline" keySplines="{spline}" dur="{T}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{sy:.0f};{ty:.1f};{ty:.1f};{ey:.0f};{sy:.0f}" keyTimes="{kt}" calcMode="spline" keySplines="{spline}" dur="{T}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></circle>')
    out.append("</g>")
    out.append(f'<rect x="{W/2-120}" y="{oy + 7*CELL + 34}" width="240" height="2" rx="1" fill="url(#ink)" opacity="0.8"><animate attributeName="width" values="0;240;240;0;0" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/><animate attributeName="x" values="{W/2};{W/2-120};{W/2-120};{W/2};{W/2}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></rect>')
    out.append("</svg>")
    open(os.path.join(ROOT, "banner.svg"), "w", encoding="utf-8").write("\n".join(out))
    return len(targets)


def typing():
    lines = ["Full-stack + AI/ML engineer",
             "Teaching rocks to think. Results may vary.",
             "It works on my machine. Shipping the machine.",
             "My LLM was 99% confident. It was also wrong.",
             "There's no place like 127.0.0.1",
             "git commit -m \"fixed it (for real this time)\"",
             "Sleep is just garbage collection for the brain.",
             "Coffee in, commits out."]
    W, H, FS, CW = 900, 54, 24, 14.4  # CW = forced width per character
    SLOT, TYPE, ERASE = 5.0, 0.055, 0.025  # seconds per line, per typed char, per erased char
    T = SLOT * len(lines)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{html.escape(" | ".join(lines))}">']
    for i, s in enumerate(lines):
        n = len(s); w = n * CW; x0 = (W - w) / 2; start = i * SLOT
        t_typed = start + n * TYPE; t_erase = start + SLOT - 0.2 - n * ERASE
        times, widths = [0.0], [0.0]
        for k in range(1, n + 1): times.append(start + k * TYPE); widths.append(k * CW)
        for k in range(n - 1, -1, -1): times.append(t_erase + (n - k) * ERASE); widths.append(k * CW)
        times.append(T); widths.append(0.0)
        kt = ";".join(f"{t / T:.5f}" for t in times)
        wv = ";".join(f"{v:.1f}" for v in widths)
        cx = ";".join(f"{x0 + v:.1f}" for v in widths)
        vis = f'values="0;1;0" keyTimes="0;{start / T:.5f};{(start + SLOT) / T:.5f}"' if i else f'values="1;0" keyTimes="0;{SLOT / T:.5f}"'
        out.append(f'<clipPath id="c{i}"><rect x="{x0:.1f}" y="0" height="{H}" width="0"><animate attributeName="width" values="{wv}" keyTimes="{kt}" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
        out.append(f'<g opacity="0"><animate attributeName="opacity" {vis} calcMode="discrete" dur="{T}s" repeatCount="indefinite"/>'
                   f'<text x="{x0:.1f}" y="{H/2 + FS*0.36:.1f}" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#c{i})" '
                   f'font-family="Consolas, \'SFMono-Regular\', Menlo, \'DejaVu Sans Mono\', monospace" font-size="{FS}" font-weight="600" fill="#2f81f7">{html.escape(s, quote=False)}</text>'
                   f'<rect y="{H/2 - FS*0.55:.1f}" width="2.5" height="{FS*1.1:.1f}" fill="#2f81f7" x="{x0:.1f}">'
                   f'<animate attributeName="x" values="{cx}" keyTimes="{kt}" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/></rect></g>')
    out.append("</svg>")
    open(os.path.join(ROOT, "typing.svg"), "w", encoding="utf-8").write("\n".join(out))


print("particles:", banner())
typing()
print("ok")
