import unittest
from midastouch.dataloader import Dataloader

DATADIR = "/Users/eduardoravkin/Desktop/software/vela_eo/Data/midas/"

class TestRareInvestors(unittest.TestCase):

    def test_graph_scores_5(self):
            
            dl = Dataloader(datadir = DATADIR+"test_data/test_graph_5.csv")
            g = dl.load_data_to_graph()

            g.remove_rare_investors(n_investments=1)
            self.assertTrue(set(g.nodes.keys()) == set(['Accel','X','Y','Z','GV','A']),msg="Nodes are not as expected, got: "+str(set(g.nodes.keys())))
            self.assertTrue(set([(node.key, g.nodes['A'].neighbors[node]) for node in g.nodes['A'].neighbors]) == set([('Y',1),('GV',1)]), msg="Neighbors are not as expected, got: "+str(g.nodes['A'].neighbors))

            g.remove_rare_investors(n_investments=2)
            self.assertTrue(set(g.nodes.keys()) == set(['X', 'Y', 'Z', 'A']),msg="Nodes are not as expected, got: "+str(set(g.nodes.keys())))
            self.assertTrue(set([(node.key, g.nodes['X'].neighbors[node]) for node in g.nodes['X'].neighbors]) == set([('Y',1),('Z',1)]), msg="Neighbors are not as expected, got: "+str(g.nodes['X'].neighbors))

            # try the same again but from freshly loaded graph
            dl = Dataloader(datadir = DATADIR+"test_data/test_graph_5.csv")
            g = dl.load_data_to_graph()

            g.remove_rare_investors(n_investments=2)
            self.assertTrue(set(g.nodes.keys()) == set(['X', 'Y', 'Z', 'A']),msg="Nodes are not as expected, got: "+str(set(g.nodes.keys())))
            self.assertTrue(set([(node.key, g.nodes['X'].neighbors[node]) for node in g.nodes['X'].neighbors]) == set([('Y',1),('Z',1)]), msg="Neighbors are not as expected, got: "+str(g.nodes['X'].neighbors))

