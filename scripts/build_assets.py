"""Builds the static SVGs in assets/. Run: python3 scripts/build_assets.py"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
random.seed(24)

FONT = "font-family: 'Hiragino Maru Gothic ProN', 'M PLUS Rounded 1c', 'Nunito', 'Yu Gothic', 'PingFang SC', system-ui, sans-serif;"
SKY = '''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0b1030"/><stop offset=".55" stop-color="#2a1d5c"/><stop offset="1" stop-color="#5b3a7a"/>
    </linearGradient>'''
GLOW = '''<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>'''
STAR_CSS = '''
    .tw { animation: tw 3s ease-in-out infinite; }
    @keyframes tw { 0%, 100% { opacity: .25; } 50% { opacity: 1; } }'''


def stars(n, w, h, big=0.15):
    out = []
    for _ in range(n):
        x, y = random.uniform(0, w), random.uniform(0, h)
        d = random.uniform(-3, 0)
        if random.random() < big:
            s = random.uniform(3, 5)
            out.append(f'<path class="tw" style="animation-delay:{d:.2f}s" fill="#fff4d6" d="M{x:.0f} {y-s:.1f} Q{x:.0f} {y:.0f} {x+s:.1f} {y:.0f} Q{x:.0f} {y:.0f} {x:.0f} {y+s:.1f} Q{x:.0f} {y:.0f} {x-s:.1f} {y:.0f} Q{x:.0f} {y:.0f} {x:.0f} {y-s:.1f}Z"/>')
        else:
            out.append(f'<circle class="tw" style="animation-delay:{d:.2f}s" cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(.6, 1.6):.1f}" fill="#fff"/>')
    return "".join(out)


def petals(n, w, h):
    out = []
    for i in range(n):
        x = random.uniform(0, w)
        dur = random.uniform(9, 15)
        out.append(
            f'<g class="fall" style="--x:{random.uniform(-80, 80):.0f}px;animation-duration:{dur:.1f}s;animation-delay:{-random.uniform(0, dur):.1f}s">'
            f'<path class="spin" style="animation-duration:{random.uniform(2, 4):.1f}s" transform="translate({x:.0f} -20)" '
            f'fill="#ffb7c5" opacity=".85" d="M0 -6 C5 -6 7 0 0 7 C-7 0 -5 -6 0 -6 Z"/></g>')
    return "".join(out)


PETAL_CSS = lambda h: f'''
    .fall {{ animation: fall linear infinite; }}
    @keyframes fall {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(var(--x), {h + 40}px); }} }}
    .spin {{ transform-box: fill-box; transform-origin: center; animation: spin linear infinite; }}
    @keyframes spin {{ to {{ rotate: 360deg; }} }}'''


def header():
    W, H = 1000, 320
    mx, my, mr = 740, 150, 112
    craters = "".join(
        f'<circle cx="{mx+dx}" cy="{my+dy}" r="{r}" fill="#f1dcae" opacity=".55"/>'
        for dx, dy, r in [(-40, -30, 18), (30, 10, 24), (-10, 50, 12), (50, -50, 10), (-60, 30, 8)])
    # Two figures on the hill, one with long hair blowing in the wind.
    people = '''
      <g fill="#140d2e">
        <circle cx="718" cy="214" r="9"/>
        <path d="M708 224 Q718 219 728 224 L731 262 L705 262 Z"/>
        <path d="M727 232 Q737 238 744 240" stroke="#140d2e" stroke-width="5" stroke-linecap="round" fill="none"/>
        <circle cx="756" cy="218" r="8.5"/>
        <path class="hair" d="M749 214 Q756 206 764 213 Q768 232 790 246 Q772 248 760 238 Q752 232 749 214 Z"/>
        <path d="M747 228 Q756 223 765 228 L772 262 L740 262 Z"/>
      </g>'''
    shoot = '''<g class="shoot"><line x1="0" y1="0" x2="90" y2="0" stroke="url(#sh)" stroke-width="2" stroke-linecap="round"/></g>'''
    clouds = "".join(
        f'<g class="cloud" style="animation-duration:{d}s;animation-delay:-{d*o:.0f}s"><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx*.28:.0f}" fill="#b89be0" opacity="{op}"/>'
        f'<ellipse cx="{x+rx*.4:.0f}" cy="{y-rx*.12:.0f}" rx="{rx*.5:.0f}" ry="{rx*.22:.0f}" fill="#b89be0" opacity="{op}"/></g>'
        for x, y, rx, op, d, o in [(200, 250, 120, .18, 70, .1), (600, 200, 90, .14, 90, .5), (900, 280, 140, .2, 80, .8)])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    {SKY}
    {GLOW}
    <radialGradient id="halo"><stop offset=".55" stop-color="#fff1c9" stop-opacity=".5"/><stop offset="1" stop-color="#fff1c9" stop-opacity="0"/></radialGradient>
    <radialGradient id="moon" cx="40%" cy="35%"><stop offset="0" stop-color="#fffaf0"/><stop offset="1" stop-color="#f7e6bd"/></radialGradient>
    <linearGradient id="title" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd1dc"/><stop offset=".5" stop-color="#ff9ec0"/><stop offset="1" stop-color="#c8b6ff"/></linearGradient>
    <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
    <clipPath id="c"><rect width="{W}" height="{H}" rx="24"/></clipPath>
  </defs>
  <style>
    text {{ {FONT} }}
    .t {{ font-size: 104px; font-weight: 800; letter-spacing: 4px; }}
    .jp {{ font-size: 28px; font-weight: 700; fill: #fff4d6; letter-spacing: 4px; }}
    .en {{ font-size: 16px; fill: #d9ccff; letter-spacing: 2px; }}
    .halo {{ transform-origin: {mx}px {my}px; animation: breathe 6s ease-in-out infinite; }}
    @keyframes breathe {{ 50% {{ transform: scale(1.06); opacity: .8; }} }}
    .shoot {{ animation: shoot 7s ease-in infinite; opacity: 0; }}
    @keyframes shoot {{ 0% {{ transform: translate(80px, 20px) rotate(-155deg); opacity: 0; }} 3% {{ opacity: 1; }}
      12% {{ transform: translate(-160px, 130px) rotate(-155deg); opacity: 0; }} 100% {{ opacity: 0; }} }}
    .cloud {{ animation: drift linear infinite; }}
    @keyframes drift {{ from {{ transform: translateX(-300px); }} to {{ transform: translateX(1100px); }} }}
    .hair {{ transform-origin: 756px 214px; animation: wind 3s ease-in-out infinite; }}
    @keyframes wind {{ 50% {{ transform: rotate(-4deg); }} }}
    .bob {{ animation: bob 4s ease-in-out infinite; }}
    @keyframes bob {{ 50% {{ transform: translateY(-5px); }} }}{STAR_CSS}{PETAL_CSS(H)}
  </style>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="url(#sky)"/>
    {stars(90, W, 240)}
    <g transform="translate(780 40)">{shoot}</g>
    <circle cx="{mx}" cy="{my}" r="{mr*1.6:.0f}" fill="url(#halo)" class="halo"/>
    <circle cx="{mx}" cy="{my}" r="{mr}" fill="url(#moon)"/>
    {craters}
    {clouds}
    <path d="M520 {H} Q640 255 760 262 Q900 268 1000 240 L1000 {H} Z" fill="#1c1240"/>
    <path d="M0 {H} Q180 270 420 290 Q520 298 620 {H} Z" fill="#23174d"/>
    {people}
    <g class="bob">
      <text x="56" y="160" class="t" fill="url(#title)" filter="url(#glow)">GA24</text>
      <path class="tw" fill="#fff4d6" d="M318 72 Q320 84 332 86 Q320 88 318 100 Q316 88 304 86 Q316 84 318 72Z"/>
      <path class="tw" style="animation-delay:-1.5s" fill="#ffb7c5" d="M40 70 Q41 77 48 78 Q41 79 40 86 Q39 79 32 78 Q39 77 40 70Z"/>
    </g>
    <text x="60" y="210" class="jp">とにかく、つくる。</text>
    <text x="62" y="244" class="en">tools, decks &amp; odd visual machines</text>
    {petals(14, W, H)}
  </g>
</svg>
'''


def about():
    rows = [("speaks", "中文 · deutsch · english"), ("writes", "python · typescript · swift · lua"),
            ("building", "pptxforge, selfobserver, phosphor-lab, shelfi"), ("habit", "every school presentation becomes a web app"),
            ("fav anime", "tonikawa: over the moon for you ☾")]
    top, lh = 108, 36
    H = top + len(rows) * lh + 10
    items = "".join(
        f'<g class="r" style="animation-delay:{.2 + i*.12:.2f}s"><circle cx="46" cy="{top + i*lh - 5}" r="3" fill="#ffb7c5"/>'
        f'<text x="62" y="{top + i*lh}" class="k">{k}</text><text x="220" y="{top + i*lh}" class="v">{v}</text></g>'
        for i, (k, v) in enumerate(rows))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {H}" width="1000" height="{H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#171236"/><stop offset="1" stop-color="#2b1b4f"/></linearGradient>
    <clipPath id="c"><rect width="1000" height="{H}" rx="20"/></clipPath>
  </defs>
  <style>
    text {{ {FONT} }}
    .h {{ font-size: 15px; font-weight: 800; fill: #ffb7c5; letter-spacing: 4px; }}
    .s {{ font-size: 14px; fill: #a99bd6; }}
    .k {{ font-size: 15px; fill: #a99bd6; }}
    .v {{ font-size: 15px; fill: #fff4d6; }}
    .r {{ opacity: 0; animation: in .6s ease-out forwards; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}{STAR_CSS}{PETAL_CSS(H)}
  </style>
  <g clip-path="url(#c)">
    <rect width="1000" height="{H}" fill="url(#bg)"/>
    {stars(30, 1000, H, big=.1)}
    <circle cx="940" cy="{H-30}" r="70" fill="#fff4d6" opacity=".07"/>
    <circle cx="940" cy="{H-30}" r="42" fill="#fff4d6" opacity=".09"/>
    <text x="40" y="52" class="h">ABOUT ME</text>
    <text x="960" y="52" class="s" text-anchor="end">student · builder · moon enjoyer</text>
    <line x1="40" y1="72" x2="960" y2="72" stroke="#ffb7c5" stroke-opacity=".25" stroke-dasharray="2 6" stroke-linecap="round"/>
    {items}
    {petals(6, 1000, H)}
  </g>
  <rect x="1" y="1" width="998" height="{H-2}" rx="19" fill="none" stroke="#ffb7c5" stroke-opacity=".3" stroke-width="1.5"/>
</svg>
'''


def card(name, lines, tags, meta, art_css, art):
    desc = "".join(f'<text x="26" y="{96+i*20}" class="d">{l}</text>' for i, l in enumerate(lines))
    x, chips = 26, []
    for t in tags:
        w = len(t) * 7.4 + 20
        chips.append(f'<rect x="{x}" y="180" width="{w:.0f}" height="26" rx="13" fill="#ffb7c5" fill-opacity=".12" stroke="#ffb7c5" stroke-opacity=".4"/><text x="{x+10}" y="197" class="g">{t}</text>')
        x += w + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 490 230" width="490" height="230">
  <defs>
    {SKY}
    {GLOW}
    <clipPath id="c"><rect width="490" height="230" rx="20"/></clipPath>
  </defs>
  <style>
    text {{ {FONT} }}
    .m {{ font-size: 11px; fill: #a99bd6; letter-spacing: 3px; font-weight: 700; }}
    .n {{ font-size: 26px; font-weight: 800; fill: #ffd1dc; }}
    .d {{ font-size: 13.5px; fill: #efe6ff; }}
    .g {{ font-size: 12px; fill: #ffd1dc; }}{STAR_CSS}{art_css}
  </style>
  <g clip-path="url(#c)">
    <rect width="490" height="230" fill="url(#sky)"/>
    {stars(25, 490, 230, big=.1)}
    {art}
    <text x="26" y="38" class="m">{meta}</text>
    <text x="26" y="70" class="n" filter="url(#glow)">{name}</text>
    {desc}
    {"".join(chips)}
  </g>
  <rect x="1" y="1" width="488" height="228" rx="19" fill="none" stroke="#ffb7c5" stroke-opacity=".3" stroke-width="1.5"/>
</svg>
'''


def card_pptxforge():
    slides = "".join(f'''<g class="s" style="animation-delay:{-i*1.5}s">
        <rect x="-50" y="-30" width="100" height="60" rx="8" fill="#fff4d6"/>
        <rect x="-38" y="-18" width="{40+i*8}" height="7" rx="3.5" fill="#ff9ec0"/>
        <rect x="-38" y="-3" width="58" height="4" rx="2" fill="#c8b6ff"/>
        <rect x="-38" y="6" width="44" height="4" rx="2" fill="#c8b6ff"/>
        <circle cx="30" cy="12" r="{7+i*2}" fill="#ffb7c5"/></g>''' for i in range(4))
    css = '''
    .deck { transform: translate(400px, 78px); }
    .s { animation: deal 6s cubic-bezier(.6,0,.3,1) infinite; opacity: 0; }
    @keyframes deal {
      0% { transform: translate(40px, 30px) rotate(12deg) scale(.7); opacity: 0; }
      12% { opacity: 1; } 25% { transform: none; opacity: 1; }
      50% { transform: translate(-22px, -14px) rotate(-8deg) scale(.9); opacity: .6; }
      100% { transform: translate(-56px, -36px) rotate(-22deg) scale(.7); opacity: 0; } }'''
    return card("pptxforge", ["PowerPoint decks from Python.", "Themed layouts, native 3D models", "that morph between slides and", "cinematic transitions."],
                ["python", "pptx", "3d", "pypi"], "PROJECT 01", css, f'<g class="deck">{slides}</g>')


def card_selfobserver():
    css = '''
    .orb { transform-origin: 410px 80px; animation: orb 6s linear infinite; }
    @keyframes orb { to { transform: rotate(360deg); } }
    .orb2 { transform-origin: 410px 80px; animation: orb 10s linear infinite reverse; }'''
    art = '''<circle cx="410" cy="80" r="62" fill="none" stroke="#c8b6ff" stroke-opacity=".35" stroke-dasharray="3 6"/>
      <circle cx="410" cy="80" r="40" fill="none" stroke="#ffb7c5" stroke-opacity=".3"/>
      <circle cx="410" cy="80" r="24" fill="#fff4d6"/><circle cx="402" cy="74" r="5" fill="#f1dcae"/><circle cx="416" cy="88" r="4" fill="#f1dcae"/>
      <g class="orb"><circle cx="472" cy="80" r="5" fill="#ff9ec0" filter="url(#glow)"/></g>
      <g class="orb2"><circle cx="410" cy="40" r="3.5" fill="#c8b6ff" filter="url(#glow)"/></g>'''
    return card("SelfObserver", ["Local activity tracker. Window", "titles and screenshots go through", "local Ollama models and come out as", "a timeline, a forecast and notes."],
                ["python", "ollama", "flask", "hdbscan"], "PROJECT 02", css, art)


def stack():
    names = ["python", "typescript", "javascript", "swift", "lua", "html/css", "react", "flask", "blender", "godot", "ollama", "obsidian"]
    x, y, out = 20, 14, []
    for i, s in enumerate(names):
        w = len(s) * 9.5 + 44
        if x + w > 980:
            x, y = 20, y + 52
        d = f"animation-delay:{i*.25 - len(names)*.25:.2f}s"
        out.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="38" rx="19" style="{d}"/>'
                   f'<path style="{d}" d="M{x+18} {y+12} Q{x+19} {y+18} {x+25} {y+19} Q{x+19} {y+20} {x+18} {y+26} Q{x+17} {y+20} {x+11} {y+19} Q{x+17} {y+18} {x+18} {y+12}Z"/>'
                   f'<text x="{x+32}" y="{y+24}" style="{d}">{s}</text>')
        x += w + 12
    H = y + 52
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {H}" width="1000" height="{H}">
  <style>
    text {{ {FONT} font-size: 15px; fill: #efe6ff; animation: tt 3s linear infinite; }}
    rect {{ fill: #1d1542; stroke: #ffb7c5; stroke-opacity: .3; stroke-width: 1.5; animation: rr 3s linear infinite; }}
    path {{ fill: #ffb7c5; animation: pp 3s linear infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes rr {{ 0%, 10% {{ fill: #4a2d6e; stroke-opacity: 1; }} 11%, 100% {{ fill: #1d1542; stroke-opacity: .3; }} }}
    @keyframes tt {{ 0%, 10% {{ fill: #fff; }} 11%, 100% {{ fill: #cbbdf0; }} }}
    @keyframes pp {{ 0% {{ transform: scale(1.5) rotate(45deg); fill: #fff4d6; }} 10% {{ transform: scale(1.5) rotate(90deg); }} 11%, 100% {{ transform: none; fill: #ffb7c5; }} }}
  </style>
  {"".join(out)}
</svg>
'''


def footer():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 140" width="1000" height="140">
  <defs>
    <linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="#ffb7c5"/><stop offset="1" stop-color="#c8b6ff"/></linearGradient>
    {SKY}
  </defs>
  <style>
    text {{ {FONT} }}
    .rocket {{ animation: fly 5s ease-in-out infinite; }}
    @keyframes fly {{ 0% {{ transform: translate(0, 0); opacity: 0; }} 10% {{ opacity: 1; }} 80% {{ opacity: 1; }} 100% {{ transform: translate(320px, -60px); opacity: 0; }} }}
    .trail {{ stroke-dasharray: 4 8; animation: dash 1s linear infinite; }}
    @keyframes dash {{ to {{ stroke-dashoffset: -12; }} }}{STAR_CSS}
  </style>
  <rect width="1000" height="140" rx="20" fill="url(#sky)"/>
  {stars(40, 1000, 110, big=.2).replace('fill="#fff"', 'fill="#c8b6ff"')}
  <circle cx="780" cy="44" r="24" fill="#f7e6bd"/><circle cx="772" cy="38" r="5" fill="#f1dcae"/><circle cx="788" cy="52" r="4" fill="#f1dcae"/>
  <g class="rocket" transform="translate(440 104)">
    <path class="trail" d="M-60 12 Q-30 8 -8 2" fill="none" stroke="#ffb7c5" stroke-width="2" stroke-linecap="round"/>
    <path d="M0 0 C6 -6 18 -8 24 -6 C22 0 16 8 8 10 Z" fill="#fff4d6"/><circle cx="14" cy="-2" r="2.5" fill="#ff9ec0"/>
  </g>
  <text x="500" y="130" text-anchor="middle" font-size="15" font-weight="700" fill="url(#t)" letter-spacing="3" dy="-6">fly me to the moon ☾ またね</text>
</svg>
'''


files = {"header.svg": header(), "about.svg": about(), "card-pptxforge.svg": card_pptxforge(),
         "card-selfobserver.svg": card_selfobserver(), "stack.svg": stack(), "footer.svg": footer()}
OUT.mkdir(exist_ok=True)
for name, svg in files.items():
    (OUT / name).write_text(svg)
print("wrote", ", ".join(files))
