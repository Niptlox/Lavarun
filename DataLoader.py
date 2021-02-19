import pickle
import os.path

DATA_FILE = "data\\save\\data.dat"

def checking_file():
    if not os.path.exists(DATA_FILE):
        print("os.path.exists(DATA_FILE)")
        with open(DATA_FILE, 'wb') as f:
            pickle.dump({"null": True}, f)


def get_max_score():
    data_new = get_dict_data()
    max_score_f = data_new.get("max_score", -1)
    return max_score_f


def get_dict_data():
    checking_file()
    with open(DATA_FILE, 'rb') as f:
        data_new = pickle.load(f)
    print("get_dict_data", data_new)
    return data_new


def put_max_score(max_score):
    data = get_dict_data()
    data["max_score"] = max_score
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(data, f)
