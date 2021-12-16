import pandas as pd
from midastouch.graph import Graph

class Dataloader:

    def __init__(self, datadir):
        self.datadir = datadir
        self.loaded = False
    
    def load_original_data(self):
        self.df = pd.read_csv(self.datadir,index_col=False)
        # only consider rows of dataframe that have a no nan entries
        self.df = self.df.dropna(axis=0, how='any')
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
    
    def load_raw_data_to_graph(self):
        ''' Assumes data is in the format of a csv file which contains the following columns:
            - round_created_at
            - round_name
            - company_name
            - investor_name
            Returns an undirected graph where an edge between two VC funds is the number of times they co-invested 
            in the same company. First, we do this regardless of the time of investment (or whether it was at the
            same time). Later will implement different weighting based on funding rounds.
        '''
        # TODO: implement adding more weight (e.g. +x instead of +1) if brand-name investor invests in a later round

        if not self.loaded:
            self.load_original_data()

        assert 'round_created_at' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)
        assert 'round_name' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)
        assert 'company_name' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)
        assert 'investor_name' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)

        g = Graph()
        d = {} # key: company_name, value: list of investors that invested in that company
        for i in range(len(self.df)):

            if self.df.iloc[i]['company_name'] not in d:
                d[self.df.iloc[i]['company_name']] = [self.df.iloc[i]['investor_name']]
                g.add_node(self.df.iloc[i]['investor_name'])
            else:
                for investor in d[self.df.iloc[i]['company_name']]:
                    # increase the weight of the edge between the two investors
                    # weights are doubled if an investor invests twice
                    # edges between an investor and himself are not constructed
                    g.increase_weight(investor, self.df.iloc[i]['investor_name'], 1) 
                d[self.df.iloc[i]['company_name']].append(self.df.iloc[i]['investor_name'])
        
        return g

        