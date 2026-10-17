"""Personal profile, contact routes, and browsable learning collections."""
import json
from html import escape as esc
from urllib.parse import urlsplit

STAGES = [('open','待探索','Open'),('exploring','正在探索','Exploring'),('synthesis','形成初步认识','Initial synthesis'),('revisiting','持续修订','Revisiting')]

def read(data, name):
    return json.loads((data/name).read_text(encoding='utf-8'))

def localized(value, lang):
    return value.get(lang) or value.get('zh') or value.get('en') or '' if isinstance(value,dict) else str(value or '')

def link(value):
    if urlsplit(value).scheme not in ('https','http') or not urlsplit(value).netloc:
        raise ValueError('Enter a complete http(s) link')
    return esc(value,quote=True)

def paragraph(value):
    return ''.join('<p>'+esc(p).replace('\n','<br>')+'</p>' for p in str(value or '').split('\n\n') if p.strip())

def home(data, lang):
    d=read(data,'site.json');p=d[lang];en=lang=='en'
    avatar=d.get('avatar','assets/profile.jpg')
    if avatar.startswith('/') and not avatar.startswith('//'):avatar=avatar[1:]
    if not avatar.startswith('assets/') or '..' in avatar:raise ValueError('Profile image must be in assets/')
    name=d['name_en' if en else 'name_zh']
    b=f'<section class="profile-hero" id="about"><img class="profile-avatar" src="{esc(avatar,quote=True)}" width="2048" height="966" alt="'+('Personal profile image' if en else '个人头像')+f'"><div><p class="eyebrow">LEARN · THINK · EXPLORE · DEEPEN</p><h1>{esc(name)}</h1><p class="identity">{esc(p["identity"])}</p></div></section>'
    b+=f'<p class="profile-lead">{esc(p.get("lead",""))}</p>'+p.get('introduction','')
    b+='<div class="text-links"><a href="'+('blog-en.html' if en else 'blog.html')+'">'+('My writing ↗' if en else '读我的博客 ↗')+'</a><a href="'+('contact-en.html' if en else 'contact.html')+'">'+('Get in touch ↗' if en else '联系我 ↗')+'</a></div>'
    for key,anchor,zh,eng,kind in [('education','education','学业经历','Education','records'),('honors','honors','所获荣誉','Honors','records'),('disciplines','interests','学科兴趣','Academic interests','chips'),('research_summary','research','研究兴趣','Research interests','text'),('hobbies','life','生活与爱好','Beyond study','chips')]:
        if not p.get(key):continue
        b+=f'<section class="profile-section" id="{anchor}"><p class="eyebrow">{eng.upper()}</p><h2>{eng if en else zh}</h2>'
        if kind=='text':b+='<p>'+esc(p[key])+'</p>'
        else:b+='<ul class="'+('profile-records' if kind=='records' else 'interest-list')+'">'+''.join('<li>'+esc(v)+'</li>' for v in p[key])+'</ul>'
        b+='</section>'
    return b

def contacts(data,lang):
    d=read(data,'contact.json');en=lang=='en';b=paragraph(localized(d['intro'],lang))
    primary_email=next((x.get('email') for x in d['routes'] if x.get('email')),'')
    b+='<div class="contact-card"><strong>'+('WeChat' if en else '微信')+'</strong><p>'+esc(next((x.get('value','') for x in d['socials'] if x['name']=='微信'),''))+'</p><strong>'+('Email' if en else '邮箱')+'</strong><p><a href="mailto:'+esc(primary_email,quote=True)+'">'+esc(primary_email)+'</a></p></div>'
    routes=[]
    for item in d['routes']:
        email=(item.get('email') or '').strip();u=(item.get('form_url') or '').strip()
        if not email and not u:continue
        card='<article class="contact-card"><h2>'+esc(localized(item['name'],lang))+'</h2>'+paragraph(localized(item.get('description',''),lang))
        if email:
            import re
            if not re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+',email):raise ValueError('Invalid contact email')
            # The shared email is displayed once above the contact topics.
        if u:card+='<p><a href="'+link(u)+'">'+('Open contact form ↗' if en else '填写联系表单 ↗')+'</a></p>'
        routes.append(card+'</article>')
    b+='<div class="contact-grid">'+''.join(routes)+'</div>'
    social=[]
    for item in d['socials']:
        if item['name']=='微信':continue
        value=(item.get('value') or '').strip();u=(item.get('url') or '').strip()
        if not value and not u:continue
        label=esc(item['name']);v=esc(value or item['name'])
        social.append('<div class="social-line"><strong>'+label+'</strong>'+('<a href="'+link(u)+'">'+v+' ↗</a>' if u else '<span>'+v+'</span>')+'</div>')
    if social:b+='<section class="profile-section"><h2>'+('Elsewhere' if en else '也可以在这里找到我')+'</h2>'+''.join(social)+'</section>'
    if d.get('first_message'):b+='<section class="profile-section"><h2>'+('A simple way to start' if en else '从一句问候开始')+'</h2>'+paragraph(localized(d['first_message'],lang))+'</section>'
    return b

def collection(data,key,lang):
    d=read(data,key+'.json');en=lang=='en';subjects=read(data,'media-subjects.json' if key in ('articles','videos') else 'subjects.json')['subjects']
    if key=='articles':
        papers=read(data,'papers.json')
        mapping={'electronics':'engineering','math':'natural','economics':'social','social':'social','natural':'natural','methods':'interdisciplinary'}
        d['entries']=d['entries']+[dict(e,category='papers',subjects=e.get('subjects') or [mapping.get(e.get('category'),'interdisciplinary')]) for e in papers['entries']]
    categories={x['id']:localized(x['name'],lang) for x in d['categories']}
    subject_names={x['id']:localized(x['name'],lang) for x in subjects}
    stages={a:c if en else b for a,b,c in STAGES}
    entries=[]
    for e in d['entries']:
        if 'draft' in e and not isinstance(e['draft'],bool):raise ValueError('draft must be boolean')
        if e.get('draft',False):continue
        if e.get('category') not in categories:raise ValueError('Unknown category')
        if not isinstance(e.get('subjects',[]),list) or any(s not in subject_names for s in e.get('subjects',[])):raise ValueError('Unknown subject')
        if key=='questions' and e.get('stage','open') not in stages:raise ValueError('Unknown question stage')
        entries.append(e)
    def select(name,label,options):
        return '<label>'+label+f'<select data-filter="{name}"><option value="">'+('All' if en else '全部')+'</option>'+''.join(f'<option value="{esc(k,quote=True)}">{esc(v)}</option>' for k,v in options.items())+'</select></label>'
    b='<div class="filters" hidden>'+select('subject','Subject' if en else '学科',subject_names)+select('category',('Format' if en else ('媒介类型' if key=='articles' else '内容形式')) if key in ('videos','articles') else ('Topic' if en else '问题主题'),categories)
    if key=='questions':b+=select('stage','Stage' if en else '探索状态',stages)
    b+='<button type="button" data-reset>'+(('Back to start' if en else '回到起始') if key in ('articles','videos') else ('Reset' if en else '重置'))+'</button></div>'
    b+=f'<p class="collection-count" data-count aria-live="polite">{len(entries)} '+('entries' if en else '条内容')+'</p><div class="filtered-list">'
    grouped=key in ('videos','articles')
    if grouped:
        entries.sort(key=lambda e:list(subject_names).index((e.get('subjects') or ['interdisciplinary'])[0]))
    group=None
    for e in entries:
        if grouped:
            primary=(e.get('subjects') or ['interdisciplinary'])[0]
            if primary!=group:
                if group is not None:b+='</section>'
                group=primary
                b+='<section data-subject-group><h2>'+esc(subject_names[group])+'</h2>'
        title=localized(e.get('title'),lang)
        if not title:raise ValueError('Every entry needs a title')
        cat=e['category'];sub=e.get('subjects') or (['interdisciplinary'] if grouped else []);stage=e.get('stage','open')
        b+=f'<article class="resource-card" data-entry data-category="{esc(cat,quote=True)}" data-subject="{esc(" ".join(sub),quote=True)}" data-stage="{esc(stage,quote=True)}">'
        labels=[categories[cat]]+[subject_names[s] for s in sub]
        if key=='questions':labels.append(stages[stage])
        b+='<div class="entry-labels">'+''.join('<span>'+esc(v)+'</span>' for v in labels)+'</div><h2>'
        b+=('<a href="'+link(e['url'])+'">'+esc(title)+' ↗</a>' if e.get('url') else esc(title))+'</h2>'
        b+=paragraph(localized(e.get('note',''),lang))
        if key=='questions':
            b+='<details class="question-notebook"><summary>'+('Materials, reflections & synthesis' if en else '参考材料 · 我的思考 · 总结心得')+'</summary><h3>'+('Reference materials' if en else '参考材料')+'</h3>'
            materials=e.get('materials',[])
            if materials:
                b+='<ul>'+''.join('<li><a href="'+link(m['url'])+'">'+esc(m['title'])+' ↗</a>'+paragraph(m.get('note',''))+'</li>' for m in materials)+'</ul>'
            else:b+='<p class="muted">'+('Materials will be added here.' if en else '参考材料陆续补充。')+'</p>'
            for field,zh,english in [('thoughts','我的思考','My reflections'),('summary','总结心得','Working synthesis')]:
                b+='<h3>'+ (english if en else zh)+'</h3>'+paragraph(e.get(field,'') or ('Notes will grow here.' if en else '留待继续思考与记录。'))
            b+='</details>'
        b+='</article>'
    if group is not None:b+='</section>'
    b+='</div><p class="collection-empty" data-empty'+(' hidden' if entries else '')+'>'+('No matching entries yet.' if en else '这里还没有符合条件的内容，后续会逐步补充。')+'</p><script src="browse.js?v=broad-subjects-3" defer></script>'
    return b


def thoughts(data,lang):
    entries=[e for e in read(data,'thoughts.json')['entries'] if not e.get('draft',True)]
    entries.sort(key=lambda e:e.get('date',''),reverse=True)
    if not entries:return '<p class="collection-empty">'+('Notes will appear here.' if lang=='en' else '新的想法，会陆续记录在这里。')+'</p>'
    b='<div class="short-notes">'
    for e in entries:
        b+='<article class="short-note"><p class="meta">'+esc(e.get('date',''))+'</p>'+paragraph(localized(e.get('body',''),lang))+'</article>'
    return b+'</div>'
