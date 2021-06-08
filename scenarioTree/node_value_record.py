import numpy as np

from scenarioTree.tree import NodeValue
from typing import List

class INodeValueGetter:
     def get_node_value(self):
         raise NotImplementedError


# TODO: add the kind of distribution to the random node values
class RandomNodeValueGetter:
    def generate_random_additive_node_values(self, number=1, dimension=1, seed=None):
        self.seed = seed or 0

        return [VectorNodeValue(vector_value=np.random(dimension)) for i in range(0, number)]


class MarkovTreeDataGetter:
    def __init__(self, state_labels: List['str'], markov_node_values=None, dimension=1):
        self.markov_state_value = {}
        # self.markov_state_value = markov_state
        # node_values = [v is None for k,v in self.markov_state_value]
        #todo integrate them in logger
        np.random.seed(0)
        num_state = np.arange(0, len(state_labels))
        if markov_node_values is None:
            print("generating random node values for the markov state, "
                  "in future add a node value getter")
        for (i, k) in zip(num_state, state_labels):
            if markov_node_values is None:
                self.markov_state_value[f'{k}'] = VectorNodeValue(vector_value=np.random.random(dimension))
            else:
                self.markov_state_value[f'{k}'] = markov_node_values[i]

    def update_markov_state(self, markov_state: str, node_value: NodeValue):
        self.markov_state_value[f'{markov_state}'] = node_value

    def get_markov_state_node_value(self, markov_state):
        return self.markov_state_value[f'{markov_state}']

class VectorNodeValue(NodeValue):
    def __init__(self, vector_value=np.array([0]), scenario_tree_id=None, node_ids=None):
        self.vector_value = vector_value
        self.scenario_tree_id = scenario_tree_id
        self.node_ids = node_ids


class MarkovAdditiveNodeValue(NodeValue):
    pass
