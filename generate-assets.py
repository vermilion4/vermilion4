"""Generate the themed SVG assets for the vermilion4 GitHub profile README.

Theme: AdaOS x neon-Tokyo night x game UI. Brand colours: black, maroon
#800000, crimson #C1121F. Every asset carries its own dark background so it
reads the same on GitHub light and dark mode. Animations are CSS inside the
SVG (GitHub keeps them when the SVG is shown as an image) and switch off under
prefers-reduced-motion.
"""
import os
import random
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)
os.makedirs(os.path.join(OUT, "achievements"), exist_ok=True)
os.makedirs(os.path.join(OUT, "sections"), exist_ok=True)

MONO = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
DISPLAY = "'Arial Black','Helvetica Neue',Arial,sans-serif"
JP = "'Hiragino Sans','Yu Gothic','Meiryo','Noto Sans JP','Noto Sans CJK JP',sans-serif"

CRIMSON = "#C1121F"
MAROON = "#800000"
INK = "#F2E9EA"
DIM = "#9C8C8F"

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(w, h, body, style="", defs="", label=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{esc(label)}">\n'
        f"<title>{esc(label)}</title>\n"
        f"<style>{style}{REDUCED}</style>\n<defs>{defs}</defs>\n{body}\n</svg>\n"
    )


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


GLOW_DEFS = """
<filter id="glow" x="-30%" y="-60%" width="160%" height="220%">
  <feGaussianBlur stdDeviation="5" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="softglow" x="-30%" y="-60%" width="160%" height="220%">
  <feGaussianBlur stdDeviation="2.2" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="2" fill="#000" opacity=".22"/>
</pattern>
"""


def frame(w, h, r=16, stroke=CRIMSON, op=0.55):
    """Outer border + corner brackets, game-HUD style."""
    b = 22
    s = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="none" stroke="{stroke}" stroke-opacity="{op}" stroke-width="2"/>'
    for x, y, dx, dy in [(10, 10, 1, 1), (w - 10, 10, -1, 1), (10, h - 10, 1, -1), (w - 10, h - 10, -1, -1)]:
        s += f'<path d="M{x} {y+dy*b} V{y} H{x+dx*b}" fill="none" stroke="{stroke}" stroke-width="3" stroke-linecap="square"/>'
    return s


# ---------------------------------------------------------------- skyline ---
def skyline(rng, w, base_y, layers, window_class="win"):
    """Two-layer city silhouette with lit windows. Returns svg markup."""
    out = []
    for li, (color, hmin, hmax, wmin, wmax, lit) in enumerate(layers):
        x = -10
        while x < w + 10:
            bw = rng.randint(wmin, wmax)
            bh = rng.randint(hmin, hmax)
            top = base_y - bh
            out.append(f'<rect x="{x}" y="{top}" width="{bw}" height="{bh+80}" fill="{color}"/>')
            if rng.random() < 0.25:  # antenna
                out.append(f'<rect x="{x+bw//2}" y="{top-14}" width="2" height="14" fill="{color}"/>')
            if lit:
                for wy in range(top + 8, base_y - 6, 11):
                    for wx in range(x + 5, x + bw - 6, 9):
                        if rng.random() < 0.18:
                            c = rng.choice(["#ffb347", "#ff6b6b", "#ffd9a0", "#ff3b4f"])
                            d = round(rng.uniform(0, 6), 2)
                            cls = window_class if rng.random() < 0.3 else ""
                            out.append(
                                f'<rect class="{cls}" style="animation-delay:{d}s" x="{wx}" y="{wy}" width="4" height="5" fill="{c}" opacity=".85"/>'
                            )
            x += bw + rng.randint(0, 3)
    return "\n".join(out)


def vsign(x, y, chars, color, size=22, delay=0):
    """Vertical neon sign with stacked Japanese characters."""
    h = len(chars) * (size + 6) + 14
    s = f'<g class="neon" style="animation-delay:{delay}s">'
    s += f'<rect x="{x}" y="{y}" width="{size+16}" height="{h}" rx="4" fill="#0a0306" stroke="{color}" stroke-width="2" filter="url(#softglow)"/>'
    for i, ch in enumerate(chars):
        s += (
            f'<text x="{x+(size+16)/2}" y="{y+12+(i+1)*(size+6)-6}" text-anchor="middle" font-family="{JP}" '
            f'font-size="{size}" font-weight="700" fill="{color}" filter="url(#softglow)">{ch}</text>'
        )
    return s + "</g>"


# ----------------------------------------------------------------- header ---
def header():
    W, H = 1000, 360
    rng = random.Random(7)
    stars = "".join(
        f'<circle class="tw" style="animation-delay:{rng.uniform(0,4):.2f}s" cx="{rng.randint(0,W)}" cy="{rng.randint(0,170)}" r="{rng.choice([.6,.9,1.2])}" fill="#fff" opacity=".7"/>'
        for _ in range(70)
    )
    # Synthwave sun with sliced bands
    sx, sy, sr = 760, 236, 118
    bands = "".join(
        f'<rect class="band" style="animation-delay:{-i*0.9:.1f}s" x="{sx-sr}" y="{sy+8+i*16}" width="{2*sr}" height="{3+i*1.4:.1f}" fill="#12040a"/>'
        for i in range(7)
    )
    rain = "".join(
        f'<line x1="{x}" y1="{y}" x2="{x-6}" y2="{y+22}" stroke="#ffb3bb" stroke-opacity=".22" stroke-width="1"/>'
        for x, y in ((rng.randint(0, W + 40), rng.randint(-60, H)) for _ in range(110))
    )
    far = skyline(rng, W, 300, [("#1d070d", 60, 150, 26, 60, False)])
    near = skyline(rng, W, 312, [("#0b0306", 40, 110, 22, 52, True)])
    defs = GLOW_DEFS + f"""
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#040208"/><stop offset=".55" stop-color="#1a0610"/><stop offset="1" stop-color="#4a0a14"/>
</linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffb199"/><stop offset=".45" stop-color="#ff4d5e"/><stop offset="1" stop-color="{MAROON}"/>
</linearGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#ff3b4f" stop-opacity=".55"/><stop offset="1" stop-color="#ff3b4f" stop-opacity="0"/></radialGradient>
<linearGradient id="shade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#040208" stop-opacity=".85"/><stop offset=".5" stop-color="#040208" stop-opacity=".55"/><stop offset=".62" stop-color="#040208" stop-opacity="0"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a0710"/><stop offset="1" stop-color="#050104"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="18"/></clipPath>
"""
    grid = "".join(
        f'<line x1="{W/2}" y1="312" x2="{W/2 + (i-10)*120}" y2="{H}" stroke="{CRIMSON}" stroke-opacity=".35"/>'
        for i in range(21)
    )
    grid += '<g class="floorlines">' + "".join(
        f'<line x1="0" y1="{312+o}" x2="{W}" y2="{312+o}" stroke="{CRIMSON}" stroke-opacity=".35"/>' for o in (6, 15, 28, 46)
    ) + "</g>"
    style = """
.tw{animation:tw 3.2s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}
.win{animation:win 5s steps(1) infinite}@keyframes win{0%,60%{opacity:.85}61%,80%{opacity:.1}81%{opacity:.85}}
.band{animation:band 6.3s linear infinite}@keyframes band{from{transform:translateY(0)}to{transform:translateY(-16px)}}
.rain{animation:rain .7s linear infinite}@keyframes rain{from{transform:translate(0,-40px)}to{transform:translate(-12px,40px)}}
.neon{animation:neon 4s infinite}@keyframes neon{0%,18%,22%,62%,64%,100%{opacity:1}20%,63%{opacity:.35}}
.title{animation:flick 6s infinite}@keyframes flick{0%,40%,44%,100%{opacity:1}42%{opacity:.55}}
.blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:.3}}
.pulse{animation:pulse 1.6s ease-in-out infinite}@keyframes pulse{50%{opacity:.25}}
"""
    body = f"""
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>
{stars}
<circle cx="{sx}" cy="{sy}" r="{sr+80}" fill="url(#sunglow)"/>
<circle cx="{sx}" cy="{sy}" r="{sr}" fill="url(#sun)"/>
{bands}
{far}
{near}
{vsign(600, 168, "開発者", "#ff3b4f", 18, 0)}
{vsign(905, 176, "エイダ", "#ffb347", 18, 1.3)}
<rect y="312" width="{W}" height="{H-312}" fill="url(#floor)"/>
{grid}
<rect width="{W}" height="312" fill="url(#shade)"/>
<g class="rain">{rain}</g>

<text x="56" y="48" font-family="{MONO}" font-size="13" fill="{DIM}" letter-spacing="2">AdaOS 2.0 <tspan fill="{CRIMSON}">▸</tspan> SYSTEM ONLINE <tspan class="pulse" fill="#4ade80">●</tspan></text>
<text x="944" y="48" text-anchor="end" font-family="{MONO}" font-size="13" fill="{DIM}" letter-spacing="2">1P <tspan fill="{CRIMSON}">♥ ♥ ♥</tspan>   HI-SCORE <tspan fill="{INK}">11 HACKATHONS</tspan></text>

<text x="54" y="104" font-family="{JP}" font-size="15" fill="#ff6b7a" letter-spacing="6" opacity=".9">フロントエンド・エンジニア</text>
<g class="title">
<text x="52" y="172" font-family="{DISPLAY}" font-size="66" font-weight="900" fill="{CRIMSON}" opacity=".7" filter="url(#glow)" letter-spacing="1">ADAEZE NDUPU</text>
<text x="52" y="172" font-family="{DISPLAY}" font-size="66" font-weight="900" fill="#fff4f4" letter-spacing="1">ADAEZE NDUPU</text>
</g>
<text x="56" y="206" font-family="{MONO}" font-size="16" fill="{INK}" letter-spacing="3">FRONTEND ENGINEER <tspan fill="{CRIMSON}">//</tspan> OTTAWA, CANADA</text>

<rect x="52" y="226" width="236" height="34" rx="4" fill="#0b0306" fill-opacity=".8" stroke="{CRIMSON}" stroke-opacity=".7"/>
<text class="blink" x="68" y="248" font-family="{MONO}" font-size="14" font-weight="700" fill="#fff" letter-spacing="3">▶ PRESS START</text>
<text x="300" y="248" font-family="{MONO}" font-size="13" fill="{DIM}" letter-spacing="1">adacoder.com</text>

<rect width="{W}" height="{H}" fill="url(#scan)"/>
</g>
{frame(W, H, 18)}
"""
    write(
        "header.svg",
        svg(W, H, body, style, defs, "Adaeze Ndupu, Frontend Engineer in Ottawa, Canada. Press start: adacoder.com"),
    )


# --------------------------------------------------------------- dialogue ---
def dialogue():
    W, H = 1000, 150
    lines = [
        ("Hi! I'm Ada, a frontend engineer at Appnigma.ai.", "I turn designs into pixel-perfect experiences."),
        ("Five years of React and Next.js in production,", "and lately I build with AI, not just around it."),
        ("11 hackathons and counting. One trophy so far.", "Always looking for the next quest. Team up?"),
        ("Off the clock: games, anime, and whatever", "I'm learning this week. (I learn fast.)"),
    ]
    n = len(lines)
    per = 100 / n
    style = ".cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:.3}}"
    groups = []
    for i, (a, b) in enumerate(lines):
        s, e = i * per, (i + 1) * per
        # visibility window for this page
        style += (
            f"@keyframes v{i}{{0%{{opacity:{1 if i == 0 else 0}}}"
            + (f"{s:.2f}%{{opacity:0}}{s+0.01:.2f}%{{opacity:1}}" if i else "")
            + f"{e-0.01:.2f}%{{opacity:1}}{e:.2f}%{{opacity:0}}100%{{opacity:0}}}}"
            f".p{i}{{animation:v{i} 22s infinite}}"
        )
        # typewriter covers: line a over first 30% of page, line b next 30%
        for j, (txt, row) in enumerate(((a, 0), (b, 1))):
            t0 = s + per * (0.02 + 0.32 * j)
            t1 = t0 + per * 0.3
            steps = max(len(txt), 1)
            style += (
                f"@keyframes t{i}{j}{{0%,{t0:.2f}%{{transform:translateX(0);animation-timing-function:steps({steps},end)}}"
                f"{t1:.2f}%,100%{{transform:translateX(900px)}}}}"
                f".c{i}{j}{{animation:t{i}{j} 22s infinite}}"
            )
        groups.append(
            f'<g class="p{i}">'
            f'<text x="60" y="82" font-family="{MONO}" font-size="19" fill="{INK}">{esc(a)}</text>'
            f'<text x="60" y="114" font-family="{MONO}" font-size="19" fill="{INK}">{esc(b)}</text>'
            f'<rect class="c{i}0" x="56" y="62" width="900" height="28" fill="#0d0709"/>'
            f'<rect class="c{i}1" x="56" y="94" width="900" height="28" fill="#0d0709"/>'
            f"</g>"
        )
    defs = GLOW_DEFS + '<clipPath id="tb"><rect x="44" y="56" width="880" height="72"/></clipPath>'
    body = f"""
<rect x="20" y="30" width="{W-40}" height="{H-44}" rx="10" fill="#0d0709" stroke="{CRIMSON}" stroke-width="2"/>
<rect x="26" y="36" width="{W-52}" height="{H-56}" rx="7" fill="none" stroke="{MAROON}" stroke-opacity=".8"/>
<g clip-path="url(#tb)">{''.join(groups)}</g>
<rect x="40" y="12" width="104" height="34" rx="5" fill="{CRIMSON}"/>
<text x="92" y="35" text-anchor="middle" font-family="{DISPLAY}" font-size="16" font-weight="900" fill="#fff" letter-spacing="3">ADA</text>
<text class="cur" x="948" y="128" text-anchor="end" font-family="{MONO}" font-size="16" fill="{CRIMSON}">▼</text>
"""
    label = " ".join(" ".join(p) for p in lines)
    write("dialogue.svg", svg(W, H, body, style, defs, label))


# ------------------------------------------------------------ player card ---
def player_card():
    W, H = 1000, 400
    stats = [("FRONTEND", 10), ("UI POLISH", 9), ("AI BUILDS", 8), ("TECH WRITING", 7), ("GAMING", 9), ("ANIME LORE", 10)]
    info = [("NAME", "Adaeze Ndupu"), ("CLASS", "Frontend Engineer"), ("GUILD", "Appnigma.ai"), ("REGION", "Ottawa, Canada"), ("LEVEL", "5+ years in production")]
    style = """
.ring{transform-origin:170px 168px;animation:spin 18s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
.ring2{transform-origin:170px 168px;animation:spin 26s linear infinite reverse}
.seg{opacity:0;animation:fill .25s ease-out forwards}@keyframes fill{to{opacity:1}}
.pulse{animation:pulse 1.6s ease-in-out infinite}@keyframes pulse{50%{opacity:.25}}
"""
    defs = GLOW_DEFS + f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14070b"/><stop offset="1" stop-color="#070305"/></linearGradient>
<linearGradient id="hex" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CRIMSON}"/><stop offset="1" stop-color="#2a0308"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>
"""
    cx, cy, r = 170, 168, 92
    import math
    hexpts = " ".join(f"{cx + r*math.cos(math.radians(60*i-90)):.1f},{cy + r*math.sin(math.radians(60*i-90)):.1f}" for i in range(6))
    hexpts2 = " ".join(f"{cx + (r-10)*math.cos(math.radians(60*i-90)):.1f},{cy + (r-10)*math.sin(math.radians(60*i-90)):.1f}" for i in range(6))
    left = f"""
<circle class="ring" cx="{cx}" cy="{cy}" r="{r+22}" fill="none" stroke="{CRIMSON}" stroke-width="2" stroke-dasharray="6 10" opacity=".8"/>
<circle class="ring2" cx="{cx}" cy="{cy}" r="{r+34}" fill="none" stroke="{MAROON}" stroke-width="1.5" stroke-dasharray="40 14 4 14" opacity=".9"/>
<polygon points="{hexpts}" fill="url(#hex)" filter="url(#softglow)"/>
<polygon points="{hexpts2}" fill="#0b0306" stroke="#ff6b7a" stroke-opacity=".5"/>
<text x="{cx}" y="{cy+22}" text-anchor="middle" font-family="{DISPLAY}" font-size="62" font-weight="900" fill="#fff" letter-spacing="2">AN</text>
<text x="{cx}" y="{cy-34}" text-anchor="middle" font-family="{JP}" font-size="13" fill="#ff8a95" letter-spacing="4">エイダ</text>
<rect x="{cx-62}" y="306" width="124" height="30" rx="15" fill="{CRIMSON}"/>
<text x="{cx}" y="327" text-anchor="middle" font-family="{DISPLAY}" font-size="15" font-weight="900" fill="#fff" letter-spacing="2">LV. 5+</text>
<text x="{cx}" y="364" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="2"><tspan class="pulse" fill="#4ade80">●</tspan> ONLINE · PARTY OPEN</text>
"""
    mid = f'<text x="340" y="62" font-family="{MONO}" font-size="12" fill="{CRIMSON}" letter-spacing="4">PLAYER 1 ▸ STATUS</text>'
    for i, (k, v) in enumerate(info):
        y = 104 + i * 40
        mid += (
            f'<text x="340" y="{y}" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="3">{k}</text>'
            f'<text x="438" y="{y}" font-family="{SANS}" font-size="18" font-weight="700" fill="{INK}">{esc(v)}</text>'
            f'<line x1="340" y1="{y+14}" x2="620" y2="{y+14}" stroke="#ffffff" stroke-opacity=".06"/>'
        )
    mid += (
        f'<text x="340" y="326" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="3">SPECIAL MOVES</text>'
        f'<text x="340" y="350" font-family="{SANS}" font-size="14" fill="{INK}">Pixel-perfect UI · AI-native products ·</text>'
        f'<text x="340" y="370" font-family="{SANS}" font-size="14" fill="{INK}">Technical writing (OpenReplay, Hashnode)</text>'
    )
    right = f'<text x="664" y="62" font-family="{MONO}" font-size="12" fill="{CRIMSON}" letter-spacing="4">ATTRIBUTES</text>'
    d = 0.3
    for i, (k, v) in enumerate(stats):
        y = 100 + i * 46
        right += f'<text x="664" y="{y}" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="2">{k}</text>'
        right += f'<text x="944" y="{y}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{INK}">{"MAX" if v == 10 else f"{v}/10"}</text>'
        for s in range(10):
            x = 664 + s * 28
            right += f'<rect x="{x}" y="{y+8}" width="24" height="12" rx="2" fill="#ffffff" fill-opacity=".07"/>'
            if s < v:
                col = CRIMSON if v < 10 else "#ff4d5e"
                right += f'<rect class="seg" style="animation-delay:{d:.2f}s" x="{x}" y="{y+8}" width="24" height="12" rx="2" fill="{col}"/>'
                d += 0.035
    body = f"""
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{left}{mid}{right}
<line x1="316" y1="40" x2="316" y2="370" stroke="{CRIMSON}" stroke-opacity=".25"/>
<line x1="644" y1="40" x2="644" y2="370" stroke="{CRIMSON}" stroke-opacity=".25"/>
<rect width="{W}" height="{H}" fill="url(#scan)" opacity=".5"/>
</g>
{frame(W, H, 16)}
"""
    label = "Player 1: Adaeze Ndupu. Class: Frontend Engineer. Guild: Appnigma.ai. Region: Ottawa, Canada. Level: 5+ years in production. Attributes: frontend max, UI polish 9, AI builds 8, technical writing 7, gaming 9, anime lore max."
    write("player-card.svg", svg(W, H, body, style, defs, label))


# -------------------------------------------------------------- quest log ---
def quest_log():
    quests = [
        ("ACTIVE", "Appnigma.ai", "Frontend Engineer", "Sep 2025 — now",
         "Own the frontend: self-serve onboarding, Dev Hub connections, and an AI chat that builds Salesforce projects."),
        ("CLEARED", "Sonnul", "Frontend Engineer", "Mar 2024 — Sep 2025",
         "Built the drag-and-drop Salesforce builder and gen-AI chat that grew into Appnigma.ai."),
        ("CLEARED", "Funtech AI · Code Funhouse", "Lead Frontend Developer", "Oct 2023 — May 2026",
         "Moved React to Next.js, built Blockly coding for kids, gamified learning maps, parent payments."),
        ("CLEARED", "Warehöuzit", "Lead Frontend Developer", "Nov 2022 — Sep 2023",
         "Responsive React and Next.js interfaces, code reviews and QA with the design team."),
    ]
    W, row = 1000, 92
    H = 70 + row * len(quests) + 20
    style = """
.act{animation:act 1.8s ease-in-out infinite}@keyframes act{50%{opacity:.45}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 1.8s ease-out infinite}@keyframes ping{from{transform:scale(1);opacity:.8}to{transform:scale(2.6);opacity:0}}
"""
    defs = GLOW_DEFS + f'<clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
    rows = ""
    for i, (st, co, role, per, note) in enumerate(quests):
        y = 70 + i * row
        active = st == "ACTIVE"
        dot = (
            f'<circle class="ping" cx="62" cy="{y+28}" r="8" fill="{CRIMSON}"/><circle cx="62" cy="{y+28}" r="8" fill="{CRIMSON}"/>'
            if active
            else f'<circle cx="62" cy="{y+28}" r="7" fill="#0b0306" stroke="{MAROON}" stroke-width="2"/><path d="M58 {y+28} l3 3 l5 -6" stroke="#ff8a95" stroke-width="2" fill="none"/>'
        )
        badge_fill = CRIMSON if active else "#2a0b11"
        badge_txt = "#fff" if active else "#ff8a95"
        rows += f"""
{dot}
<rect class="{'act' if active else ''}" x="92" y="{y+14}" width="{82 if active else 90}" height="24" rx="4" fill="{badge_fill}"/>
<text x="{133 if active else 137}" y="{y+31}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{badge_txt}" letter-spacing="2">{st}</text>
<text x="196" y="{y+33}" font-family="{SANS}" font-size="20" font-weight="700" fill="{INK}">{esc(co)}</text>
<text x="944" y="{y+33}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{DIM}">{esc(per)}</text>
<text x="196" y="{y+58}" font-family="{MONO}" font-size="13" fill="#ff8a95" letter-spacing="1">{esc(role.upper())}</text>
<text x="196" y="{y+80}" font-family="{SANS}" font-size="14.5" fill="#cbbfc1">{esc(note)}</text>
"""
    line = f'<line x1="62" y1="{70+28}" x2="62" y2="{70+row*(len(quests)-1)+28}" stroke="{MAROON}" stroke-width="2" stroke-dasharray="3 5"/>'
    body = f"""
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="#0a0507"/>
<text x="980" y="{H-14}" text-anchor="end" font-family="{JP}" font-size="96" font-weight="900" fill="#ffffff" fill-opacity=".025">クエスト</text>
<text x="40" y="44" font-family="{MONO}" font-size="12" fill="{CRIMSON}" letter-spacing="4">QUEST LOG ▸ CAREER MODE</text>
<text x="960" y="44" text-anchor="end" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="2">1 ACTIVE · 3 CLEARED</text>
{line}{rows}
<rect width="{W}" height="{H}" fill="url(#scan)" opacity=".4"/>
</g>
{frame(W, H, 16)}
"""
    label = "Quest log. " + " ".join(f"{st}: {co}, {role}, {per}. {note}" for st, co, role, per, note in quests)
    write("quest-log.svg", svg(W, H, body, style, defs, label))


# ------------------------------------------------------------------ cards ---
CARDS = [
    dict(id="appnigma", no=1, rarity="SSR", stars=5, kind="MAIN QUEST · WORK", glyph="⚡", name="Appnigma AI",
         c1="#1f2937", c2="#0b0f19", glow="#ff3b4f",
         lines=["The platform I build at work: an AI", "chat that assembles a working", "Salesforce project, plus self-serve", "AppExchange onboarding."],
         chips=["Next.js", "Salesforce", "Gen AI"]),
    dict(id="handovr", no=2, rarity="SR", stars=4, kind="HACKATHON · PAYPAL AI", glyph="💸", name="Handovr AI",
         c1="#0f3d2e", c2="#06190f", glow="#4ade80",
         lines=["Payment that releases when the", "work passes. Claude tests the site", "in a real browser against signed", "checks, then PayPal pays out."],
         chips=["Next.js", "PayPal", "Postgres"]),
    dict(id="inkswap", no=3, rarity="SR", stars=4, kind="HACKATHON · BUILD WITH AI", glyph="🖋️", name="InkSwap",
         c1="#3b2a52", c2="#1b1424", glow="#c084fc",
         lines=["Chrome extension that translates", "raw manga where you read it, by", "meaning, and re-letters each line", "to fit its speech bubble."],
         chips=["TypeScript", "WXT", "Claude"]),
    dict(id="couchconsensus", no=4, rarity="SR", stars=4, kind="HACKATHON · AMAZON DEV", glyph="🛋️", name="CouchConsensus",
         c1="#1A2740", c2="#0E1626", glow="#38bdf8",
         lines=["Ends “what should we watch?” in", "under three minutes. A Fire TV app,", "everyone swipes on their phone,", "the TV announces one pick."],
         chips=["React Native", "Bedrock", "WebSockets"]),
    dict(id="minxx", no=5, rarity="SR", stars=4, kind="CLIENT · E-COMMERCE", glyph="💄", name="Minxx Club",
         c1="#5a1438", c2="#23081a", glow="#f472b6",
         lines=["Production store for a luxury lash", "and beauty brand, with an AI", "shopping assistant and real-time", "virtual try-on."],
         chips=["Next.js", "Sanity", "Stripe"]),
    dict(id="codefunhouse", no=6, rarity="SR", stars=4, kind="CLIENT · ED-TECH", glyph="🧩", name="Code Funhouse",
         c1="#7b2ff7", c2="#2e1065", glow="#a78bfa",
         lines=["Kids learn to code with AI tutors:", "an in-browser sandbox, block-based", "coding, gamified learning maps and", "subscription billing."],
         chips=["Next.js", "Sanity", "Blockly"]),
]


def card(c):
    W, H = 320, 470
    style = """
.holo{animation:holo 5s ease-in-out infinite}@keyframes holo{0%,55%{transform:translateX(-420px)}100%{transform:translateX(420px)}}
.float{animation:float 4s ease-in-out infinite}@keyframes float{50%{transform:translateY(-6px)}}
.star{animation:star 2.4s ease-in-out infinite}@keyframes star{50%{opacity:.45}}
"""
    defs = GLOW_DEFS + f"""
<linearGradient id="art" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['c1']}"/><stop offset="1" stop-color="{c['c2']}"/></linearGradient>
<radialGradient id="aura" cx=".5" cy=".55" r=".5"><stop offset="0" stop-color="{c['glow']}" stop-opacity=".55"/><stop offset="1" stop-color="{c['glow']}" stop-opacity="0"/></radialGradient>
<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['glow']}"/><stop offset=".5" stop-color="{CRIMSON}"/><stop offset="1" stop-color="{c['glow']}"/></linearGradient>
<pattern id="dots" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#fff" opacity=".09"/></pattern>
<clipPath id="cc"><rect x="6" y="6" width="{W-12}" height="{H-12}" rx="14"/></clipPath>
<clipPath id="ac"><rect x="20" y="56" width="{W-40}" height="196" rx="8"/></clipPath>
"""
    stars = "".join(
        f'<text class="star" style="animation-delay:{i*0.2:.1f}s" x="{W-26-i*17}" y="38" text-anchor="end" font-size="15" fill="#ffd166">★</text>'
        for i in range(c["stars"])
    )
    chips, cx = "", 22
    for ch in c["chips"]:
        w = 14 + len(ch) * 7.4
        chips += (
            f'<rect x="{cx}" y="{H-62}" width="{w:.0f}" height="24" rx="12" fill="#ffffff" fill-opacity=".08" stroke="{c["glow"]}" stroke-opacity=".6"/>'
            f'<text x="{cx + w/2:.1f}" y="{H-45}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{INK}">{esc(ch)}</text>'
        )
        cx += w + 8
    tag = "".join(
        f'<text x="22" y="{332+i*21}" font-family="{SANS}" font-size="14" fill="#d9cdd0">{esc(l)}</text>'
        for i, l in enumerate(c["lines"])
    )
    body = f"""
<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="18" fill="url(#edge)"/>
<g clip-path="url(#cc)">
<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="#0c0709"/>
<rect x="20" y="20" width="{50 if c['rarity']=='SR' else 58}" height="24" rx="4" fill="{CRIMSON if c['rarity']=='SSR' else '#2a0b11'}" stroke="#ffd166" stroke-opacity="{.9 if c['rarity']=='SSR' else .4}"/>
<text x="{45 if c['rarity']=='SR' else 49}" y="37" text-anchor="middle" font-family="{DISPLAY}" font-size="13" font-weight="900" fill="#ffd166" letter-spacing="1">{c['rarity']}</text>
{stars}
<g clip-path="url(#ac)">
<rect x="20" y="56" width="{W-40}" height="196" fill="url(#art)"/>
<rect x="20" y="56" width="{W-40}" height="196" fill="url(#dots)"/>
<circle cx="{W/2}" cy="158" r="110" fill="url(#aura)"/>
<text class="float" x="{W/2}" y="186" text-anchor="middle" font-size="84">{c['glyph']}</text>
<text x="34" y="242" font-family="{MONO}" font-size="11" fill="#fff" fill-opacity=".55" letter-spacing="2">No.{c['no']:03d}/006</text>
</g>
<rect x="20" y="56" width="{W-40}" height="196" rx="8" fill="none" stroke="#fff" stroke-opacity=".12"/>
<text x="22" y="282" font-family="{MONO}" font-size="11" fill="{c['glow']}" letter-spacing="2">{esc(c['kind'])}</text>
<text x="22" y="309" font-family="{SANS}" font-size="23" font-weight="800" fill="#fff">{esc(c['name'])}</text>
{tag}
{chips}
<rect class="holo" x="-120" y="0" width="160" height="{H}" fill="url(#shine)" transform="skewX(-18)"/>
</g>
"""
    label = f"{c['name']} ({c['kind'].title()}): {' '.join(c['lines'])} Built with {', '.join(c['chips'])}."
    write(f"cards/{c['id']}.svg", svg(W, H, body, style, defs, label))


# ----------------------------------------------------------- achievements ---
ACH = [
    dict(id="medbot", gold=True, title="Best Overall Project", sub="MedBot AI · CodeEDU: SpringHacks 2024", score=100, tier="LEGENDARY"),
    dict(id="handovr", title="Escrow, But Make It AI", sub="Handovr AI · PayPal AI Hackathon", score=50, tier="SHIPPED"),
    dict(id="couchconsensus", title="Couch Diplomat", sub="CouchConsensus · Amazon Developer Hackathon", score=50, tier="SHIPPED"),
    dict(id="inkswap", title="Lost in Translation? Never.", sub="InkSwap · Build With AI: Basics", score=50, tier="SHIPPED"),
    dict(id="dealflow", title="Four Agents, One Email", sub="DealFlow · Airia AI Agents Hackathon", score=50, tier="SHIPPED"),
    dict(id="shipsafe", title="Merge With Confidence", sub="ShipSafe · GitLab AI Hackathon", score=50, tier="SHIPPED"),
]


def achievement(a):
    W, H = 490, 104
    gold = a.get("gold")
    main = "#ffd166" if gold else CRIMSON
    style = """
.shine{animation:sh 4.5s ease-in-out infinite}@keyframes sh{0%,60%{transform:translateX(-200px)}100%{transform:translateX(700px)}}
.spin{transform-origin:52px 52px;animation:spin 10s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
"""
    defs = GLOW_DEFS + f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{'#2a1d05' if gold else '#1c070c'}"/><stop offset="1" stop-color="#0a0507"/></linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="52"/></clipPath>
"""
    # trophy glyph drawn as paths so it never depends on emoji fonts
    trophy = (
        f'<path d="M40 34 h24 v10 a12 12 0 0 1 -24 0 z" fill="{main}"/>'
        f'<path d="M40 37 h-6 a6 6 0 0 0 6 10 M64 37 h6 a6 6 0 0 1 -6 10" stroke="{main}" stroke-width="3" fill="none"/>'
        f'<rect x="49" y="55" width="6" height="8" fill="{main}"/><rect x="42" y="63" width="20" height="6" rx="2" fill="{main}"/>'
    )
    body = f"""
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle cx="52" cy="52" r="36" fill="#0a0507" stroke="{main}" stroke-width="3" {'filter="url(#softglow)"' if gold else ''}/>
<circle class="spin" cx="52" cy="52" r="43" fill="none" stroke="{main}" stroke-opacity=".5" stroke-dasharray="4 8"/>
{trophy}
<text x="106" y="34" font-family="{MONO}" font-size="11" fill="{main}" letter-spacing="3">ACHIEVEMENT UNLOCKED · {a['tier']}</text>
<text x="106" y="62" font-family="{SANS}" font-size="19" font-weight="800" fill="#fff">{esc(a['title'])}</text>
<text x="106" y="84" font-family="{SANS}" font-size="13" fill="#bfb2b5">{esc(a['sub'])}</text>
<text x="{W-26}" y="34" text-anchor="end" font-family="{DISPLAY}" font-size="13" font-weight="900" fill="{main}">G {a['score']}</text>
<rect class="shine" x="0" y="0" width="120" height="{H}" fill="url(#sh)" transform="skewX(-20)"/>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="52" fill="none" stroke="{main}" stroke-opacity="{.85 if gold else .45}" stroke-width="2"/>
"""
    write(f"achievements/{a['id']}.svg", svg(W, H, body, style, defs, f"Achievement unlocked: {a['title']}. {a['sub']}"))


# ------------------------------------------------------- section headers ---
SECTIONS = [
    ("profile", "01", "PLAYER PROFILE", "プロフィール"),
    ("quests", "02", "QUEST LOG", "クエスト"),
    ("loadout", "03", "LOADOUT", "そうび"),
    ("collection", "04", "CARD COLLECTION", "コレクション"),
    ("achievements", "05", "ACHIEVEMENTS", "じっせき"),
    ("save", "06", "SAVE DATA", "セーブデータ"),
    ("warp", "07", "WARP ZONE", "ワープ"),
]


def section(sid, num, title, jp):
    W, H = 1000, 64
    tw = len(title) * 17.8
    x_jp = 112 + tw + 18
    cs = int(x_jp + len(jp) * 17 + 24)
    style = ".cur{animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}.run{animation:run 3s linear infinite}@keyframes run{from{transform:translateX(0)}to{transform:translateX(24px)}}"
    defs = GLOW_DEFS + f"""
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CRIMSON}"/><stop offset="1" stop-color="{CRIMSON}" stop-opacity="0"/></linearGradient>
<pattern id="chev" width="24" height="16" patternUnits="userSpaceOnUse"><path d="M4 2 l8 6 l-8 6" stroke="{CRIMSON}" stroke-opacity=".35" stroke-width="2" fill="none"/></pattern>
<clipPath id="cl"><rect x="{cs}" y="22" width="{W-cs-40}" height="20"/></clipPath>
"""
    body = f"""
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="#0b0608" stroke="{CRIMSON}" stroke-opacity=".35"/>
<rect x="14" y="13" width="66" height="38" rx="6" fill="{CRIMSON}"/>
<text x="47" y="40" text-anchor="middle" font-family="{DISPLAY}" font-size="20" font-weight="900" fill="#fff">{num}</text>
<text x="100" y="41" font-family="{DISPLAY}" font-size="23" font-weight="900" fill="#fff" letter-spacing="2">{esc(title)}</text>
<text x="{x_jp}" y="40" font-family="{JP}" font-size="14" fill="#ff8a95" letter-spacing="3">{jp}</text>
<g clip-path="url(#cl)"><rect class="run" x="{cs-24}" y="22" width="{W}" height="20" fill="url(#chev)"/></g>
<text class="cur" x="{W-22}" y="40" text-anchor="end" font-family="{MONO}" font-size="16" fill="{CRIMSON}">■</text>
"""
    write(f"sections/{sid}.svg", svg(W, H, body, style, defs, f"{num} {title}"))


# ----------------------------------------------------------------- footer ---
def footer():
    W, H = 1000, 230
    rng = random.Random(3)
    city = skyline(rng, W, H, [("#1d070d", 30, 80, 24, 50, False), ("#0b0306", 18, 52, 20, 44, True)])
    n = 10
    style = """
.win{animation:win 5s steps(1) infinite}@keyframes win{0%,60%{opacity:.85}61%,80%{opacity:.1}81%{opacity:.85}}
.blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:.3}}
"""
    digits = ""
    for i in range(n):
        s, e = i * 10, (i + 1) * 10
        style += f"@keyframes d{i}{{0%{{opacity:{1 if i==0 else 0}}}" + (f"{s-0.01:.2f}%{{opacity:0}}{s}%{{opacity:1}}" if i else "") + f"{e-0.01:.2f}%{{opacity:1}}{e}%,100%{{opacity:0}}}}.d{i}{{animation:d{i} 10s infinite}}"
        digits += f'<text class="d{i}" x="660" y="132" font-family="{DISPLAY}" font-size="40" font-weight="900" fill="{CRIMSON}" filter="url(#softglow)">{9-i}</text>'
    defs = GLOW_DEFS + f"""
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050206"/><stop offset="1" stop-color="#3a0812"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="18"/></clipPath>
"""
    body = f"""
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{city}
<text x="{W/2}" y="70" text-anchor="middle" font-family="{DISPLAY}" font-size="38" font-weight="900" fill="{CRIMSON}" opacity=".7" filter="url(#glow)" letter-spacing="4">THANKS FOR PLAYING</text>
<text x="{W/2}" y="70" text-anchor="middle" font-family="{DISPLAY}" font-size="38" font-weight="900" fill="#fff4f4" letter-spacing="4">THANKS FOR PLAYING</text>
<text x="640" y="132" text-anchor="end" font-family="{MONO}" font-size="22" font-weight="700" fill="{INK}" letter-spacing="4">CONTINUE?</text>
{digits}
<text class="blink" x="{W/2}" y="170" text-anchor="middle" font-family="{MONO}" font-size="15" fill="#fff" letter-spacing="3">▶ YES  —  adacoder.com</text>
<rect width="{W}" height="{H}" fill="url(#scan)"/>
</g>
{frame(W, H, 18)}
"""
    write("footer.svg", svg(W, H, body, style, defs, "Thanks for playing. Continue? adacoder.com"))


if __name__ == "__main__":
    header()
    dialogue()
    player_card()
    quest_log()
    for c in CARDS:
        card(c)
    for a in ACH:
        achievement(a)
    for s in SECTIONS:
        section(*s)
    footer()
    print("ok")
