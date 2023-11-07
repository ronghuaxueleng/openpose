import json
import os

import pandas as pd
import numpy as np
import glob

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
        data = json.load(f)
        data = np.array(data['people'][0]['pose_keypoints_2d']).reshape(-1, 3)
        df = pd.DataFrame(data, columns=['X', 'Y', 'P'],
                          index=idnex_map[len(data)])
        df.to_csv('output.csv')


if __name__ == '__main__':
    # getOneSpecificData('jsons/face1/full_body.json')
    # getOneSpecificData('jsons/face1/face.json')
    root_path = 'jsons'
    json_dir_list = os.listdir(root_path)
    for json_dir in json_dir_list:
        print(json_dir)
