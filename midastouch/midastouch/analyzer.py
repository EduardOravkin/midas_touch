import pandas as pd
from midastouch.some_investors import some_investors
import networkx as nx

class Analyzer:
    '''
    Class which vizualizes the data from an experiment.
    '''

    def __init__(self, datadir, paramdir):
        self.datadir = datadir
        self.paramdir = paramdir
        self.loaded = False

    def load_data(self):
        self.loaded = True
        self._df = pd.read_csv(self.datadir, index = False)
    
    def load_parameters(self):
        self.parameters = pd.read_csv(self.paramdir, index = False)
    
    def get_parameters(self):
        return {key : self.parameters[key] for key in self.parameters.keys() if key not in set(['datadir', 'experiment_dir', 'timestamp', 'brand_names'])}
    
    def get_data(self):
        return self._df

    def get_brand_names(self):
        return self.parameters['brand_names']
    
    # order self._df by score from largest to lowest and return the first top_n datapoints of the ordered dataframe
    def investor_ranking(self, top_n = 100):
        pd.set_option('display.max_rows', top_n)
        return self._df.sort_values(by = 'score', ascending = False).head(top_n)

    # return number of investors which have a score of at least x and at most y
    def investor_count(self, x, y):
        return len(self._df[(self._df['score'] >= x) & (self._df['score'] <= y)])

    # return datapoints where the investor name is in the list some_investors
    def investor_sample(self, some_investors=some_investors):
        '''
        Shows the ranking of a sample of investors specified in some_investor, which is a hand-picked list of investors which.
        '''
        return self._df[self._df['investor'].isin(some_investors)].sort_values(by = 'score', ascending = False)

    # construct a graph where the nodes are the self._df['investor'] and the edges are the self._df['neighbors']
    def get_investor_graph(self):
        G = nx.Graph()
        G.add_nodes_from(self._df['investor'])
        G.add_edges_from(self._df['neighbors'].tolist())
        return G

    # visualize graph using networkx
    def vizsualize_investor_graph(self):
        G = self.get_investor_graph()
        nx.draw(G, with_labels = True)
        nx.draw_networkx_labels(G, pos = nx.spring_layout(G))
        nx.draw_networkx_edge_labels(G, pos = nx.spring_layout(G))
        nx.draw_networkx_edge_labels(G, pos = nx.spring_layout(G), edge_labels = nx.get_edge_attributes(G, 'weight'))



    

    

