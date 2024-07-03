import torch
import torch.nn as nn
from pvtv2 import pvt_v2_b3

class Conv2D(nn.Module):
    def __init__(self, in_c, out_c, kernel_size=3, padding=1, dilation=1, bias=True, act=True):
        super().__init__()

        self.act = act
        self.conv = nn.Sequential(
            nn.Conv2d(in_c, out_c, kernel_size, padding=padding, dilation=dilation, bias=bias),
            nn.BatchNorm2d(out_c)
        )
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.conv(x)
        if self.act == True:
            x = self.relu(x)
        return x

class ResidualBlock(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()

        self.relu = nn.ReLU()
        self.conv = nn.Sequential(
            nn.Conv2d(in_c, out_c, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU(),
            nn.Conv2d(out_c, out_c, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_c)
        )
        self.shortcut = nn.Sequential(
            nn.Conv2d(in_c, out_c, kernel_size=1, padding=0),
            nn.BatchNorm2d(out_c)
        )

    def forward(self, inputs):
        x1 = self.conv(inputs)
        x2 = self.shortcut(inputs)
        x = self.relu(x1 + x2)
        return x

class DecoderBlock(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()

        self.up = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=True)
        self.r1 = ResidualBlock(in_c+out_c, out_c)

    def forward(self, x, s):
        x = self.up(x)
        x = torch.cat([x, s], axis=1)
        x = self.r1(x)
        return x

class UpBlock(nn.Module):
    def __init__(self, in_c, out_c, scale):
        super().__init__()

        self.up = nn.Upsample(scale_factor=scale, mode="bilinear", align_corners=True)
        self.r1 = ResidualBlock(in_c, out_c)

    def forward(self, inputs):
        x = self.up(inputs)
        x = self.r1(x)
        return x

class PVTSeg(nn.Module):
    def __init__(self):
        super().__init__()

        """ Encoder """
        self.backbone = pvt_v2_b3()  ## [64, 128, 320, 512]
        path = 'pvt_v2_b3.pth'
        save_model = torch.load(path)
        model_dict = self.backbone.state_dict()
        state_dict = {k: v for k, v in save_model.items() if k in model_dict.keys()}
        model_dict.update(state_dict)
        self.backbone.load_state_dict(model_dict)

        """ Channel Reduction """
        self.c1 = Conv2D(64, 64, kernel_size=1, padding=0)
        self.c2 = Conv2D(128, 64, kernel_size=1, padding=0)
        self.c3 = Conv2D(320, 64, kernel_size=1, padding=0)
        self.c4 = Conv2D(512, 64, kernel_size=1, padding=0)

        self.d1 = DecoderBlock(64, 64)
        self.d2 = DecoderBlock(64, 64)
        self.d3 = DecoderBlock(64, 64)
        self.d4 = UpBlock(64, 64, 4)

        self.r1 = ResidualBlock(64, 64)
        self.y = nn.Conv2d(64, 1, kernel_size=1, padding=0)

    def forward(self, inputs):
        """ Encoder """
        pvt1 = self.backbone(inputs)
        e1 = pvt1[0]  ## [-1, 64, h/4, w/4]
        e2 = pvt1[1]  ## [-1, 128, h/8, w/8]
        e3 = pvt1[2]  ## [-1, 320, h/16, w/16]
        e4 = pvt1[3]  ## [-1, 512, h/32, w/32]

        c1 = self.c1(e1)
        c2 = self.c2(e2)
        c3 = self.c3(e3)
        c4 = self.c4(e4)

        d1 = self.d1(c4, c3)
        d2 = self.d2(d1, c2)
        d3 = self.d3(d2, c1)

        x = self.d4(d3)
        x = self.r1(x)
        y = self.y(x)

        return y

if __name__ == "__main__":
    x = torch.randn((4, 3, 256, 256))
    model = PVTSeg()
    y = model(x)
    print(y.shape)
