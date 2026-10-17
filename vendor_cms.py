"""Fetch a pinned, integrity-checked CMS bundle for same-origin hosting."""
from pathlib import Path
from urllib.request import urlopen
import tarfile,io,hashlib,base64,sys

ROOT=Path(__file__).resolve().parent/'docs'/'admin'
VERSION='0.246.1'
URL=f'https://registry.npmjs.org/@sveltia/cms/-/cms-{VERSION}.tgz'
INTEGRITY='XCVJxKFT6r/LvcozeYGEc+L0pI3bVHq9pknaORGs67eVqGf+Bh0IIul65ZPyEs9jV7x3+E3/mTMo73IUJ/lNvg=='
def main():
    if len(sys.argv)>1:b=Path(sys.argv[1]).read_bytes()
    else:
        with urlopen(URL,timeout=60) as r:b=r.read()
    if base64.b64encode(hashlib.sha512(b).digest()).decode()!=INTEGRITY:raise ValueError('CMS package integrity mismatch')
    count=0
    with tarfile.open(fileobj=io.BytesIO(b),mode='r:gz') as t:
        for member in t.getmembers():
            if not member.isfile():continue
            if member.name.startswith('package/dist/') and member.name.endswith('.js'):
                rel=member.name.removeprefix('package/dist/')
            elif member.name=='package/LICENSE.txt':rel='SVELTIA-LICENSE.txt'
            else:continue
            p=(ROOT/rel).resolve()
            if not p.is_relative_to(ROOT.resolve()):raise ValueError('Invalid package path')
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(t.extractfile(member).read());count+=1
    print(f'Installed Sveltia CMS {VERSION}: {count} local assets; package SHA-512 verified.')
if __name__=='__main__':main()
