## 79 ########################################################################

import torch
#import torch.nn as nn
#import torch.nn.parallel
#import torch.optim as optim
#import torch.utils.data
#import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
import torchvision
torchvision.disable_beta_transforms_warning()
import torchvision.transforms.v2 as v2

_fill=(0,0,0)

_transforms=dict(
    RandomPerspective=True,
    RandomPerspective_distortion_scale=0.3,
    RandomPerspective_p=0.3,
    RandomPerspective_fill=_fill,

    RandomRotation=True,
    RandomRotation_angle=12,
    RandomRotation_fill=_fill,

    RandomResizedCrop=True,
    RandomResizedCrop_scale=(0.85,1),
    RandomResizedCrop_ratio=(0.85,1.2),

    RandomHorizontalFlip=True,
    RandomHorizontalFlip_p=0.5,
        
    RandomVerticalFlip=False,
    RandomVerticalFlip_p=0.5,

    RandomZoomOut=True,
    RandomZoomOut_fill=_fill,
    RandomZoomOut_side_range=(1.0,1.5),

    ColorJitter=False,
    ColorJitter_brightness=(0,1),
    ColorJitter_contrast=(0,1),
    ColorJitter_saturation=(0,2),
    ColorJitter_hue=(-.03,.03),
)





def get_transforms(d,image_size):

    geometric_transforms_list=[]

    k='RandomPerspective'
    if k in d and d[k]:
        geometric_transforms_list.append(
            v2.RandomPerspective(
                distortion_scale=d['RandomPerspective_distortion_scale'],
                p=d['RandomPerspective_p'],
                interpolation=transforms.InterpolationMode.BILINEAR,
                fill=d['RandomPerspective_fill'],
            )
        )

    k='RandomRotation'
    if k in d and d[k]:
        geometric_transforms_list.append(
            v2.RandomRotation(d['RandomRotation_angle'],fill=d['RandomRotation_fill'])
        )

    k='RandomZoomOut'
    if k in d and d[k]:
        geometric_transforms_list.append(
            v2.RandomZoomOut(side_range=d['RandomZoomOut_side_range'],fill=d['RandomZoomOut_fill'])
        )


    k='Pad'
    if k in d and d[k]:
        geometric_transforms_list.append(
            #v2.Pad(padding=(640-360)//2,fill=d['Pad_fill)
            v2.Pad(padding=64,fill=d['Pad_fill'])
        )

    k='CenterCrop'
    if k in d and d[k]:
        geometric_transforms_list.append(
            v2.CenterCrop(size=640)
        )

    
    k='RandomResizedCrop'
    if k in d and d[k]:
        geometric_transforms_list.append(
            v2.RandomResizedCrop(
                image_size,
                scale=d['RandomResizedCrop_scale'],
                ratio=d['RandomResizedCrop_ratio'],
                antialias=True,
            )
        )

    k='Resize'
    if k in d and d[k]:
        geometric_transforms_list.append(
            v2.Resize(size=image_size,antialias=True)
        )
    
    k='RandomHorizontalFlip'
    if k in d and d[k]:
        geometric_transforms_list.append(
            v2.RandomHorizontalFlip(p=d['RandomHorizontalFlip_p'])
        )
        
    k='RandomVerticalFlip'
    if k in d and d[k]:
        geometric_transforms_list.append(
            v2.RandomVerticalFlip(p=d['RandomVerticalFlip_p'])
        )

    color_transforms_list=[]
    k='ColorJitter'
    if k in d and d[k]:
        color_transforms_list.append(
            v2.ColorJitter(
                brightness=d['ColorJitter_brightness'],
                contrast=d['ColorJitter_contrast'],
                saturation=d['ColorJitter_saturation'],
                hue=d['ColorJitter_hue'],
            )
        )

    return geometric_transforms_list,color_transforms_list




