import os,sys,json,subprocess,numpy as np,soundfile as sf,soxr
LIB=os.environ.get('LIB',os.path.expanduser('~/lemo-opuscar'));sys.path.insert(0,LIB)
from core.audio.sfx import SR,add,bp,lp,hp,compress,limit
from core.audio import sampler as S
H=os.path.dirname(os.path.abspath(__file__));E=json.load(open(H+'/events.json'));DUR=139.4;N=int(DUR*SR);rng=np.random.default_rng(7)
tr=[e for e in E['ev'] if e['type']=='track'][0]['data']
T=np.arange(N)/SR;V=np.interp(T,[r[0] for r in tr],[r[1] for r in tr])
from scipy.ndimage import uniform_filter1d
sm=lambda x,ms:uniform_filter1d(np.asarray(x,float),max(1,int(SR*ms/1000)))
# voix
raw=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',H+'/../audio/La_Machine.mp3','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)
y=hp(raw[:int(137.3*SR)].astype(float),75,2);y=compress(y/np.abs(y).max(),thr=.25,ratio=3,att=.005,rel=.12);y=y/np.abs(y).max()*.62
vo=np.zeros(N);vo[:len(y)]=y[:N];duck=sm((sm(np.abs(vo),80)>.012).astype(float),350)
# plume
w=rng.standard_normal(N);a=sm(np.clip(V/900,0,1.4)**.5,40);pen=lp(a*(bp(w,2000,7000,2)*.6+bp(w,600,2200,2)*.5),8500,2)*.045
# violoncelles : une ligne, ré mineur, qui se tend puis se relâche
n=[];L=lambda t,p,d,v=.42:n.append((t,'cellos',p,d,v,0.0))
for t,p,d,v in [(8,'A2',4,.35),(12,'D3',3.4,.42),(15.4,'F3',2.2,.45),(17.5,'A3',2.3,.5),(19.8,'C4',2.6,.55),(22.4,'Bb2',1.6,.35),(24.1,'C#3',3.2,.4),(27.2,'D3',3.4,.35),(31,'A2',3.6,.38),(34.8,'C3',3,.4),(37.8,'D3',2.6,.42),(40.4,'E3',2.2,.48),(43.9,'F3',4.4,.42),(48.7,'E3',4.2,.42),(53,'D3',2.2,.42),(55.2,'C#3',3.4,.42),(59,'A2',2.6,.45),(61.4,'A3',4,.52),(65.8,'G3',4,.46),(71.6,'D3',3.4,.36),(75.1,'Eb3',2.2,.36),(79,'D3',3.2,.36),(82.3,'Eb3',2,.42),(84.4,'G#2',3.4,.52),(87.2,'C#3',1.7,.5),(90.8,'A2',3,.4),(93.9,'C3',3.2,.42),(97.4,'E3',3.4,.45),(101.2,'G3',2.4,.5),(103.7,'F3',1.7,.42),(105.5,'E3',1.5,.4),(108.8,'D3',3.2,.5),(112.7,'A2',3.4,.4),(116.4,'C3',3.8,.42),(120.4,'D3',2.4,.46),(122.8,'F3',3.2,.5),(126,'A3',3.4,.55),(129.4,'C4',3.2,.55),(132.6,'Bb3',2.6,.5),(135.2,'C#4',2.6,.5)]: L(t,p,d,v)
for t,p,d in [(12,'D2',10),(31,'D2',9),(43.9,'D2',12),(59,'D2',11),(90.8,'D2',12),(112.7,'D2',10),(122.8,'D2',12)]: n.append((t,'cellos',p,d,.28,0.0))
for i in range(0,20): n.append((43.9+i*1.0,'cellos_pizz','D3' if i%2 else 'A2',.6,.3,.2))
for i in range(0,26): n.append((90.9+i*.5,'cellos_pizz',['D3','A2','F3','A2'][i%4],.4,.28,-.2))
for i in range(0,28): n.append((122.8+i*.5,'cellos_pizz',['D3','A3','F3','A3'][i%4],.4,.3+.008*i,.15))
for t,p in [(.2,'D3'),(1.1,'A2'),(2.2,'D3'),(3.28,'C#3')]: n.append((t,'cellos_pizz',p,.8,.4,0.0))
m=np.asarray(S.render(n,DUR))[:N];m=np.pad(m,((0,max(0,N-len(m))),(0,0)));g=np.ones(N)
for s0,s1 in [(4.75,5.9),(89.2,90.5),(106.95,107.6),(137.75,139.4)]: g[int(s0*SR):int(s1*SR)]=0
m=m*sm(g,140)[:,None];m/=np.sqrt(np.mean(m**2))+1e-9;m*=.034;m*=(1-.35*duck)[:,None]
# bruitages
fx=np.zeros((N,2),np.float32)
def put(f,t,gain,pan=0,off=0,maxd=None,fade=.03):
    if f.endswith('.ogg'): x,sr=sf.read(f)
    else: x,sr=sf.read(H+'/sfx/'+f+'.wav')
    x=x.mean(1) if x.ndim>1 else x; x=soxr.resample(x,sr,SR) if sr!=SR else x; x=x[int(off*SR):]
    if maxd: x=x[:int(maxd*SR)]
    k=min(len(x),int(fade*SR)); x=x.copy(); x[-k:]*=np.linspace(1,0,k); add(fx,(x/(np.abs(x).max()+1e-9)*gain).astype(np.float32),t,1.0,pan)
put('click',5.2,.3);put('boom',3.28,.14);put('boom',4.8,.1)
put('whoosh',10.6,.12,off=.2);put('applause',20.4,.16,maxd=2.2,fade=.8);put('whoosh',23.7,.2,off=.1,maxd=1.8,fade=.6)
for t in (24.4,26.0,28.2): put('bubbles',t,.16)
put('heart',26.2,.2,maxd=3.4);put('whoosh',30.4,.13,off=.2,maxd=1.2,fade=.5)
for t in (34.88,43.97,48.73,59.08,67.83,91.0,97.46,101.39): put('boom',t,.17)
for t in (42.2,58.2,74.4,111.3): put('whoosh',t,.1,off=.2,maxd=1.4,fade=.5)
put('knock',77.0,.42);put('knock',78.3,.3)
put('whoosh',84.1,.22,off=.1,maxd=1.8,fade=.6);put('boom',84.43,.35);put('heart',86,.22,maxd=3.2)
put('click',108.82,.14);put('boom',108.82,.24);put('whoosh',121.3,.16,maxd=2.4,fade=.8)
# fin : le câble se branche, montée puis coupure nette avant la boucle
d=int(1.1*SR);t=np.arange(d)/SR;rise=np.sin(2*np.pi*(90*t+150*t**2.2))*np.linspace(0,1,d)**2+bp(rng.standard_normal(d),800,6000,2)*np.linspace(0,1,d)**3*.6
add(fx,(rise*.12).astype(np.float32),137.2,1.0,0)
put('click',138.3,.5);put('plug',138.32,.42);put('boom',138.3,.45)
d=int(.55*SR);t=np.arange(d)/SR;hum=(np.sin(2*np.pi*50*t)+.5*np.sin(2*np.pi*100*t)+.35*np.sin(2*np.pi*150*t))*np.exp(-t/.16);add(fx,(hum*.12).astype(np.float32),138.34,1.0,0)
room=lp(rng.standard_normal(N),500,2)*.0012
mix=np.stack([vo]*2,1)+m+np.stack([pen*(1-.45*duck)]*2,1)+fx+room[:,None];mix[-int(.05*SR):]*=np.linspace(1,0,int(.05*SR))[:,None]
os.makedirs(H+'/out',exist_ok=True);sf.write(H+'/out/mix.wav',limit(mix,.95).astype(np.float32),SR)
db=lambda x:round(20*np.log10(np.sqrt(np.mean(x**2))+1e-9),1);print('voix',db(vo[duck>.5]),'musique sous voix',db(m[duck>.5]),'plume',db(pen),'bruitages',db(fx),'pic',np.abs(mix).max())
print('\n'.join(S.credits(['cellos','cellos_pizz'])))
