import torch
import torch.nn as nn
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
from torch.autograd import Variable

batchSize = 64
imageSize = 64

transform = transforms.Compose([transforms.Scale(imageSize),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                    ])


dataset = dset.CIFAR10(root='./data', download=True, transform=transform)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batchSize, shuffle=True)

def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('Batchnorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)


# defining the generator
class Generator(nn.Module):
    
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
                    nn.Conv2dTranspose(100, 512, 4, 1, 0, bias=False),
                    nn.BatchNorm2d(512),
                    nn.ReLU(True),
                    nn.Conv2dTranspose(512, 256, 4, 2, 1, bias=False),
                    nn.BatchNorm2d(256),
                    nn.ReLU(True),
                    nn.Conv2dTranspose(256, 128, 4, 2, 1, bias=False),
                    nn.BatchNorm2d(128),
                    nn.ReLU(True),
                    nn.Conv2dTranspose(128, 64, 4, 2, 1, bias=False),
                    nn.BatchNorm2d(64),
                    nn.ReLU(True),
                    nn.Conv2dTranspose(64, 3, 4, 2, 1, bias=False),
                    nn.Tanh()
                    )
        
