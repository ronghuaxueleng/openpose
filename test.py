import json
import pandas as pd
import numpy as np
import glob
import csv


def getFileName(path):
    filelist = glob.glob(path + "/*")
    return filelist


def getSpecificData(filelist):
    for i in range(len(filelist)):
        with open(filelist[i]) as f:
            data = json.load(f)
            data = np.array(data['people'][0]['pose_keypoints_2d']).reshape(-1, 3)
        df = pd.DataFrame(data, columns=['X', 'Y', 'P'],
                          index=["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist",
                                 "MidHip", "RHip", \
                                 "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar",
                                 "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel"])

        # 自分の必要なデータを取り出す
        writeCSV([float(df.at["RElbow", "X"]), float(df.at["RElbow", "Y"]), float(df.at["RWrist", "X"]),
                  float(df.at["RWrist", "Y"]), float(df.at["LElbow", "X"]) \
                     , float(df.at["LElbow", "Y"]), float(df.at["LWrist", "X"]), float(df.at["LWrist", "Y"])])


def writeCSV(data):
    with open('output.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(data)


def main():
    filelist = getFileName(input("JSONのディレクトリのパスを入力:　"))
    with open('output.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        # 自分の必要なデータの列の名前を用意。上のデータと同じだけの列数を揃える。
        writer.writerow(
            ["RElbow_x", "RElbow_y", "RWrist_x", "RWrist_y", "LElbow_x", "LElbow_y", "LWrist_x", "LWrist_y"])
    getSpecificData(filelist)


if __name__ == '__main__':
    main()
