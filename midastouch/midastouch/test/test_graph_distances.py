import unittest
from midastouch.graph import Graph
from midastouch.dataloader import Dataloader

DATADIR = "/Users/eduardoravkin/Desktop/software/vela_eo/Data/midas/"


class TestGraphDistances(unittest.TestCase):
    
    def test_graph_distance_2(self):
            
            dl = Dataloader(datadir = DATADIR+"test_data/test_graph_2.csv")
            g = dl.load_data_to_graph()
            g.bfs_distance()

            self.assertTrue([(node.key, node.distance) for node in g.bfs('Accel')] == [('Accel',0), ('X',1), ('Y',1), ('Z',2)], 
                            msg=f"got {[(node.key, node.distance) for node in g.bfs('Accel')]}")


    def test_graph_distance_3(self):
        
        dl = Dataloader(datadir = DATADIR+"test_data/test_graph_3.csv")
        g = dl.load_data_to_graph()
        g.bfs_distance()

        self.assertTrue([(node.key, node.distance) for node in g.bfs('Accel')] == [('Accel', 0), ('X',1), ('Z',1), ('Y',2), ('A',3), ('B', 4)],
                        msg=f"got {[(node.key, node.distance) for node in g.bfs('Accel')]}")


    def test_graph_distance_5(self):

        dl = Dataloader(datadir = DATADIR+"test_data/test_graph_5.csv")
        g = dl.load_data_to_graph()
        g.bfs_distance()

        self.assertTrue([(node.key, node.distance) for node in g.bfs('Accel')] == [('Accel', 0), ('X',1), ('Z',1), ('Y',2), ('GV',0), ('C', 3), ('A',1), ('B', 2)],
                        msg=f"got {[(node.key, node.distance) for node in g.bfs('Accel')]}")

if __name__ == '__main__':
    unittest.main()