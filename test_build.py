"""Exercise publishing behavior with temporary test content only."""
from pathlib import Path
import tempfile,shutil,json,unittest
import build

class PublishingTests(unittest.TestCase):
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
    def test_bad_category_rejected(self):
        self.write('books',[{'category':'not-a-category','title':'Test'}])
        with self.assertRaises(ValueError):build.collection('books','zh')
    def test_quote_needs_source(self):
        self.write('quotes',[{'category':'knowledge','title':'Test','quote':'Test quote'}])
        with self.assertRaises(ValueError):build.collection('quotes','zh')
    def test_unsafe_source_scheme_rejected(self):
        self.write('books',[{'category':'computing','title':'Test','url':'javascript:alert(1)'}])
        with self.assertRaises(ValueError):build.collection('books','zh')

if __name__=='__main__':unittest.main()
