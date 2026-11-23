import sys, json, re, os
from bs4 import BeautifulSoup
ROOT = sys.argv[1]; OUT = sys.argv[2]
T = lambda el: re.sub(r'\s+', ' ', el.get_text(' ', strip=True)).strip() if el else ''
A = lambda src: src.split('assets/')[-1] if src else ''
cat = BeautifulSoup(open(f'{ROOT}/produkty/index.html', encoding='utf-8'), 'html.parser')
cards = []
for a in cat.select('a.product-card'):
    cards.append(dict(id=a['href'].split('/')[0], category=a['data-category'], demand=a['data-demand'], business=a['data-business'],
        search=a.get('data-search',''), overline=T(a.select_one('.overline')), name=T(a.find('h3')),
        text=T(a.find('h3').find_next_sibling('p')), img=A(a.find('img')['src']),
        specs=[(T(li.find('span')), T(li.find('strong'))) for li in a.select('.card-specs li')]))
filters = {}
for lab in cat.select('#catalog-filters label'):
    i = lab.find('input')
    if i and i.get('name') in ('category','demand','business'): filters.setdefault(i['name'], []).append((i['value'], T(lab)))
products = []
for c in cards:
    s = BeautifulSoup(open(f'{ROOT}/produkty/{c["id"]}/index.html', encoding='utf-8'), 'html.parser')
    hero = s.select_one('.detail-copy')
    p = dict(id=c['id'], card=c, title=T(s.find('title')), desc=s.find('meta', attrs={'name':'description'})['content'],
        img=A(s.select_one('.detail-photo img')['src']), kategorie=T(hero.select_one('.eyebrow')), name=T(hero.find('h1')),
        claim=T(hero.find('h2')), perex=' '.join(T(x) for x in hero.find_all('p') if not x.get('class')),
        metrics=[(T(d.find('strong')), T(d.find('span'))) for d in s.select('.metrics > div')],
        story=[T(x) for x in s.select('#prehled .product-story p')], feats=[T(x.find('h3')) for x in s.select('#prehled .feature-grid article')],
        gallery=[(A(i['src']), i.get('alt','')) for i in s.select('section.gallery img')],
        variants=[dict(name=T(v.find('h3')), text=T(v.select_one('.variant-description')), img=A(v.find('img')['src']) if v.find('img') else '') for v in s.select('#varianty .variant')],
        params=[(T(d.find('dt')), T(d.find('dd'))) for d in s.select('#parametry dl > div')],
        param_note=T(s.select_one('#parametry p.fine')).replace('Zdroj: Zumex ↗','').strip(),
        source=(s.select_one('#parametry p.fine a') or {}).get('href',''),
        selection=T(s.select_one('#parametry .selection-note p')),
        docs=[(T(a).replace('↗','').replace('↓','').strip(' ·'), a['href'].replace('../../','')) for a in s.select('.doclinks a')],
        tech=[(T(x.find('h3')), T(x.find('p'))) for x in s.select('#technologie article')],
        colors=None, fruit=None, dims=None)
    f = s.select_one('#ovoce')
    if f:
        p['fruit'] = dict(icons=[A(i['src']) for i in f.select('.zx-fruit-icons img')], text=T(f.select_one('.zx-fruit-copy > p:not(.eyebrow):not(.zx-note)')),
            items=[T(li) for li in f.select('.zx-list li')], kits=[(T(d.find('dt')), T(d.find('dd'))) for d in f.select('.zx-kits div')],
            note=T(f.select_one('.zx-note')))
    dm = s.select_one('#rozmery')
    if dm:
        p['dims'] = dict(groups=[dict(name=T(g.find('h3')), rows=[(T(li.find('span')), T(li.find('strong'))) for li in g.select('li')]) for g in dm.select('.zx-dim-group')],
            notes=[T(n) for n in dm.select('.zx-dims-copy .zx-note')],
            drawing=[T(x.find('b')) for x in dm.select('.zx-dim-h, .zx-dim-w')] or None)
    cl = s.select_one('#barvy')
    if cl:
        p['colors'] = dict(sub=T(cl.select_one('.zx-colors-sub')), items=[dict(name=T(li.find('b')), style=li.find('span')['style']) for li in cl.select('.zx-swatches li')])
    products.append(p)
json.dump(dict(products=products, filters=filters), open(OUT,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(products), {k: len(v) for k, v in filters.items()})
print(json.dumps(products[0], ensure_ascii=False)[:1800])
