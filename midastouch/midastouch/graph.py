from midastouch.brand_names import brand_names
import numpy as np

class Node:

    def __init__(self, key, score = 0):
        assert 0<=score<=1, "Score must be between 0 and 1, got {}".format(score)
        assert isinstance(key, str), "Key must be a string, got {}".format(key)

        if key in brand_names:
            score = 1

        #TODO: add a function which will check whether the key is similar to a brand name
        # to make sure that no typos are in the dataset

        self.key = key
        self.score = score
        self.neighbors = {} # key: Node, value: weight
        self.distance = 0 # distance from hand-picked nodes, see bfs_distance()

    def update_score(self, max_dist = 4):
        '''
        This function updates the score of the current node. It calculates the weighted 
        average of the scores of its neighbors, modified based on the distance of the 
        neighbor to the hand-picked set of nodes.
        '''
        if len(self.neighbors) == 0:
            pass
        else:
            # calculate the weighted average of the scores of its neighbors
            total_score = 0
            total_weight = 0
            for neighbor in self.neighbors:
                total_score += self.neighbors[neighbor] * neighbor.score * max(0,(1 - neighbor.distance/max_dist)) # assumes the distances have been computed already
                total_weight += self.neighbors[neighbor]
            self.score = total_score / total_weight


class Graph:

    def __init__(self):
        self.nodes = {} # key: Node.key, value : Node

    def add_node(self, key, score = 0):
        node = Node(key, score)
        self.nodes[key] = node
    
    def _add_edge(self, key1, key2, weight = 1):
        assert isinstance(weight, (int, np.int64, float)) , 'weight must be an integer or float, got {}'.format(type(weight))
        
        if key1 not in self.nodes:
            self.add_node(key1)
        if key2 not in self.nodes:
            self.add_node(key2)

        self.nodes[key1].neighbors[self.nodes[key2]] = weight
        self.nodes[key2].neighbors[self.nodes[key1]] = weight 
    
    def has_edge(self, key1, key2):
        if key1 not in self.nodes or key2 not in self.nodes:
            return False

        # check whether graph is directed
        if self.nodes[key2] in self.nodes[key1].neighbors:
            if self.nodes[key1] not in self.nodes[key2].neighbors:
                raise ValueError('Graph is not a directed graph')
        
        if self.nodes[key1] in self.nodes[key2].neighbors:
            if self.nodes[key2] not in self.nodes[key1].neighbors:
                raise ValueError('Graph is not a directed graph')

        return self.nodes[key2] in self.nodes[key1].neighbors

    def get_edge(self, key1, key2):
        if key1 not in self.nodes or key2 not in self.nodes:
            #raise ValueError(f'{key1} or {key2} not in graph')
            return None
        
        if self.has_edge(key1, key2):
            assert self.nodes[key1].neighbors[self.nodes[key2]] == self.nodes[key2].neighbors[self.nodes[key1]], 'weights of neighbors are not equal'
            return self.nodes[key1].neighbors[self.nodes[key2]]
        else:
            return None

    def increase_weight(self, key1, key2, weight=1):
        assert isinstance(weight, (int, np.int64, float)) , 'weight must be an integer or float, got {}'.format(type(weight))

        if not key1 == key2:
            
            if self.has_edge(key1, key2):
                self.nodes[key1].neighbors[self.nodes[key2]] += weight
                self.nodes[key2].neighbors[self.nodes[key1]] += weight
            else:
                self._add_edge(key1, key2, weight)

    def bfs(self, key):
        assert key in self.nodes, 'key not in graph, got {}'.format(key)

        output = []
        visited = set()

        node = self.nodes[key]
        visited.add(node)
        queue = [node]

        while queue:
            node = queue.pop(0)
            output.append(node)

            for neighbor in node.neighbors:
            
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return output
    
    def bfs_distance(self, hand_picked = brand_names):
        ''' 
        Takes a list of hand_picked as input which correspond to a fixed, hand-picked set of 
        nodes in the graph. This function then computes the shortes distance of every node of
        the graph to this hand-picked set of nodes.
        '''
        if len(hand_picked) == 0:
            raise ValueError('hand_picked must not be empty')
        
        queue = [self.nodes[i] for i in brand_names if i in self.nodes]
        visited = set(queue)

        while len(queue) > 0:
            node = queue.pop(0)

            for neighbor in node.neighbors:

                if neighbor not in visited:
                    neighbor.distance = node.distance + 1
                    visited.add(neighbor)
                    queue.append(neighbor)
    
    def calculate_scores(self, hand_picked = brand_names, cvg_thresh = 0.001):
        '''
        Takes a list of hand_picked nodes as input. This function then computes the score of every node of
        the graph. The score is supposed to reflect how related the current node is to this set of 
        hand-picked nodes.
        '''
        if len(hand_picked) == 0:
            raise ValueError('hand_picked must not be empty')

        converged = False
        while not converged:

            max_diff = 0
            for node_key in self.nodes:

                if node_key not in hand_picked:
                    tmp = self.nodes[node_key].score
                    self.nodes[node_key].update_score()
                    max_diff = max(max_diff,abs(tmp - self.nodes[node_key].score))
            
            if max_diff < cvg_thresh:
                converged = True
