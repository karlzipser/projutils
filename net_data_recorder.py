##                                                                          ##
##############################################################################
##                                                                          ##
print(__file__)
from utilz2 import *
import torch
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
class Data_Recorder():

    def __init__(self,name='',dataloader=None,):
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
                #soD('processed',self.processed)
                self.accumulated=[]
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

if False:
    def moving_average(data, window_size):
        """ Smooth data using a moving average """
        cumsum = np.cumsum(data)
        cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
        return cumsum[window_size - 1:] / window_size

    def xy_moving_average(x,y,window_size):
        x,y=na(x),na(y)
        sx=moving_average(x,window_size)
        sy=moving_average(y,window_size)
        return x,y
    n=5
    processed=loD('processed');clf()
    figure(2);clf()
    for c in classes:
        f=[]
        ig=[]
        for p in processed:
            f.append(p['accuracy'][classes[c]])
            ig.append(p['ig'])
        x=moving_average(ig,n)
        y=moving_average(f,n)
        plot(x,y,label=classes[c])
    plt.title('accuracy')
    plt.legend(kys(classes),loc='upper left')
    #plt.ylim(0,1)



    figure(3);clf()
    for c in classes:
        f=[]
        ig=[]
        for p in processed:
            f.append(p['f1_scores'][classes[c]])
            ig.append(p['ig'])
        x=moving_average(ig,n)
        y=moving_average(f,n)
        plot(x,y,label=classes[c])
    plt.title('f1-scores')
    plt.legend(kys(classes),loc='upper left')
    #plt.ylim(0,1)




    fig=figure(1);clf()
    ax=fig.add_subplot(111)
    disp=ConfusionMatrixDisplay(
        confusion_matrix=processed[-1]['confusion_matrix'],
        display_labels=kys(classes))
    disp.plot(ax=ax,cmap=plt.cm.Blues)


    figure(4);clf()
    f=[]
    ig=[]
    for p in processed:
        f.append(p['loss'])
        ig.append(p['ig'])
    x=moving_average(ig,n)
    y=moving_average(f,n)
    plot(x,y,label=classes[c])
    plt.title('loss')
    plt.legend(kys(classes),loc='upper left')
    #plt.ylim(0,1)

##                                                                          ##
##############################################################################
##                                                                          ##

