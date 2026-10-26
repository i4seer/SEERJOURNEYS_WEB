"""Refresh Journey's web artwork without building or changing the source books.

Requires Pillow, fonttools and beautifulsoup4. Run from this site:
python scripts/sync_journey_artwork.py --source C:/SEERJOURNEYS
"""
from pathlib import Path
import argparse, hashlib, json, re, shutil, sys
from PIL import Image, ImageOps
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.runtime'), str(ROOT.parent / 'SEERWORLDS_WEB/.runtime')]
from bs4 import BeautifulSoup

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def version(p):
    p = p.split('?')[0]
    return p + '?v=' + digest(ROOT / p.lstrip('/'))[:12]

def sync(source, pages_only=False):
    records = []
    if not pages_only:
        for folder in ('covers','scenes','fonts'):
            (ROOT / 'assets' / folder).mkdir(exist_ok=True)
        for n in range(1,11):
            b = source / f'book{n:02}'
            front = b / 'images-print/cover-front.png'
            art = b / 'images-print/background-art-master.png'
            im = Image.open(front).convert('RGB'); im.thumbnail((1280,2048),Image.Resampling.LANCZOS)
            target = ROOT / f'assets/covers/book{n:02}.webp'
            im.save(target,quality=90,method=6)
            # Retain any existing PNG/JPG aliases for external links.
            for ext in ('png','jpg'):
                alias = target.with_suffix('.'+ext)
                if alias.exists(): im.save(alias)
            scene = ImageOps.fit(Image.open(art).convert('RGB'),(1600,1000),Image.Resampling.LANCZOS)
            scene.save(ROOT / f'assets/scenes/book{n:02}.webp',quality=88,method=6)
            if n == 1:
                scene.save(ROOT/'assets/hero-road.webp',quality=90,method=6)
            records.append({'number':n,'cover':f'/assets/covers/book{n:02}.webp','size':list(im.size),
                'source_cover':front.relative_to(source).as_posix(),'source_cover_sha256':digest(front),
                'artwork':f'/assets/scenes/book{n:02}.webp','source_art':art.relative_to(source).as_posix(),
                'source_art_sha256':digest(art)})
        for name in ('journey-wordmark','journey-map-paper'):
            im = Image.open(source/f'assets/{name}.png')
            im.thumbnail((1600,1600),Image.Resampling.LANCZOS)
            im.save(ROOT/f'assets/{name}.webp',quality=92,method=6)
        for name in ('AlfaSlabOne-Regular','Charter-Regular','Charter-Italic'):
            font = TTFont(source/f'fonts/{name}.ttf');font.flavor='woff';font.save(ROOT/f'assets/fonts/{name}.woff')
        for name in ('AlfaSlabOne-OFL.txt','Charter-LICENSE.txt'):
            shutil.copyfile(source/'fonts'/name,ROOT/'assets/fonts'/name)
        for name in ('author','logo'):
            im=Image.open(source/f'assets/{name}.png');im.thumbnail((900,900),Image.Resampling.LANCZOS)
            im.save(ROOT/f'assets/{name}.webp',quality=90,method=6)
        (ROOT/'data/journey-artwork.json').write_text(json.dumps({'source':str(source),'books':records},indent=2)+'\n',encoding='utf-8')
    else:
        records=json.loads((ROOT/'data/journey-artwork.json').read_text())['books']
    # Version the stylesheet's local artwork before versioning HTML references.
    for css in (ROOT/'assets/site.css',ROOT/'assets/journey-cover-theme.css'):
        raw=css.read_text(encoding='utf-8')
        raw=re.sub(r'(/assets/[\w/.-]+\.(?:webp|woff))(?:\?v=[\w]+)?',lambda m:version(m[1]) if (ROOT/m[1].lstrip('/')).exists() else m[0],raw)
        css.write_text(raw,encoding='utf-8',newline='\n')
    for page in ROOT.rglob('*.html'):
        if '.runtime' in page.parts:continue
        soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
        if not soup.select_one('link[data-journey-theme]'):
            link=soup.new_tag('link',rel='stylesheet',href='/assets/journey-cover-theme.css')
            link['data-journey-theme']='';soup.select_one('link[href*="/assets/site.css"]').insert_after(link)
        for img in soup.select('.brand img'):
            img['src']='/assets/journey-wordmark.webp';img['width']=350;img['height']=95
        hero=soup.select_one('.hero h1')
        if hero:
            hero.clear();img=soup.new_tag('img',src='/assets/journey-wordmark.webp',alt='Journey');img['width']=1000;img['height']=273;hero.append(img)
            soup.select_one('.hero-tagline').string='The road did not end.'
        # Shelf visibility follows the verified publication record: books 1–3.
        for shelf in soup.select('.books-row,.books-grid'):
            for card in list(shelf.find_all(recursive=False)):
                image=card.select_one('img[src*="/covers/book"]')
                if image and int(re.search(r'book(\d+)',image['src'])[1])>3:card.decompose()
            if not shelf.find_next_sibling(class_='development-notice'):
                notice=soup.new_tag('aside',attrs={'class':'development-notice'})
                notice.append(BeautifulSoup('<p class="eyebrow">The road continues</p><h3>More books in development</h3><p>Sam’s journey continues beyond the first three books. Further adventures are planned; publication news will appear here.</p><a href="/news/">Follow the news →</a>','html.parser'))
                shelf.insert_after(notice)
        if page==ROOT/'index.html':
            head=soup.select_one('.books-row').parent.select_one('.section-head')
            head.select_one('.eyebrow').string='Published books'
            head.select_one('h2').string='Start where the road begins.'
            for a in head.parent.select('a.text-link'):a.string='View published books →'
        note=soup.select_one('.catalog-note')
        if note:note.string='The first three Journey books are published in Kindle and paperback. Read them in order, beginning with Mile Twenty-Four.'
        # Use each book's own illustration above its detail page.
        cover=soup.select_one('img.book-cover')
        if cover:
            n=int(re.search(r'book(\d+)',cover['src'])[1])
            banner=soup.select_one('.subhero')
            if banner:banner['style']=f'--book-scene:url({version(records[n-1]["artwork"])})'
            duplicate=soup.select_one('.book-info h1')
            if duplicate:duplicate.name='h2'
        nav=soup.select_one('.main-nav');button=soup.select_one('.menu-btn')
        if nav and button:nav['id']='main-navigation';button['aria-controls']='main-navigation'
        theme=soup.select_one('meta[name="theme-color"]')
        if theme:theme['content']='#0c2b1d'
        for img in soup.select('img'):
            path=img.get('src','').split('?')[0]
            if path.startswith('/') and (ROOT/path.lstrip('/')).suffix in ('.webp','.jpg','.png') and (ROOT/path.lstrip('/')).exists():
                with Image.open(ROOT/path.lstrip('/')) as im:img['width'],img['height']=im.size
            img['decoding']='async'
        for tag,attr in [('img','src'),('script','src'),('link','href')]:
            for el in soup.select(f'{tag}[{attr}]'):
                p=el[attr].split('?')[0]
                if p.startswith('/assets/') and (ROOT/p.lstrip('/')).is_file():el[attr]=version(p)
        for el in soup.select('meta[property="og:image"]'):
            url=el['content'];p='/'+url.split('/',3)[-1].split('?')[0]
            if (ROOT/p.lstrip('/')).is_file():el['content']='https://'+(ROOT/'CNAME').read_text().strip()+version(p)
        page.write_text(str(soup),encoding='utf-8',newline='\n')
    print(f'Updated {len(records)} cover designs and all Journey pages.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=Path('C:/SEERJOURNEYS'));parser.add_argument('--pages-only',action='store_true')
    args=parser.parse_args();sync(args.source,args.pages_only)
