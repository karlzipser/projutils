##                                                                          ##
##############################################################################
##                                                                          ##
print(__file__)
from utilz2 import *
import torch
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
class Data_Recorder():

    def __init__(self,name='',dataloader=None,noise_level=0.,noise_p=0.,):
        super(Data_Recorder,self).__init__()
        packdict(self,locals())
        self.accumulated=[]
        self.processed=[]

    def add(self,data,):
            assert 't' not in data
            data['t']=time.time()
            for i in rlen(self.accumulated):
                self.accumulated[i]['inputs']=None
            self.accumulated.append(data)
            if len(self.accumulated)>=100:
                predictions,labels=self.get_predictions()
                accuracy,correct,total=get_accuracy2(predictions,labels)

                loss=self.get_mean_loss()

                self.processed.append(dict(
                    t=data['t'],
                    ig=data['ig'],
                    accuracy=accuracy,
                    correct=correct,
                    total=total,
                    loss=loss,
                    f1_scores=f1_score(labels,predictions,average=None),
                    confusion_matrix=confusion_matrix(labels,predictions),
                    ))
                self.accumulated=[]

    def save(self,path):
        assert path
        mkdirp(path)
        so(opj(path,'data_recorder-'+get_safe_name(self.name)+'.pkl'),
            self.processed)

    def load(self,path):
        path=opj(path,'data_recorder-'+get_safe_name(self.name)+'.pkl')
        #cg(path)
        assert os.path.isfile(path)
        self.accumulate=[]
        self.processed=lo(path,noisy=True)
        ig0=self.processed[-1]['ig']
        for p in self.processed:
            p['ig']-=ig0

    def latest(self):
        if len(self.accumulated):
            return self.accumulated[-1]
        else:
            return None

    def get_predictions(self):
        labels=[]
        predictions=[]
        for a in self.accumulated:
            l=list(a['labels'].numpy())
            o=a['outputs']
            p=[]
            for i in range(o.size()[0]):
                p.append(torch.argmax(o[i,:,0,0]).item())
            labels+=l
            predictions+=p
        return predictions,labels

    def get_mean_loss(self):
        loss=0
        for a in self.accumulated:
            loss+=a['loss'].item()
        return loss/len(self.accumulated)


def get_accuracy2(predictions,labels):
    correct={}
    total={}
    accuracy={}
    for i in range(10):
        correct[i]=0
        total[i]=0

    for l,p in zip(labels,predictions):
        total[l]+=1
        if l==p:
            correct[l]+=1
    for i in range(10):
        accuracy[i]=correct[i]/total[i]
    return accuracy,correct,total
#eoc

#EOF

##                                                                          ##
##############################################################################
##                                                                          ##


##                                                                          ##
##############################################################################
##                                                                          ##

