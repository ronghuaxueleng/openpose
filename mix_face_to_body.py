import json
import os

import numpy as np
import pandas as pd

idnex_map = {
    25: ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist",
         "MidHip", "RHip",
         "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar",
         "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel"],
    18: ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist", "RHip",
         "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar"]
}


def getOneSpecificData(json_path):
    with open(json_path) as f:
        json_data = json.load(f)
        data = np.array(json_data['people'][0]['pose_keypoints_2d']).reshape(-1, 3)
        return pd.DataFrame(data, columns=['X', 'Y', 'P'],
                            index=idnex_map[len(data)]), json_data


if __name__ == '__main__':
    root_path = 'jsons'
    json_dir_list = os.listdir(root_path)
    for json_dir in json_dir_list:
        face_path = os.path.join(root_path, json_dir, 'face.json')
        full_body_path = os.path.join(root_path, json_dir, 'full_body.json')
        fix_full_body_path = os.path.join(root_path, json_dir, 'full_body_fix.json')
        face, face_json = getOneSpecificData(face_path)
        body, body_json = getOneSpecificData(full_body_path)
        for index, row in face.iterrows():
            if row['X'] != 0.0 and row['Y'] != 0.0 and row['P'] != 0.0:
                body['X'][index] = row['X']
                body['Y'][index] = row['Y']
        body_json['people'][0]['pose_keypoints_2d'] = []
        for index, row in body.iterrows():
            body_json['people'][0]['pose_keypoints_2d'].append(row['X'])
            body_json['people'][0]['pose_keypoints_2d'].append(row['Y'])
            body_json['people'][0]['pose_keypoints_2d'].append(row['P'])
        if 'face_keypoints_2d' in face_json['people'][0]:
            body_json['people'][0]['face_keypoints_2d'] = face_json['people'][0]['face_keypoints_2d']
        with open(fix_full_body_path, "w") as sf:
            json.dump(body_json, sf)

