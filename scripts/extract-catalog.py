from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import re,json
root=Path(__file__).resolve().parents[1]
class N:
 def __init__(self,tag='',attrs=(),parent=None):self.tag=tag;self.a=dict(attrs);self.children=[];self.parent=parent
 def text(self):return ''.join(c if isinstance(c,str) else c.text() for c in self.children).strip()
 def all(self,pred):
  out=[]
  for c in self.children:
   if isinstance(c,N):
    if pred(c):out.append(c)
    out+=c.all(pred)
  return out
 def cls(self,s):return s in self.a.get('class','').split()
class P(HTMLParser):
 def __init__(self,t):super().__init__(convert_charrefs=True);self.root=N();self.cur=self.root;self.feed(t)
 def handle_starttag(self,t,a):
  n=N(t,a,self.cur);self.cur.children.append(n)
  if t not in ['img','input','meta','link','br','hr','source','area','wbr']:self.cur=n
 def handle_endtag(self,t):
  n=self.cur
  while n.parent and n.tag!=t:n=n.parent
  if n.parent:self.cur=n.parent
 def handle_data(self,d):self.cur.children.append(d)
def first(n,p):return next(iter(n.all(p)),None)
def txt(n,p,default=''):
 x=first(n,p);return x.text() if x else default
categories=[]
custom=P((root/'customizer.html').read_text()).root
for i,card in enumerate(custom.all(lambda n:n.cls('gift-category-card'))):
 route=card.a['href'].removesuffix('.html')
 if route=='wooden-gift-1594':route='wooden-table-top-gifts'
 categories.append(dict(id=route,route=route,name=txt(card,lambda n:n.tag=='h3'),description=txt(card,lambda n:n.tag=='p'),active=True,sortOrder=i,version=1))
# Normalize the two historical wooden gift category URLs into the existing wooden gifts collection.
catroutes={c['route']:c['id'] for c in categories}
catroutes.update({'heart-wooden-gifts':'wooden-table-top-gifts','round-wooden-gifts':'wooden-table-top-gifts'})
products={};route_map={}
wood=json.loads(re.search(r'const jrProducts = (\[.*?\]);',(root/'product-view.js').read_text()).group(1))
for path in sorted(root.glob('*.html')):
 t=path.read_text();doc=P(t).root;shop=first(doc,lambda n:n.cls('jr-shop'))
 if not shop:continue
 a=shop.a;code=a.get('data-code',a.get('data-product',''))
 if not code:continue
 crumb=first(doc,lambda n:n.cls('breadcrumbs'))
 links=crumb.all(lambda n:n.tag=='a') if crumb else []
 category_route=(links[-1].a['href'].removesuffix('.html') if links else '')
 category=catroutes.get(category_route)
 if not category:raise Exception((path.name,category_route))
 if a.get('data-product'):
  w=next(x for x in wood if x['code']==code);vs=[dict(code=v['code'],size=v['size'],price=v['price'],courier=v['delivery'],image={'url':'/'+v['image']}) for v in wood if v['shape']==w['shape']]
  name=w['name'];size=w['size'];price=w['price'];courier=w['delivery'];image={'url':'/'+w['image']}
 else:
  vs=json.loads(a.get('data-variants','[]'));vs=[dict(code=str(v['code']),size=v['size'],price=v['price'],courier=v['delivery']) for v in vs]
  name=a['data-name'];size=a['data-size'];price=float(a['data-price']);courier=float(a['data-delivery'])
  photo=first(shop,lambda n:n.cls('mdf-photo') or n.cls('calendar-photo'))
  image={'cssClass':photo.a['class']} if photo else {'url':first(shop,lambda n:n.tag=='img').a['src']}
 if not vs:vs=[dict(code=code,size=size,price=price,courier=courier)]
 identity=vs[0]['code']
 if identity not in products:
  paras=shop.all(lambda n:n.tag=='p');desc=next((p.text() for p in paras if p.text().startswith(('A personalized','Your portrait','Create a'))),'')
  specs={}
  for dl in shop.all(lambda n:n.tag=='dl'):
   for row in dl.all(lambda n:n.tag=='div'):
    dt=first(row,lambda n:n.tag=='dt');dd=first(row,lambda n:n.tag=='dd')
    if dt and dd:specs[dt.text()]=dd.text()
  products[identity]=dict(id=identity,code=identity,name=name,category=category,description=desc or 'Personalized with your photos. Contact JR Captures to confirm your design.',price=vs[0]['price'],courier=vs[0]['courier'],size=vs[0]['size'],dispatch=specs.get('Dispatch time','Same day'),material=specs.get('Material',specs.get('Product features','')),variants=vs,image=image,route=path.stem,aliases=[],active=True,deleted=False,sortOrder=len(products),version=1)
 products[identity]['aliases'].append(path.stem)
 route_map[path.stem]=identity
seed={'categories':categories,'products':list(products.values())}
(root/'scripts/catalog-import.json').write_text(json.dumps(seed,ensure_ascii=False,indent=2))
print(json.dumps({'products':len(products),'categories':len(categories),'legacy_product_routes':len(route_map)}))
