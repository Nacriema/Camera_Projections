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

From OA'B' and OAB we have: $\frac{f}{Z} = \frac{r}{R}$
From A'B'C' and ABC we have: \frac{x}{X} = \frac{y}{Y} = \frac{r}{R}

Then **perspective projection equation**: $x = \frac{Xf}{Z}, y = \frac{Yf}{Z}, z = f$

Using matrix notation:

$\begin{bmatrix}x_h
\\ y_h
\\ z_h
\\ w
\end{bmatrix}  = \begin{bmatrix}
f &0  &0  &0 \\ 
0 &f  &0  &0 \\ 
0 &0  &f  &1 \\ 
0 &0  &1  &0 
\end{bmatrix}\begin{bmatrix}X
\\ Y
\\ Z
\\ 1
\end{bmatrix}$

Verify the correctness of the above matrix (homogenize using w=Z)

$x = \frac{x_h}{w} = \frac{fX}{Z}, y = \frac{y_h}{w} = \frac{fY}{Z}, z = \frac{z_h}{w} = f$

Because we the image on the 2D image plane, then the z coordinate of the 3D point in the image plane is f, we just want
the x, and y coordinate on the image, the above matrix equation can minimize at:

$\begin{bmatrix}x_h
\\ y_h
\\ w
\end{bmatrix}  = \begin{bmatrix}
f &0  &0  &0 \\ 
0 &f  &0  &0 \\  
0 &0  &1  &0 
\end{bmatrix}\begin{bmatrix}X
\\ Y
\\ Z
\\ 1
\end{bmatrix}$ 

One thing that we should know that the image root is not coincides with principal point, let's call the principal point 
coordinate on image plane is $(u_0, v_0)$, then our matrix equation becomes:

\begin{bmatrix}x_h
\\ y_h
\\ w
\end{bmatrix}  = \begin{bmatrix}
f &0  &u_0  &0 \\ 
0 &f  &v_0  &0 \\  
0 &0  &1  &0 
\end{bmatrix}\begin{bmatrix}X
\\ Y
\\ Z
\\ 1
\end{bmatrix}

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
$X_c = R(X_w - C)$

When we apply them, we get the general mapping of a pinhole camera:

$P = KR \begin{bmatrix}
I| -C
\end{bmatrix}$

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

$u = f\frac{X}{Z} + u_0, v = f\frac{Y}{Z} + v_0$

Then we can easily compute the X, Y of the point in real-word:

$X = (u - u_0)\frac{Z}{f}, Y = (v - v_0)\frac{Z}{f}$

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