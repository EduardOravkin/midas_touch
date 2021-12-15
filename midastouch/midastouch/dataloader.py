import pandas as pd
from midastouch.graph import Graph

class Dataloader:

    def __init__(self, datadir):
        self.datadir = datadir
        self.loaded = False
    
    def load_original_data(self):
        self.df = pd.read_csv(self.datadir,index_col=False)
        self.loaded = True

    def load_data_to_graph(self):
        ''' Assumes data is in the format of a csv file with the following columns:
            - investor_name
            - strength
            - base_investor
            Returns an undirected graph where each data point in the above dataset defines
            an edge with weight strength between investor_name and base_investor.'''

        if not self.loaded:
            self.load_original_data()

        assert 'investor_name' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)
        assert 'strength' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)
        assert 'base_investor' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)

        g = Graph()
        for i in range(len(self.df)):

            assert isinstance(self.df.iloc[i]['investor_name'], str), 'investor_name is not a string, got {},{},{},{}'.format(i,self.df.iloc[i]['investor_name'], 
                                                                                                                self.df.iloc[i]['strength'], 
                                                                                                                self.df.iloc[i]['base_investor'])
            assert isinstance(self.df.iloc[i]['base_investor'], str), 'base_investor is not a string, got {},{},{},{}'.format(i,self.df.iloc[i]['investor_name'], 
                                                                                                                self.df.iloc[i]['strength'], 
                                                                                                                self.df.iloc[i]['base_investor'])
            assert self.df.iloc[i]['investor_name'] != self.df.iloc[i]['base_investor'], "investor_name and base_investor cannot be the same, got {},{},{},{}".format(i,self.df.iloc[i]['investor_name'], 
                                                                                                                                                    self.df.iloc[i]['strength'], 
                                                                                                                                                    self.df.iloc[i]['base_investor'])
            assert self.df.iloc[i]['strength'] > 0, "strength must be greater than 0, got {},{},{},{}".format(i,self.df.iloc[i]['investor_name'], 
                                                                                                self.df.iloc[i]['strength'], 
                                                                                                self.df.iloc[i]['base_investor'])
            try:
                float(self.df.iloc[i]['strength'])   
            except:
                raise ValueError('strength is not a float, got {},{},{},{}'.format(i,self.df.iloc[i]['investor_name'], 
                                                                          self.df.iloc[i]['strength'], 
                                                                          self.df.iloc[i]['base_investor']))
            
            # (some of the edges may be duplicated in the dataset because of different funding rounds)
            # if edge exists, increase the weight, otherwise create the edge
            g.increase_weight(self.df.iloc[i]['investor_name'], self.df.iloc[i]['base_investor'], float(self.df.iloc[i]['strength']))

        return g