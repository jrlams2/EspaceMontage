# Cale chaque phrase du script sur les pauses de la voix (programmation dynamique), sans transcription automatique.
import subprocess,re,json,numpy as np
V='../audio/La_Machine.mp3'
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',V,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
h=160;rms=np.sqrt(np.convolve(x*x,np.ones(320)/320,'same')[::h]+1e-12);db=20*np.log10(rms);sp=db>-40
runs=[];i=0
while i<len(sp):
    if not sp[i]:
        j=i
        while j<len(sp) and not sp[j]: j+=1
        if (j-i)*.01>=.06: runs.append((i*.01,j*.01))
        i=j
    else: i+=1
start=runs[0][1] if runs and runs[0][0]<.05 else 0.0
end=[a for a,b in runs if b>len(x)/16000-.6 or b-a>2][-1]
P=[(a,b) for a,b in runs if a>start+.05 and b<end]
txt=open('../voix.txt').read().replace('\n',' ')
ph=[p.strip() for p in re.findall(r'[^.?!:,»]+(?:\.\.\.|[.?!:,])+(?: ?»)?',txt) if re.search(r'\w',p)]
out=[]
for p in ph: out.append(p)
ph=out
# virgules courtes : on garde la phrase entière
def syl(s):
    s=s.lower(); s=re.sub(r"(e|es|ent)\b(?=\W|$)",lambda m:m.group(0) if len(m.string)<4 else '',s)
    return max(1,len(re.findall(r'[aeiouyàâéèêëîïôùûœ]+',s)))
sy=np.array([syl(p) for p in ph],float); n=len(ph);m=len(P)
speech=(end-start)-sum(b-a for a,b in P); rate=sy.sum()/speech
cs=lambda a,b: (b-a)-sum(max(0,min(b,q)-max(a,p)) for p,q in P)
# frontières possibles : pauses (0 = début, m+1 = fin)
A=[start]+[b for a,b in P]+[end]; B=[start]+[a for a,b in P]+[end]
L=[0]+[b-a for a,b in P]+[0]
strong=[bool(re.search(r'[.?!]',p[-3:])) for p in ph]
ANC={'Choisis':6,'Parce que dans':9,'Le grand amour':17,'Une fois dedans':26,'Robert':34.6,'Un.':44,'Mais ce corps':51,'Et l\'expérience':63.8,'Affaire':70,'Un inconnu':79,'« On peut':86,'Une moitié':97,"C'est peut-être juste":107.8,'Une petite machine':115,'Ce soir':124,'Réfléchis':134,'Sauf qu':71.5,'Felipe':75,'Imagine une':12,'Cette fois':90.5,'Deux':48.7,'Trois':59.1}
an=[next((v for k,v in ANC.items() if p.startswith(k)),None) for p in ph]
INF=1e9;C=np.full((n+1,m+2),INF);K=np.zeros((n+1,m+2),int);C[0,0]=0
for i in range(1,n+1):
    for j in range(1,m+2):
        for k in range(max(0,j-9),j):
            if C[i-1,k]>=INF: continue
            d=cs(A[k],B[j]); e=sy[i-1]/rate
            c=C[i-1,k]+4*(np.log((d+.15)/(e+.15)))**2 - (min(L[j],.7)*(1.0 if strong[i-1] else .5) if j<m+1 else 0) + (8*max(0,abs(A[k]-an[i-1])-.9) if an[i-1] else 0)
            if c<C[i,j]: C[i,j]=c;K[i,j]=k
j=m+1;r=[]
for i in range(n,0,-1): k=K[i,j]; r.append((round(A[k],2),round(B[j],2),ph[i-1])); j=k
r=r[::-1]; json.dump([dict(t0=a,t1=b,text=t) for a,b,t in r],open('cues.json','w'),ensure_ascii=False,indent=0)
for c in r: print(*c)
print('pauses',m,'phrases',n,'debit',rate)
