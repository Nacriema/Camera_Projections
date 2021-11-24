#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sep 15 11:04:59 2021

@author: Nacriema

Refs:

"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
from utils import img_to_pointcloud, intrinsic_from_fov
import open3d as o3d

# load image
# img = cv2.cvtColor(cv2.imread('./data/rgb.png'), cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(cv2.imread('./data/sample6.jpg'), cv2.COLOR_BGR2RGB)

# depth image stored as float32 in meters and the size equal to img.shape
# depth = cv2.imread('./data/depth.exr', cv2.IMREAD_ANYDEPTH)

# leres is in the correct form, far-white-high value, close-black-low value
# depth = cv2.imread('data/sample6_leres.png', cv2.IMREAD_ANYDEPTH)

depth = cv2.imread('./data/sample6_midas.png', cv2.IMREAD_ANYDEPTH)
depth = depth.max() - depth

depth = depth / np.max(depth) * 1000.
depth = depth.astype('float32')
print(np.unique(depth))
print("-----")


height, width, _ = img.shape
K = intrinsic_from_fov(height, width, 90)
img_to_pointcloud(img, depth, K, clamp=900.)
