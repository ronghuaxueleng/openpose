import json
import pandas as pd
import numpy as np
import glob
import csv

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

    # 检索自己需要的数据
    writeCSV([float(df.at["RElbow", "X"]), float(df.at["RElbow", "Y"]), float(df.at["RWrist", "X"]),
              float(df.at["RWrist", "Y"]), float(df.at["LElbow", "X"])
                 , float(df.at["LElbow", "Y"]), float(df.at["LWrist", "X"]), float(df.at["LWrist", "Y"])])


def writeCSV(data):
    with open('output.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(data)


def main():
    # filelist = getFileName(input("输入JSON目录路径:　"))
    with open('output.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        # 准备自己需要的数据列的名称。与上面的数据相同的列数对齐。
        writer.writerow(
            ["RElbow_x", "RElbow_y", "RWrist_x", "RWrist_y", "LElbow_x", "LElbow_y", "LWrist_x", "LWrist_y"])
    # getSpecificData(filelist)
    getOneSpecificData('full_body1.json')


if __name__ == '__main__':
    main()
