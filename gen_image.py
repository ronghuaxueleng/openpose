import json
import os
import cv2
import numpy as np

# 骨骼关键点连接对
pose_pairs = {
    25: [[0, 1], [0, 15], [0, 16], [15, 17], [16, 18],
         [1, 2], [1, 5], [1, 8], [2, 3], [3, 4], [5, 6],
         [6, 7], [8, 9], [8, 12], [9, 10], [10, 11],
         [11, 22], [11, 24], [22, 23], [12, 13], [13, 14],
         [14, 21], [14, 19], [19, 20]],
    18: [[1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7],
         [1, 8], [8, 9], [9, 10], [1, 11], [11, 12], [12, 13],
         [1, 0], [0, 14], [14, 16], [0, 15], [15, 17],
         [2, 17], [5, 16]]
}

# 绘制用的颜色
pose_colors = {
    25: [(255., 0., 85.), (255., 0., 0.), (255., 85., 0.), (255., 170., 0.),
         (255., 255., 0.), (170., 255., 0.), (85., 255., 0.), (0., 255., 0.),
         (255., 0., 0.), (0., 255., 85.), (0., 255., 170.), (0., 255., 255.),
         (0., 170., 255.), (0., 85., 255.), (0., 0., 255.), (255., 0., 170.),
         (170., 0., 255.), (255., 0., 255.), (85., 0., 255.), (0., 0., 255.),
         (0., 0., 255.), (0., 0., 255.), (0., 255.,255.), (0., 255., 255.), (0., 255., 255.)],
    18: [[0,100,255], [0,100,255],   [0,255,255],
         [0,100,255], [0,255,255],   [0,100,255],
         [0,255,0],   [255,200,100], [255,0,255],
         [0,255,0],   [255,200,100], [255,0,255],
         [0,0,255],   [255,0,0],     [200,200,0],
         [255,0,0],   [200,200,0],   [0,0,0]]
}

# 手部关键点连接对
hand_pairs = [[0, 1], [0, 5], [0, 9], [0, 13], [0, 17],
              [1, 2],
              [2, 3],
              [3, 4],
              [5, 6], [6, 7], [7, 8],
              [9, 10], [10, 11], [11, 12],
              [13, 14], [14, 15], [15, 16],
              [17, 18], [18, 19], [19, 20]]

hand_colors = [(100., 100., 100.),
               (100, 0, 0),
               (150, 0, 0),
               (200, 0, 0), (255, 0, 0), (100, 100, 0), (150,150, 0), (200, 200, 0), (255, 255, 0),
               (0, 100, 50), (0, 150, 75), (0, 200, 100), (0,255, 125), (0, 50, 100), (0, 75, 150),
               (0, 100, 200), (0, 125, 255), (100, 0, 100), (150, 0, 150),
               (200, 0, 200), (255, 0, 255)]


def handle_json(dir_path, filename):
    jsonfile = os.path.join(dir_path, filename)
    print('hand json {}'.format(jsonfile))
    with open(jsonfile, 'r') as f:
        data = json.load(f)
    # 纯黑色背景
    img = cv2.imread('black.jpg')
    for d in data['people']:
        kpt = np.array(d['pose_keypoints_2d']).reshape((-1, 3))
        for p in pose_pairs[len(kpt)]:
            pt1 = tuple(list(map(int, kpt[p[0], 0:2])))
            c1 = kpt[p[0], 2]
            pt2 = tuple(list(map(int, kpt[p[1], 0:2])))
            c2 = kpt[p[1], 2]
            print('== {}, {}, {}, {} =='.format(pt1, c1, pt2, c2))
            if c1 == 0.0 or c2 == 0.0:
                continue
            color = tuple(list(map(int, pose_colors[len(kpt)][p[0]])))
            img = cv2.line(img, pt1, pt2, color, thickness=4)
            img = cv2.circle(img, pt1, 4, color, thickness=-
            1, lineType=8, shift=0)
            img = cv2.circle(img, pt2, 4, color, thickness=-
            1, lineType=8, shift=0)
        if 'hand_left_keypoints_2d' in d:
            kpt_left_hand = np.array(d['hand_left_keypoints_2d']).reshape((21, 3))
            for q in hand_pairs:
                pt1 = tuple(list(map(int, kpt_left_hand[q[0], 0:2])))
                c1 = kpt_left_hand[p[0], 2]
                pt2 = tuple(list(map(int, kpt_left_hand[q[1], 0:2])))
                c2 = kpt_left_hand[q[1], 2]
                # print('** {}, {}, {}, {} **'.format(pt1, c1, pt2, c2))
                if c1 == 0.0 or c2 == 0.0:
                    continue
                color = tuple(list(map(int, hand_colors[q[0]])))
                img = cv2.line(img, pt1, pt2, color, thickness=4)
            kpt_right_hand = np.array(d['hand_right_keypoints_2d']).reshape((21, 3))
            for k in hand_pairs:
                pt1 = tuple(list(map(int, kpt_right_hand[k[0], 0:2])))
                c1 = kpt_right_hand[k[0], 2]
                pt2 = tuple(list(map(int, kpt_right_hand[k[1], 0:2])))
                c2 = kpt_right_hand[k[1], 2]
                print('** {}, {}, {}, {} **'.format(pt1, c1, pt2, c2))
                if c1 == 0.0 or c2 == 0.0:
                    continue
                color = tuple(list(map(int, hand_colors[q[0]])))
                img = cv2.line(img, pt1, pt2, color, thickness=4)
    if not os.path.exists('results'):
        os.makedirs('results')
    # 保存图片
    cv2.imwrite('{}/{}.jpg'.format(dir_path, filename), img)


if __name__ == '__main__':
    root_path = 'jsons'
    json_dir_list = os.listdir(root_path)
    for json_dir in json_dir_list:
        sub_dir_path = os.path.join(root_path, json_dir)
        handle_json(sub_dir_path, 'face.json')
        handle_json(sub_dir_path, 'full_body.json')
        handle_json(sub_dir_path, 'full_body_fix.json')
