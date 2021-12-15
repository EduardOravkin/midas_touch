import unittest
from midastouch.graph import Graph
from midastouch.dataloader import Dataloader

DATADIR = "/Users/eduardoravkin/Desktop/software/vela_eo/Data/midas/"


class TestGraphBasic(unittest.TestCase):
    
    def testgraph(self):

        g = Graph()
        g.add_node('a',1)
        g.add_node('b',0.5)
        g.add_node('c')
        g.add_node('d')

        g.increase_weight('a', 'b', weight=1)
        g.increase_weight('a', 'c', weight=2)
        g.increase_weight('b', 'c', weight=100)
        g.increase_weight('b', 'd', weight=3)

        self.assertEqual(list(g.nodes.keys()), ['a', 'b', 'c', 'd'])
        self.assertTrue([(node.key, node.score) for node in g.bfs('a')] == [('a',1), ('b',0.5), ('c',0), ('d',0)],
                        msg="got {}".format([(node.key, node.score) for node in g.bfs('a')]))

    def test_graph_increase_weight(self):
        g = Graph()
        g.add_node('a')
        g.add_node('b')
        g.increase_weight('a', 'b', 1)
        self.assertTrue(g.get_edge('a','b') == 1)
        g.increase_weight('a', 'b', 1)
        self.assertTrue(g.get_edge('a','b') == 2)

if __name__ == '__main__':
    unittest.main()