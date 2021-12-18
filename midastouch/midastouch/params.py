from midastouch.brand_names import brand_names
import os
root_dir_path = os.path.dirname(os.path.realpath(__file__))+'/../../'
DATADIR = root_dir_path + 'Data/midas/'
EXPERIMENT_DIR = root_dir_path + 'experiments/midas/'

params = {
'datadir' : DATADIR+"midas_touch_dataset_eduard.csv",
'experiment_dir' : EXPERIMENT_DIR, 
'before_after_weights' : {'before':4, 'same time': 1, 'after':0.5},
'decay' : 'exponential',
'max_dist' : 3,
'n_investments' : 3,
'cvg_thresh' : 0.001,
'brand_names' : brand_names
}