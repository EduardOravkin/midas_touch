from midastouch.runner import Runner
from midastouch.params import DATADIR
from midastouch.brand_names import brand_names

import datetime, time, random, logging, copy, itertools
from multiprocessing import Pool

EXPERIMENT_DIR = "/Users/eduardoravkin/Desktop/software/vela_eo/experiments/midas/experiment_2021_12_17_18_00_00/"

default_params = {
'datadir' : DATADIR+"midas_touch_dataset_eduard.csv",
'experiment_dir' : EXPERIMENT_DIR, 
'before_after_weights' : {'before':4, 'same time': 1, 'after':0.5},
'decay' : 'exponential',
'max_dist' : 3,
'n_investments' : 10,
'cvg_thresh' : 0.001,
'brand_names' : brand_names
}

def run(param):
    try: 
        print(param[0])
        logging.info(param[0])

        params = copy.deepcopy(default_params)
        params['before_after_weights'] = param[1]
        params['decay'] = param[2]
        params['n_investments'] = param[3]
        r = Runner(**params)
        r.run()
    except Exception as e:
        logging.error(str(e)+"\n"+str(params)+"\n")

if __name__ == '__main__':
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
    logging.basicConfig(filename='logfile_{timestamp}.log'.format(timestamp=timestamp), level=logging.INFO)

    combinations_of_before_after_weights = [
    {'before':4, 'same time': 1, 'after':0.5},
    {'before':2, 'same time': 1, 'after':0.5},
    {'before':4, 'same time': 1, 'after':0.1},
    {'before':4, 'same time': 2, 'after':1},
    {'before':1, 'same time': 1, 'after':1},
    ]

    combinations_of_decays = ['exponential', 'linear']

    combinations_of_n_investments = [10,15,30]

    # list of all possible tuples of params
    tmp = list(itertools.product(*[combinations_of_before_after_weights, combinations_of_decays, combinations_of_n_investments])) 
    n_runs = len(tmp)
    combinations_of_params = [(f'{i}/{n_runs}',) + tmp[i] for i in range(n_runs)]

    pool = Pool(processes=1) # use all available cores
    pool.map(run, combinations_of_params)
    