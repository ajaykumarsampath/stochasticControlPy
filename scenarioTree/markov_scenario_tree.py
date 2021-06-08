import itertools
import operator
# from operator import mul
from typing import List

import numpy as np

from scenarioTree.tree import Node, ScenarioTree
from scenarioTree.node_value_record import MarkovTreeDataGetter

class MarkovNode(Node):
    def __init__(self, *args, markov_state=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.markov_state = markov_state

    def as_dict(self):
        return {**super().as_dict(), 'markov_state': self.markov_state}

class MarkovScenarioTree(ScenarioTree):
    def __init__(self, name: str = None, root_node: MarkovNode = None, state_labels: List[str] = None,
                 markov_probability_matrix: np.mat = None, **kwargs):
        if root_node is None:
            root_node = MarkovNode(parent_id=None, node_id='root')
        super().__init__(name, root_node)

        number_states = len(state_labels)
        self.state_labels = state_labels

        assert markov_probability_matrix.shape == (number_states, number_states)
        self.probability_matrix = markov_probability_matrix
        self.markov_tree_value_getter = kwargs.get('markov_tree_getter',
                                             MarkovTreeDataGetter(state_labels=state_labels, dimension=1))

    def build_scenario_tree(self, *args, node_ids: List[str] = None, **kwargs):
        prediction_horizon = kwargs['prediction_horizon']
        number_node_ids = prediction_horizon * len(self.state_labels)
        number_states = len(self.state_labels)
        branching_factor = [number_states] * prediction_horizon

        nodes_at_stage = list(itertools.accumulate(branching_factor, operator.mul))
        cumulative_nodes_stage_wise = list(itertools.accumulate(nodes_at_stage, operator.add))

        if node_ids is None:
            # todo include a logging msg
            print("in future display a warning in the debug mode")
            node_ids = [f'{self.name}_node_{i}' for i in np.arange(0, sum(list(nodes_at_stage)))]

        # todo: eliminate zero probability states
        leaf_ids = []
        for stage in range(0, prediction_horizon):
            if stage == 0:
                nodes_stage = self.generate_transition_nodes(self.nodes['root']['node'], node_ids[0:number_states])
                for n in nodes_stage:
                    self.add_node('root', n)
                    leaf_ids.append(n.node_id)
            else:
                current_stage_node_ids = node_ids[cumulative_nodes_stage_wise[stage-1]:
                                                  cumulative_nodes_stage_wise[stage]]
                # print(current_stage_node_ids)
                pre_stage_nodes = leaf_ids
                leaf_ids = []
                for i in range(0, nodes_at_stage[stage - 1]):
                    # current_node = self.nodes[f'{pre_stage_nodes[i]}']['node']
                    parent_node = self.nodes[f'{pre_stage_nodes[i]}']['node']
                    transition_nodes = self.generate_transition_nodes(parent_node,
                                                               current_stage_node_ids[i*number_states: (i+1)*number_states])
                    self.add_children(parent_node=parent_node, children=transition_nodes)
                    leaf_ids = leaf_ids + list(parent_node.children_details.keys())

        self.leaf_node_ids = leaf_ids

    def generate_transition_nodes(self, node: MarkovNode, child_node_ids: List['str']):
        if node.node_id == 'root' and node.markov_state is None:
            transition_probability = np.diagonal(self.probability_matrix)
        else:
            markov_state = node.markov_state
            markov_state_index = self.state_labels.index(markov_state)
            transition_probability = self.probability_matrix[markov_state_index, :]

        parent_id = node.node_id
        child_nodes = []
        for (state, p, id) in zip(self.state_labels, transition_probability, child_node_ids):
            current_node = MarkovNode(parent_id=parent_id, node_id=id, markov_state=state,
                                      probability=p)
            child_nodes.append(current_node)

        return child_nodes


