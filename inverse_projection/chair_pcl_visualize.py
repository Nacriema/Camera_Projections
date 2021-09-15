#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sep 15 16:36:28 2021

@author: Nacriema

Refs:

Apply the predefined function to visualize chair from depth image
"""
from PIL import Image
import cv2
import scipy.io as scio
from utils import intrinsic_from_fov, pixel_coord_np
import numpy as np
import open3d as o3d

depth_images = scio.loadmat('./data/1a6f615e8b1b5ae4dbbc9440457e303e.mat')
Z_depths = depth_images.get('Z')

Z_depth = Z_depths[0]
print(Z_depth.shape)

height, width = Z_depth.shape
K = intrinsic_from_fov(height, width, 50)
K_inv = np.linalg.inv(K)

pixel_coords = pixel_coord_np(width, height)
cam_coords = K_inv[:3, :3] @ pixel_coords * Z_depth.flatten()

pcd_cam = o3d.geometry.PointCloud()
pcd_cam.points = o3d.utility.Vector3dVector(cam_coords.T[:, :3])
o3d.visualization.draw_geometries([pcd_cam])