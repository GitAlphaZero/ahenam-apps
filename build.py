"""Generates the static privacy/support site for Ahenam's apps (GitHub Pages)."""
import html
import pathlib

PUBLISHER = "Ahenam"
EMAIL = "stephenjeevaratnam@gmail.com"
EFFECTIVE = "November 25, 2026"
OUT = pathlib.Path(__file__).parent / "docs"

APPS = [
    ("wirebolt", "Wirebolt", "Electrician calculators: voltage drop, wire size, conduit fill, box fill and bending."),
    ("bluelinefitter", "Blueline Fitter", "Pipefitting offsets, take-outs and pipe and flange reference."),
    ("roofdial", "RoofDial", "Roof pitch gauge and roofing material estimates."),
    ("mudmath", "MudMath", "Concrete, block, brick and rebar estimating."),
    ("sightglass", "Sightglass", "HVAC refrigerant charts, superheat, subcooling and duct sizing."),
    ("toolroom", "Toolroom", "Machinist calculators: feeds, speeds, threads and tapping."),
    ("weldbench", "WeldBench", "Welding settings, heat input and filler metal calculators."),
    ("stairwise", "Stairwise", "Stair stringer layout and framing calculators."),
    ("tileline", "Tileline", "Pool water balance and chemical dosing for pool techs."),
]

CSS = """
:root{--bg:#fafafa;--fg:#16181d;--muted:#5c6370;--card:#fff;--line:#e3e5e8;--accent:#1d6fd8}
@media (prefers-color-scheme:dark){:root{--bg:#0f1115;--fg:#eceef2;--muted:#a0a6b0;--card:#181b21;--line:#2a2e36;--accent:#6aa8ff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:720px;margin:0 auto;padding:32px 16px 64px}h1{font-size:28px;line-height:1.2;margin:0 0 4px}
h2{font-size:19px;margin:28px 0 8px}p,li{color:var(--fg)}.muted{color:var(--muted)}a{color:var(--accent)}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:12px 0}
nav{font-size:14px;margin-bottom:24px}ul{padding-left:20px}
"""


def page(title: str, body: str, back: str = "") -> str:
    nav = f'<nav><a href="{back}">← All apps</a></nav>' if back else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><main>{nav}{body}</main></body></html>"""


def privacy(name: str) -> str:
    n = html.escape(name)
    return f"""
<h1>{n} Privacy Policy</h1>
<p class="muted">Effective {EFFECTIVE} · Published by {PUBLISHER}</p>
<p>{n} ("the app") is a calculator and reference tool. This policy explains what information is
collected when you use it and how it is used.</p>

<h2>Information we collect</h2>
<p>We do not ask you to create an account, and we do not collect your name, email address or contacts.
Everything you enter into the calculators stays on your device. We do not receive it.</p>

<h2>Advertising (Google AdMob)</h2>
<p>The free version shows banner ads from Google AdMob. To show and measure ads, Google may collect:</p>
<ul>
<li>Device identifiers, including the Apple Advertising Identifier (IDFA) <strong>only if you allow tracking</strong> when iOS asks</li>
<li>IP address and approximate location derived from it</li>
<li>Ad interactions, app usage and diagnostic data (such as crashes and performance)</li>
</ul>
<p>If you decline tracking, you may still see ads, but they will not be personalized using the IDFA.
Users in regions that require it are asked for consent before personalized ads are shown, and can change that choice later.
Google's use of this data is described in
<a href="https://policies.google.com/technologies/partner-sites">How Google uses information from sites or apps that use its services</a>
and the <a href="https://policies.google.com/privacy">Google Privacy Policy</a>.</p>

<h2>In-app purchases</h2>
<p>If the app offers in-app purchases, they are processed by Apple. We never receive your payment
details. We only receive confirmation that a purchase is active, so paid features can be unlocked.</p>

<h2>Children</h2>
<p>The app is intended for tradespeople and is not directed at children under 13. We do not knowingly
collect personal information from children.</p>

<h2>Data sharing and retention</h2>
<p>We do not sell your personal information. We do not store personal data on our own servers.
Data collected by Google for advertising is kept according to Google's policies.</p>

<h2>Your choices</h2>
<ul>
<li>Change tracking permission: iOS Settings → Privacy &amp; Security → Tracking</li>
<li>Reset your advertising identifier or limit ad tracking in iOS Settings</li>
</ul>

<h2>Changes</h2>
<p>If this policy changes, we will update this page and its effective date.</p>

<h2>Contact</h2>
<p>Questions about privacy: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
"""


def support(name: str, desc: str, slug: str) -> str:
    n = html.escape(name)
    return f"""
<h1>{n} Support</h1>
<p class="muted">{html.escape(desc)}</p>
<div class="card">
<p><strong>Need help or found a wrong result?</strong><br>
Email <a href="mailto:{EMAIL}?subject={html.escape(name)}%20support">{EMAIL}</a> with your device model,
iOS version and the values you entered. We usually reply within 2 business days.</p>
</div>
<h2>Common questions</h2>
<p><strong>Why do I see ads?</strong><br>Ads keep every tool free. A paid ad-free option is planned for a future update.</p>
<p><strong>Are the results guaranteed?</strong><br>No. {n} is a reference tool. Always confirm against
the applicable code, the manufacturer's instructions and your local authority having jurisdiction.</p>
<p><a href="../privacy/">Privacy policy</a></p>
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / ".nojekyll").write_text("")
    items = "".join(
        f'<div class="card"><strong>{html.escape(n)}</strong><br><span class="muted">{html.escape(d)}</span><br>'
        f'<a href="{s}/support/">Support</a> · <a href="{s}/privacy/">Privacy policy</a></div>'
        for s, n, d in APPS
    )
    (OUT / "index.html").write_text(
        page(f"{PUBLISHER} Apps", f"<h1>{PUBLISHER} Apps</h1><p class='muted'>Field tools for the trades.</p>{items}"
             f"<p>Contact: <a href='mailto:{EMAIL}'>{EMAIL}</a></p>")
    )
    for slug, name, desc in APPS:
        for kind, body in (("privacy", privacy(name)), ("support", support(name, desc, slug))):
            d = OUT / slug / kind
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(page(f"{name} {kind.title()}", body, back="../../"))
    print("built", len(APPS), "apps into", OUT)


if __name__ == "__main__":
    main()
