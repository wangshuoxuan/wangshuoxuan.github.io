"""Supplied photographs with discreet country, city, and landmark captions."""
from html import escape as esc

PHOTOS = {
    'rome': (1024, 683, "意大利 · 罗马 · 古城天际线", "Italy · Rome · Historic skyline", "罗马的穹顶与城市天际线", "Domes and rooftops of Rome"),
    'new-york': (415, 739, "美国 · 纽约 · 帝国大厦", "United States · New York · Empire State Building", "暮色中的纽约天际线", "New York skyline at dusk"),
    'chicago': (810, 1080, "美国 · 芝加哥 · 威利斯大厦", "United States · Chicago · Willis Tower", "暮色中的芝加哥与威利斯大厦", "Chicago and Willis Tower at dusk"),
    'versailles': (597, 335, "法国 · 凡尔赛 · 凡尔赛宫", "France · Versailles · Palace of Versailles", "凡尔赛宫与花园", "Palace and gardens of Versailles"),
    'london': (800, 534, "英国 · 伦敦 · 威斯敏斯特宫与大本钟", "United Kingdom · London · Palace of Westminster and Big Ben", "蓝调时刻的威斯敏斯特宫与大本钟", "Palace of Westminster and Big Ben at blue hour"),
    'paris': (1503, 1200, "法国 · 巴黎 · 协和广场与埃菲尔铁塔", "France · Paris · Place de la Concorde and Eiffel Tower", "日落时的协和广场与埃菲尔铁塔", "Place de la Concorde and Eiffel Tower at sunset"),
    'beijing': (1920, 1080, "中国 · 北京 · 传统城楼与国贸天际线", "China · Beijing · Historic gate and CBD skyline", "秋日银杏、传统城楼与北京现代天际线", "Autumn ginkgo, a historic gate, and the modern Beijing skyline"),
    'fallingwater': (640, 736, "美国 · 米尔伦，宾夕法尼亚州 · 流水别墅", "United States · Mill Run, Pennsylvania · Fallingwater", "秋日林间的流水别墅", "Fallingwater among autumn trees"),
    'kyoto': (600, 399, "日本 · 京都 · 樱花与三重塔", "Japan · Kyoto · Cherry blossoms and pagoda", "樱花掩映中的京都三重塔", "A Kyoto pagoda framed by cherry blossoms"),
    'parthenon': (2048, 966, "希腊 · 雅典 · 帕特农神庙", "Greece · Athens · Parthenon", "雅典帕特农神庙", "The Parthenon in Athens"),
}
PAGE_PHOTOS = {'books': 'kyoto', 'courses': 'versailles', 'videos': 'new-york', 'articles': 'london', 'blog': 'chicago', 'friends': 'beijing'}
ASSETS = {'kyoto': 'assets/places/kyoto-v2.webp', 'parthenon': 'assets/profile.jpg'}

def figure(key, lang, priority=False, src=None):
    w,h,zh,en,alt_zh,alt_en=PHOTOS[key]
    caption=en if lang=='en' else zh
    alt=alt_en if lang=='en' else alt_zh
    source=src or ASSETS.get(key,'assets/places/'+key+'.webp')
    loading='eager' if priority else 'lazy'
    fetch=' fetchpriority="high"' if priority else ''
    image=(f'<img src="{esc(source,quote=True)}" width="{w}" height="{h}" '
           f'alt="{esc(alt,quote=True)}" loading="{loading}" decoding="async"{fetch}>')
    if key=='paris':
        image='<div class="place-photo__paris-frame">'+image+'</div>'
    return '<figure class="place-photo">'+image+'<figcaption>'+esc(caption)+'</figcaption></figure>'

def illustrated_heading(content, page, lang):
    key=PAGE_PHOTOS.get(page)
    if not key:return content
    w,h,*_=PHOTOS[key]
    layout='portrait' if h>w else 'landscape'
    return '<div class="illustrated-heading illustrated-heading--'+layout+'"><div class="illustrated-heading__copy">'+content+'</div>'+figure(key,lang)+'</div>'
