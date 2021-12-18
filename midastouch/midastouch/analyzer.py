from networkx.classes.function import neighbors
import pandas as pd
from midastouch.some_investors import some_investors
from midastouch.brand_names import brand_names
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import json, ast

class Analyzer:
    '''
    Class which vizualizes the data from an experiment.
    '''

    def __init__(self, datadir, paramdir):
        self.datadir = datadir
        self.paramdir = paramdir
        self.loaded_data = False
        self.loaded_parameters = False

    def load_data(self):
        self.loaded_data = True
        self._df = pd.read_csv(self.datadir, index_col = False)
    
    def load_parameters(self):
        self.loaded_parameters = True
        self.parameters = json.load(open(self.paramdir))
    
    def get_parameters(self):
        if not self.loaded_parameters:
            self.load_parameters()
        return {key : self.parameters[key] for key in self.parameters.keys() if key not in set(['datadir', 'experiment_dir', 'timestamp', 'brand_names'])}
    
    def get_data(self):
        if not self.loaded_data:
            self.load_data()
        return self._df

    def get_brand_names(self):
        return self.parameters['brand_names']
    
    # order self._df by score from largest to lowest and return the first top_n datapoints of the ordered dataframe
    def investor_ranking(self, top_n = 100):
        if not self.loaded_data:
            self.load_data()
        pd.set_option('display.max_rows', top_n)
        return self._df.sort_values(by = 'score', ascending = False).head(top_n)

    # return number of investors which have a score of at least x and at most y
    def investor_count(self, bottom_score, top_score):
        if not self.loaded_data:
            self.load_data()
        return len(self._df[(self._df['score'] >= bottom_score) & (self._df['score'] <= top_score)])
    
    # plot graph of investor counts
    def investor_count_chart(self):
        if not self.loaded_data:
            self.load_data()
        score_boundaries = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
        score_labels = [f'{boundary-0.1}-{boundary}' for boundary in score_boundaries]

        n_investors = [self.investor_count(bottom_score=boundary-0.1,top_score=boundary) for boundary in score_boundaries]

        x = np.arange(len(score_labels))  # the label locations
        width = 0.7  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2,n_investors, width, label='number of investments')

        # Add some text for labels, title, etc.
        ax.set_ylabel('Number of Investors')
        ax.set_xlabel('Score Range')
        ax.set_title('Number of Investors by Score')
        ax.set_xticks(x, score_boundaries)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        fig.tight_layout()
        plt.show()

    # return datapoints where the investor name is in the list some_investors
    def investor_sample(self, some_investors=some_investors):
        '''
        Shows the ranking of a sample of investors specified in some_investor, which is a hand-picked list of investors which.
        '''
        if not self.loaded_data:
            self.load_data()
        pd.set_option('display.max_rows', len(some_investors))
        return self._df[self._df['investor_name'].isin(some_investors)].sort_values(by = 'score', ascending = False)

    # construct a graph where the nodes are the self._df['investor_name'] and the edges are the self._df['neighbors']
    def investor_graph(self):
        if not self.loaded_data:
            self.load_data()
        G = nx.Graph()
        for i in range(len(self._df)):
            G.add_node(self._df.iloc[i]['investor_name'])
            neighbors = ast.literal_eval(self._df.iloc[i]['neighbors'])
            for key in neighbors.keys():
                G.add_edge(self._df.iloc[i]['investor_name'], key, weight = neighbors[key])
        return G
    

    # visualize graph using networkx
    def vizualize_investor_graph(self):
        #TODO: implement this correctly, currenly not working
        if not self.loaded_data:
            self.load_data()
        G = self.investor_graph()
        #set some labels
        labels = {}    
        for node in G.nodes():
            if (node in some_investors) or (node in brand_names):
                labels[node] = node
        #set the argument 'with labels' to False so you have unlabeled graph
        nx.draw(G, with_labels=False)
        #Now only add labels to the nodes 
        nx.draw_networkx_labels(G,labels=labels,font_color='r')



    

    

