# Inverse projection transformation


## 1. Camera mapping 

A camera is a mapping between the 3D word and a 2D image as: 

![cam-mapping](./images/im_1.png)

And in Homogeneous coordinate:

![](./images/im_2.png)

Here, we consider the simplest pinhole camera model with no skew or distortion factor.

![](./images/im_3.png)

We can find the equations of the perspective projection

![](./images/im_4.jpg)

From OA'B' and OAB we have:  
![](https://latex.codecogs.com/svg.latex?%5Cfrac%7Bf%7D%7BZ%7D%20%3D%20%5Cfrac%7Br%7D%7BR%7D)

From A'B'C' and ABC we have:

![](https://latex.codecogs.com/svg.latex?%5Cfrac%7Bx%7D%7BX%7D%20%3D%20%5Cfrac%7By%7D%7BY%7D%20%3D%20%5Cfrac%7Br%7D%7BR%7D)


Then **perspective projection equation**:
![](https://latex.codecogs.com/svg.latex?x%20%3D%20%5Cfrac%7BXf%7D%7BZ%7D%2C%20y%20%3D%20%5Cfrac%7BYf%7D%7BZ%7D%2C%20z%20%3D%20f)


Using matrix notation:

![](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7Dx_h%20%5C%5C%20y_h%20%5C%5C%20z_h%20%5C%5C%20w%20%5Cend%7Bbmatrix%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20f%20%260%20%260%20%260%20%5C%5C%200%20%26f%20%260%20%260%20%5C%5C%200%20%260%20%26f%20%261%20%5C%5C%200%20%260%20%261%20%260%20%5Cend%7Bbmatrix%7D%5Cbegin%7Bbmatrix%7DX%20%5C%5C%20Y%20%5C%5C%20Z%20%5C%5C%201%20%5Cend%7Bbmatrix%7D)


Verify the correctness of the above matrix (homogenize using w=Z)

![](https://latex.codecogs.com/svg.latex?x%20%3D%20%5Cfrac%7Bx_h%7D%7Bw%7D%20%3D%20%5Cfrac%7BfX%7D%7BZ%7D%2C%20y%20%3D%20%5Cfrac%7By_h%7D%7Bw%7D%20%3D%20%5Cfrac%7BfY%7D%7BZ%7D%2C%20z%20%3D%20%5Cfrac%7Bz_h%7D%7Bw%7D%20%3D%20f)


Because we the image on the 2D image plane, then the z coordinate of the 3D point in the image plane is f, we just want
the x, and y coordinate on the image, the above matrix equation can minimize at:

![](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7Dx_h%20%5C%5C%20y_h%20%5C%5C%20w%20%5Cend%7Bbmatrix%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20f%20%260%20%260%20%260%20%5C%5C%200%20%26f%20%260%20%260%20%5C%5C%200%20%260%20%261%20%260%20%5Cend%7Bbmatrix%7D%5Cbegin%7Bbmatrix%7DX%20%5C%5C%20Y%20%5C%5C%20Z%20%5C%5C%201%20%5Cend%7Bbmatrix%7D)


One thing that we should know that the image root is not coincides with principal point, let's call the principal point 
coordinate on image plane is ![](https://latex.codecogs.com/svg.latex?%28u_0%2C%20v_0%29) , then our matrix equation becomes:

![](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7Dx_h%20%5C%5C%20y_h%20%5C%5C%20w%20%5Cend%7Bbmatrix%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20f%20%260%20%26u_0%20%260%20%5C%5C%200%20%26f%20%26v_0%20%260%20%5C%5C%200%20%260%20%261%20%260%20%5Cend%7Bbmatrix%7D%5Cbegin%7Bbmatrix%7DX%20%5C%5C%20Y%20%5C%5C%20Z%20%5C%5C%201%20%5Cend%7Bbmatrix%7D)


In general, there are **three different** coordinate systems related to map the point in real word into a point on 2D 
image:

![](./images/im_5.png)

so we need to know the transformations between them

The projection matrix P can decomposed into two matrices:

![](./images/im_6.png)

Let's assume that the camera and word share the same coordinate system, then we have the exactly what we have on the above.
But if they are different, we must align them by using Rigid transformation

![](./images/im_7.png)

Translation in H.C:

![](./images/im_8.png)

In homogeneous coordinates, this can be done by:
![](https://latex.codecogs.com/svg.latex?X_c%20%3D%20R%28X_w%20-%20C%29)


When we apply them, we get the general mapping of a pinhole camera:

![](https://latex.codecogs.com/svg.latex?P%20%3D%20KR%20%5Cbegin%7Bbmatrix%7D%20I%7C%20-C%20%5Cend%7Bbmatrix%7D)


And in Matrix form: 

![](./images/im_9.png)

## 2. Properties of perspective projection

### Many-to-one mapping:

The projection of a point is not unique (any point on the light ray has the same projection)

![](./images/im_10.png)

On the above image, all points on OP line have the same projection p on image plane.

### Scaling/Foreshortening
### Effect of focal length 

* As f gets smaller, more points project onto image plane (wide-angle camera)
* As f gets larger, the field of view becomes smaller (more telescopic)

### Lines, distances, angles

* Lines in 3D project to lines in 2D.
* Distances and angles are **not** preserved.
* Parallel lines **do not** in general project to parallel lines (unless they are parallel to the image plane).

### Vanishing point, vanishing line 

## 3. Inverse projection

From the given formular, suppose that we no need to consider the extrinsic matrix [R|t]. 

Then the u, v of point (X, Y, Z, 1) in the camera coordinate on the image plane is: 

![](https://latex.codecogs.com/svg.latex?u%20%3D%20f%5Cfrac%7BX%7D%7BZ%7D%20&plus;%20u_0%2C%20v%20%3D%20f%5Cfrac%7BY%7D%7BZ%7D%20&plus;%20v_0)

Then we can easily compute the X, Y of the point in real-word:

![](https://latex.codecogs.com/svg.latex?X%20%3D%20%28u%20-%20u_0%29%5Cfrac%7BZ%7D%7Bf%7D%2C%20Y%20%3D%20%28v%20-%20v_0%29%5Cfrac%7BZ%7D%7Bf%7D)

In above equation, we need (u,v) coordinate of pixel on image, also the Z-depth image to recover the points in word coordinate.

Pseudo-code:
```python
cam_points = np.zeros((img_h * img_w, 3))
i = 0
# Loop through each pixel in the image
for v in range(height):
    for u in range(width):
        # Apply equation in fig 5
        x = (u - u0) * depth[v, u] / fx
        y = (v - v0) * depth[v, u] / fy
        z = depth[v, u]
        cam_points[i] = (x, y, z)
        i += 1
```

Using Matrix Algebra: 
```python
cam_coords = K_inv @ pixel_coords * depth.flatten()
```

## References 
1. [Projective Camera Model](https://www.imatest.com/support/docs/pre-5-2/geometric-calibration-deprecated/projective-camera/)