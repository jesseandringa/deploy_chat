import numpy as np


def computeCov2D(mean, focal_x, focal_y, tan_fovx, tan_fovy, cov3D, viewmatrix):
    t = np.dot(viewmatrix, np.append(mean, 1.0))

    limx = 1.3 * tan_fovx
    limy = 1.3 * tan_fovy
    txtz = t[0] / t[2]
    tytz = t[1] / t[2]
    t[0] = min(limx, max(-limx, txtz)) * t[2]
    t[1] = min(limy, max(-limy, tytz)) * t[2]

    J = np.array(
        [
            [focal_x / t[2], 0, -(focal_x * t[0]) / (t[2] * t[2])],
            [0, focal_y / t[2], -(focal_y * t[1]) / (t[2] * t[2])],
            [0, 0, 0],
        ]
    )

    W = viewmatrix[:3, :3]

    T = np.dot(W, J)

    Vrk = np.array(
        [
            [cov3D[0], cov3D[1], cov3D[2]],
            [cov3D[1], cov3D[3], cov3D[4]],
            [cov3D[2], cov3D[4], cov3D[5]],
        ]
    )

    cov = np.dot(np.transpose(T), np.dot(np.transpose(Vrk), T))

    # "lowpass filter"
    cov[0, 0] += 0.3
    cov[1, 1] += 0.3
    return cov[0, 0], cov[0, 1], cov[1, 1]


def ndc2Pix(v, S):
    return ((v + 1.0) * S - 1.0) * 0.5


def main(
    a_center,
    a_col,
    a_opacity,
    a_covA,
    a_covB,
    W,
    H,
    focal_x,
    focal_y,
    tan_fovx,
    tan_fovy,
    scale_modifier,
    projmatrix,
    viewmatrix,
    boxmin,
    boxmax,
):
    p_orig = a_center

    # Discard splats outside of the scene bounding box (should not happen)
    # if (p_orig.x < boxmin.x || p_orig.y < boxmin.y || p_orig.z < boxmin.z ||
    #     p_orig.x > boxmax.x || p_orig.y > boxmax.y || p_orig.z > boxmax.z):
    #         gl_Position = vec4(0, 0, 0, 1)
    #         return

    # Transform point by projecting
    p_hom = np.dot(projmatrix, np.append(p_orig, 1))
    p_w = 1.0 / (p_hom[3] + 1e-7)
    p_proj = np.dot(p_hom[:3], p_w)

    # Perform near culling, quit if outside
    p_view = np.dot(viewmatrix, np.append(p_orig, 1))
    if p_view[2] <= 0.4:
        return None, None, None, None, None

    cov3D = np.array([a_covA[0], a_covA[1], a_covA[2], a_covB[0], a_covB[1], a_covB[2]])
    cov = computeCov2D(p_orig, focal_x, focal_y, tan_fovx, tan_fovy, cov3D, viewmatrix)

    det = cov[0] * cov[2] - cov[1] * cov[1]
    if det == 0.0:
        return None, None, None, None, None

    det_inv = 1.0 / det
    conic = np.dot(np.array([cov[2], -cov[1], cov[0]]), det_inv)

    mid = 0.5 * (cov[0] + cov[2])
    lambda1 = mid + np.sqrt(max(0.1, mid * mid - det))
    lambda2 = mid - np.sqrt(max(0.1, mid * mid - det))
    my_radius = np.ceil(3.0 * np.sqrt(max(lambda1, lambda2)))
    point_image = np.array([ndc2Pix(p_proj[0], W), ndc2Pix(p_proj[1], H)])

    my_radius *= 0.15 + scale_modifier * 0.85
    scale_modif = 1.0 / scale_modifier
    print("point_image:", point_image)
    screen_pos = np.dot(
        point_image + my_radius,
        np.array([1, 1]),
    )

    col = a_col
    con_o = np.append(conic, a_opacity)
    xy = point_image
    pixf = screen_pos
    depth = p_view[2]

    clip_pos = screen_pos / np.array([W, H]) * 2.0 - 1.0
    print("clip_pos:", clip_pos)

    return col, depth, scale_modif, con_o, xy, pixf


# Example usage
a_col = np.array([0.5, 0.5, 0.5])
a_opacity = 0.7
a_covA = np.array([1.0, 1.0, 1.0])
a_covB = np.array([2.0, 2.0, 2.0])
W = 1920.0
H = 1080.0
focal_x = 1.0
focal_y = 1.0
tan_fovx = 1.0
tan_fovy = 1.0
scale_modifier = 1.0
boxmin = np.zeros(3)
boxmax = np.ones(3)
projection_matrix = np.array(
    [
        [0.8653073310852051, 0, 0, 0],
        [0, 2.3002474308013916, 0, 0],
        [0, 0, -1.0020020008087158, -1],
        [0, 0, -0.20020020008087158, 0],
    ]
)

view_projection_matrix = np.array(
    [
        [0.8653073310852051, 8.624546950685429e-33, -6.135493079603875e-17, -0],
        [-0, -2.3002474308013916, -6.135493079603875e-17, -6.123234262925839e-17],
        [5.298479605673307e-17, -1.4084953537867137e-16, 1.0020020008087158, 1],
        [-0, -0, 0.8018018007278442, 1],
    ]
)

view_matrix = np.array([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 1]])

position = np.array([-2.5, -5.5, 12])


result = main(
    position,
    a_col,
    a_opacity,
    a_covA,
    a_covB,
    W,
    H,
    focal_x,
    focal_y,
    tan_fovx,
    tan_fovy,
    scale_modifier,
    view_projection_matrix,
    view_matrix,
    boxmin,
    boxmax,
)
# print(result)
