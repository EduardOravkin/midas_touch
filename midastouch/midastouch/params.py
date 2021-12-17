DATADIR = "/Users/eduardoravkin/Desktop/software/vela_eo/Data/midas/"
EXPERIMENT_DIR = "/Users/eduardoravkin/Desktop/software/vela_eo/experiments/midas/"
from midastouch.brand_names import brand_names

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