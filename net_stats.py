## 79 ########################################################################

import torch
from utilz2 import *

def get_accuracy(net,testloader,classes,device):
    correct_pred = {classname: 0 for classname in classes}
    total_pred = {classname: 0 for classname in classes}
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            images=images.to(device)
            labels=labels.to(device)
            outputs = net(images)
            _, predictions = torch.max(outputs, 1)
            for label, prediction in zip(labels, predictions):
                if label == prediction:
                    correct_pred[classes[label]] += 1
                total_pred[classes[label]] += 1
    stats=[]
    ctr=0
    acc_mean=0
    for classname, correct_count in correct_pred.items():
        accuracy = 100 * float(correct_count) / total_pred[classname]
        acc_mean+=accuracy
        ctr+=1
        stats.append(f'**** Accuracy for class: {classname:5s} is {accuracy:.1f} %')
    acc_mean/=ctr
    stats.append(d2n('\tMean accuracy is ',int(acc_mean),'%.'))
    stats='\n'.join(stats)
    return stats,acc_mean

#EOF