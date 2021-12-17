import unittest
from midastouch.graph import Graph
from midastouch.dataloader import Dataloader

DATADIR = "/Users/eduardoravkin/Desktop/software/vela_eo/Data/midas/"


class TestGraphBasic(unittest.TestCase):
    
    def testgraph(self):

        g = Graph()
        g.update_node('a')
        g.nodes['a'].score = 1
        g.update_node('b')
        g.nodes['b'].score = 0.5
        g.update_node('c')
        g.update_node('d')

        g.update_edge('a', 'b', weight=1)
        g.update_edge('a', 'c', weight=2)
        g.update_edge('b', 'c', weight=100)
        g.update_edge('b', 'd', weight=3)

        self.assertEqual(list(g.nodes.keys()), ['a', 'b', 'c', 'd'])
        self.assertTrue([(node.key, node.score) for node in g.bfs('a')] == [('a',1), ('b',0.5), ('c',0), ('d',0)],
                        msg="got {}".format([(node.key, node.score) for node in g.bfs('a')]))

    def test_graph_update_edge(self):
        g = Graph()
        g.update_node('a')
        g.update_node('b')
        g.update_edge('a', 'b', 1)
        self.assertTrue(g.get_edge('a','b') == 1)
        g.update_edge('a', 'b', 1)
        self.assertTrue(g.get_edge('a','b') == 2)

    def test_graph_update_node(self):
        g = Graph()

        g.update_node('a')
        self.assertTrue((g.nodes['a'].investments == 1) & (g.nodes['a'].score == 0), msg="got {}, {}".format(g.nodes['a'].investments, g.nodes['a'].score))

        g.add_node_if_not_exists('a')
        self.assertTrue((g.nodes['a'].investments == 1) & (g.nodes['a'].score == 0), msg="got {}, {}".format(g.nodes['a'].investments, g.nodes['a'].score))

        g.update_node('a')
        self.assertTrue((g.nodes['a'].investments == 2) & (g.nodes['a'].score == 0), msg="got {}, {}".format(g.nodes['a'].investments, g.nodes['a'].score))

        g.update_edge_and_nodes('a', 'b', 10)
        self.assertTrue((g.nodes['a'].investments == 3) & (g.nodes['b'].investments == 1) & (g.get_edge('a','b') == 10), msg="got {}, {}, {}".format(g.nodes['a'].investments, g.nodes['b'].investments, g.get_edge('a','b')))

        g.update_edge('a', 'b', 1)
        self.assertTrue((g.nodes['a'].investments == 3) & (g.nodes['b'].investments == 1) & (g.get_edge('a','b') == 11), msg="got {}, {}, {}".format(g.nodes['a'].investments, g.nodes['b'].investments, g.get_edge('a','b')))

        self.assertEqual(list(g.nodes.keys()), ['a','b'])
    
    def test_graph_remove_node(self):
        g = Graph()
        g.update_node('a')
        g.update_node('b')
        g.update_edge('a', 'b', 1)
        g.update_edge('b', 'a', 1)
        g.remove_node('a')
        self.assertEqual(list(g.nodes.keys()), ['b'])
        self.assertEqual(g.get_edge('b','a'), None)
        self.assertEqual(g.get_edge('a','b'), None)


if __name__ == '__main__':
    unittest.main()