"""Full-frame supplied photographs, with discreet bilingual place captions."""
from html import escape as esc

PHOTOS = {
    'rome': (1024, 683, '罗马 · 意大利', 'Rome · Italy', '罗马的穹顶与城市天际线', 'Domes and rooftops of Rome'),
    'new-york': (415, 739, '纽约 · 美国', 'New York · United States', '暮色中的纽约天际线', 'New York skyline at dusk'),
    'chicago': (810, 1080, '芝加哥 · 美国', 'Chicago · United States', '暮色中的芝加哥与威利斯大厦', 'Chicago and Willis Tower at dusk'),
    'versailles': (597, 335, '凡尔赛 · 法国', 'Versailles · France', '凡尔赛宫与花园', 'Palace and gardens of Versailles'),
    'london': (800, 534, '伦敦 · 英国', 'London · United Kingdom', '蓝调时刻的威斯敏斯特宫与大本钟', 'Palace of Westminster and Big Ben at blue hour'),
    'paris': (1503, 1200, '巴黎 · 法国', 'Paris · France', '日落时的协和广场与埃菲尔铁塔', 'Place de la Concorde and the Eiffel Tower at sunset'),
    'beijing': (1920, 1080, '北京 · 中国', 'Beijing · China', '秋日银杏、传统城楼与北京现代天际线', 'Autumn ginkgo, a historic gate, and the modern Beijing skyline'),
    'fallingwater': (640, 736, '米尔伦，宾夕法尼亚州 · 美国', 'Mill Run, Pennsylvania · United States', '秋日林间的流水别墅', 'Fallingwater among autumn trees'),
    'kyoto': (640, 426, '京都 · 日本', 'Kyoto · Japan', '樱花与京都的朱红色三重塔', 'Cherry blossoms and a vermilion pagoda in Kyoto'),
}
PAGE_PHOTOS = {'books': 'rome', 'courses': 'versailles', 'videos': 'new-york', 'articles': 'london', 'blog': 'fallingwater', 'friends': 'paris'}

def figure(key, lang):
    w,h,zh,en,alt_zh,alt_en=PHOTOS[key]
    caption=en if lang=='en' else zh
    alt=alt_en if lang=='en' else alt_zh
    return (f'<figure class="place-photo"><img src="assets/places/{key}.webp" '
            f'width="{w}" height="{h}" alt="{esc(alt,quote=True)}" loading="lazy" decoding="async">'
            f'<figcaption>{esc(caption)}</figcaption></figure>')

def illustrated_heading(content, page, lang):
    key=PAGE_PHOTOS.get(page)
    if not key:return content
    w,h,*_=PHOTOS[key]
    layout='portrait' if h>w else 'landscape'
    return '<div class="illustrated-heading illustrated-heading--'+layout+'"><div class="illustrated-heading__copy">'+content+'</div>'+figure(key,lang)+'</div>'
