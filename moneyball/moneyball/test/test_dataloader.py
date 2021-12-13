from unittest import TestCase
from moneyball.dataset.dataloader import DataLoader
import os
import pandas as pd

class TestDataloader(TestCase):

    def test_load_original(self):

        dl = DataLoader(data_dir=os.getcwd() + 'Data/')

        dfs  = dl.load_original()

        self.assertTrue(len(dfs) == 2)
        self.assertTrue(len(dfs['succ']) == len(dfs['unsucc']))
        self.assertTrue(type(dfs['succ']['list']) == pd.DataFrame) 
