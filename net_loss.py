## 79 ########################################################################
# branch master
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
        s_level=100,
        name='train loss',
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
    def add(self,d,external_ctr=None):
        self.acc+=d
        self.acc_ctr+=1
        #if not self.sampletimer.rcheck():
        #    return
        if self.acc_ctr<5:
            return
        #print(self.name,self.acc_ctr)
        d=self.acc/self.acc_ctr
        self.acc=0
        self.acc_ctr=0
        if isNone(external_ctr):
            self.ctr+=1
        else:
            self.ctr=external_ctr
        self.i.append(self.ctr)
        self.t.append(time.time())
        self.f.append(d)

        if len(self.r):
            #s=1-(1-self.s)/max(1,(self.s_level-self.ctr))
            s=1-(1-self.s)*self.ctr/(self.s_level+self.ctr)
            #print(s)
            #s=self.s
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
        so(opj(self.path,get_safe_name(self.name)),d)
    def load(self):
        d=lo(opj(self.path,get_safe_name(self.name)))
        for k in d:
            self.__dict__[k]=d[k]
        cb('loaded',opj(self.path,get_safe_name(self.name)))
    def plot(self,clear=True,rawcolor='c',smoothcolor='b',savefig=False):
        #if not self.plottimer.rcheck():
        #    return
        #print(self.name)
        figure('loss')
        if clear:
            clf()
        idx=int(len(self.i)*(100-self.pct_to_show)/100)
        plot(self.i[idx:],self.f[idx:],rawcolor)
        plot(self.i[idx:],self.r[idx:],smoothcolor,label=self.name)
        plt.xlabel('iterations');
        plt.ylabel('loss')
        plt.title('loss')#d2s(self.name,self.path.replace(opjh(),'')))
        
        if savefig:
            plt.savefig(opj(self.path,'loss.pdf'))
    def do(self,d,external_ctr=None):
        self.add(d,external_ctr=external_ctr)
        #self.plot()
        self.save()
    def current(self):
        return self.r[-1]
#eoc
#EOF
## 79 ########################################################################
