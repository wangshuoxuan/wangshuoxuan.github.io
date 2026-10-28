"""Exercise publishing behavior with temporary test content only."""
from pathlib import Path
import tempfile,shutil,json,unittest
import build

class PublishingTests(unittest.TestCase):
    def test_bilingual_essay_starts_in_english(self):
        source=Path(__file__).resolve().parent/'content/posts/health-for-a-better-life.md'
        if not source.exists():self.skipTest('Published essay not present')
        build.build()
        page=(build.OUT/'post-health-for-a-better-life.html').read_text(encoding='utf-8')
        self.assertIn('data-reading="en"',page)
        self.assertIn('class="post-zh" lang="zh-CN" hidden',page)
        self.assertEqual(page.count('<h1>'),1)
        for view in ['en','zh','both']:
            self.assertIn(f'data-reading="{view}" aria-pressed=',page)
        self.assertIn('RMB 120',page)
        self.assertIn('research group meeting',page)
        self.assertIn('我目前服用',page)
        self.assertIn('<html lang="zh-CN">',page)
        self.assertIn('href="blog.html">我的博客',page)
        self.assertIn('href="post-health-for-a-better-life-en.html" lang="en">English',page)
        english=(build.OUT/'post-health-for-a-better-life-en.html').read_text(encoding='utf-8')
        self.assertIn('<html lang="en">',english)
        self.assertIn('href="blog-en.html">Blog',english)
        self.assertIn('href="post-health-for-a-better-life.html" lang="zh-CN">中文',english)
        self.assertIn('href="post-health-for-a-better-life-en.html"',(build.OUT/'blog-en.html').read_text(encoding='utf-8'))

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        source=Path(__file__).resolve().parent
        shutil.copytree(source/'content',self.root/'content')
        shutil.copytree(source/'docs',self.root/'docs')
        build.ROOT=self.root;build.DATA=self.root/'content';build.OUT=self.root/'docs'
    def tearDown(self):self.tmp.cleanup()
    def write(self,key,entries):
        p=build.DATA/(key+'.json');d=json.loads(p.read_text(encoding='utf-8'));d['entries']=entries
        p.write_text(json.dumps(d),encoding='utf-8')
    def post(self,draft):
        (build.DATA/'posts'/'test-publication.md').write_text('---\ntitle: Test publication\ndate: 2026-10-17\nsummary: Test summary\ncategory: research\nlang: en\ndraft: '+str(draft).lower()+'\n---\n\n## Evidence\n\nA **test** paragraph.\n',encoding='utf-8')
    def test_post_publish_and_withdraw(self):
        self.post(False);build.build()
        self.assertIn('<strong>test</strong>',(build.OUT/'post-test-publication.html').read_text(encoding='utf-8'))
        self.assertIn('Test publication',(build.OUT/'feed.xml').read_text(encoding='utf-8'))
        self.post(True);build.build()
        self.assertFalse((build.OUT/'post-test-publication.html').exists())
        self.assertNotIn('Test publication',(build.OUT/'feed.xml').read_text(encoding='utf-8'))
        self.assertNotIn('Test publication',(build.OUT/'blog.html').read_text(encoding='utf-8'))
    def test_collection_drafts_and_escaping(self):
        self.write('books',[{'category':'computing','title':'<script>test</script>','note':'A & B'},{'category':'computing','title':'PRIVATE_DRAFT','draft':True}])
        s=build.collection('books','zh')
        self.assertIn('&lt;script&gt;test&lt;/script&gt;',s)
        self.assertIn('A &amp; B',s)
        self.assertNotIn('PRIVATE_DRAFT',s)
    def test_simple_reading_links(self):
        self.write('books',[{'title':'Reading website','url':'https://example.org/books','note':'A short recommendation'}])
        page=build.collection('books','zh')
        self.assertIn('href="https://example.org/books"',page)
        self.assertIn('A short recommendation',page)
        self.assertIn('class="category-index"',page)
        self.assertIn('id="cat-general"',page)
    def test_editor_categories_match_public_data(self):
        build.sync_editor()
        config=build.yaml.safe_load((build.OUT/'admin'/'config.yml').read_text(encoding='utf-8'))
        for key in ['books','papers','videos','articles']:
            fields=next(c for c in config['collections'] if c['name']==key)['files'][0]['fields']
            options=next(f for f in next(f for f in fields if f['name']=='entries')['fields'] if f['name']=='category')['options']
            data=json.loads((build.DATA/f'{key}.json').read_text(encoding='utf-8'))
            self.assertEqual([o['value'] for o in options],[c['id'] for c in data['categories']])
    
    def test_bad_category_rejected(self):
        self.write('videos',[{'category':'not-a-category','title':'Test'}])
        with self.assertRaises(ValueError):build.collection('videos','zh')
    def test_quote_needs_source(self):
        self.write('quotes',[{'category':'knowledge','title':'Test','quote':'Test quote'}])
        with self.assertRaises(ValueError):build.collection('quotes','zh')
    def test_unsafe_source_scheme_rejected(self):
        self.write('books',[{'category':'computing','title':'Test','url':'javascript:alert(1)'}])
        with self.assertRaises(ValueError):build.collection('books','zh')
    def test_cms_yaml_frontmatter(self):
        (build.DATA/'posts'/'20261017-120000.md').write_text('---\ntitle: CMS test\ndate: 2026-10-17\nsummary: >-\n  A multiline summary\n  from a visual editor.\ncategory: essay\nlang: zh\ndraft: false\n---\n\n## Body\n\nA paragraph.\n',encoding='utf-8')
        items=build.posts()
        item=next(d for d in items if d['title']=='CMS test')
        self.assertEqual(item['date'],'2026-10-17')
        self.assertEqual(item['summary'],'A multiline summary from a visual editor.')
    def test_question_notebook_and_draft_privacy(self):
        self.write('questions',[{'title':'A question','category':'methods','subjects':['math'],'stage':'exploring','materials':[{'title':'Reference','url':'https://example.org','note':'Helpful'}],'thoughts':'A <thought>','summary':'A synthesis'},{'title':'PRIVATE','category':'methods','draft':True}])
        page=build.collection('questions','zh')
        for expected in ['data-subject="math"','data-stage="exploring"','https://example.org','A &lt;thought&gt;','A synthesis']:
            self.assertIn(expected,page)
        self.assertNotIn('PRIVATE',page)
        self.write('videos',[{'title':'Bad','category':'talks','subjects':['invalid']}])
        with self.assertRaises(ValueError):build.collection('videos','zh')

    def test_profile_updates_home_and_contact(self):
        p=build.DATA/'site.json';d=json.loads(p.read_text(encoding='utf-8'))
        d['zh']['identity']='Test identity'
        p.write_text(json.dumps(d),encoding='utf-8')
        p=build.DATA/'contact.json';d=json.loads(p.read_text(encoding='utf-8'));d['routes'][0]['email']='test@example.org';d['socials'][0]['url']='https://github.com/example';p.write_text(json.dumps(d),encoding='utf-8');build.build()
        home=(build.OUT/'index.html').read_text(encoding='utf-8')
        contact=(build.OUT/'contact.html').read_text(encoding='utf-8')
        self.assertIn('Test identity',home)
        self.assertIn('mailto:test@example.org',contact)
        self.assertIn('href="https://github.com/example"',contact)
        self.assertNotIn('id="projects"',home)
        self.assertNotIn('#projects',home)


    def test_bilingual_toc_language_attributes_and_anchor_targets(self):
        from html.parser import HTMLParser
        import bilingual
        class Nodes(HTMLParser):
            def __init__(self):
                super().__init__(); self.chinese=[]; self.ids=set(); self.links=[]
            def handle_starttag(self,tag,attrs):
                attrs=dict(attrs)
                if 'post-zh' in attrs.get('class','').split():self.chinese.append(attrs)
                if attrs.get('id'):self.ids.add(attrs['id'])
                if tag=='a' and attrs.get('href','').startswith('#'):self.links.append(attrs['href'][1:])
        post={'raw_body':'Intro\n\n## First section\n\n### Detail\n\nText',
              'body_zh':'开头\n\n## 第一节\n\n### 细节\n\n正文'}
        parser=Nodes();parser.feed(bilingual.render(post))
        self.assertTrue(parser.chinese)
        for attrs in parser.chinese:
            self.assertEqual(attrs.get('lang'),'zh-CN')
            self.assertIn('hidden',attrs)
        self.assertTrue(parser.links)
        self.assertTrue(set(parser.links).issubset(parser.ids))

if __name__=='__main__':unittest.main()
