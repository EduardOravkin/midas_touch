import unittest
from midastouch.graph import Graph
from midastouch.dataloader import Dataloader

DATADIR = "/Users/eduardoravkin/Desktop/software/vela_eo/Data/midas/"

class TestRawToGraph(unittest.TestCase):
    
    def test_raw_to_graph_1(self):
            
            dl = Dataloader(datadir = DATADIR+"test_data/test_raw_data_1.csv")
            g = dl.load_raw_data_to_graph()

            self.assertTrue([(node.key, g.nodes['VC_a'].neighbors[node]) for node in g.nodes['VC_a'].neighbors] == [('VC_b', 1)],
                            msg="got {}".format([(node.key, g.nodes['VC_a'].neighbors[node]) for node in g.nodes['VC_a'].neighbors]))
            self.assertTrue([(node.key, g.nodes['VC_b'].neighbors[node]) for node in g.nodes['VC_b'].neighbors] == [('VC_a', 1)],
                            msg="got {}".format([(node.key, g.nodes['VC_b'].neighbors[node]) for node in g.nodes['VC_b'].neighbors]))
                            
    def test_raw_to_graph_2(self):
            
            dl = Dataloader(datadir = DATADIR+"test_data/test_raw_data_2.csv")
            g = dl.load_raw_data_to_graph()

            self.assertTrue([(node.key, g.nodes['VC_a'].neighbors[node]) for node in g.nodes['VC_a'].neighbors] == [('VC_b', 1), ('VC_c', 1)],
                            msg="got {}".format([(node.key, g.nodes['VC_a'].neighbors[node]) for node in g.nodes['VC_a'].neighbors]))    
            self.assertTrue([(node.key, g.nodes['VC_b'].neighbors[node]) for node in g.nodes['VC_b'].neighbors] == [('VC_a', 1), ('VC_c', 2)],
                            msg="got {}".format([(node.key, g.nodes['VC_b'].neighbors[node]) for node in g.nodes['VC_b'].neighbors]))
            self.assertTrue([(node.key, g.nodes['VC_c'].neighbors[node]) for node in g.nodes['VC_c'].neighbors] == [('VC_a', 1), ('VC_b', 2)],
                            msg="got {}".format([(node.key, g.nodes['VC_c'].neighbors[node]) for node in g.nodes['VC_c'].neighbors]))
            self.assertTrue([(node.key, g.nodes['VC_d'].neighbors[node]) for node in g.nodes['VC_d'].neighbors] == [],
                            msg="got {}".format([(node.key, g.nodes['VC_d'].neighbors[node]) for node in g.nodes['VC_d'].neighbors]))

    def test_raw_to_graph_3(self):
            
            dl = Dataloader(datadir = DATADIR+"test_data/test_raw_data_3.csv")
            g = dl.load_raw_data_to_graph()

            self.assertTrue([(node.key, g.nodes['VC_a'].neighbors[node]) for node in g.nodes['VC_a'].neighbors] == [('VC_b', 3), ('VC_c', 3)],
                            msg="got {}".format([(node.key, g.nodes['VC_a'].neighbors[node]) for node in g.nodes['VC_a'].neighbors]))
            self.assertTrue([(node.key, g.nodes['VC_b'].neighbors[node]) for node in g.nodes['VC_b'].neighbors] == [('VC_a', 3), ('VC_c', 1)],
                            msg="got {}".format([(node.key, g.nodes['VC_b'].neighbors[node]) for node in g.nodes['VC_b'].neighbors]))
            self.assertTrue([(node.key, g.nodes['VC_c'].neighbors[node]) for node in g.nodes['VC_c'].neighbors] == [('VC_a', 3), ('VC_b', 1)],
                            msg="got {}".format([(node.key, g.nodes['VC_c'].neighbors[node]) for node in g.nodes['VC_c'].neighbors]))
    
    def test_raw_to_graph_4(self):
            # tests whether node investments are correctly calculated
            dl = Dataloader(datadir = DATADIR+"test_data/test_raw_data_4.csv")
            g = dl.load_raw_data_to_graph()

            self.assertTrue(g.nodes['VC_a'].investments == 2, msg="got {}".format(g.nodes['VC_a'].investments))
            self.assertTrue(g.nodes['VC_b'].investments == 3, msg="got {}".format(g.nodes['VC_b'].investments))
            self.assertTrue(g.nodes['VC_c'].investments == 1, msg="got {}".format(g.nodes['VC_c'].investments))
