import unittest
from midastouch.graph import Graph
from midastouch.dataloader import Dataloader

DATADIR = "/Users/eduardoravkin/Desktop/software/vela_eo/Data/midas/"

class TestRoundsRank(unittest.TestCase):
    
    def test_raw_to_graph_1(self):
            
            dl = Dataloader(datadir = DATADIR+"test_data/test_dataloader_funding_rounds_rank.csv")
            g = dl.load_raw_data_to_graph(
                before_after_weights={
                    "before": 4,
                    "same time": 1,
                    "after": 0.5,
                }
            )

            self.assertTrue([(node.key, g.nodes['Accel'].neighbors[node]) for node in g.nodes['VC_a'].neighbors] == [('GV',1),('VC_b', 0.5)],
                            msg="got {}".format([(node.key, g.nodes['Accel'].neighbors[node]) for node in g.nodes['Accel'].neighbors]))

            self.assertTrue([(node.key, g.nodes['GV'].neighbors[node]) for node in g.nodes['GV'].neighbors] == [('Accel', 1), ('VC_a',4)],
                            msg="got {}".format([(node.key, g.nodes['GV'].neighbors[node]) for node in g.nodes['GV'].neighbors]))

            self.assertTrue([(node.key, g.nodes['VC_a'].neighbors[node]) for node in g.nodes['VC_a'].neighbors] == [('GV', 4), ('VC_b',1)],
                            msg="got {}".format([(node.key, g.nodes['VC_a'].neighbors[node]) for node in g.nodes['VC_a'].neighbors]))

            self.assertTrue([(node.key, g.nodes['VC_b'].neighbors[node]) for node in g.nodes['VC_b'].neighbors] == [('VC_a',1), ('Accel', 0.5)],
                            msg="got {}".format([(node.key, g.nodes['VC_b'].neighbors[node]) for node in g.nodes['VC_b'].neighbors]))
