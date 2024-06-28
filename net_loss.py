## 79 ########################################################################
# branch master
print(__file__)
from utilz2 import *
import torch

class Loss_Recorder():
    def __init__(
        self,
        path,
        plottime=30,
        savetime=30,
        sampletime=10,
        pct_to_show=100,
        nsamples=30,
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
        if self.acc_ctr<self.nsamples:
            return
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
            s=1-(1-self.s)*self.ctr/(self.s_level+self.ctr)
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
        f=opj(self.path,get_safe_name(self.name)+'.pkl')
        cg(f)
        d=lo(f)
        for k in d:
            self.__dict__[k]=d[k]
        cb('loaded',f)
    def plot(self,clear=True,rawcolor='c',smoothcolor='b',savefig=False,fig='loss'):
        figure(fig)
        if clear:
            clf()
        idx=int(len(self.i)*(100-self.pct_to_show)/100)
        plot(self.i[idx:],self.f[idx:],rawcolor)
        plot(self.i[idx:],self.r[idx:],smoothcolor,label=self.name)
        plt.xlabel('iterations');
        plt.ylabel(self.name)
        plt.title(self.name)
        if savefig:
            plt.savefig(opj(self.path,get_safe_name(fig+'.pdf')))
    def do(self,d,external_ctr=None):
        self.add(d,external_ctr=external_ctr)
        self.save()
    def current(self):
        if len(self.r):
            return self.r[-1]
        else:
            cE('warning')
            kprint(self.__dict__)
            return 0
#eoc

#EOF
## 79 ########################################################################
