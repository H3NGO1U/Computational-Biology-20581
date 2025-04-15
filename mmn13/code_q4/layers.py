import numpy as np
from typing import List

HIDDEN_BIAS_FILE = "hidden.txt"
VISIBLE_BIAS_FILE = "visible.txt"
NUM_OF_HIDDEN = 17
NUM_OF_INPUT = 12
NUM_OF_OUTPUT = 3
NUM_OF_VISIBLE = NUM_OF_INPUT + NUM_OF_OUTPUT
NUM_OF_DISCRETE_GROUPS = 3

def turn_on_neurons(neurons: List, indices: List):
    for index in indices:
        neurons[index] = 1

class HiddenLayer:
    def __init__(self, randomize_bias: bool):
        #If training, initialize bias vector with random data.
        #Else, load bias from file
        self.bias = np.random.randn(NUM_OF_HIDDEN) if randomize_bias else np.loadtxt(HIDDEN_BIAS_FILE)
        self.neurons = np.zeros(NUM_OF_HIDDEN)

    def __str__(self):
        return f"Hidden Layer: {self.neurons}"

class VisibleLayer:
    def __init__(self, randomize_bias: bool, input_values: List = None, ranges: List = None):
        #If training, initialize bias vector with random data.
        #Else, load bias from file
        self.bias = np.random.randn(NUM_OF_VISIBLE) if randomize_bias else np.loadtxt(VISIBLE_BIAS_FILE)
        if input_values:
            self.set_input(input_values, ranges)
        self.reset_output()

    def set_input(self, input_values, ranges):
        self.input_neurons = np.zeros(NUM_OF_INPUT)
        discrete_values = [self.convert_to_discrete(input_values[i], ranges[i], NUM_OF_DISCRETE_GROUPS) for i in range(len(input_values))]
        indices = [i * NUM_OF_DISCRETE_GROUPS + val  for i, val in enumerate(discrete_values)]
        turn_on_neurons(self.input_neurons, indices)

    def set_output(self, output_index: int):
        self.output_neurons[output_index] = 1

    def reset_output(self):
        self.output_neurons = np.zeros(NUM_OF_OUTPUT)

    def get_all_neurons(self):
        return np.concatenate((self.input_neurons, self.output_neurons), axis=0)
    
    def convert_to_discrete(self, cur_val ,cur_range , num_of_groups) -> int:
        """
        Return the number of the group the cur_val is assigned to, out of <num_of_groups>.
        """
        if num_of_groups == 0:
            raise Exception("Number of discrete groups cannot be zero")
        min_val, max_val = cur_range
        gap = (max_val - min_val) / num_of_groups
        if cur_val <= min_val:
            return 0
        if cur_val >= max_val:
            return num_of_groups - 1
        return int((cur_val - min_val) // gap)
        
    def __str__(self):
        return f"Visible Layer: \nInput neurons: {self.input_neurons}\nOutput neurons: {self.output_neurons}"   
    
    