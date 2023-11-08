# 将25关键点转换成18关键点
import json

json18_path = './k18/pose1_keypoints.json'
json25_path = './k25/pose1_keypoints.json'
dict = {}


def joint_map(k25):
    k18 = []
    joint_index = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    for k in joint_index:
        k18.append(k25[3 * k])
        k18.append(k25[3 * k + 1])
        k18.append(k25[3 * k + 2])
    assert len(k18) == 18 * 3
    return k18


def get_json_data(json_path):
    with open(json_path, 'rb') as f:
        params = json.load(f)
        for i in range(len(params['people'])):
            params['people'][i]['pose_keypoints_2d'] = joint_map(params['people'][i]['pose_keypoints_2d'])
        dict = params
    f.close()
    return dict


def write_json_data(dict):
    with open(json18_path, 'w') as r:
        json.dump(dict, r)
    r.close()


the_revised_dict = get_json_data(json25_path)
write_json_data(the_revised_dict)
