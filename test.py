import json
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


def getFileName(path):
    filelist = glob.glob(path + "/*")
    return filelist


def getSpecificData(filelist):
    for i in range(len(filelist)):
        getOneSpecificData(filelist[i])


def getOneSpecificData(json_path):
    with open(json_path) as f:
        data = json.load(f)
        data = np.array(data['people'][0]['pose_keypoints_2d']).reshape(-1, 3)
        df = pd.DataFrame(data, columns=['X', 'Y', 'P'],
                          index=idnex_map[len(data)])
        df.to_csv('output.csv')


def main():
    # filelist = getFileName(input("输入JSON目录路径:　"))
    # getSpecificData(filelist)
    getOneSpecificData('full_body1.json')


if __name__ == '__main__':
    main()
