"""Build collection pages and Markdown posts. No remote content is fetched."""
from pathlib import Path
from html import escape as esc
from urllib.parse import urlsplit
from datetime import date
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import markdown
import yaml
import personal

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'docs'
DATA = ROOT / 'content'
BASE = 'https://wangshuoxuan.github.io/'

def site_data():
    path=DATA/'site.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}

def site_contact():
    d=site_data()
    email=d.get('email','2400012712@stu.pku.edu.cn').strip()
    github=d.get('github','https://github.com/wangshuoxuan').strip()
    if not re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+',email):raise ValueError('Enter a valid public email address')
    url(github)
    return email,github

def home_content(lang):
    return personal.home(DATA,lang)
SECTIONS = [
 ('courses','课程','Courses','按学科整理值得学习的课程。','Courses worth studying, organized by subject.'),
 ('books','书籍','Books','书籍与阅读网站，附上一点推荐理由。','Books and reading websites, with a short recommendation.'),
 ('videos','视频','Videos','播客、演讲、课程，以及值得留存的中短视频。','Podcasts, talks, courses, and shorter videos.'),
 ('articles','文章','Articles','来自公众号、博客与开放网络的文章。','Articles from newsletters, blogs, and the open web.'),
 ('papers','论文','Papers','值得阅读的论文与学术资源，附上简短推荐。','Recommended papers and academic resources, with brief notes.'),
 ('questions','感兴趣的问题','Questions','为值得长期追问的问题保留一个位置。','A place for questions worth sustained attention.'),
 ('apps','应用与工具','Apps & tools','按实际用途整理应用、软件与工作流。','Apps, software, and workflows, organized by use.'),
 ('quotes','格言','Quotes','保留原话，也保留出处与理解它的语境。','Quotations, their sources, and the context that gives them meaning.'),
]
NAMES = {x[0]:x for x in SECTIONS}

def text(obj, key, lang):
    value = obj.get(key, '')
    if isinstance(value, dict): return value.get(lang) or value.get('zh') or value.get('en') or ''
    return str(value)

def url(value):
    if not isinstance(value,str) or urlsplit(value).scheme not in ('https','http'):
        raise ValueError('Source links must use http:// or https://')
    return esc(value,quote=True)

def file(key,lang): return key+('-en' if lang=='en' else '')+'.html'

def navigation(lang,current):
    en = lang=='en'
    home = 'en.html' if en else 'index.html'
    groups = [
      ('About','关于我', []),
      ('Writing & thinking','写作与思考',[('blog','我的博客','Blog',file('blog',lang)),('questions','感兴趣的问题','Questions',file('questions',lang)),('thoughts','短文章','Short notes',file('thoughts',lang))]),
      ('Library','收藏与推荐',[(k,z,e,file(k,lang)) for k,z,e,*_ in SECTIONS if k in ['books','videos','articles','courses','apps','quotes']]),
    ]
    parts=[]
    for eg,zg,items in groups:
        links=''.join(f'<a href="{href}"'+(' aria-current="page"' if current==k else '')+f'>{esc(e if en else z)}</a>' for k,z,e,href in items)
        parts.append(f'<div class="nav-group"><a class="nav-label" href="{home}">{eg if en else zg}</a></div>' if not items else f'<div class="nav-group"><div class="nav-label">{eg if en else zg}</div>{links}</div>')
    parts.append(f'<div class="nav-contact"><a href="{file("contact",lang)}"'+(' aria-current="page"' if current=='contact' else '')+f'>{"Contact" if en else "联系我"} <span aria-hidden="true">↗</span></a></div>')
    return '<nav class="nav site-nav" aria-label="'+('Site navigation' if en else '全站目录')+'">'+''.join(parts)+'</nav>'

def shell(key,lang,title,description,body):
    en=lang=='en'
    this = ('en.html' if en else 'index.html') if key=='home' else file(key,lang)
    other = ('index.html' if en else 'en.html') if key=='home' else file(key,'zh' if en else 'en')
    nav=navigation(lang,key)
    name=esc(site_data().get('name_en' if en else 'name_zh','Wangshuoxuan' if en else '王烁瑄'))
    language=f'<a href="{other}" lang="'+('zh-CN">中文' if en else 'en">English')+'</a>'
    footer=f'<footer><span>© 2026 {name}</span><span>'+('A growing personal website' if en else '持续积累，随时修订')+'</span><a href="admin/index.html">'+('Edit site' if en else '管理内容')+f'</a><a href="#main">'+('Back to top ↑' if en else '回到顶部 ↑')+'</a></footer>'
    return f'''<!doctype html>
<html lang="{'en' if en else 'zh-CN'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · {name}</title><meta name="description" content="{esc(description,quote=True)}">
<meta name="theme-color" content="#faf9f6"><link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="styles.css?v={hashlib.sha256((OUT / 'styles.css').read_bytes()).hexdigest()[:12]}"><link rel="alternate" type="application/atom+xml" title="Blog" href="feed.xml">
<link rel="alternate" hreflang="{'zh-CN' if en else 'en'}" href="{other}">
</head><body><a class="skip" href="#main">{'Skip to content' if en else '跳至正文'}</a>
<div class="layout"><header class="sidebar"><a class="wordmark" href="{'en.html' if en else 'index.html'}">{name}<span aria-hidden="true" style="color:var(--accent)">.</span></a><span class="side-caption">A PERSONAL WEBSITE</span>
<div class="desktop-menu">{nav}</div><details class="mobile-menu"><summary>{'Explore this site' if en else '浏览全站目录'} <span>11</span></summary>{nav}</details>
<div class="language">{language}</div><p class="side-note">{'Learning in public' if en else '阅读 · 思考 · 写作'}</p></header>
<main id="main" tabindex="-1">{body}{footer}</main></div></body></html>'''

def heading(title,en_title,description,lang):
    return f'<header class="page-header"><p class="eyebrow">{esc(en_title)}</p><h1>{esc(title)}</h1><p class="page-description">{esc(description)}</p></header>'

def render_item(item,lang,kind):
    title=text(item,'title',lang)
    if not title: raise ValueError('Every entry needs a title')
    source=item.get('url')
    title_html=f'<a href="{url(source)}">{esc(title)} ↗</a>' if source else esc(title)
    meta=[text(item,k,lang) for k in ('creator','year','format','duration','status') if item.get(k)]
    meta_html=f'<p class="meta">{esc(" · ".join(meta))}</p>' if meta else ''
    note=text(item,'note',lang)
    tags=item.get('tags',[])
    if kind=='quotes':
        quote=text(item,'quote',lang)
        if not quote or not source: raise ValueError('Quotes require original text and a source URL')
        quote_html=f'<blockquote>{esc(quote)}</blockquote>'
    else: quote_html=''
    return f'<article class="library-entry"><h3>{title_html}</h3>{meta_html}{quote_html}'+(f'<p>{esc(note)}</p>' if note else '')+(f'<p class="entry-tags">{esc(" · ".join(tags))}</p>' if tags else '')+'</article>'

def collection(key,lang):
    if key in ('videos','questions','articles'):
        _,zh,en,zd,ed=NAMES[key]
        return shell(key,lang,en if lang=='en' else zh,ed if lang=='en' else zd,heading(en if lang=='en' else zh,en,ed if lang=='en' else zd,lang)+personal.collection(DATA,key,lang))
    d=json.loads((DATA/f'{key}.json').read_text(encoding='utf-8'))
    ids=[c['id'] for c in d['categories']]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate category id')
    if any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',i) for i in ids):raise ValueError('Invalid category id')
    if any('draft' in e and not isinstance(e['draft'],bool) for e in d['entries']):raise ValueError('draft must be true or false')
    entries=[e for e in d['entries'] if not e.get('draft',False)]
    if key=='books':
        entries=[dict(e,category=e.get('category') or 'general') for e in entries]
    if any(e.get('category') not in ids for e in entries):raise ValueError('Unknown category')
    en=lang=='en'; _,zh,eng,zd,ed=NAMES[key]
    title=eng if en else zh
    intro=heading(title,eng,ed if en else zd,lang)
    if key=='articles':intro+='<p class="text-links"><a href="'+file('papers',lang)+'">'+('Research papers ↗' if en else '论文 ↗')+'</a></p>'
    count=f'{len(entries)} '+('entries' if en else '条记录')
    intro+=f'<p class="collection-count">{count}</p>'
    intro+='<nav class="category-index" aria-label="'+('Categories' if en else '分类索引')+'">'+''.join(f'<a href="#cat-{c["id"]}">{esc(text(c,"name",lang))}<span>{sum(e["category"]==c["id"] for e in entries)}</span></a>' for c in d['categories'])+'</nav>'
    if not entries:
        intro+='<p class="collection-empty">'+('No personal entries have been added yet. Categories are ready for future additions.' if en else '尚未添加个人条目。分类已备好，后续逐条补充。')+'</p>'
    for c in d['categories']:
        items=[e for e in entries if e['category']==c['id']]
        desc=c.get('description',{}).get(lang,'')
        intro+=f'<section class="library-category" id="cat-{c["id"]}"><div class="section-heading"><h2>{esc(text(c,"name",lang))}</h2><span>{len(items):02}</span></div>'+ (f'<p class="category-description">{esc(desc)}</p>' if desc else '')
        intro+=''.join(render_item(e,lang,key) for e in items)
        intro+='</section>'
    return shell(key,lang,title,ed if en else zd,intro)

def posts():
    result=[]
    for p in sorted((DATA/'posts').glob('*.md')):
        raw=p.read_text(encoding='utf-8')
        if not raw.startswith('---\n'):raise ValueError('Posts need metadata between --- lines')
        front,body=raw[4:].split('\n---\n',1)
        d=yaml.safe_load(front)
        if not isinstance(d,dict):raise ValueError('Invalid post metadata')
        if 'draft' in d and not isinstance(d['draft'],bool):raise ValueError('draft must be true or false')
        if d.get('draft',True):continue
        slug=d.get('slug',p.stem)
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError('Use a lowercase ASCII post slug')
        if any(x['slug']==slug for x in result):raise ValueError('Duplicate post slug')
        if isinstance(d.get('date'),date):d['date']=d['date'].isoformat()[:10]
        date.fromisoformat(d['date'])
        if not d.get('title') or not d.get('summary'):raise ValueError('Published posts need title and summary')
        d.update(slug=slug,body=markdown.markdown(body,extensions=['fenced_code','tables','footnotes','toc']))
        result.append(d)
    return sorted(result,key=lambda d:(d['date'],d['slug']),reverse=True)

def blog(lang,items):
    en=lang=='en'
    title='Blog' if en else '我的博客'
    body=heading(title,'Blog & notes','Essays, research notes, and working thoughts.' if en else '长文、研究笔记与日常思考，都可以从这里开始。',lang)
    body+='<p class="collection-count">'+str(len(items))+(' published posts' if en else '篇已发布文章')+' · <a href="feed.xml">RSS / Atom ↗</a></p>'
    body+='<nav class="category-index" aria-label="Blog categories">'+''.join(f'<a href="#blog-{i}">{esc(label)}</a>' for i,label in enumerate(['研究笔记','随笔','阅读札记','其他写作'] if not en else ['Research notes','Essays','Reading notes','Other writing']))+'</nav>'
    groups=[('research','Research notes' if en else '研究笔记'),('essay','Essays' if en else '随笔'),('reading','Reading notes' if en else '阅读札记'),('other','Other writing' if en else '其他写作')]
    for i,(cat,label) in enumerate(groups):
        body+=f'<section class="library-category" id="blog-{i}"><h2>{label}</h2>'
        filtered=[d for d in items if (d.get('category')==cat or (cat=='other' and d.get('category') not in ['research','essay','reading']))]
        if not filtered:body+='<p class="muted">'+('No posts yet.' if en else '尚未发布文章。')+'</p>'
        for d in filtered:
            body+=f'<article class="library-entry"><p class="meta"><time datetime="{esc(d["date"])}">{esc(d["date"])}</time></p><h3><a href="post-{d["slug"]}.html">{esc(d["title"])}</a></h3><p>{esc(d["summary"])}</p></article>'
        body+='</section>'
    return shell('blog',lang,title,'Essays and notes by Wangshuoxuan.',body)

def feed(items):
    ns='http://www.w3.org/2005/Atom'; ET.register_namespace('',ns)
    root=ET.Element('{'+ns+'}feed')
    def add(node,tag,text):ET.SubElement(node,'{'+ns+'}'+tag).text=text
    add(root,'title','王烁瑄 · Blog');add(root,'id',BASE+'blog.html')
    add(root,'updated',(items[0]['date'] if items else '2026-10-17')+'T00:00:00Z')
    ET.SubElement(root,'{'+ns+'}link',{'rel':'self','href':BASE+'feed.xml'})
    ET.SubElement(root,'{'+ns+'}link',{'href':BASE+'blog.html'})
    author=ET.SubElement(root,'{'+ns+'}author');add(author,'name','王烁瑄')
    for d in items:
        entry=ET.SubElement(root,'{'+ns+'}entry');link=BASE+'post-'+d['slug']+'.html'
        add(entry,'title',d['title']);add(entry,'id',link);add(entry,'updated',d['date']+'T00:00:00Z');add(entry,'summary',d['summary'])
        ET.SubElement(entry,'{'+ns+'}link',{'href':link})
    ET.ElementTree(root).write(OUT/'feed.xml',encoding='utf-8',xml_declaration=True)

def sync_editor():
    """Use content taxonomy for both public sections and CMS choices."""
    import hashlib
    config_path=OUT/'admin'/'config.yml'
    config=yaml.safe_load(config_path.read_text(encoding='utf-8'))
    for collection_config in config['collections']:
        key=collection_config['name']
        if key not in ['books','papers','videos','articles','questions','courses']:continue
        data=json.loads((DATA/f'{key}.json').read_text(encoding='utf-8'))
        fields=collection_config['files'][0]['fields']
        next(f for f in fields if f['name']=='categories')['default']=data['categories']
        entry_fields=next(f for f in fields if f['name']=='entries')['fields']
        next(f for f in entry_fields if f['name']=='category')['options']=[{'value':c['id'],'label':text(c,'name','zh')} for c in data['categories']]
        if key in ('videos','questions','articles'):
            subjects=json.loads((DATA/'subjects.json').read_text(encoding='utf-8'))['subjects']
            next(f for f in entry_fields if f['name']=='subjects')['options']=[{'value':c['id'],'label':text(c,'name','zh')} for c in subjects]
    config_text=yaml.safe_dump(config,allow_unicode=True,sort_keys=False)
    config_path.write_text(config_text,encoding='utf-8')
    version=hashlib.sha256(config_text.encode()).hexdigest()[:12]
    p=OUT/'admin'/'index.html'
    html=p.read_text(encoding='utf-8')
    html=re.sub(r'href="config.yml\?v=[^"]+"',f'href="config.yml?v={version}"',html)
    p.write_text(html,encoding='utf-8')

def build():
    OUT.mkdir(exist_ok=True)
    for p in OUT.glob('post-*.html'):p.unlink() # generated post output only; remove unpublished drafts
    for lang in ('zh','en'):
        source=home_content(lang)
        (OUT/('en.html' if lang=='en' else 'index.html')).write_text(shell('home',lang,'Home' if lang=='en' else '首页','Personal website of Wangshuoxuan.',source),encoding='utf-8')
        for key,*_ in SECTIONS:(OUT/file(key,lang)).write_text(collection(key,lang),encoding='utf-8')
        en=lang=='en'
        title='Contact' if en else '联系我'
        body=heading(title,'Contact','Say hello. Let’s get to know each other.' if en else '欢迎认识我，也让我认识你。',lang)
        body+=personal.contacts(DATA,lang)
        (OUT/file('contact',lang)).write_text(shell('contact',lang,title,'Contact Wangshuoxuan.',body),encoding='utf-8')
    for lang in ('zh','en'):
        (OUT/file('cv',lang)).write_text(shell('home',lang,'About' if lang=='en' else '关于我','Personal profile',home_content(lang)),encoding='utf-8')
    for lang in ('zh','en'):
        title='Short notes' if lang=='en' else '短文章'
        (OUT/file('thoughts',lang)).write_text(shell('thoughts',lang,title,title,heading(title,'Short notes','Brief thoughts, recorded and revisited.' if lang=='en' else '简短地记录想法，也为之后的思考留白。',lang)+personal.thoughts(DATA,lang)),encoding='utf-8')
    items=posts()
    for lang in ('zh','en'):(OUT/file('blog',lang)).write_text(blog(lang,items),encoding='utf-8')
    for d in items:
        lang=d.get('lang','zh');en=lang=='en'
        body=f'<header class="page-header"><a href="{file("blog",lang)}">← '+('Blog' if en else '返回博客')+f'</a><h1>{esc(d["title"])}</h1><p class="meta"><time datetime="{d["date"]}">{d["date"]}</time></p></header><article class="prose">{d["body"]}</article>'
        page=shell('blog',lang,d['title'],d['summary'],body)
        # A post has no translated counterpart unless its author writes one.
        page=re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">','',page)
        page=page.replace('class="language"','class="language no-print"')
        (OUT/f'post-{d["slug"]}.html').write_text(page,encoding='utf-8')
    feed(items)
    sync_editor()
    print(f'Built {len(list(OUT.glob("*.html")))} pages and {len(items)} published posts.')

if __name__=='__main__':build()
