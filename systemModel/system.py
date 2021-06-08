import numpy as np
from dataclasses import dataclass
from typing import List

class System:
    def __init__(self, dynamics: dict=None, constraints: dict=None):
        self.dynamics = dynamics or {}
        self.constraints = constraints or {}
        if len(self.dynamics) == 0:
            self.dynamics['A'] = 0
            self.dynamics['B'] = 0
            self.dynamics['C'] = 0
        else:
            assert self.dynamics['A'].shape[0] == self.dynamics['A'].shape[0], "Matrix A should be square"
            assert self.dynamics['A'].shape[0] == self.dynamics['B'].shape[0], "Matrix B and Matrix A row size is not equal"
            assert self.dynamics['A'].shape[0] == self.dynamics['C'].shape[0], "Matrix B and Matrix A row size is not equal"

        if len(self.constraints) == 0:
            self.constraints['F'] = 0
            self.constraints['G'] = 0
            self.constraints['g'] = 0
        else:
            assert self.constraints['F'].shape[0] == self.constraints['G'].shape[0], "Constraint F and G row is not equal"
            assert self.constraints['F'].shape[0] == self.constraints['g'].shape[0], "Constraint F and g row is not equal"
            assert self.constraints['F'].shape[1] == self.dynamics['A'].shape[0], "Constraint F and " \
                                                                                  "Matrix A columns is not equal"
            assert self.constraints['G'].shape[1] == self.dynamics['B'].shape[0], "Constraint G and " \
                                                                                  "Matrix A columns is not equal"

    def update_state(self, state: np.array, control: np.array, disturbance: np.array):
        updated_state = np.matmul(self.dynamics['A'], state) + np.matmul(self.dynamics['B'], control) \
                       + np.matmul(self.dynamics['C'], disturbance)
        return updated_state

    def are_constraints_satisfied(self, state, control) -> bool:
        constraint = np.matmul(self.constraints['F'], state) + np.matmul(self.constraints['G'], control) \
                     - self.constraints['g']
        return True if constraint.max() <= 0 else False


@dataclass
class SystemDataRecord:
    timestamp: int
    state: np.array = 0
    control: np.array = 0


class ISystemDataRecorder:
    def get_system_data_record(self, timestamp):
        raise NotImplementedError

    def add_system_data_record(self, system_data_records):
        raise NotImplementedError

    def get_latest_system_data_record(self):
        raise NotImplementedError


class SystemGenerator:
    def get_system_dynamics(self):
        raise NotImplementedError

    def get_system_constraints(self):
        raise NotImplementedError

    def get_system_model(self):
        dynamics = self.get_system_dynamics()
        constraints = self.get_system_constraints()
        # system = System(dynamics=dynamics, constraints=constraints)
        return System(dynamics=dynamics, constraints=constraints)


class SystemSimulator:
    def __init__(self, system):
        self.system = system

    def simulate(self, timestamps: List[int], system_data_recorder: ISystemDataRecorder):
        initial_system_data = system_data_recorder.get_latest_system_data_record()





class markov_linear_system:
    def __init__(self):
        pass