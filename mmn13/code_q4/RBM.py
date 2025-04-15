from layers import *
import numpy as np
import random

WEIGHTS_FILE = "weights.txt"

MIN_SEPAL_LEN = 4.3
MAX_SEPAL_LEN = 7.9

MIN_SEPAL_WIDTH = 2.0
MAX_SEPAL_WIDTH = 4.4

MIN_PETAL_LEN = 1.0
MAX_PETAL_LEN = 6.9

MIN_PETAL_WIDTH = 0.1
MAX_PETAL_WIDTH = 2.5

ranges = [(MIN_SEPAL_LEN, MAX_SEPAL_LEN),
            (MIN_SEPAL_WIDTH, MAX_SEPAL_WIDTH),
            (MIN_PETAL_LEN, MAX_PETAL_LEN), 
            (MIN_PETAL_WIDTH, MAX_PETAL_WIDTH)]

outputs = ["I. setosa", "I. versicolor", "I. virginica"]

def get_probability(neurons: np.ndarray, bias: float, weights: np.ndarray, T: int = 1) -> float:
    activation_energy =  bias + np.dot(neurons, weights)
    return  1 / (1 + np.exp(-activation_energy/T))

def get_neuron_next_value(neurons: np.ndarray, bias: float, weights: np.ndarray, T: int = 1) -> int:
    return 1 if get_probability(neurons, bias, weights, T) >= random.random() else 0
   
class RBM:
    def __init__(self, input_values: List, temperature: int, randomize: bool = False):
        self.visible_layer = VisibleLayer(input_values = input_values, ranges = ranges, randomize_bias=randomize)
        self.hidden_layer = HiddenLayer(randomize_bias=randomize)
        self.temperature = temperature
        if not randomize:
            self.weights = np.loadtxt(WEIGHTS_FILE)
        else:
            self.weights = np.random.randn(NUM_OF_VISIBLE, NUM_OF_HIDDEN)

    def __str__(self):
        return str(self.visible_layer) + "\n" + str(self.hidden_layer) + "\n\n"
        
    def step(self):
        for i in range(len(self.hidden_layer.neurons)):
            self.hidden_layer.neurons[i] = get_neuron_next_value(self.visible_layer.get_all_neurons(), self.hidden_layer.bias[i], self.weights[:, i], self.temperature)
        for i in range(len(self.visible_layer.output_neurons)):
            self.visible_layer.output_neurons[i] = get_neuron_next_value(self.hidden_layer.neurons, self.visible_layer.bias[i+NUM_OF_INPUT], self.weights[i+NUM_OF_INPUT], self.temperature)
        self.temperature -= 1
        
    def classify(self) -> str:
        while self.temperature > 0: 
            self.step()
        if self.visible_layer.output_neurons.tolist().count(1) == 1:
            index = self.visible_layer.output_neurons.tolist().index(1)
            return outputs[index]
        else:
            return "Could not determine"


class TrainRBM:
    def __init__(self, train_rate: float):
        self.train_rate = train_rate
        self.weights = np.random.randn(NUM_OF_VISIBLE, NUM_OF_HIDDEN) * 0.01
        self.visible_layer = VisibleLayer(randomize_bias = True)
        self.hidden_layer = HiddenLayer(randomize_bias = True)

    def train(self, input_data: List[float], output_data: str):
        self.visible_layer.set_input(input_data, ranges)
        self.visible_layer.reset_output()
        self.visible_layer.set_output(outputs.index(output_data))
        original_visible_neurons = self.visible_layer.get_all_neurons()
        for i in range(NUM_OF_HIDDEN):
            self.hidden_layer.neurons[i] = get_neuron_next_value(self.visible_layer.get_all_neurons(), self.hidden_layer.bias[i], self.weights[:, i])
        for i in range(NUM_OF_VISIBLE):
            if i < NUM_OF_INPUT:
                self.visible_layer.input_neurons[i] = get_neuron_next_value(self.hidden_layer.neurons, self.visible_layer.bias[i], self.weights[i])
            else:
                self.visible_layer.output_neurons[i-NUM_OF_INPUT] = get_neuron_next_value(self.hidden_layer.neurons, self.visible_layer.bias[i], self.weights[i])
        hidden_probs = [0] * NUM_OF_HIDDEN       
        for i in range(NUM_OF_HIDDEN):
            hidden_probs[i] = get_probability(original_visible_neurons, self.hidden_layer.bias[i], self.weights[:, i])
            self.hidden_layer.bias[i] += self.train_rate * (hidden_probs[i] - self.hidden_layer.neurons[i])
        for i in range(NUM_OF_VISIBLE):
            self.visible_layer.bias[i] += self.train_rate * (original_visible_neurons[i] - self.visible_layer.get_all_neurons()[i])
        for i in range(NUM_OF_VISIBLE):
            for j in range(NUM_OF_HIDDEN):
                self.weights[i][j] += self.train_rate * (original_visible_neurons[i] * hidden_probs[j] - self.visible_layer.get_all_neurons()[i] * self.hidden_layer.neurons[j])

    def save_trained_data(self):
        np.savetxt(VISIBLE_BIAS_FILE, self.visible_layer.bias)
        np.savetxt(HIDDEN_BIAS_FILE, self.hidden_layer.bias)
        np.savetxt(WEIGHTS_FILE, self.weights)



        