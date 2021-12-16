import unittest
from midastouch.graph import Graph
from midastouch.dataloader import Dataloader

DATADIR = "/Users/eduardoravkin/Desktop/software/vela_eo/Data/midas/"
ok_thresh = 0.01
cvg_thresh = 0.01

class TestGraphScores(unittest.TestCase):
    
    def test_graph_scores_1(self, ok_thresh = ok_thresh):
            
            dl = Dataloader(datadir = DATADIR+"test_data/test_graph_1.csv")
            g = dl.load_data_to_graph()
            g.bfs_distance()
            g.calculate_scores(cvg_thresh = cvg_thresh)

            true_scores = {
                'Accel': 1,
                'X': 8/13,
                'Y': 6/13,
            }
            proposed_scores = {node.key : node.score for node in g.bfs('Accel')}

            self.assertTrue(all([abs(proposed_scores[key] - true_scores[key]) < ok_thresh for key in true_scores.keys()]),
                            msg=f"got {[(node.key, node.distance, node.score) for node in g.bfs('Accel')]}"
                            )


    def test_graph_scores_2(self, ok_thresh = ok_thresh):
        
        dl = Dataloader(datadir = DATADIR+"test_data/test_graph_2.csv")
        g = dl.load_data_to_graph()
        g.bfs_distance()
        g.calculate_scores(cvg_thresh = cvg_thresh)

        true_scores = {
            'Accel': 1,
            'X': 8/13,
            'Y': 8/13,
            'Z': 6/13,
        }
        proposed_scores = {node.key : node.score for node in g.bfs('Accel')}
    
        self.assertTrue(all([abs(proposed_scores[key] - true_scores[key]) < ok_thresh for key in true_scores.keys()]),
                        msg=f"got {[(node.key, node.distance, node.score) for node in g.bfs('Accel')]}"
                        )
        

    def test_graph_scores_3(self, ok_thresh = ok_thresh):
        
        dl = Dataloader(datadir = DATADIR+"test_data/test_graph_3.csv")
        g = dl.load_data_to_graph()
        g.bfs_distance()
        g.calculate_scores(cvg_thresh = cvg_thresh)

        true_scores = {
            'Accel': 1,
            'X': 248/433,
            'Y': 96/433,
            'Z': 1052/1299,
            'A': 24/433,
            'B': 6/433,
        }
        proposed_scores = {node.key : node.score for node in g.bfs('Accel')}
    
        self.assertTrue(all([abs(proposed_scores[key] - true_scores[key]) < ok_thresh for key in true_scores.keys()]),
                        msg=f"got {[(node.key, node.distance, node.score) for node in g.bfs('Accel')]}"
                        )

    
    def test_graph_scores_4(self, ok_thresh = ok_thresh):
        
        dl = Dataloader(datadir = DATADIR+"test_data/test_graph_4.csv")
        g = dl.load_data_to_graph()
        g.bfs_distance()
        g.calculate_scores(cvg_thresh = cvg_thresh)

        true_scores = {
            'Accel': 1,
            'X': 8/63,
            'Y': 2/21,
            'Z': 2/21,
        }
        proposed_scores = {node.key : node.score for node in g.bfs('Accel')}
    
        self.assertTrue(all([abs(proposed_scores[key] - true_scores[key]) < ok_thresh for key in true_scores.keys()]),
                        msg=f"got {[(node.key, node.distance, node.score) for node in g.bfs('Accel')]}"
                        )

    def test_graph_scores_5(self, ok_thresh = ok_thresh):
        
        dl = Dataloader(datadir = DATADIR+"test_data/test_graph_5.csv")
        g = dl.load_data_to_graph()
        g.bfs_distance()
        g.calculate_scores(cvg_thresh = cvg_thresh)

        true_scores = {
            'Accel': 1,
            'GV': 1,
            'X': 15812/26655,
            'Y': 2376/8885,
            'Z': 7652/8885,
            'A': 11512/26655,
            'B': 2878/8885,
            'C': 1188/8885,
        }
        proposed_scores = {node.key : node.score for node in g.bfs('Accel')}
    
        self.assertTrue(all([abs(proposed_scores[key] - true_scores[key]) < ok_thresh for key in true_scores.keys()]),
                        msg=f"got {[(node.key, node.distance, node.score) for node in g.bfs('Accel')]}"
                        )
    
    def test_graph_scores_initial_given_data(self, ok_thresh = ok_thresh):
        
        dl = Dataloader(datadir = DATADIR+"ventech_RMap.csv")
        g = dl.load_data_to_graph()
        g.bfs_distance()
        g.calculate_scores(cvg_thresh = cvg_thresh)

        # the ventech dataset is such that all of the edges have
        # one of the brand name investors as a target
        # therefore all of the scores should be 1
        # and all of the distances should be either 1 or 0
        proposed_scores = {node.key : 1 for node in g.bfs('Accel')}

        self.assertTrue(all([abs(proposed_scores[key] - 1) < ok_thresh for key in proposed_scores.keys()]))    
    

if __name__ == '__main__':
    unittest.main()