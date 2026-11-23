# -*- coding: utf-8 -*-
"""Generátor webu Zumex Česko. python3 build.py <root webu> <content.json> [pages...]"""
import sys, json, html, re, os
ROOT, CONTENT = sys.argv[1], sys.argv[2]
ONLY = set(sys.argv[3:])
C = json.load(open(CONTENT, encoding='utf-8'))
P = {p['id']: p for p in C['products']}
ORDER = [p['id'] for p in C['products']]
e = lambda s: html.escape(str(s or '').replace(' — ', ', ').replace(' – ', ', '), quote=True)
CSSV = '5'

# ---------- ikony (inline SVG, stroke) ----------
ICONS = {
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'arrow-up-right': '<path d="M7 17 17 7M8 7h9v9"/>',
 'search': '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
 'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'pin': '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 'download': '<path d="M12 4v11m0 0-4.5-4.5M12 15l4.5-4.5M5 20h14"/>',
 'file': '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
 'close': '<path d="M6 6l12 12M18 6 6 18"/>',
 'plus': '<path d="M12 5v14M5 12h14"/>',
 'drop': '<path d="M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11z"/>',
 'briefcase': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
 'flag': '<path d="M5 21V4m0 1c5-4 9 3 14-1v10c-5 4-9-3-14 1"/>',
 'headset': '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>',
 'cart': '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M3 4h2l2.4 11h11L21 8H6.2"/>',
 'filter': '<path d="M4 6h16M7 12h10M10 18h4"/>',
 'wrench': '<path d="M14.5 5.5a4 4 0 0 0 5 5L12 18a2.1 2.1 0 0 1-3-3z"/><path d="M14.5 5.5 17 3"/>',
 'shield': '<path d="M12 3 5 6v6c0 4.5 3 7.5 7 9 4-1.5 7-4.5 7-9V6z"/><path d="m9 12 2 2 4-4"/>',
 'chevron-left': '<path d="m15 6-6 6 6 6"/>',
 'chevron-right': '<path d="m9 6 6 6-6 6"/>',
 'check': '<path d="m5 12 4.5 4.5L19 7"/>',
 'image': '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/>',
}
def icon(name, cls='icon'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

# ---------- kontakty ----------
PHONE_MAIN = ('+420 272 740 832', 'tel:+420272740832')
PHONES = [('+420 272 740 832', 'tel:+420272740832', ''), ('+420 272 738 859', 'tel:+420272738859', ''),
          ('+420 724 011 902', 'tel:+420724011902', 'servisní mobil'), ('+420 603 140 893', 'tel:+420603140893', 'mobil')]
MAP = 'https://www.google.com/maps/search/?api=1&query=KARMEB+Kou%C5%99imsk%C3%A1+4+Praha'

# ---------- rozvržení ----------
def head(p, title, desc, page_class=''):
    return f'''<!doctype html>
<html lang="cs" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{p}assets/hero-soul-sunset.webp">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{p}favicon.svg">
<link rel="preload" href="{p}assets/fonts/manrope-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/tokens.css?v={CSSV}">
<link rel="stylesheet" href="{p}assets/css/components.css?v={CSSV}">
<script>document.documentElement.classList.replace('no-js','js')</script>
</head>
<body class="{page_class}">
<a class="skip-link" href="#obsah">Přeskočit na obsah</a>
'''

NAV_ITEMS = [('Produkty', 'produkty/index.html', 'produkty'), ('Technologie', 'index.html#technologie', 'technologie'),
             ('Servis a záruka', 'index.html#servis', 'servis'), ('Kontakt', 'kontakt/index.html', 'kontakt')]

def nav(p, active=''):
    links = ''.join(f'<a href="{p}{href}"{" aria-current=\"page\"" if key == active else ""}>{e(t)}</a>' for t, href, key in NAV_ITEMS)
    return f'''<header class="site-header">
 <nav class="nav" aria-label="Hlavní navigace">
  <a class="nav-logo" href="{p}index.html"><img src="{p}assets/logo.webp" alt="Zumex Česko" width="480" height="183"></a>
  <div class="nav-menu" id="menu">{links}
   <div class="nav-mobile-cta"><a class="btn btn-primary" href="{p}kontakt/index.html">Nezávazná poptávka {icon("arrow")}</a></div>
  </div>
  <div class="nav-actions">
   <a class="icon-btn nav-search" href="{p}produkty/index.html#hledat" aria-label="Hledat produkt">{icon("search")}</a>
   <a class="btn btn-primary btn-sm" href="{p}kontakt/index.html">Nezávazná poptávka</a>
   <button class="icon-btn nav-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Otevřít menu">{icon("menu")}</button>
  </div>
 </nav>
</header>
<main id="obsah">
'''

def footer(p):
    cats = [('Lisy na citrusy', 'produkty/index.html#citrusy'), ('Samočisticí lisy', 'produkty/index.html#samocistici'),
            ('Ovoce a zelenina', 'produkty/index.html#multifruit'), ('Cold Press', 'produkty/index.html#cold-press'),
            ('Průmyslové technologie', 'produkty/index.html#prumyslove')]
    cl = ''.join(f'<li><a href="{p}{h}">{e(t)}</a></li>' for t, h in cats)
    return f'''</main>
<footer class="site-footer">
 <div class="container">
  <div class="footer-grid">
   <div>
    <img class="footer-logo" src="{p}assets/logo-white.webp" alt="Zumex" width="480" height="183">
    <p>Autorizovaný zástupce Zumex pro Českou republiku a Slovensko. Prodej, servis a originální náhradní díly.</p>
   </div>
   <div><h3>Produkty</h3><ul>{cl}</ul></div>
   <div><h3>Služby</h3><ul>
    <li><a href="{p}index.html#servis">Servis a záruka</a></li>
    <li><a href="{p}kontakt/index.html">Kontakt</a></li>
    <li><a href="https://www.gastronakup.cz/" rel="noopener">E-shop gastronakup.cz</a></li>
    <li><a href="https://www.zumex.com/en/" rel="noopener" target="_blank">Oficiální katalog Zumex</a></li>
   </ul></div>
   <div><h3>KARMEB spol. s r.o.</h3><ul>
    <li><p>Kouřimská 2368/4<br>130 00 Praha 3</p></li>
    <li><a href="{PHONE_MAIN[1]}">{PHONE_MAIN[0]}</a></li>
    <li><a href="mailto:gastro@karmeb.com">gastro@karmeb.com</a></li>
   </ul></div>
  </div>
  <div class="footer-bottom">
   <span>© 2026 KARMEB spol. s r.o. Fotografie a produktové podklady: Zumex Group.</span>
   <a href="{p}styleguide.html">Styleguide</a>
  </div>
 </div>
</footer>
<script src="{p}assets/js/site.js" defer></script>
</body>
</html>
'''

def page(path, p, title, desc, body, active='', page_class=''):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(head(p, title, desc, page_class) + nav(p, active) + body + footer(p))
    print('wrote', path)

# ---------- komponenty ----------
def product_card(prod, p, tag=None):
    c = prod['card']
    specs = ''.join(f'<li>{e(k)}<strong>{e(v)}</strong></li>' for k, v in c['specs'][:2])
    t = f'<span class="card-tag">{e(tag)}</span>' if tag else ''
    attrs = f' data-category="{e(c["category"])}" data-demand="{e(c["demand"])}" data-business="{e(c["business"])}" data-search="{e(c["search"])}"'
    return f'''<a class="card-product reveal" href="{p}produkty/{prod["id"]}/index.html"{attrs}>
 <div class="card-media">{t}<img src="{p}assets/{e(c["img"])}" alt="{e(prod["name"])}" loading="lazy"></div>
 <div class="card-body">
  <span class="caption">{e(cat_label(prod))}</span>
  <h3 class="card-title">{e(prod["name"])}</h3>
  <p class="card-text">{e(c["text"])}</p>
  <ul class="card-specs">{specs}</ul>
  <div class="card-foot"><span class="small"><b>Detail a parametry</b></span><span class="card-arrow">{icon("arrow")}</span></div>
 </div>
</a>'''

CAT_LABEL = {'citrusy': 'Lisy na citrusy', 'samocistici': 'Samočisticí lisy', 'odstavnovace': 'Ovoce a zelenina',
             'ananas': 'Kráječ a loupač ananasu', 'cold-press': 'Cold Press', 'prumyslove': 'Průmyslové technologie'}
def cat_label(prod):
    return CAT_LABEL.get(prod['card']['category'], prod['kategorie'])

def section_head(title, lead=None, left=False, tag='h2'):
    l = f'<p class="lead">{e(lead)}</p>' if lead else ''
    return f'<div class="section-head{" section-head--left" if left else ""} reveal"><{tag}>{e(title)}</{tag}>{l}</div>'

def cta_band(p, title, text, dark=False):
    return f'''<section class="section section--tight"><div class="container">
 <div class="cta-band{" cta-band--dark" if dark else ""} reveal">
  <div><h2>{e(title)}</h2><p>{e(text)}</p></div>
  <div class="btn-row">
   <a class="btn {"btn-accent" if dark else "btn-primary"} btn-lg" href="{PHONE_MAIN[1]}">{icon("phone")} {PHONE_MAIN[0]}</a>
   <a class="btn {"btn-ghost-dark" if dark else "btn-secondary"} btn-lg" href="mailto:gastro@karmeb.com">Napsat e-mail</a>
  </div>
 </div>
</div></section>
'''

SERVICE_ITEMS = [
 ('Mezinárodní záruka 2 roky', 'Rozsah záruky a její uplatnění se řídí podmínkami výrobce pro konkrétní zařízení. Připravte si doklad o nákupu a výrobní číslo, s dalším postupem vám pomůže náš servis.', 'Záruční podmínky výrobce', 'https://www.zumex.com/en/warranty-conditions/'),
 ('Originální náhradní díly', 'Pomůžeme určit správný originální díl pro váš model. Pošlete nám označení stroje, výrobní číslo a ideálně fotografii potřebného dílu.', 'Poptat náhradní díl', 'mailto:servis@karmeb.com?subject=N%C3%A1hradn%C3%AD%20d%C3%ADly%20Zumex'),
 ('Registrace produktu', 'Zaregistrujte svůj přístroj a mějte údaje o něm po ruce pro servisní komunikaci. Záruční podmínky se mohou lišit podle modelu.', 'Přejít na registraci produktu', 'https://zumex.cz/registrace-produktu/'),
 ('Technická podpora ZumexService', 'Potřebujete poradit s obsluhou, čištěním nebo závadou? Napište model a stručný popis potíží. Domluvíme s vámi další postup.', 'servis@karmeb.com', 'mailto:servis@karmeb.com'),
]
def accordion(items, open_first=True):
    out = ''
    for i, (q, a, lt, lh) in enumerate(items):
        ext = ' target="_blank" rel="noopener"' if lh.startswith('http') else ''
        out += f'<details{" open" if (i == 0 and open_first) else ""}><summary>{e(q)}{icon("plus")}</summary><div class="accordion-body"><p>{e(a)}</p><a class="link" href="{e(lh)}"{ext}>{e(lt)}</a></div></details>'
    return f'<div class="accordion">{out}</div>'

def service_section(p, dark=True):
    return f'''<section class="section{" section--dark" if dark else ""}" id="servis"><div class="container">
 <div class="split" style="align-items:start">
  <div class="reveal">
   <h2>Servis a náhradní díly řešíme z Prahy</h2>
   <p class="lead" style="margin-top:18px">Jako autorizovaný zástupce zajišťujeme opravy a dodávky náhradních dílů pro zařízení Zumex v České republice i na Slovensku.</p>
   <div style="margin-top:32px"><span class="caption">Servisní mobil</span><a href="tel:+420724011902" class="h2" style="display:block;margin-top:4px">+420 724 011 902</a></div>
   <div class="btn-row" style="margin-top:28px"><a class="btn btn-accent" href="mailto:servis@karmeb.com">Napsat servisu {icon("arrow")}</a></div>
  </div>
  <div class="reveal">{accordion(SERVICE_ITEMS)}</div>
 </div>
</div></section>
'''

def contact_cards(p):
    tel = ''.join(f'<a href="{h}">{e(n)}</a>' + (f'<span class="caption">{e(m)}</span>' if m else '') for n, h, m in PHONES)
    return f'''<div class="grid grid-4">
 <div class="card card-contact reveal"><span class="icon-tile">{icon("pin")}</span><h3>Adresa</h3><p>Kouřimská 2368/4<br>130 00 Praha 3<br>Česká republika</p><a class="link" href="{MAP}" target="_blank" rel="noopener">Zobrazit na mapě</a></div>
 <div class="card card-contact reveal"><span class="icon-tile">{icon("phone")}</span><h3>Telefony</h3>{tel}</div>
 <div class="card card-contact reveal"><span class="icon-tile">{icon("mail")}</span><h3>E-mail</h3><a href="mailto:gastro@karmeb.com">gastro@karmeb.com</a><span class="caption">obchod</span><a href="mailto:servis@karmeb.com">servis@karmeb.com</a><span class="caption">servis</span></div>
 <div class="card card-contact card-contact--accent reveal"><span class="icon-tile">{icon("cart")}</span><h3>E-shop</h3><p>Vybavení a stroje také online.</p><div style="margin-top:12px"><a class="btn btn-accent btn-sm" href="https://www.gastronakup.cz/" rel="noopener">gastronakup.cz {icon("arrow-up-right")}</a></div></div>
</div>'''

TRUST = [('drop', '100 % čerstvá šťáva'), ('briefcase', 'Navrženo pro profesionály'), ('flag', 'Vyrobeno ve Španělsku'), ('headset', 'Podpora v České republice')]

# ---------- úvodní stránka ----------
FRUITS = [('pomeranc','Pomeranče'),('mandarinka','Mandarinky'),('citron','Citrony'),('limetka','Limetky'),('grapefruit','Grapefruity'),
          ('granatove-jablko','Granátová jablka'),('ananas','Ananas'),('jablko','Jablka'),('mrkev','Mrkev'),('zazvor','Zázvor'),('okurka','Okurky a celer'),('cervena-repa','Červená řepa')]
SHOWCASE = [
 ('Lisy na citrusy', 'Kavárny, bary, hotely', 'drop', ['soul-series-2','minex','essential','versatile'], 'produkty/index.html#citrusy'),
 ('Samoobsluha v obchodě', 'Juice corner a supermarkety', 'cart', ['zitrux-compact','zitrux','speed-up','speed-s-plus'], 'produkty/index.html#samocistici'),
 ('Ovoce, zelenina, ananas', 'Smoothie a fresh bary', 'flag', ['multifruit','pineomatic','mastery','speed-pomegranates'], 'produkty/index.html#multifruit'),
 ('Průmyslová výroba', 'Linky na šťávy', 'wrench', ['z450-z450p','zbp','zws','zf-zbib'], 'produkty/index.html#prumyslove'),
]
def mini_card(prod, p):
    c = prod['card']
    spec = c['specs'][0][1] if c['specs'] else ''
    return f'<a class="mini-card spotlight" href="{p}produkty/{prod["id"]}/index.html"><div class="mini-media"><img src="{p}assets/{e(c["img"])}" alt="" loading="lazy"></div><div><h3>{e(prod["name"])}</h3><p>{e(prod["claim"])}</p><b>{e(spec)} {icon("arrow")}</b></div></a>'

def build_home():
    p = ''
    trust = ''.join(f'<div class="trust-item"><span class="icon-tile">{icon(i)}</span>{e(t)}</div>' for i, t in TRUST)
    featured = ['soul-series-2', 'versatile', 'speed-up', 'zitrux-compact']
    cards = ''.join(product_card(P[i], p) for i in featured)
    fruits = ''.join(f'<span class="fruit"><img src="assets/ovoce/{f}.svg" alt="" width="120" height="100">{e(t)}</span>' for f, t in FRUITS)
    tabs = ''.join(f'<button class="showcase-tab" role="tab" id="tab-{i}" aria-controls="panel-{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><span class="icon-tile">{icon(ic)}</span><span>{e(t)}<small>{e(sub)}</small></span></button>' for i, (t, sub, ic, ids, h) in enumerate(SHOWCASE))
    panels = ''.join(f'<div class="showcase-panel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}"{"" if i == 0 else " hidden"}>' + ''.join(mini_card(P[x], p) for x in ids) + f'<div class="showcase-more"><a class="btn btn-light btn-sm" href="{h}">Zobrazit vše v kategorii {icon("arrow")}</a></div></div>' for i, (t, sub, ic, ids, h) in enumerate(SHOWCASE))
    feats = [('drop', 'Technologie pro chuť', 'Od kompaktního lisu po výrobu šťáv. Šťáva bez hořkosti.'),
             ('briefcase', 'Stroj pro váš provoz', 'Výběr podle prostoru, spotřeby a způsobu obsluhy.'),
             ('wrench', 'Servis z Prahy', 'Opravy a originální náhradní díly pro ČR i Slovensko.'),
             ('shield', 'Záruka 2 roky', 'Mezinárodní záruka výrobce na zařízení Zumex.')]
    fc = ''.join(f'<div class="feature-card">{icon(i)}<h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, t, d in feats)
    body = f"""<section class="hero-center"><div class="container">
 <h1 class="split-text">Profesionální lisy na citrusy Zumex pro kavárny, hotely a obchody</h1>
 <p class="lead">Proměňte čerstvé ovoce v zážitek, za kterým se zákazníci vracejí. Najdeme správný stroj pro vaši kavárnu, hotel i obchod.</p>
 <div class="btn-row"><a class="btn btn-accent btn-lg magnet" href="produkty/index.html">Vybrat automatický lis {icon("arrow")}</a><a class="btn btn-secondary btn-lg" href="#kontakt">Poradit s výběrem</a></div>
 <div class="hero-bento">
  <div class="tile tile--citron reveal"><strong data-count="20">20</strong><span>produktových řad od baru po výrobní linku</span></div>
  <div class="tile tile--photo reveal"><img src="assets/hero-soul-sunset.webp" alt="Zumex Soul se sklenicí čerstvé pomerančové šťávy" width="1000" height="537" fetchpriority="high"></div>
  <div class="tile tile--peach reveal"><img class="tile-product" src="assets/main3.png" alt="Lis na citrusy Zumex Versatile" width="400" height="400"><img class="tile-sticker" src="assets/vyrobeno-ve-spanelsku.webp" alt="Vyrobeno ve Španělsku" width="480" height="431"></div>
  <div class="tile tile--dark reveal"><div class="tile-bars" aria-hidden="true"><i></i><i></i><i></i><i></i></div><strong data-count="40">40</strong><span>plodů za minutu u lisů Speed Up a Zitrux</span></div>
  <div class="tile tile--surface reveal"><strong><span data-count="2" style="display:inline;margin:0;font-size:inherit;color:inherit">2</span> roky</strong><span>mezinárodní záruka a servis přímo z Prahy</span></div>
 </div>
</div></section>

<section class="section--tight" aria-label="Co lisy Zumex zpracují" style="padding-bottom:clamp(48px,6vw,80px)"><div class="marquee"><div class="marquee-track">{fruits}</div></div></section>

<section class="section section--surface" id="technologie"><div class="container">
 <div class="why-grid">
  <figure class="why-media reveal" data-video style="margin:0">
   <video playsinline preload="none" poster="assets/conical-video-poster.jpg" aria-label="Zumex Conical System, ukázka lisovací technologie"><source src="assets/zumex-conical-system.mp4" type="video/mp4"></video>
   <button class="play-btn" type="button" aria-label="Přehrát video Conical System"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l12.5-7.5z"/></svg></button>
   <figcaption>Conical System® v akci<span>Oficiální video Zumex, 22 sekund</span></figcaption>
  </figure>
  <div class="reveal">
   <h2>Proč si vybrat Zumex</h2>
   <p class="lead" style="margin-top:16px">Od kompaktního Conical System® až po automatizované čištění Zitrux. Technologie Zumex zjednoduší přípravu šťávy i každodenní péči o stroj.</p>
   <div class="feature-cards">{fc}</div>
  </div>
 </div>
</div></section>

<section class="section" id="produkty"><div class="container">
 {section_head("Nejoblíbenější lisy na citrusy", "Vyberte podle místa na baru, denní spotřeby a toho, jestli chcete, aby si zákazníci točili šťávu sami.")}
 <div class="grid grid-4">{cards}</div>
 <div class="section-foot"><a class="btn btn-primary" href="produkty/index.html">Zobrazit všech {len(ORDER)} produktových řad {icon("arrow")}</a></div>
</div></section>

<section class="section" id="reseni" style="padding-top:0"><div class="container">
 <div class="showcase reveal" data-showcase>
  <div class="section-head"><h2>Najděte stroj podle svého provozu</h2><p class="lead">Kavárna potřebuje jiný lis než supermarket nebo výrobna. Vyberte, kde budete šťávu podávat.</p></div>
  <div class="showcase-grid"><div class="showcase-tabs" role="tablist" aria-label="Typ provozu">{tabs}</div><div>{panels}</div></div>
 </div>
</div></section>

<section class="section section--peach section--tight"><div class="container">
 <p class="statement">Šťáva z lisů Zumex nepřijde do kontaktu se slupkou, proto zůstává <span class="accent-word">sladká a bez hořkosti</span> od první do poslední sklenice.</p>
</div></section>

{service_section(p, dark=False)}

{cta_band(p, "Nevíte, který lis se hodí do vašeho provozu?", "Napište nám, kolik šťávy denně připravujete a kolik máte místa. Doporučíme konkrétní model a konfiguraci.")}

<section class="section section--citron" id="kontakt"><div class="container">
 {section_head("Kontakt na KARMEB spol. s r.o.", "Autorizovaný zástupce Zumex pro Českou republiku a Slovensko.")}
 {contact_cards(p)}
</div></section>
"""
    page('index.html', p, 'Profesionální lisy na citrusy Zumex | KARMEB Praha',
         'Profesionální lisy na citrusy a odšťavňovače Zumex pro kavárny, hotely, obchody i průmyslovou výrobu. Prodej, servis a náhradní díly z Prahy.', body)

# ---------- katalog ----------
DOC_TITLES = {'zumex-1': 'Prospekt Minex', 'zumex-16': 'Barevná provedení Minex', 'zumex-15': 'Návod k čištění Minex',
 'zumex-21': 'Prospekt Soul Series 2', 'zumex-20': 'Technický list Soul Series 2', 'zumex-24': 'Bezpečnostní pokyny Soul Series 2',
 'zumex-6': 'Prospekt Essential Pro', 'zumex-18': 'Technický list Essential Pro', 'zumex-19': 'Návod k čištění Essential',
 'zumex-9': 'Prospekt Speed Up', 'zumex-23': 'Protokol čištění', 'zumex-11': 'Návod k obsluze Speed Up a Speed S+plus',
 'zumex-10': 'Prospekt Speed Pomegranates', 'zumex-4': 'Prospekt řady Speed', 'zumex-12': 'Návod k čištění Speed Pomegranates',
 'zumex-5': 'Prospekt Zitrux', 'zumex-13': 'Technický list Zitrux', 'zumex-7': 'Katalog náhradních dílů Zitrux',
 'zumex-2': 'Technický list Zitrux Compact', 'zumex-17': 'Katalog náhradních dílů Zitrux Compact', 'zumex-14': 'Návod k obsluze Zitrux Compact',
 'zumex-3': 'Prospekt Multifruit', 'zumex-8': 'Recepty Multifruit', 'zumex-22': 'Technický list Multifruit'}
def fsize(path):
    try:
        b = os.path.getsize(os.path.join(ROOT, path))
        return f'{b/1048576:.1f} MB'.replace('.', ',')
    except OSError:
        return ''

def build_catalog():
    p = '../'
    fs = ''
    names = {'category': 'Kategorie', 'demand': 'Intenzita provozu', 'business': 'Váš podnik'}
    for g in ('category', 'demand', 'business'):
        fs += f'<fieldset><legend>{names[g]}</legend>' + ''.join(f'<label class="check"><input type="checkbox" name="{g}" value="{e(v)}"> {e(t)}</label>' for v, t in C['filters'][g]) + '</fieldset>'
    cards = ''.join(product_card(P[i], p) for i in ORDER)
    body = f"""<section class="section" style="padding-top:clamp(40px,5vw,72px)"><div class="container">
 <nav class="breadcrumbs" aria-label="Drobečková navigace"><a href="{p}index.html">Úvod</a><span>/</span><span>Produkty</span></nav>
 <div class="split" style="align-items:end;margin-bottom:clamp(28px,4vw,48px)">
  <div><h1 class="split-text">Katalog profesionálních lisů a odšťavňovačů Zumex</h1></div>
  <div><p class="lead">Od první sklenice za barem po celou výrobní linku. Vyberte si podle suroviny, intenzity provozu a způsobu použití.</p>
   <div class="input-search" id="hledat" style="margin-top:20px">{icon("search")}<label class="sr-only" for="product-search">Najít produkt</label><input class="input" id="product-search" type="search" placeholder="Model, ovoce, použití…" autocomplete="off"></div></div>
 </div>
 <div class="catalog">
  <div>
   <button class="btn btn-secondary filter-toggle" type="button" aria-expanded="false" aria-controls="catalog-filters">{icon("filter")} Filtry</button>
   <form class="filters" id="catalog-filters" role="search" aria-label="Filtrování produktů">{fs}<button class="btn btn-secondary btn-sm" type="reset">Vymazat všechny filtry</button></form>
  </div>
  <div>
   <div class="catalog-bar"><p id="catalog-count" class="small muted" role="status" aria-live="polite">{len(ORDER)} produktových řad</p><span class="caption">Parametry, varianty a dokumentace u každého produktu</span></div>
   <div class="grid grid-3 catalog-grid">{cards}</div>
   <div class="catalog-empty" hidden><h2 class="h3">Tomu neodpovídá žádný produkt</h2><p class="muted" style="margin:10px 0 20px">Zkuste upravit filtry nebo hledaný výraz. Případně nám napište, co potřebujete.</p><button class="btn btn-primary" type="button" data-reset>Zrušit filtry</button></div>
  </div>
 </div>
</div></section>
{cta_band(p, "Nevíte, který lis se hodí do vašeho provozu?", "Napište nám, kolik šťávy denně připravujete a kolik máte místa. Doporučíme konkrétní model a konfiguraci.")}
"""
    page('produkty/index.html', p, 'Katalog lisů a odšťavňovačů Zumex | KARMEB Praha',
         'Všech 20 produktových řad Zumex: lisy na citrusy, samočisticí lisy, odšťavňovače na ovoce a zeleninu, cold press i průmyslové linky. Parametry, varianty a dokumentace.', body, active='produkty')

# ---------- detail produktu ----------
def build_detail(pid):
    p = '../../'
    d = P[pid]
    name = d['name']
    mail = f'mailto:gastro@karmeb.com?subject=Popt%C3%A1vka%20Zumex%20{e(name).replace(" ", "%20")}'
    stats = ''.join(f'<div class="stat"><strong>{e(v)}</strong><span>{e(k)}</span></div>' for v, k in d['metrics'][:3])
    tabs = [('prehled', 'Přehled')]
    secs = []
    # Přehled
    colors = ['bento-item--citron', 'bento-item--peach', 'bento-item--surface']
    feats = ''.join(f'<div class="card {colors[i % 3].replace("bento-item", "card")}" style="display:flex;gap:14px;align-items:flex-start;border:0;background:var(--{["citron","peach","surface"][i % 3]})"><span class="icon-tile" style="background:#fff;color:var(--ink);width:40px;height:40px">{icon("check")}</span><p style="color:var(--ink);font-weight:600">{e(f)}</p></div>' for i, f in enumerate(d['feats']))
    story = ''.join(f'<p>{e(x)}</p>' for x in d['story'])
    secs.append(f"""<section class="section" id="prehled"><div class="container"><div class="split" style="align-items:start">
 <div class="reveal"><h2>Co {e(name)} umí</h2><div class="prose" style="margin-top:20px">{story}</div></div>
 <div class="stack reveal">{feats}</div></div></div></section>""")
    # Galerie
    if d['gallery']:
        figs = ''.join(f'<figure><img src="{p}assets/{e(g)}" alt="{e(a)}" loading="lazy"></figure>' for g, a in d['gallery'])
        nav_ = f'<div class="carousel-nav"><button class="icon-btn" type="button" data-dir="-1" aria-label="Předchozí fotka">{icon("chevron-left")}</button><button class="icon-btn" type="button" data-dir="1" aria-label="Další fotka">{icon("chevron-right")}</button></div>' if len(d['gallery']) > 1 else ''
        secs.append(f"""<section class="section--tight" style="padding-top:0"><div class="container" data-gallery>
 <div class="gallery{" gallery--single" if len(d["gallery"]) == 1 else ""}">{figs}</div>
 {f'<div style="display:flex;justify-content:flex-end;margin-top:14px">{nav_}</div>' if nav_ else ''}</div></section>""")
    # Suroviny
    f = d.get('fruit')
    if f:
        tabs.append(('suroviny', 'Suroviny'))
        icons = f['icons'] + [''] * len(f['items'])
        chips = ''.join(f'<span class="fruit">' + (f'<img src="{p}assets/{e(icons[i])}" alt="" width="120" height="100">' if icons[i] and i < len(f['icons']) else '') + f'{e(it)}</span>' for i, it in enumerate(f['items']))
        kits = ''.join(f'<div class="kit"><span>{e(k)}</span><strong>{e(v)}</strong></div>' for k, v in f['kits'])
        note = f'<p class="small muted" style="margin-top:16px;max-width:60ch">{e(f["note"])}</p>' if f.get('note') else ''
        secs.append(f"""<section class="section section--surface" id="suroviny"><div class="container"><div class="split">
 <div class="product-media reveal" style="background:#fff;aspect-ratio:5/4"><img src="{p}assets/{e(d["img"])}" alt="" loading="lazy"></div>
 <div class="reveal"><h2>Co {e(name)} zpracuje</h2><p class="lead" style="margin-top:16px">{e(f["text"])}</p>
  <div class="fruit-list">{chips}</div>{f'<div class="kit-list">{kits}</div>' if kits else ''}{note}</div>
</div></div></section>""")
    # Varianty
    if d['variants']:
        tabs.append(('varianty', 'Varianty'))
        vc = ''
        for v in d['variants']:
            media = f'<img src="{p}assets/{e(v["img"])}" alt="{e(v["name"])}" loading="lazy">' if v['img'] else icon('image', 'icon icon-lg')
            vm = f'mailto:gastro@karmeb.com?subject=Popt%C3%A1vka%20{e(v["name"]).replace(" ", "%20")}'
            vc += f'<div class="card-variant reveal"><div class="card-media{"" if v["img"] else " is-empty"}">{media}</div><div class="card-body"><h3>{e(v["name"])}</h3><p>{e(v["text"])}</p><div class="card-foot"><a class="btn-text" href="{vm}">Poptat variantu {icon("arrow")}</a></div></div></div>'
        secs.append(f"""<section class="section" id="varianty"><div class="container">
 {section_head("Varianty a provedení", "Jedna řada, vaše konfigurace. Fotografie jsou ilustrační, výbava a parametry se mohou lišit podle varianty.")}
 <div class="grid grid-3">{vc}</div></div></section>""")
    # Rozměry
    dm = d.get('dims')
    if dm:
        tabs.append(('rozmery', 'Rozměry'))
        groups = ''.join(f'<div class="dim-group">' + (f'<h3>{e(g["name"])}</h3>' if g['name'] else '') + '<ul class="dim-rows">' + ''.join(f'<li><span>{e(k)}</span><strong>{e(v)}</strong></li>' for k, v in g['rows']) + '</ul></div>' for g in dm['groups'])
        notes = ''.join(f'<p class="small muted" style="margin-top:14px">{e(n)}</p>' for n in dm['notes'])
        if dm.get('drawing') and len(dm['drawing']) == 2:
            h, w = dm['drawing']
            fig = f'<figure class="dim-figure reveal" aria-label="Rozměry {e(name)}"><div class="dim-h"><span>Výška<b>{e(h)}</b></span></div><div class="dim-img"><img src="{p}assets/{e(d["img"])}" alt="" loading="lazy"></div><div class="dim-w"><span>Šířka <b>{e(w)}</b></span></div></figure>'
        else:
            fig = f'<div class="product-media reveal" style="aspect-ratio:5/4"><img src="{p}assets/{e(d["img"])}" alt="" loading="lazy"></div>'
        secs.append(f"""<section class="section section--surface" id="rozmery"><div class="container"><div class="split">
 <div class="reveal"><h2>Rozměry</h2><p class="lead" style="margin:12px 0 24px">Kolik místa {e(name)} potřebuje.</p>{groups}{notes}</div>
 <div style="background:#fff;border-radius:var(--r-xl);padding:clamp(20px,3vw,40px)">{fig}</div></div></div></section>""")
    # Barvy
    cl = d.get('colors')
    if cl:
        tabs.append(('barvy', 'Barvy'))
        sw = ''.join(f'<li><span class="swatch" style="{e(c["style"].replace("background:", "background:", 1))}"></span>{e(c["name"])}</li>' for c in cl['items'])
        secs.append(f"""<section class="section" id="barvy"><div class="container">
 {section_head("Barevná provedení", cl["sub"])}
 <ul class="swatches reveal">{sw}</ul>
 <p class="caption" style="text-align:center;margin-top:28px">Barevné odstíny na obrazovce jsou orientační. Vzorník vám rádi ukážeme.</p></div></section>""")
    # Parametry
    tabs.append(('parametry', 'Parametry'))
    rows = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in d['params'])
    src = f' <a class="link" href="{e(d["source"])}" target="_blank" rel="noopener">Zdroj: Zumex</a>' if d['source'] else ''
    sel = f'<div class="cta-inline reveal" style="margin-top:32px"><div><h3 class="h4">Co zvážit při výběru</h3><p class="small muted" style="margin-top:4px;max-width:70ch">{e(d["selection"])}</p></div><a class="btn btn-primary" href="{mail}">Probrat konfiguraci {icon("arrow")}</a></div>' if d['selection'] else ''
    secs.append(f"""<section class="section{"" if (cl or not dm) else ""}" id="parametry"><div class="container">
 {section_head("Technické parametry", None, left=True)}
 <dl class="spec-table reveal">{rows}</dl>
 <p class="caption" style="margin-top:16px">{e(d["param_note"])}{src}</p>{sel}</div></section>""")
    # Technologie
    if d['tech']:
        tabs.append(('technologie', 'Technologie'))
        tc = ''.join(f'<div class="card spotlight reveal"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in d['tech'])
        secs.append(f"""<section class="section section--dark" id="technologie"><div class="container">
 {section_head("Technologie a výbava", "Co uvnitř dělá rozdíl v chuti, hygieně i obsluze.")}
 <div class="grid grid-3 tech-grid">{tc}</div></div></section>""")
    # Dokumentace
    docs = ''
    for t, h in d['docs']:
        if h.startswith('http'):
            docs += f'<a class="doc reveal" href="{e(h)}" target="_blank" rel="noopener"><span class="icon-tile">{icon("arrow-up-right")}</span><div>Oficiální stránka výrobce<span>zumex.com, anglicky</span></div></a>'
        else:
            key = os.path.splitext(os.path.basename(h))[0]
            docs += f'<a class="doc reveal" href="{p}{e(h)}" download><span class="icon-tile">{icon("download")}</span><div>{e(DOC_TITLES.get(key, t))}<span>PDF, {fsize(h)}</span></div></a>'
    if docs:
        tabs.append(('dokumentace', 'Dokumentace'))
        secs.append(f"""<section class="section" id="dokumentace"><div class="container">
 {section_head("Dokumentace ke stažení", "Prospekty, technické listy a návody výrobce.", left=True)}
 <div class="doc-list">{docs}</div></div></section>""")
    # Podobné
    same = [x for x in ORDER if x != pid and P[x]['card']['category'] == d['card']['category']]
    others = [x for x in ORDER if x != pid and x not in same]
    rel = (same + others)[:4]
    secs.append(f"""<section class="section section--surface"><div class="container">
 {section_head("Podobné produkty", None)}
 <div class="grid grid-4">{''.join(product_card(P[x], p) for x in rel)}</div></div></section>""")

    tabhtml = ''.join(f'<a href="#{a}">{t}</a>' for a, t in tabs)
    body = f"""<section class="section" style="padding:clamp(28px,4vw,56px) 0 clamp(40px,5vw,64px)"><div class="container">
 <nav class="breadcrumbs" aria-label="Drobečková navigace"><a href="{p}index.html">Úvod</a><span>/</span><a href="{p}produkty/index.html">Produkty</a><span>/</span><span>{e(name)}</span></nav>
 <div class="product-hero">
  <div class="product-media"><img src="{p}assets/{e(d["img"])}" alt="{e(name)}" fetchpriority="high"></div>
  <div>
   <span class="caption" style="font-weight:700">{e(cat_label(d))}</span>
   <h1 class="split-text" style="margin-top:8px">{e(name)}</h1>
   <p class="lead">{e(d["perex"])}</p>
   <div class="stats">{stats}</div>
   <div class="btn-row"><a class="btn btn-accent btn-lg magnet" href="{mail}">Poptat tento produkt {icon("arrow")}</a><a class="btn btn-secondary btn-lg" href="#parametry">Technické parametry</a></div>
   <p class="caption" style="margin-top:14px">Cenu a dostupnost vám potvrdíme podle konfigurace.</p>
  </div>
 </div>
</div></section>
<nav class="tabs" aria-label="Sekce produktu"><div class="tabs-inner">{tabhtml}</div></nav>
{''.join(secs)}
{cta_band(p, f"Chcete {name} do svého provozu?", "Pošlete nám, kolik šťávy denně připravujete a kolik máte místa. Ozveme se s doporučenou konfigurací a cenou.")}
"""
    desc = f'{name}: {d["card"]["text"]} Parametry, varianty, rozměry a dokumentace. Prodej a servis Zumex v Praze.'
    page(f'produkty/{pid}/index.html', p, f'{name} | {cat_label(d)} Zumex | KARMEB Praha', desc, body, active='produkty')

def build_details():
    for pid in ORDER:
        build_detail(pid)

# ---------- kontakt a 404 ----------
def build_contact():
    p = '../'
    body = f"""<section class="section" style="padding-top:clamp(40px,5vw,72px)"><div class="container">
 <nav class="breadcrumbs" aria-label="Drobečková navigace"><a href="{p}index.html">Úvod</a><span>/</span><span>Kontakt</span></nav>
 <div class="split" style="align-items:end;margin-bottom:clamp(32px,4vw,56px)">
  <h1 class="split-text">Kontakt a servis Zumex v Praze</h1>
  <p class="lead">KARMEB spol. s r.o. je autorizovaný zástupce Zumex pro Českou republiku a Slovensko. Poradíme s výběrem, dodáme stroj a postaráme se o servis.</p>
 </div>
 {contact_cards(p)}
</div></section>
{service_section(p, dark=True)}
{cta_band(p, "Nevíte, který lis se hodí do vašeho provozu?", "Napište nám, kolik šťávy denně připravujete a kolik máte místa. Doporučíme konkrétní model a konfiguraci.")}
"""
    page('kontakt/index.html', p, 'Kontakt a servis Zumex | KARMEB Praha',
         'Kontakt na KARMEB spol. s r.o., autorizovaného zástupce Zumex pro ČR a SR. Adresa Kouřimská 2368/4, Praha 3, telefony, e-mail a servis.', body, active='kontakt')

def build_404():
    p = '/zumex-web/'
    body = f"""<section class="section"><div class="container" style="text-align:center;max-width:720px">
 <h1>Tahle stránka neexistuje</h1>
 <p class="lead" style="margin:18px auto 0">Odkaz je možná starý nebo v něm je překlep. Zkuste katalog nebo nám rovnou zavolejte.</p>
 <div class="btn-row" style="justify-content:center;margin-top:32px"><a class="btn btn-accent btn-lg" href="{p}produkty/index.html">Do katalogu {icon("arrow")}</a><a class="btn btn-secondary btn-lg" href="{PHONE_MAIN[1]}">{PHONE_MAIN[0]}</a></div>
</div></section>"""
    page('404.html', p, 'Stránka nenalezena | Zumex Česko', 'Stránka nebyla nalezena.', body)

# ---------- styleguide ----------
def build_styleguide():
    p = ''
    colors = [('--bg', '#ffffff', 'Pozadí'), ('--surface', '#f4f3f1', 'Povrch'), ('--surface-2', '#ebe9e5', 'Povrch hover'),
              ('--ink', '#111111', 'Text'), ('--muted', '#5e5d59', 'Ztlumený text'), ('--line', '#e3e1dc', 'Linky'),
              ('--accent', '#ff6a13', 'Akcent Zumex'), ('--accent-soft', '#fff1e7', 'Akcent jemný'), ('--citron', '#d9e4a2', 'Citron (plochy)'), ('--peach', '#ffdccf', 'Peach (plochy, ikony)'), ('--dark', '#131313', 'Tmavá plocha'),
              ('--success', '#2f8f4e', 'Úspěch'), ('--error', '#c8312b', 'Chyba')]
    sw = ''.join(f'<div class="sg-swatch"><div style="background:var({t})"></div><p><b>{e(n)}</b><br><code>{t}</code> {h}</p></div>' for t, h, n in colors)
    types = [('H1', 'h1', 'Profesionální lisy na citrusy', 'Manrope ExtraBold 800, 64 / 38 px, řádkování 1,06'),
             ('H2', 'h2', 'Nejoblíbenější lisy na citrusy', 'Manrope ExtraBold 800, 46 / 30 px, 1,12'),
             ('H3', 'h3', 'Kavárny, bary a hotely', 'Manrope ExtraBold 800, 24 / 20 px, 1,3'),
             ('H4', 'h4', 'Technické parametry', 'Manrope ExtraBold 800, 18 px, 1,4'),
             ('Perex', 'p class="lead"', 'Najdeme správný stroj pro vaši kavárnu, hotel i obchod.', 'Manrope 400, 19 / 17 px, 1,6'),
             ('Text', 'p', 'Soul Series 2 přináší automatické lisování citrusů i na bar, kde je každý centimetr důležitý.', 'Manrope 400, 16 px, 1,65'),
             ('Malý text', 'p class="small"', 'Údaje výrobce pro uvedené provedení.', 'Manrope 400, 14 px'),
             ('Popisek', 'p class="caption"', 'Servisní mobil', 'Manrope 400, 12,5 px, ztlumená'),
             ('Odkaz', 'a class="link" href="#"', 'Zobrazit na mapě', 'Manrope 700, podtržení v akcentu'),
             ('Citát', 'blockquote class="quote"', 'Šťáva nepřijde do kontaktu se slupkou, proto zůstává sladká.', 'Manrope 600, 26 / 20 px')]
    ty = ''.join(f'<div><code>{n}<br>{d}</code><{tag}>{e(t)}</{tag.split()[0]}></div>' for n, tag, t, d in types)
    icons = ''.join(f'<span class="icon-tile" title="{k}">{icon(k)}</span>' for k in ICONS)
    body = f'''<section class="section"><div class="container">
 <h1>Styleguide Zumex Česko</h1>
 <p class="lead" style="margin-top:16px">Všechny styly a komponenty webu na jednom místě. Stránky používají jen tokeny z <code>tokens.css</code> a komponenty z <code>components.css</code>.</p>

 <div class="sg-block" style="margin-top:48px"><h2>Barvy</h2><div class="grid grid-4">{sw}</div>
  <p class="small muted" style="margin-top:16px">Akcent je oranžová Zumex na tlačítka, zvýraznění a jeden CTA pruh. Citron a peach jsou doplňkové plochy pro karty a sekce, nikdy pro text ani tlačítka.</p></div>

 <div class="sg-block"><h2>Typografie</h2><div class="sg-type">{ty}</div></div>

 <div class="sg-block"><h2>Mezery, zaoblení a stíny</h2>
  <div class="sg-row">{''.join(f'<div style="text-align:center"><div style="width:{v}px;height:{v}px;background:var(--accent-soft);border-radius:4px;margin:0 auto 6px"></div><span class="caption">{v}</span></div>' for v in [4,8,12,16,24,32,48,64,96])}</div>
  <div class="sg-row" style="margin-top:24px">{''.join(f'<div style="width:110px;height:80px;background:var(--surface);border-radius:var({r});display:grid;place-items:center" class="caption">{r}</div>' for r in ['--r-sm','--r-md','--r-lg','--r-xl','--r-pill'])}</div>
  <div class="sg-row" style="margin-top:24px">{''.join(f'<div style="width:160px;height:90px;background:#fff;border-radius:var(--r-md);box-shadow:var({s});display:grid;place-items:center" class="caption">{s}</div>' for s in ['--shadow-sm','--shadow-md','--shadow-lg'])}</div></div>

 <div class="sg-block"><h2>Tlačítka</h2>
  <div class="sg-row"><a class="btn btn-accent" href="#">Vybrat automatický lis {icon("arrow")}</a><a class="btn btn-primary" href="#">Nezávazná poptávka</a><a class="btn btn-secondary" href="#">Poradit s výběrem</a><a class="btn btn-text" href="#">Detail a parametry {icon("arrow")}</a></div>
  <div class="sg-row" style="margin-top:16px"><a class="btn btn-primary btn-sm" href="#">Malé</a><a class="btn btn-primary" href="#">Střední</a><a class="btn btn-primary btn-lg" href="#">Velké</a><a class="btn btn-primary is-disabled" href="#">Neaktivní</a><span class="icon-btn">{icon("search")}</span></div>
  <div class="sg-row" style="margin-top:16px;background:var(--dark);padding:20px;border-radius:var(--r-lg)"><a class="btn btn-light" href="#">Na tmavé ploše</a><a class="btn btn-ghost-dark" href="#">Obrysové na tmavé</a></div></div>

 <div class="sg-block"><h2>Navigace</h2><p class="small muted" style="margin-bottom:16px">Plovoucí zaoblená lišta, na mobilu hamburger s otevřeným panelem.</p>
  <div style="background:var(--surface);padding:20px;border-radius:var(--r-lg)"><div class="nav" style="position:static">
   <a class="nav-logo" href="#"><img src="assets/logo.webp" alt="Zumex" width="480" height="183"></a>
   <div class="nav-menu" style="display:flex;position:static;box-shadow:none;border:0;flex-direction:row;padding:0;background:none"><a href="#" aria-current="page">Produkty</a><a href="#">Technologie</a><a href="#">Servis a záruka</a><a href="#">Kontakt</a></div>
   <div class="nav-actions"><span class="icon-btn">{icon("search")}</span><a class="btn btn-primary btn-sm" href="#">Nezávazná poptávka</a></div></div></div>
  <div style="max-width:390px;margin-top:16px;background:var(--surface);padding:16px;border-radius:var(--r-lg)">
   <div class="nav" style="padding:8px 8px 8px 18px"><a class="nav-logo" href="#"><img src="assets/logo.webp" alt="" style="height:28px"></a><span class="icon-btn" style="margin-left:auto">{icon("close")}</span></div>
   <div class="nav-menu is-open" style="position:static;display:flex;margin-top:10px;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:12px"><a href="#">Produkty</a><a href="#">Technologie</a><a href="#">Servis a záruka</a><a href="#">Kontakt</a><div class="nav-mobile-cta" style="display:flex"><a class="btn btn-primary" style="width:100%" href="#">Nezávazná poptávka</a></div></div></div></div>

 <div class="sg-block"><h2>Karty</h2>
  <h3 class="h4" style="margin-bottom:12px">Produkt</h3>
  <div class="grid grid-4">{product_card(P["soul-series-2"], p)}{product_card(P["minex"], p, tag="Štítek")}
   <div class="card-product"><div class="card-media is-empty">{icon("image","icon icon-lg")}</div><div class="card-body"><span class="caption">Kategorie</span><h3 class="card-title">Prázdný stav obrázku</h3><p class="card-text">Když produkt zatím nemá fotku.</p></div></div></div>
  <h3 class="h4" style="margin:32px 0 12px">Provoz</h3>
  <div class="grid grid-3"><a class="card-segment" href="#"><div><h3>Kavárny, bary a hotely</h3><p>Od malého baru po snídaňový bufet.</p><span class="btn-text">Objevit lisy {icon("arrow")}</span></div><img src="assets/main0.png" alt=""></a>
   <a class="card-segment card-segment--dark" href="#"><div><h3>Průmyslová výroba šťáv</h3><p>Mytí, lisování, plnění i čištění.</p><span class="btn-text">Průmyslové technologie {icon("arrow")}</span></div><img src="assets/12-0.webp" alt=""></a>
   <div class="card-variant"><div class="card-media"><img src="assets/v4-1.png" alt=""></div><div class="card-body"><h3>Varianta produktu</h3><p>Širší samostatný komplet pro samoobslužný prostor.</p><a class="btn-text" href="#">Poptat variantu {icon("arrow")}</a></div></div></div>
  <h3 class="h4" style="margin:32px 0 12px">Kontakt, technologie, dokument</h3>
  {contact_cards(p)}
  <div class="grid grid-3" style="margin-top:16px"><div class="card"><h3>Conical System®</h3><p>Ovoce se před řezem vystředí, takže řez je přesný a čistý.</p></div>
   <a class="doc" href="#"><span class="icon-tile">{icon("file")}</span><div>Technický list<span>PDF, 1,6 MB</span></div></a>
   <div class="stat"><strong>18 plodů/min</strong><span>Výkon se sadou M/S</span></div></div></div>

 <div class="sg-block"><h2>Formulářové prvky</h2>
  <div class="grid grid-3">
   <div class="field"><label for="sg1">Jméno a firma</label><input class="input" id="sg1" placeholder="Jana Nováková, Kavárna U Lípy"></div>
   <div class="field"><label for="sg2">Typ provozu</label><select class="select" id="sg2"><option>Kavárna nebo bar</option><option>Hotel</option><option>Obchod</option></select></div>
   <div class="field is-error"><label for="sg3">E-mail</label><input class="input" id="sg3" value="jana@"><span class="field-error">Zadejte prosím platný e-mail.</span></div>
   <div class="field" style="grid-column:span 2"><label for="sg4">Zpráva</label><textarea class="textarea" id="sg4" placeholder="Kolik šťávy denně připravujete?"></textarea></div>
   <div class="field"><span class="label">Volby</span><label class="check"><input type="checkbox" checked> Lisy na citrusy</label><label class="check"><input type="checkbox"> Samočisticí lisy</label></div>
   <div class="field"><span class="label">Vyhledávání</span><div class="input-search">{icon("search")}<input class="input" type="search" placeholder="Model, ovoce, použití"></div></div>
   <div class="field" style="grid-column:span 2"><span class="label">Filtry</span><div class="chips"><label class="chip"><input type="checkbox" checked>Lisy na citrusy</label><label class="chip"><input type="checkbox">Samočisticí lisy</label><label class="chip"><input type="checkbox">Cold Press</label></div></div>
  </div></div>

 <div class="sg-block"><h2>Bloky</h2>
  {accordion(SERVICE_ITEMS[:2])}
  <div style="margin-top:24px" class="cta-band"><div><h2>Nevíte, který lis vybrat?</h2><p>Doporučíme konkrétní model a konfiguraci.</p></div><div class="btn-row"><a class="btn btn-primary btn-lg" href="#">{icon("phone")} {PHONE_MAIN[0]}</a><a class="btn btn-secondary btn-lg" href="#">Napsat e-mail</a></div></div>
  <div style="margin-top:16px" class="cta-band cta-band--dark"><div><h2>Tmavá varianta CTA</h2><p>Pro stránky, kde je oranžová už jinde.</p></div><div class="btn-row"><a class="btn btn-accent btn-lg" href="#">Zavolat</a></div></div>
  <div style="margin-top:16px" class="cta-inline"><div><h3 class="h4">Co zvážit při výběru</h3><p class="small muted">Malý CTA blok uvnitř stránky.</p></div><a class="btn btn-primary" href="#">Probrat konfiguraci</a></div>
  <div class="tabs" style="position:static;margin-top:24px"><div class="tabs-inner"><a class="is-active" href="#">Přehled</a><a href="#">Suroviny</a><a href="#">Varianty</a><a href="#">Rozměry</a><a href="#">Parametry</a></div></div>
  <dl class="spec-table" style="margin-top:24px"><div><dt>Výkon</dt><dd>18 plodů/min</dd></div><div><dt>Zásobník</dt><dd>3–6 pomerančů</dd></div><div><dt>Příkon</dt><dd>100 W</dd></div><div><dt>Napájení</dt><dd>100–240 V, 50–60 Hz</dd></div></dl>
  <blockquote class="quote" style="margin-top:28px">Šťáva nepřijde do kontaktu se slupkou, proto zůstává sladká a bez hořkosti.</blockquote>
  <p class="small muted" style="margin-top:20px">Patička je vidět dole na této stránce.</p></div>

 <div class="sg-block"><h2>Ikony a grafika</h2><div class="sg-row">{icons}</div>
  <div class="sg-row" style="margin-top:24px"><img src="assets/logo.webp" alt="" style="height:48px;width:auto"><div style="background:var(--dark);padding:16px 20px;border-radius:var(--r-md)"><img src="assets/logo-white.webp" alt="" style="height:48px;width:auto"></div><img src="assets/vyrobeno-ve-spanelsku.webp" alt="" style="height:110px;width:auto">
   {''.join(f'<img src="assets/ovoce/{f}.svg" alt="" style="height:64px;width:auto">' for f in ["pomeranc","mandarinka","citron","limetka","granatove-jablko","jablko","mrkev","ananas"])}</div>
  <div class="swatches" style="margin-top:28px;justify-content:flex-start"><li style="list-style:none"><span class="swatch" style="background:linear-gradient(90deg,#151515 50%,transparent 50%),radial-gradient(circle,rgba(255,255,255,.4) 1.3px,transparent 1.9px) 0 0/6px 6px,#8b8e91"></span>Black Smoke Grey</li><li style="list-style:none"><span class="swatch" style="background:#f26b21"></span>Pample Orange</li></div></div>

 <div class="sg-block"><h2>Obrazový styl</h2>
  <div class="grid grid-3"><div class="product-media" style="aspect-ratio:1/1"><img src="assets/main0.png" alt=""></div>
   <div class="hero-media" style="aspect-ratio:1/1"><img class="hero-photo" src="assets/hero-soul-sunset.webp" alt=""></div>
   <div class="gallery gallery--single"><figure><img src="assets/g4-0.webp" alt="" style="height:100%;aspect-ratio:1/1"></figure></div></div>
  <p class="small muted" style="margin-top:16px">Produkty vždy na světle šedém podkladu se zaoblením 24 až 36 px. Atmosférické fotky ve stejném zaoblení, bez ztmavujících overlayů.</p></div>
</div></section>
'''
    page('styleguide.html', p, 'Styleguide | Zumex Česko', 'Vizuální systém webu Zumex Česko: barvy, typografie, tlačítka a komponenty.', body)

BUILDERS = {'home': build_home, 'styleguide': build_styleguide, 'catalog': build_catalog, 'details': build_details, 'contact': build_contact, '404': build_404}
if __name__ == '__main__':
    for name, fn in BUILDERS.items():
        if not ONLY or name in ONLY:
            fn()
