from unittest import TestCase
import unittest
from midastouch.dataloader import Dataloader
from midastouch.params import DATADIR

class TestDataloader(unittest.TestCase):
    
    def test_load_data_test_1(self):
        
        dl = Dataloader(datadir = DATADIR+"test_data/test_graph_1.csv")
        g = dl.load_data_to_graph()

        self.assertEqual(set(g.nodes.keys()), set(['Accel', 'X', 'Y']), msg=f"got {list(g.nodes.keys())}")
        self.assertTrue([(node.key, node.score) for node in g.bfs('Accel')] == [('Accel', 1), ('X',0), ('Y',0)], 
                        msg=f"got {[(node.key, node.score) for node in g.bfs('Accel')]}")


    def test_load_data_test_2(self):

        dl = Dataloader(datadir = DATADIR+"test_data/test_graph_2.csv")
        g = dl.load_data_to_graph()

        self.assertEqual(set(g.nodes.keys()), set(['Accel', 'X', 'Y', 'Z']), msg=f"got {list(g.nodes.keys())}")
        self.assertTrue([(node.key, node.score) for node in g.bfs('Accel')] == [('Accel', 1), ('X',0), ('Y',0), ('Z',0)], 
                        msg=f"got {[(node.key, node.score) for node in g.bfs('Accel')]}")
        self.assertTrue([(node.key, node.score) for node in g.bfs('X')] == [('X', 0), ('Accel',1), ('Z',0), ('Y',0)], 
                        msg=f"got {[(node.key, node.score) for node in g.bfs('Accel')]}")
    

    def test_load_data_test_3(self):

        dl = Dataloader(datadir = DATADIR+"test_data/test_graph_3.csv")
        g = dl.load_data_to_graph()

        self.assertEqual(set(g.nodes.keys()), set(['Accel', 'X', 'Y', 'Z', 'A', 'B']), 
                        msg=f"got {list(g.nodes.keys())}")
        self.assertTrue([(node.key, node.score) for node in g.bfs('Accel')] == [('Accel', 1), ('X',0), ('Z',0), ('Y',0), ('A',0), ('B',0)],
                        msg=f"got {[(node.key, node.score) for node in g.bfs('Accel')]}")


    def test_load_ventech_data(self):
        
        dl = Dataloader(datadir = DATADIR+"ventech_RMap.csv")
        g = dl.load_data_to_graph()
        self.assertTrue(g is not None)


if __name__ == '__main__':
    unittest.main()