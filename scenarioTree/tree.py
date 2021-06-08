from typing import List
from copy import deepcopy


class NodeValue:
    def __init__(self):
        # pass
        raise NotImplementedError


# we can generalise this with a node and scenario tree node
class Node:
    def __init__(self, node_id=None, parent_id: str = None, children_details: dict = None,
                 value: NodeValue = None, probability=1):
        # self.stage_index = stage_index
        # self.node_index = node_index
        self.node_id = node_id
        self.parent_id = parent_id
        #self.children_details = deepcopy(children_details)
        self.children_details = children_details or {}
        self.value = value
        self.conditional_probability = probability

    def as_dict(self):
        return {'node_id': self.node_id,
                'parent_id': self.parent_id,
                'children_details': self.children_details,
                'value': self.value,
                'probability': self.conditional_probability}



class ScenarioTree(object):
    def __init__(self, name: str=None, root_node: Node = None):
        self.name = name
        self.nodes: dict = {}
        if root_node is None:
            root_node = Node(parent_id=None, node_id='root')

        self.nodes['root'] = {'node': root_node, 'stage': 0, 'probability': 1}
        self.leaf_node_ids = []

    def build_scenario_tree(self, *args, node_ids: List[str] = None, **kwargs):
        raise NotImplementedError

    def get_node_values(self, node_value_data_getter, node_ids:List[str]=None):
        raise NotImplementedError

    def add_node(self, parent_node_id: str, child_node: Node):
        # check from the not what is the parent, if the parent exists then update the parent node children
        # the details  of the node
        assert (parent_node_id in self.nodes.keys())
        parent_node = self.nodes[f'{parent_node_id}']['node']
        parent_node.children_details.update({f'{child_node.node_id}': child_node.conditional_probability})

        parent_stage = self.nodes[f'{parent_node_id}']['stage']
        parent_probability = self.nodes[f'{parent_node_id}']['probability']

        self.nodes[f'{child_node.node_id}'] = {'node': child_node, 'stage': parent_stage + 1,
                                'probability': parent_probability * child_node.conditional_probability}

    def add_children(self, parent_node:Node, children: List[Node], parent_node_id=None):
        if parent_node_id is None:
            parent_node_id = parent_node.node_id or 'root'
        assert (parent_node_id in self.nodes.keys())
        # assert (sum([node.conditional_probability for node in children]) == 1)

        for node in children:
            self.add_node(parent_node_id=parent_node_id, child_node=node)

    def get_nodes_stage(self, stage: int):
        return [v['node'] for k, v in self.nodes.items() if v['stage'] == stage]

    def get_node(self, node_id=None):
        # return [node for node in self.nodes if node.stage == stage and node.node_id == node_id]
        return self.nodes[node_id] or self.nodes['root']

    def get_children_node(self, stage: int = None, node_number: int = None, node_id=None):
        pass

    def get_scenarios(self):
        pass
