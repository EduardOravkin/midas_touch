from midastouch.dataloader import Dataloader
from midastouch.brand_names import brand_names
from midastouch.params import params
from midastouch.params import DATADIR, EXPERIMENT_DIR
import pandas as pd
import time, datetime, json, os

class Runner:
    ''' 
        Class used to run experiments.
    '''

    def __init__(self, 
                datadir = DATADIR+"midas_touch_dataset_eduard.csv",
                experiment_dir = EXPERIMENT_DIR, 
                before_after_weights = {'before':4, 'same time': 1, 'after':0.5},
                decay = 'exponential',
                brand_names = brand_names,
                max_dist = 3,
                n_investments = 3,
                cvg_thresh = 0.001,
                ):
        self.datadir = datadir
        self.timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
        self.experiment_dir = experiment_dir
        self.before_after_weights = before_after_weights
        self.decay = decay
        self.brand_names = brand_names
        self.max_dist = max_dist
        self.n_investments = n_investments
        self.cvg_thresh = cvg_thresh
        
    def run(self):         
        dl = Dataloader(datadir = self.datadir)
        dl.load_original_data()
        g = dl.load_raw_data_to_graph(before_after_weights=self.before_after_weights)
        g.remove_rare_investors(n_investments = self.n_investments)
        g.bfs_distance(brand_names=self.brand_names)
        g.calculate_scores(self.max_dist,self.decay,brand_names=self.brand_names,cvg_thresh=self.cvg_thresh)

        df = pd.DataFrame([])
        for node_key in g.nodes:
            df = df.append(pd.DataFrame([[
                                        node_key, 
                                        g.nodes[node_key].score,
                                        g.nodes[node_key].distance,
                                        g.nodes[node_key].investments,
                                        {node.key: g.nodes[node_key].neighbors[node] for node in g.nodes[node_key].neighbors.keys()},
                                        ]], columns = ['investor_name', 'score', 'distance', 'investments', 'neighbors']))
        
        os.makedirs(self.experiment_dir+f'experiment_{self.timestamp}', exist_ok=True)
        df.to_csv(f'{self.experiment_dir}/experiment_{self.timestamp}/experiment_{self.timestamp}.csv', index = False)
        with open(f'experiment_{self.timestamp}/params_{self.timestamp}.py', 'w') as params_file:
            params_file.write(json.dumps(vars(self)))        

if __name__ == '__main__':
    r = Runner(**params)
    r.run()
