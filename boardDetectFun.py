import numpy as np
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict
from statistics import mean
import cv2 as cv


def h_v_lines(lines):
    x_dim = lines.shape[0]
    h_lines, v_lines = [], []
    lines = lines.reshape(x_dim, 2)

    for rho, theta in lines:
        if theta < np.pi / 4 or theta > np.pi - np.pi / 4:
            v_lines.append([rho, theta])
        else:
            h_lines.append([rho, theta])
    return h_lines, v_lines


# Find the intersections of the lines
def line_intersections(h_lines, v_lines):
    points = []
    for r_h, t_h in h_lines:
        for r_v, t_v in v_lines:
            a = np.array([[np.cos(t_h), np.sin(t_h)],
                         [np.cos(t_v), np.sin(t_v)]])
            b = np.array([r_h, r_v])
            inter_point = np.linalg.solve(a, b)
            points.append(inter_point)
    return np.array(points)


# Hierarchical cluster (by euclidean distance) intersection points
def cluster_points(points):
    dists = spatial.distance.pdist(points)
    single_linkage = cluster.hierarchy.single(dists)
    flat_clusters = cluster.hierarchy.fcluster(single_linkage, 10, 'distance')
    cluster_dict = defaultdict(list)
    for i in range(len(flat_clusters)):
        cluster_dict[flat_clusters[i]].append(points[i])
    cluster_values = cluster_dict.values()
    clusters = map(lambda arr: (np.mean(np.array(arr)[:, 0]), np.mean(
        np.array(arr)[:, 1])), cluster_values)
    return sorted(list(clusters), key=lambda k: [k[1], k[0]])


def augment_points(points):
    points_shape = list(np.shape(points))
    # print('shape : ' + str(points_shape))
    augmented_points = []
    for row in range(int(points_shape[0] / 11)):
        start = row * 9
        end = (row * 9) + 8
        rw_points = points[start:end + 1]
        rw_y = []
        rw_x = []
        for point in rw_points:
            x, y = point
            rw_y.append(y)
            rw_x.append(x)
        y_mean = mean(rw_y)
        for i in range(len(rw_x)):
            point = (rw_x[i], y_mean)
            augmented_points.append(point)
    augmented_points = sorted(augmented_points, key=lambda k: [k[1], k[0]])
    return augmented_points


def boardPoints(points):
    points_shape = list(np.shape(points))
    p_x = []
    p_y = []
    diff_y = []
    y_prev = points[0][1]
    for point in points:
        x, y = point
        p_x.append(x)
        p_y.append(y)
        diff = y_prev - y
        diff_y.append(diff)
        y_prev = y
    return diff_y


def drawLines(img, lines):
    if lines is not None:
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)


def drawLinesP(img, lines):
    for points in lines:
        x1, y1, x2, y2 = points[0]
        cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
