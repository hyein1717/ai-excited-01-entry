import os, math, struct, zlib
W=H=1024
S=2
N=W*S
buf=bytearray(N*N*3)
for y in range(N):
 for x in range(N):
  g=math.exp(-(((x/S-500)/420)**2+((y/S-410)/510)**2)*2)
  i=(y*N+x)*3
  buf[i:i+3]=bytes((int(4+9*g),int(30+43*g),int(37+47*g)))
def poly(points,c):
 p=[(x*S,y*S) for x,y in points]
 for y in range(max(0,int(min(v[1] for v in p))),min(N,int(max(v[1] for v in p))+1)):
  xs=[]
  for a,b in zip(p,p[1:]+p[:1]):
   if (a[1]<=y+.5<b[1]) or (b[1]<=y+.5<a[1]): xs.append(a[0]+(y+.5-a[1])*(b[0]-a[0])/(b[1]-a[1]))
  xs.sort()
  for l,r in zip(xs[::2],xs[1::2]):
   l=max(0,int(l));r=min(N,int(r)+1)
   buf[(y*N+l)*3:(y*N+r)*3]=bytes(c)*(r-l)
def ellipse(cx,cy,rx,ry,c):
 poly([(cx+rx*math.cos(i*math.tau/100),cy+ry*math.sin(i*math.tau/100)) for i in range(100)],c)
def curve(points,steps=16):
 out=[]
 for i in range(len(points)-1):
  a=points[max(0,i-1)];b=points[i];c=points[i+1];d=points[min(len(points)-1,i+2)]
  for j in range(steps):
   t=j/steps
   out.append(tuple(.5*((2*b[k])+(-a[k]+c[k])*t+(2*a[k]-5*b[k]+4*c[k]-d[k])*t*t+(-a[k]+3*b[k]-3*c[k]+d[k])*t*t*t) for k in (0,1)))
 return out+[points[-1]]
def shape(p,c):poly(curve(p),c)
ellipse(512,904,151,19,(5,23,28))
# enormous ascending whale
body=[(505,786),(457,676),(389,558),(337,424),(324,279),(346,174),(398,116),(472,104),(539,140),(577,220),(589,332),(572,458),(549,590),(538,710),(533,786)]
shape(body,(239,161,77))
shape([(x+5,y+3) for x,y in body],(27,103,131))
shape([(402,135),(368,230),(371,355),(409,487),(470,612),(511,760),(506,608),(468,449),(445,301),(450,169)],(44,137,159))
shape([(536,169),(563,273),(556,410),(524,550),(521,669),(495,560),(477,407),(486,275)],(17,70,94))
# broad flippers
shape([(416,433),(346,476),(245,576),(189,601),(219,536),(314,429),(370,396)],(240,166,82))
shape([(416,434),(342,484),(247,575),(201,593),(235,536),(325,436),(373,405)],(30,107,132))
shape([(551,419),(635,461),(702,555),(702,582),(659,562),(574,505),(537,474)],(19,72,95))
ellipse(502,237,7,8,(4,27,34));ellipse(504,235,2,2,(254,219,153))
shape([(349,262),(392,285),(452,288),(513,270),(470,300),(401,304)],(12,59,78))
# Refined warm shoulder reflection and distant spray.
shape([(352,183),(337,274),(347,370),(369,416),(357,332),(355,247),(372,174)],(102,174,177))
for x,y,r in [(391,680,3),(633,713,3),(590,670,3),(435,658,3)]:ellipse(x,y,r,r*1.8,(172,223,218))
# bowl glass and water
ellipse(512,798,87,15,(167,220,217))
shape([(427,799),(434,856),(465,891),(512,901),(559,891),(590,856),(597,799),(568,819),(455,819)],(55,119,133))
ellipse(512,810,79,14,(42,159,174))
shape([(440,830),(454,870),(480,882),(470,872),(456,832)],(176,226,223))
shape([(583,829),(571,870),(551,882),(560,866),(571,831)],(102,183,190))
ellipse(512,799,88,13,(186,233,227));ellipse(512,800,80,8,(23,103,120))
# splash crown
for p in [[(470,800),(444,752),(421,738),(448,778),(450,804)],[(493,803),(476,739),(461,716),(469,765),(476,806)],[(535,803),(554,745),(578,722),(563,773),(557,806)],[(563,803),(592,769),(616,764),(594,786),(580,808)]]:shape(p,(222,246,235))
for x,y,r in [(425,719,6),(454,691,5),(584,700,7),(610,744,5),(404,760,4),(552,719,4)]:ellipse(x,y,r,r*1.7,(232,249,239))
# encode filtered RGB PNG
raw=bytearray()
for y in range(H):
 raw.append(0)
 for x in range(W):
  for c in range(3):raw.append(sum(buf[((y*S+dy)*N+x*S+dx)*3+c] for dy in range(S) for dx in range(S))//4)
def chunk(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
out=os.environ.get('MAKEFUN_OUTPUT_DIR','/output');os.makedirs(out,exist_ok=True)
open(os.path.join(out,'entry.png'),'wb').write(png)
