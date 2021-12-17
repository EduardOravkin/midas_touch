import pandas as pd
from midastouch.graph import Graph
from midastouch.brand_names import brand_names

class Dataloader:

    def __init__(self, datadir):
        self.datadir = datadir
        self.loaded = False
    
    def load_original_data(self):
        self.df = pd.read_csv(self.datadir,index_col=False)
        # only consider rows of dataframe that have no nan entries
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
            g.update_edge_and_nodes(self.df.iloc[i]['investor_name'], self.df.iloc[i]['base_investor'], float(self.df.iloc[i]['strength']))

        return g
    
    def load_raw_data_to_graph(self, before_after_weights = {'before':1, 'same time': 1, 'after':1}):
        ''' Assumes data is in the format of a csv file which contains the following columns:
            - round_created_at
            - round_name
            - company_name
            - investor_name
            Returns an undirected graph where an edge between two VC funds is the number of times they co-invested 
            in the same company. First, we do this regardless of the time of investment (or whether it was at the
            same time). Later will implement different weighting based on funding rounds.

            before_after_weight : {'before' : float > 0, 'same time' : float > 0, 'after' : float > 0}
                If one of the two nodes of an edge is a brand name investor,
                then if the other investor invested earlier / at the same time / later, the edge will be weighted 
                4x / 1x / 1/2x respectively (if the values). 
        '''

        if not self.loaded:
            self.load_original_data()

        assert 'round_created_at' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)
        assert 'round_name' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)
        assert 'company_name' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)
        assert 'investor_name' in self.df.columns, 'got the following columns: {}'.format(self.df.columns)
        assert list(before_after_weights.keys()) == ['before', 'same time', 'after'], 'got the following keys: {}'.format(list(before_after_weights.keys()))
        assert before_after_weights['before'] > 0, 'before_after_weights["before"] must be greater than 0, got {}'.format(before_after_weights['before'])
        assert before_after_weights['same time'] > 0, 'before_after_weights["same time"] must be greater than 0, got {}'.format(before_after_weights['same time'])
        assert before_after_weights['after'] > 0, 'before_after_weights["after"] must be greater than 0, got {}'.format(before_after_weights['after'])

        g = Graph()
        d = {} # key: company_name, value: list of investors that invested in that company
        for i in range(len(self.df)):
            
            g.update_node(self.df.iloc[i]['investor_name'])

            if self.df.iloc[i]['company_name'] not in d:
                d[self.df.iloc[i]['company_name']] = [self.df.iloc[i]]
            else:
                for datapoiont in d[self.df.iloc[i]['company_name']]:
                    # increase the weight of the edge between the two investors
                    # weights are doubled if an investor invests twice
                    # edges between an investor and himself are not constructed
                    # if one of the investors is a brand name investor, 
                    # then the weight is increased by before_after_weights 
                    # as described in the parameter description
                    weight = self.increase_weight(datapoint_1 = self.df.iloc[i],
                                                    datapoint_2 = datapoiont,
                                                    weight = 1,
                                                    before_after_weights = before_after_weights, 
                                                  )
                    g.update_edge(datapoiont['investor_name'], self.df.iloc[i]['investor_name'], weight)
                d[self.df.iloc[i]['company_name']].append(self.df.iloc[i])
        
        return g
    
    def increase_weight(self, datapoint_1, datapoint_2, before_after_weights, weight = 1):
        '''
        Increases the weight 
        '''
        if datapoint_1['investor_name'] in brand_names and datapoint_2['investor_name'] not in brand_names:
            return before_after_weights[self.compare_funding_rounds(datapoint_1, datapoint_2)] * weight

        elif datapoint_2['investor_name'] in brand_names and datapoint_1['investor_name'] not in brand_names:
            return before_after_weights[self.compare_funding_rounds(datapoint_2, datapoint_1)] * weight

        else:
            return weight

    def compare_funding_rounds(self, datapoint_1, datapoint_2):
        '''
        Returns 'before', 'same time', or 'after' depending on the time of investment of the two investments,
        relative to the first investment.
        '''
        if datapoint_1['round_created_at'] == datapoint_2['round_created_at']:
            return 'same time'
        elif datapoint_2['round_created_at'] < datapoint_1['round_created_at']:
            return 'before'
        elif datapoint_2['round_created_at'] > datapoint_1['round_created_at']:
            return 'after'
        