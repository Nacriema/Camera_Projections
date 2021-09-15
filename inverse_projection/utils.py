#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sep 15 10:00:07 2021

@author: Nacriema

Refs:
https://en.wikipedia.org/wiki/Field_of_view
https://en.wikipedia.org/wiki/Angle_of_view
"""
import numpy as np
import math
import open3d as o3d


def pixel_coord_np(width, height):
    """
    Pixel in homogenerous coordinate
    :param width:
    :param depth:
    :return: Pixel coordinate [3, width * heigh]
    """
    x = np.linspace(0, width-1, width).astype(np.int)
    y = np.linspace(0, height-1, height).astype(np.int)
    [x, y] = np.meshgrid(x, y)
    return np.vstack((x.flatten(), y.flatten(), np.ones_like(x.flatten())))


def intrinsic_from_fov(height, width, fov=120):
    """
    Return the Intrinsic of Pinhole Camera, given the field of view and sensor height, sensor width
    Basically
    fov = 2 * arctan(sensor_size / (2f))
    Because sensor_size have width and height
    Then:
    given fov is the h_fov
    h_fov = 2 * arctan(width / (2*f_x))
    v_fov = 2 * arctan(height / (2f_y))

    :param height: sensor height (pixels)
    :param width: sensor width (pixels)
    :param fov: field of view
    :return: Intrinsic matrix Shape [4, 4]
    """
    px, py = (width/2, height/2)
    h_fov = fov / 360. * 2 * np.pi
    f_x = width / (2 * np.tan(h_fov / 2))
    v_fov = 2 * np.arctan(np.tan(h_fov / 2) * height / width)
    f_y = height / (2 * np.tan(v_fov / 2.))
    return np.array([
        [f_x, 0., px, 0.],
        [0., f_y, py, 0.],
        [0., 0., 1., 0.],
        [0., 0., 0., 1.]
    ])


def img_to_pointcloud(img, depth, K, clamp=150., flip=True):
    # First clamp the depth for better visualize
    depth[depth > clamp] = 0
    rgb = o3d.geometry.Image(img)
    depth = o3d.geometry.Image(depth)
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(rgb, depth, convert_rgb_to_intensity=False)
    f_x, f_y, p_x, p_y = K[0, 0], K[1, 1], K[0, 2], K[1, 2]
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd,
                       o3d.camera.PinholeCameraIntrinsic(int(p_x*2), int(p_y*2), f_x, f_y, p_x, p_y))
    if flip:
        pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd])
