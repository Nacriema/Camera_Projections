#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sep 15 09:59:10 2021

@author: Nacriema

Refs:

This method is use for understanding, but the visualize step is not good, find the another way to visualize it
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np
from utils import *
import open3d as o3d

# load image
img = cv2.cvtColor(cv2.imread('./data/rgb.png'), cv2.COLOR_BGR2RGB)

# depth image stored as float32 in meters and the size equal to img.shape
depth = cv2.imread('./data/depth.exr', cv2.IMREAD_ANYDEPTH)

# get intrinsic params
height, width, _ = img.shape
K = intrinsic_from_fov(height, width, 90)
K_inv = np.linalg.inv(K)

# get pixel coordinate
pixel_coords = pixel_coord_np(width, height)
# print(pixel_coords)
cam_coords = K_inv[:3, :3] @ pixel_coords * depth.flatten()

# Limit points to 150m in the z-direction for visualization
cam_coords = cam_coords[:, np.where(cam_coords[2] <= 150)[0]]

pcd_cam = o3d.geometry.PointCloud()
pcd_cam.points = o3d.utility.Vector3dVector(cam_coords.T[:, :3])

pcd_cam.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
o3d.visualization.draw_geometries([pcd_cam])
