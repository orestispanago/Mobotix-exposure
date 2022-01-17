import os

exposure_times = ['1_16000', '1_8000', '1_4000', '1_2000', '1_1000', '1_500',
                  '1_250', '1_90', '1_60', '1_30', '1_10', '1_5', '1_3', '1_2', '1_1']
api_values = [80, 160, 320, 640, 1280, 2560, 4960, 10080,
              20000, 40000, 80000, 160000, 320000, 640000, 1280000]
exp_api_dict = dict(zip(exposure_times, api_values))


def make_dirs_if_not_exist(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
