import pandas as pd

class DataLoader:
    def __init__(self, data_dir):
        self.data_dir = data_dir
    
    def load_original(self):
        ''' Returns dictionary (with keys ``succ'', ``unsucc'') of 
            dictionaries (with keys ``list'', ``academic'', ``work'', ``investor'') 
            of pandas dataframes.'''    

        dfs = {}
        # succesful companies
        dfs['succ']['list'] = pd.read_csv(self.data_dir+'moneyball/'+'succ_csv/succ_list.csv')
        dfs['succ']['academic'] = pd.read_csv(self.data_dir+'moneyball/'+'succ_csv/succ_academic.csv')
        dfs['succ']['work'] = pd.read_csv(self.data_dir+'moneyball/'+'succ_csv/succ_work.csv')
        dfs['succ']['investor'] = pd.read_csv(self.data_dir+'moneyball/'+'succ_csv/succ_investor.csv')

        # unsuccesful companies
        dfs['unsucc']['list'] = pd.read_csv(self.data_dir+'moneyball/'+'unsucc_csv/unsucc_list.csv')
        dfs['unsucc']['academic'] = pd.read_csv(self.data_dir+'moneyball/'+'unsucc_csv/unsucc_academic.csv')
        dfs['unsucc']['work'] = pd.read_csv(self.data_dir+'moneyball/'+'unsucc_csv/unsucc_work.csv')
        dfs['unsucc']['investor'] = pd.read_csv(self.data_dir+'moneyball/'+'unsucc_csv/unsucc_investor.csv')

        return dfs

    def load_intersection(self):
        ''' Returns dictionary (with keys ``succ'', ``unsucc'') of pandas dataframes. 
            The dataframes will contain only those companies which are present in all of
            the ``list'', ``academic'', ``work'', ``investor'', ``datasets'''

            

        
