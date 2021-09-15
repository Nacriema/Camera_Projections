#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sep 14 11:51:31 2021

@author: Nacriema

Refs:
"""
from PIL import Image, ImageDraw
import numpy as np
from math import cos, sin


def draw_3d_bbox(calib_data, label_data, image):
    for key in label_data.keys():
        for index in range(len(label_data[key])):
            entity = label_data[key][index]
            color_choice = {
                'Car': 'red',
                'Van': 'white',
                'Pedestrian': 'green',
                'Cyclist': 'yellow',
                'DontCare': 'green',
            }
            color = color_choice.get(key)
            w = entity[7]
            h = entity[8]
            l = entity[9]
            x = entity[10]
            y = entity[11]
            z = entity[12]
            ry = entity[13]
            # Rotational matrix around the pitch
            R_y = np.array(
                [[cos(ry), 0, sin(ry)],
                 [0, 1, 0],
                 [-sin(ry), 0, cos(ry)]]
            )
            # 3D bounding box corners points
            '''                     
              B'---------------C'
             /|               /|         Object-coordinate (According to the KITTI's Document)
            A'---------------D'|         
            | |              | | h
            | B----------------C
            |/       O-------|/-l---------> z-axis 
            A----------------D  
                   / w 
                  /  |
            x-axis   | 
                     |
                     v z-axis

            '''
            x_corners = [-l / 2, l / 2, l / 2, l / 2, l / 2, -l / 2, -l / 2, -l / 2]
            y_corners = [-h, -h, 0, 0, -h, -h, 0, 0]
            z_corners = [-w / 2, -w / 2, -w / 2, w / 2, w / 2, w / 2, w / 2, -w / 2]

            # bounding box in object coordinate
            corners_3d = np.array([x_corners, y_corners, z_corners])  # Shape (3, 8)
            # rotate
            corners_3d = R_y.dot(corners_3d)
            # translate
            corners_3d += np.array([x, y, z]).reshape((3, 1))
            corners_3d_hm = np.vstack((corners_3d, np.ones((corners_3d.shape[-1]))))

            # Now corners_3D_hm points are in the Camera reference coordinate
            # MAKE THE PROJECTION MATRIX P FROM REFERENCE CAMERA TO IMAGE
            # R0_rect is purely the Rotation matrix in h.c system
            R0_rect = np.zeros((4, 4))
            R0_rect[:3, :3] = calib_data['R0_rect'].reshape(3, 3)
            R0_rect[3, 3] = 1

            # P2 is the Camera Matrix - a very big component thus image = P2.X
            # But what exactly what P2 matrix P2 generally can decompose at P2 = K[R|T]
            # K: camera intrinsic parameters
            # R: Rotation matrix
            # T: Translation
            # Due to the camera in the system is a kind of stereo vision
            P2 = calib_data['P2'].reshape(3, 4)
            P = P2 @ R0_rect
            # Project to 2D image in HC

            corners_2d = P.dot(corners_3d_hm)

            # From H.C Coordinate to Euclidean Coordinate
            corners_2d = corners_2d / corners_2d[2]
            corners_2d = corners_2d[:2]

            #######################
            # bb3d_lines_verts is use to draw 3d bounding box in 2d image with less vertex as possible 16 is the
            # smallest: https://stackoverflow.com/questions/25195363/draw-cube-vertices-with-fewest-number-of-steps
            #######################

            corners_2d = corners_2d.astype(int)
            bb3d_lines_vert_idx = [0, 1, 2, 3, 4, 5, 6, 7, 0, 5, 4, 1, 2, 7, 6, 3]
            bb2d_lines_vert = corners_2d[:, bb3d_lines_vert_idx]

            # Display these 2d point into image
            draw = ImageDraw.Draw(image)  # cam_2_im
            for point in corners_2d.T:
                draw.point((point[0], point[1]), fill='yellow')
            list_edge_draw = []
            for point in bb2d_lines_vert.T:
                list_edge_draw.extend([point[0], point[1]])
            tuple_edge_draw = tuple(list_edge_draw)
            draw.line(tuple_edge_draw, width=1, fill=color)
    image.show()


def load_data(im_src, velo_bin_src, calib_src, label_src):
    cam_2_im = Image.open(im_src).convert('RGB')
    velo_pcl = np.fromfile(velo_bin_src, dtype=np.float32).reshape(-1, 4)
    calib_data = {}
    with open(calib_src, 'r') as f:
        for line in f.readlines():
            if ':' in line.strip():
                key, value = line.split(':', 1)
                calib_data[key] = np.array([float(x) for x in value.split()])

    label_data = {}
    with open(label_src, 'r') as f:
        for line in f.readlines():
            if len(line) > 3:  # ???
                key, value = line.split(' ', 1)
                if key in label_data.keys():
                    label_data[key].append(np.array([float(x) for x in value.split()]))
                else:
                    label_data[key] = [np.array([float(x) for x in value.split()])]

    return cam_2_im, velo_pcl, calib_data, label_data


if __name__ == '__main__':
    im_source = './data/000114_image.png'
    velo_bin_source = './data/000114.bin'
    calib_source = './data/000114_calib.txt'
    label_source = './data/000114_label.txt'
    # Load all data
    image_2, velo_bin, calib, label = load_data(im_source, velo_bin_source, calib_source, label_source)
    draw_3d_bbox(calib, label, image_2)


# THIS IS DON'T NEED CURRENTLY
# Tr_velo_to_cam is the Projection matrix - Rigid Transformation in h.c system
# Tr_velo_to_cam = np.vstack((calib_data['Tr_velo_to_cam'].reshape(3, 4), np.array([0., 0., 0., 1.])))
# Tr_cam_to_velo = np.linalg.inv(Tr_velo_to_cam)
# cam_2_im.show()
# print(cam_2_im.size)
print('===============================')
