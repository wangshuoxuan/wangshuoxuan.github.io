"""Render bilingual essays with language-aware in-page navigation."""
import re
from html import escape
import markdown


def html(value, lang, section_index, subsection_index):
    rendered = markdown.markdown(value, extensions=['fenced_code', 'tables', 'footnotes'])
    if value.lstrip().startswith('## '):
        rendered = re.sub(
            r'<h2>(.*?)</h2>',
            lambda m: f'<h2 id="{lang}-section-{section_index}">{m.group(1)}</h2>',
            rendered, count=1, flags=re.S
        )
    elif value.lstrip().startswith('### '):
        rendered = re.sub(
            r'<h3>(.*?)</h3>',
            lambda m: f'<h3 id="{lang}-section-{section_index}-sub-{subsection_index}">{m.group(1)}</h3>',
            rendered, count=1, flags=re.S
        )
    return rendered


def chunks(value):
    return re.split(r'(?m)(?=^## )', value.strip())


def heading(section, marker):
    match = re.search(r'(?m)^' + re.escape(marker) + r' (.+)$', section)
    return match.group(1).strip() if match else ''


def toc_side(parts, lang, label):
    items = []
    for section_index, section in enumerate(parts[1:], start=1):
        title = heading(section, '##')
        if not title:
            continue
        title_html = escape(re.sub(r'[*_`]', '', title))
        children = re.findall(r'(?m)^### (.+)$', section)
        child_html = ''
        if children:
            links = []
            for subsection_index, child in enumerate(children, start=1):
                child_title = escape(re.sub(r'[*_`]', '', child.strip()))
                links.append(
                    f'<li><a href="#{lang}-section-{section_index}-sub-{subsection_index}">{child_title}</a></li>'
                )
            child_html = '<ul>' + ''.join(links) + '</ul>'
        items.append(
            f'<li><a href="#{lang}-section-{section_index}">{title_html}</a>{child_html}</li>'
        )
    return f'<div class="post-{"en" if lang == "en" else "zh"}" lang="{"en" if lang == "en" else "zh-CN"}' + (' hidden' if lang == 'zh' else '') + f'><h2>{label}</h2><ol>' + ''.join(items) + '</ol></div>'


def render(post):
    en, zh = chunks(post['raw_body']), chunks(post['body_zh'])
    if len(en) != len(zh):
        raise ValueError('The English and Chinese essays must have matching main sections')

    toc = (
        '<nav class="essay-toc" aria-label="Table of contents">'
        + toc_side(en, 'en', 'Contents · Jump to a section')
        + toc_side(zh, 'zh', '目录 · 选择章节直接阅读')
        + '</nav>'
    )

    pairs = []
    for index, (left, right) in enumerate(zip(en, zh)):
        ls = re.split(r'(?m)(?=^### )', left)
        rs = re.split(r'(?m)(?=^### )', right)
        if len(ls) != len(rs):
            raise ValueError('English and Chinese subsection counts must match')
        blocks = ''.join(
            '<div class="reader-pair"><div class="post-en" lang="en">'
            + html(a, 'en', index, subsection_index)
            + '</div><div class="post-zh" lang="zh-CN" hidden>'
            + html(b, 'zh', index, subsection_index)
            + '</div></div>'
            for subsection_index, (a, b) in enumerate(zip(ls, rs))
        )
        pairs.append(f'<section id="essay-section-{index}">{blocks}</section>')

    controls = '''<div class="reading-controls" role="group" aria-label="Reading language">
<button type="button" data-reading="en" aria-pressed="true">English</button>
<button type="button" data-reading="zh" aria-pressed="false">中文</button>
<button type="button" data-reading="both" aria-pressed="false">英中</button></div>'''
    return controls + toc + ''.join(pairs)


def assets(page):
    page = page.replace('</head>', '<link rel="stylesheet" href="reader.css?v=2">\n</head>')
    page = page.replace('</body>', '<script src="reader.js?v=3" defer></script></body>')
    page = page.replace('<body>', '<body class="essay-page" data-reading="en">')
    return page
