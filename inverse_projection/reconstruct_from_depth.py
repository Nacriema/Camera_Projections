#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Nov 27 20:25:06 2021

@author: Nacriema

Refs:

This is a part of the code I found at https://github.com/aim-uofa/AdelaiDepth/blob/05f8a38d87ca8b9abc0935c4e114a317bd754182/LeReS/lib/test_utils.py#L130
So currently, we use the leres model.
This code give the same result as the Open3D does
What am I missing here ???
TODO: NEED MORE RESEARCH !!!!
"""
import os
import numpy as np
from plyfile import PlyElement, PlyData
import cv2


def reconstruct_3D(depth, f):
    """
    Reconstruct depth to 3D point cloud with the provided focal length
    :param depth:
    :param f:
    :return: pcd: N x 3 array, point cloud
    """
    cu = depth.shape[1] / 2
    cv = depth.shape[0] / 2
    width = depth.shape[1]
    height = depth.shape[0]
    row = np.arange(0, width, 1)
    u = np.array([row for i in np.arange(height)])
    col = np.arange(0, height, 1)
    v = np.array([col for i in np.arange(width)])
    v = v.transpose((1, 0))

    if f > 1e5:
        print('Infinit focal length !!!')
        x = u - cu
        y = v - cv
        z = depth / depth.max() * x.max()

    else:
        x = (u - cu) * depth / f
        y = (v - cv) * depth / f
        z = depth

    x = np.reshape(x, (width * height, 1)).astype(np.float)
    y = np.reshape(y, (width * height, 1)).astype(np.float)
    z = np.reshape(z, (width * height, 1)).astype(np.float)
    pcd = np.concatenate((x, y, z), axis=1)
    pcd = pcd.astype(np.int)
    return pcd


def save_point_cloud(pcd, rgb, filename, binary=True):
    """
    Save an RGB point cloud as PLY file
    :param pcd: Nx3 matrix, the XYZ coordinates
    :param rgb: Nx3 matrix, the rgb colors for each 3D point
    :param filename:
    :param binary:
    :return:
    """
    assert pcd.shape[0] == rgb.shape[0]
    if rgb is None:
        gray_concat = np.tile(np.array([128], dtype=np.uint8), (pcd.shape[0], 3))
        points_3d = np.hstack((pcd, gray_concat))
    else:
        points_3d = np.hstack((pcd, rgb))
    python_types = (float, float, float, int, int, int)
    npy_types = [('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')]
    if binary is True:
        verticies = []
        for row_idx in range(points_3d.shape[0]):
            cur_point = points_3d[row_idx]
            verticies.append(tuple(dtype(point) for dtype, point in zip(python_types, cur_point)))
        verticies_array = np.array(verticies, dtype=npy_types)
        el = PlyElement.describe(verticies_array, 'vertex')

        PlyData([el]).write(filename)
    else:
        x = np.squeeze(points_3d[:, 0])
        y = np.squeeze(points_3d[:, 1])
        z = np.squeeze(points_3d[:, 2])
        r = np.squeeze(points_3d[:, 3])
        g = np.squeeze(points_3d[:, 4])
        b = np.squeeze(points_3d[:, 5])
        ply_head = 'ply\n' \
                   'format ascii 1.0\n' \
                   'element vertex %d\n' \
                   'property float x\n' \
                   'property float y\n' \
                   'property float z\n' \
                   'property uchar red\n' \
                   'property uchar green\n' \
                   'property uchar blue\n' \
                   'end_header' % r.shape[0]
        np.savetxt(filename, np.column_stack((x, y, z, r, g, b)), fmt="%d %d %d %d %d %d", header=ply_head, comments='')


def reconstruct_depth(depth, rgb, dir, pcd_name, focal):
    """
    :param depth:
    :param rgb:
    :param dir:
    :param pcd_name:
    :param focal:
    :return:
    """
    rgb = np.squeeze(rgb)
    depth = np.squeeze(depth)

    mask = depth < 1e-8
    depth[mask] = 0
    depth = depth / depth.max() * 10000

    pcd = reconstruct_3D(depth, f=focal)
    rgb_n = np.reshape(rgb, (-1, 3))
    save_point_cloud(pcd, rgb_n, os.path.join(dir, pcd_name + '.ply'))


# TEST
# The result the same as the open3D does
if __name__ == '__main__':
    img = cv2.cvtColor(cv2.imread('./data/sample2.jpg'), cv2.COLOR_BGR2RGB)
    depth = cv2.imread('data/sample2_leres.png', cv2.IMREAD_ANYDEPTH)
    dir = './ply_files'
    pcd_name = 'sample2_pcl'
    focal = 1976.5747979832406
    reconstruct_depth(depth, img, dir, pcd_name, focal)
