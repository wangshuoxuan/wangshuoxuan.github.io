"""Validate generated local links, section targets, and feed syntax."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent/'docs'
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__();self.path=path;self.ids=set();self.refs=[];self.h1=0;self.lang=None
        self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if 'id' in a:
            assert a['id'] not in self.ids, f'{self.path.name}: duplicate id {a["id"]}'
            self.ids.add(a['id'])
        for key in ('href','src'):
            if key in a:self.refs.append(a[key])

pages={p.resolve():Page(p) for p in ROOT.rglob('*.html')}
checked=0
for path,p in pages.items():
    assert p.h1==1 and p.lang, f'{path.name}: missing language or invalid h1 count'
    for ref in p.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=(path if not u.path else path.parent/unquote(u.path)).resolve()
        assert target.is_relative_to(ROOT.resolve()), f'Link outside site: {ref}'
        assert target.is_file(), f'{path.name}: missing target {ref}'
        if u.fragment and target in pages:
            assert unquote(u.fragment) in pages[target].ids, f'{path.name}: missing anchor {ref}'
        checked+=1
ET.parse(ROOT/'feed.xml')
print(f'Validated {len(pages)} HTML pages, {checked} local references and Atom feed.')
