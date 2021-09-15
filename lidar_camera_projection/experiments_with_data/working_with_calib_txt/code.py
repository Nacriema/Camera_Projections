#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sep 14 03:16:34 2021

@author: Nacriema

Refs:

"""
import numpy as np


data = {}
with open('../../data/000114_calib.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        key, value = line.split(":", 1)  # maxsplit=1 then 2 elements returned
        try:
            data[key] = np.array([float(x) for x in value.split()])
        except ValueError:
            pass

R0_rect = data['R0_rect'].reshape(3, 3)
R_ref2rect = np.eye(4)
R_ref2rect[:3, :3] = R0_rect
# print(R_ref2rect)

# print(data['P0'].reshape(3, 4))
# print(data['P2'].reshape(3, 4))
# print(data['Tr_velo_to_cam'])
Tr_velo_to_cam = data['Tr_velo_to_cam'].reshape(3, 4)
P_velo2cam_ref = np.vstack((Tr_velo_to_cam, np.array([0., 0., 0., 1.])))


# print(Tr_velo_to_cam)
# print(P_velo2cam_ref)
# print(data)
P_rect2cam2 = data['P2'].reshape(3, 4)
# print(data['P1'].shape)
print(P_rect2cam2)

proj_mat = P_rect2cam2 @ R_ref2rect @ P_velo2cam_ref
print(proj_mat)
# Take an object from label file and the projection matrix (P) and projects the 3D box into the image plane - im