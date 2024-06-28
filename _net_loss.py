## 79 ########################################################################

print(__file__)
from utilz2 import *
import torch

class Loss_Recorder():
    def __init__(
        self,
        path,
        plottime=10,
        savetime=10,
        sampletime=1,
        pct_to_show=100,
        s=0.1,
    ):
        super(Loss_Recorder,self).__init__()
        packdict(self,locals())
        self.f=[]
        self.t=[]
        self.i=[]
        self.r=[]
        self.ctr=-1
        self.plottimer=Timer(plottime)
        self.savetimer=Timer(savetime)
        self.sampletimer=Timer(sampletime)
        self.acc_ctr=0
        self.acc=0
    def add(self,d):
        self.acc+=d
        self.acc_ctr+=1
        if not self.sampletimer.rcheck():
            return
        d=self.acc/self.acc_ctr
        self.acc=0
        self.acc_ctr=0        
        self.ctr+=1
        self.i.append(self.ctr)
        self.t.append(time.time())
        self.f.append(d)
        if len(self.r):
            s=self.s
            a=self.r[-1]
            b=(1-s)*a+s*d
            self.r.append(b)
        else:
            self.r.append(d)
    def save(self):
        if not self.savetimer.rcheck():
            return
        d={}
        for k in ['i','f','t','r','ctr']:
            if 'timer' not in k:
                d[k]=self.__dict__[k]
        so(opj(self.path,'loss'),d)
    def load(self):
        d=lo(opj(self.path,'loss'))
        for k in d:
            self.__dict__[k]=d[k]
    def plot(self):
        if not self.plottimer.rcheck():
            return
        figure('loss')
        clf()
        idx=int(len(self.i)*(100-self.pct_to_show)/100)
        plot(self.i[idx:],self.f[idx:],'c')
        plot(self.i[idx:],self.r[idx:],'b')
        plt.xlabel('iterations');
        plt.ylabel('loss')
        plt.title(self.path.replace(opjh(),''))
        plt.savefig(opj(self.path,'loss.pdf'))
    def do(self,d):
        self.add(d)
        self.plot()
        self.save()
    def current(self):
        return self.r[-1]
#eoc
#EOF
## 79 ########################################################################
