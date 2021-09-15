#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sep 15 16:56:34 2021

@author: Nacriema

Refs:

"""

from PIL import Image
import cv2
import scipy.io as scio
from utils import intrinsic_from_fov, img_to_pointcloud
import numpy as np
import open3d as o3d

rgb_images = np.load('./data/1a6f615e8b1b5ae4dbbc9440457e303e.npy')
rgb_image = rgb_images[2]
dim = (128, 128)

rgb_image = cv2.resize(rgb_image, dim, interpolation=cv2.INTER_AREA)
print(rgb_image.shape)

depth_images = scio.loadmat('./data/1a6f615e8b1b5ae4dbbc9440457e303e.mat')
Z_depths = depth_images.get('Z')
Z_depth = Z_depths[0].tolist()
Z_depth = np.array(Z_depth, dtype=np.float32)
print(Z_depth.shape)

height, width = Z_depth.shape
K = intrinsic_from_fov(height, width, 50)
img_to_pointcloud(rgb_image, Z_depth, K, flip=False)
