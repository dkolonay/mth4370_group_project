import torch.nn as nn
from torchvision import models

class ResNet50Encoder(nn.Module):
    def __init__(self, output_dim=512):
        super().__init__()

        resnet = models.resnet50(
        	weights=models.ResNet50_Weights.IMAGENET1K_V2
        )

        self.encoder = nn.Sequential(*list(resnet.children())[:-1])

        self.output_dim = output_dim

        self.proj = nn.Linear(2048, output_dim)

    def forward(self, x):
        x = self.encoder(x)
        x = x.flatten(1)
        return self.proj(x)

class EfficientNetB0Encoder(nn.Module):
    def __init__(self, output_dim=256):
        super().__init__()

        effnet = models.efficientnet_b0(
        	weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1
        )

        self.feature_extractor = nn.Sequential(
            effnet.features,
            nn.AdaptiveAvgPool2d(1),
        )

        self.output_dim = output_dim

        self.proj = nn.Linear(1280, output_dim)

    def forward(self, x):
        x = self.feature_extractor(x)
        x = x.flatten(1)
        return self.proj(x)