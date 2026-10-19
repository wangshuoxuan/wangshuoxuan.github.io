"""Render bilingual essays from two editable Markdown bodies."""
import re
from html import escape
import markdown

def html(value):
    return markdown.markdown(value, extensions=['fenced_code','tables','footnotes'])

def chunks(value):
    return re.split(r'(?m)(?=^## )', value.strip())

def render(post):
    en, zh = chunks(post['raw_body']), chunks(post['body_zh'])
    if len(en) != len(zh):
        raise ValueError('The English and Chinese essays must have matching main sections')
    pairs=[]
    for index,(left,right) in enumerate(zip(en,zh)):
        ls=re.split(r'(?m)(?=^### )',left)
        rs=re.split(r'(?m)(?=^### )',right)
        if len(ls)!=len(rs):
            raise ValueError('English and Chinese subsection counts must match')
        blocks=''.join('<div class="reader-pair"><div class="post-en" lang="en">'+html(a)+'</div><div class="post-zh" lang="zh-CN" hidden>'+html(b)+'</div></div>' for a,b in zip(ls,rs))
        pairs.append(f'<section id="essay-section-{index}">{blocks}</section>')
    return '''<div class="reading-controls" role="group" aria-label="Reading language">
<button type="button" data-reading="en" aria-pressed="true">English</button>
<button type="button" data-reading="zh" aria-pressed="false">中文</button>
<button type="button" data-reading="both" aria-pressed="false">英中</button></div>'''+''.join(pairs)

def assets(page):
    page=page.replace('</head>','<link rel="stylesheet" href="reader.css?v=1">\n</head>')
    page=page.replace('</body>','<script src="reader.js?v=1" defer></script></body>')
    page=page.replace('<body>','<body class="essay-page" data-reading="en">')
    page=re.sub(r'<div class="language(?: no-print)?">.*?</div>','',page)
    return page
