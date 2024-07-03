# datasets

download the datasets (1) [kvasir-seg](https://drive.google.com/file/d/1yQdfow1-WvDilQTZ1zj1EbbErN1DksVF/view?usp=sharing), (2) [CVC-ClinicDB]() and (3) [PolypGen2021_MultiCenterData_v3](). 

1. more information about kvasir-seg refers to IEEE TIM 2020 paper entitled
   [EDRNet: Encoder-Decoder Residual Network for Salient Object Detection of Strip Steel Surface Defects](https://ieeexplore.ieee.org/document/9116810) (DOI：10.1109/TIM.2020.3002277) 
   by Guorong Song, Kechen Song and Yunhui Yan.

2. more information about kvasir-seg, CVC-ClinicDB, PolypGen (2021_MultiCenterData_v3

3. 

# usage

We conduct experiments using the MMSegmentation module within the OpenMMLab framework.

We implemented the model using the Pytorch framework and conducted experiments on an NVIDIA A100 GPU system.

# results of PVTSeg

We provide pth of our PVTSeg trained on kvasir-seg；
(link: https://pan.baidu.com/s/13shptjoT0MhKa1mCm9BY9g code: 7g5w) 

1.heatmaps of each methods

<img title="" src="./results/fig2.jpg" alt="" width="596">

2.Qualitative results comparison along with the heatmap on the CVC-ClinicDB.

![](./results/fig3.jpg)

3.qualitative results comparison along with the heatmap on the Kvasir-SEG.

4.The statistic results of the compared methods on kvasir-seg, CVC-ClinicDB and PolypGen (PolypGen2021_MultiCenterData_v3)s are as follows

<img title="" src="./results/PVTSeg-result1.png" alt="" width="523">

<img title="" src="./results/PVTSeg-result2.png" alt="" data-align="inline" width="523">

<img title="" src="./results/PVTSeg-result3.png" alt="" width="643">



# 
