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
        self.investments = 1
        self.neighbors = {} # key: Node, value: weight
        self.distance = 0 # distance from hand-picked nodes, see bfs_distance()

    def update_score(self, max_dist = 3, decay = 'linear'):
        '''
        This function updates the score of the current node. It calculates the weighted 
        average of the scores of its neighbors, modified based on the distance of the 
        neighbor to the hand-picked set of nodes.

        Parameters:
        -----------
        max_dist: int
            The maximum distance (from a brand name investor) of a neighbor to be considered 
            when calculating score of a current node. I.e. given a node, if a given neighbor 
            of this node has the nearest brand name investor further away than max_dist, then
            the score of this neighbor will not be considered in calculating the score of the
            given node. Also, the weight of the score of this neighbor is decreasing with the 
            distance (until it reaches max_dist).
        decay: str
            The decay function to be used. Can be 'linear' or 'exponential'.
        '''
        if len(self.neighbors) == 0:
            pass
        else:
            # calculate the weighted average of the scores of its neighbors
            total_score = 0
            total_weight = 0
            for neighbor in self.neighbors:
                total_score += self.neighbors[neighbor] * neighbor.score * self.decay_function(neighbor.distance,max_dist,decay) # assumes the distances have been computed already
                total_weight += self.neighbors[neighbor]
            self.score = total_score / total_weight
    
    def decay_function(self, distance, max_dist, decay):
        if decay == 'linear':
            return max(0, 1 - distance/max_dist)
        elif decay == 'exponential':
            return 1/(2**distance) if distance <= max_dist else 0
        else:
            raise ValueError('decay must be linear or exponential')
            


class Graph:

    def __init__(self):
        self.nodes = {} # key: Node.key, value : Node

    def _add_node(self, key):
        assert isinstance(key, str), "Key must be a string, got {}".format(key)

        node = Node(key, score=0)
        self.nodes[key] = node

    def update_node(self, key, n_investments = 1):
        assert isinstance(key, str), "Key must be a string, got {}".format(key)

        if key in self.nodes:
            self.nodes[key].investments += n_investments
        else:
            self._add_node(key)
    
    def add_node_if_not_exists(self, key):
        if key not in self.nodes:
            self._add_node(key)
    
    def _add_edge(self, key1, key2, weight = 1):
        assert isinstance(weight, (int, np.int64, float)) , 'weight must be an integer or float, got {}'.format(type(weight))

        if key1 not in self.nodes or key2 not in self.nodes:
            raise ValueError('key1 or key2 not in graph')
        
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

    def update_edge(self, key1, key2, weight=1):
        '''
        Updates the edge if the edge exists, otherwise adds the edge. 
        Does not increase the number of investments of the nodes if both exist.
        Does create the nodes if they do not exist (and hence sets their number of investments to 1).
        '''
        assert isinstance(weight, (int, np.int64, float)) , 'weight must be an integer or float, got {}'.format(type(weight))

        if not key1 == key2:
            # if the node exist do nothing, otherwise create the nodes
            self.add_node_if_not_exists(key1)
            self.add_node_if_not_exists(key2)

            if self.has_edge(key1, key2):
                self.nodes[key1].neighbors[self.nodes[key2]] += weight
                self.nodes[key2].neighbors[self.nodes[key1]] += weight
            else:
                self._add_edge(key1, key2, weight)
    
    def update_edge_and_nodes(self, key1, key2, weight=1):
        '''
        Updates the edge if the edge exists, otherwise adds the edge. 
        Does increase the number of investments of the nodes (regardless of if they exist).
        '''

        if not key1 == key2:
            if key1 in self.nodes:
                self.update_node(key1)
            if key2 in self.nodes:
                self.update_node(key2)
            self.update_edge(key1, key2, weight)
        
    def get_edge(self, key1, key2):
        if key1 not in self.nodes or key2 not in self.nodes:
            return None
        
        if self.has_edge(key1, key2):
            assert self.nodes[key1].neighbors[self.nodes[key2]] == self.nodes[key2].neighbors[self.nodes[key1]], 'weights of neighbors are not equal'
            return self.nodes[key1].neighbors[self.nodes[key2]]
        else:
            return None

    def remove_node(self, key):
        if key in self.nodes:
            for neighbor in self.nodes[key].neighbors:
                neighbor.neighbors.pop(self.nodes[key])
            self.nodes.pop(key) 

    def remove_rare_investors(self, n_investments = 3):
        '''
        Remove investors with less than n_investments investments. Note this removes all of the 
        effect (on the whole network) of the investors which have less than n_investments investments.
        '''
        assert isinstance(n_investments, (int, np.int64, float)) , 'n_investments must be an integer or float, got {}'.format(type(n_investments))
        assert n_investments >= 0, 'n_investments must be non-negative'

        for node_key in list(self.nodes.keys()):
            if self.nodes[node_key].investments <= n_investments:
                self.remove_node(node_key)

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
    
    def bfs_distance(self, brand_names = brand_names):
        ''' 
        Takes a list of brand_names as input which correspond to a fixed, hand-picked set of 
        nodes in the graph. This function then computes the shortes distance of every node of
        the graph to this hand-picked set of nodes.
        '''
        if len(brand_names) == 0:
            raise ValueError('brand_names must not be empty')
        
        queue = [self.nodes[i] for i in brand_names if i in self.nodes]
        visited = set(queue)

        while len(queue) > 0:
            node = queue.pop(0)

            for neighbor in node.neighbors:

                if neighbor not in visited:
                    neighbor.distance = node.distance + 1
                    visited.add(neighbor)
                    queue.append(neighbor)
    
    def calculate_scores(self, 
                        max_dist = 3,
                        decay = 'linear',
                        brand_names = brand_names, 
                        cvg_thresh = 0.001):
        '''
        Takes a list of brand_names nodes as input. This function then computes the score of every node of
        the graph. The score is supposed to reflect how related the current node is to this set of 
        hand-picked nodes.
        '''
        if len(brand_names) == 0:
            raise ValueError('brand_names must not be empty')

        converged = False
        while not converged:

            max_diff = 0
            for node_key in self.nodes:

                if node_key not in brand_names:
                    tmp = self.nodes[node_key].score
                    self.nodes[node_key].update_score(max_dist, decay)
                    max_diff = max(max_diff,abs(tmp - self.nodes[node_key].score))
            
            if max_diff < cvg_thresh:
                converged = True
